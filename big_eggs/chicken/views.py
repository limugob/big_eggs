import datetime
import itertools
from collections import defaultdict, namedtuple

from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.db.models import Count, Sum
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import formats, timezone
from django.utils.timezone import localdate
from django.utils.translation import ngettext
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from .filters import ChickenFilterView, EggFilter
from .forms import ChickenForm, EggBulkForm
from .models import Chicken, ChickenGroup, Egg
from .utils import today_midnight


def naive_date_to_current_datetime(date):
    """
    Convert given naive date as in current timezone and return
    as datetime (midnight).
    """
    return timezone.get_current_timezone().localize(
        datetime.datetime(year=date.year, month=date.month, day=date.day)
    )


def eggs_list_stats(request, entries):
    import matplotlib.pyplot as plt

    # https://matplotlib.org/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py

    labels = list(map(lambda x: formats.date_format(x.date, "j.n"), entries))
    ### TODO this dateformat is only for germany
    values = list(map(lambda x: x.count, entries))

    width = 0.35  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, values, width, label="Eier")

    ax.set_ylabel("Eier")
    ax.set_xlabel("Datum")
    # ax.set_title("Scores by group and gender")
    # ax.legend()

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type="image/png")
    canvas.print_png(response)
    return response
    # plt.show()


def eggs_list(request, minus_days=10, stats=False):
    last_ten_days = today_midnight() - datetime.timedelta(days=minus_days)
    eggs = Egg.objects.filter(laid__gte=last_ten_days).select_related("group")
    egg_filter = EggFilter(request.GET, queryset=eggs, request=request)
    entries = egg_filter.qs.order_by("-laid")

    # indicate if filter is active on query
    filters_active = any(request.GET.values())

    eggs_per_day = defaultdict(list)
    sum_per_day = defaultdict(int)
    for egg_entry in entries:
        eggs_per_day[localdate(egg_entry.laid)].append(egg_entry)
        sum_per_day[localdate(egg_entry.laid)] += egg_entry.quantity

    out = []
    current_dt = last_ten_days
    Entry = namedtuple("Entry", ["date", "count", "eggs_list"])
    tmc = today_midnight()
    while current_dt <= tmc:
        current_date = localdate(current_dt)
        out.append(
            Entry(current_dt, sum_per_day[current_date], eggs_per_day[current_date])
        )
        current_dt += datetime.timedelta(days=1)

    if stats:
        return eggs_list_stats(request, out)

    sum_all = sum(sum_per_day.values())
    # todays value must be substract (else sum will change after each input for today)
    sum_all -= sum_per_day[tmc.date()]
    average = sum_all / minus_days

    if request.method == "GET":
        form = EggBulkForm()
    elif request.method == "POST":
        form = EggBulkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Eintrag gespeichert.")
            return HttpResponseRedirect(
                reverse("eggs_list", kwargs={"minus_days": minus_days})
            )

    return render(
        request,
        "chicken/eggs_list.html",
        {
            "eggs_by_day": reversed(out),
            "active": "eggs_list",
            "form": form,
            "form_action": reverse("eggs_list", kwargs={"minus_days": minus_days}),
            "average": average,
            "sum_all": sum_all,
            "minus_days": minus_days,
            "filter": egg_filter,
            "filters_active": filters_active,
        },
    )


def eggs_delete(request, year=None, month=None, day=None, id=None):
    """ Delete egg entries with given id or date (year, month, day).
    """
    if id:
        eggs = Egg.objects.filter(pk=id)
    else:
        date = datetime.date(year=year, month=month, day=day)
        eggs = Egg.objects.filter(laid__date=date)
    if not eggs:
        messages.warning(request, "Keine Daten zum Löschen vorhanden.")
        return HttpResponseRedirect(reverse("eggs_list"))
    if request.method == "GET":
        return render(
            request,
            "chicken/confirm_delete.html",
            {"eggs": eggs, "cancel_url": reverse("eggs_list")},
        )
    elif request.method == "POST":
        count, _ = eggs.delete()
        message_text = ngettext(
            "Eintrag gelöscht.", "%(count)d Einträge gelöscht.", count
        ) % {"count": count,}
        messages.success(request, message_text)
        return HttpResponseRedirect(reverse("eggs_list"))


class ChickenGeneric:
    model = Chicken
    form_class = ChickenForm
    success_url = reverse_lazy("chicken_list")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "chicken_list"
        return context


class ChickenList(ChickenGeneric, ChickenFilterView):
    template_name = "chicken/chicken_list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("group")
            .order_by("group__name", "name", "entry")
        )


class ChickenCreate(ChickenGeneric, CreateView):
    pass


class ChickenUpdate(ChickenGeneric, UpdateView):
    pass


class ChickenDelete(ChickenGeneric, DeleteView):
    template_name = "chicken/confirm_delete.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cancel_url"] = context["object"].get_absolute_url()
        return context


class ChickenGroupGeneric:
    model = ChickenGroup
    success_url = reverse_lazy("chickengroup_list")
    fields = ["name", "selectable"]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "chickengroup_list"
        return context


class ChickenGroupList(ChickenGroupGeneric, ListView):
    pass


class ChickenGroupCreate(ChickenGroupGeneric, CreateView):
    pass


class ChickenGroupUpdate(ChickenGroupGeneric, UpdateView):
    pass


class ChickenGroupDelete(ChickenGroupGeneric, DeleteView):
    template_name = "chicken/confirm_delete.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["cancel_url"] = context["object"].get_absolute_url()
        return context
