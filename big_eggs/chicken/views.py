import datetime

from django.contrib import messages
from django.core.exceptions import SuspiciousOperation
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import ngettext
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import EggBulkForm, ChickenForm
from .models import Chicken, ChickenGroup, Egg
from collections import defaultdict, namedtuple
from .utils import today_midnight

def naive_date_to_current_datetime(date):
    """
    Convert given naive date as in current timezone and return 
    as datetime (midnight).
    """
    return timezone.get_current_timezone().localize(datetime.datetime(year=date.year, month=date.month, 
        day=date.day))


def eggs_list(request, minus_days=10):
    last_ten_days = today_midnight() - datetime.timedelta(days=minus_days)
    entries = Egg.objects.filter(laid__gt=last_ten_days)
    entries = entries.order_by('-laid')
    entries = entries.values('laid__date', 'group__name', 'group', 'error')
    entries = entries.annotate(eggs_count=Count('id'))

    eggs_per_day = defaultdict(list)
    sum_per_day = defaultdict(int)
    for entry in entries:
        eggs_per_day[entry['laid__date']].append(entry)
        sum_per_day[entry['laid__date']] += entry['eggs_count']

    out = []
    current_dt = last_ten_days
    Entry = namedtuple('Entry', ['date', 'count', 'eggs_list'])
    while current_dt <= today_midnight():
        current_date = timezone.localdate(current_dt)
        out.append(Entry(current_dt, sum_per_day[current_date], eggs_per_day[current_date]))
        current_dt += datetime.timedelta(days=1)

    sum_all = sum(sum_per_day.values())
    average =  sum_all/ minus_days

    if request.method == 'GET':
        form = EggBulkForm()
    elif request.method == 'POST':
        form = EggBulkForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            aware_date = timezone.make_aware(
                datetime.datetime.combine(date, datetime.datetime.min.time()))
            for _ in range(form.cleaned_data['count']):
                Egg.objects.create(
                    laid=aware_date, 
                    group_id=form.cleaned_data['group'],
                    error=form.cleaned_data['error'],
                    )
            count = form.cleaned_data['count']
            message_text = ngettext(
                'Ein Eintrag gespeichert.',
                '%(count)d Einträge gespeichert.', count) % {
                    'count': count,
            }
            messages.success(request, message_text)
            return HttpResponseRedirect(reverse('eggs_list'))

    return render(request, 'chicken/eggs_list.html', {
        'eggs_by_day': reversed(out),
        'active': 'eggs_list',
        'form': form,
        'form_action': reverse('eggs_list'),
        'average': average,
        'sum_all': sum_all,
        'minus_days': minus_days,
    }
    )


def eggs_delete(request, year, month, day, group=None, error=None):
    date = datetime.date(year=year, month=month, day=day)
    eggs = Egg.objects.filter(laid__year=year, laid__month=month, laid__day=day)
    if group:
        if group == 'None':
            group = None
        eggs = eggs.filter(group_id=group)
    if error:
        if error == 'None':
            error = ''
        eggs = eggs.filter(error=error)
    if not eggs:
        messages.warning(request, "Keine Daten zum Löschen vorhanden.")
        return HttpResponseRedirect(reverse('eggs_list'))
    if request.method == 'GET':
        return render(request, 'chicken/eggs_delete.html', {'eggs': eggs})
    elif request.method == 'POST':
        count, _ = eggs.delete()
        message_text = ngettext(
            'Ein Eintrag gelöscht.',
            '%(count)d Einträge gelöscht.', count) % {
                'count': count,
        }
        messages.success(request, message_text)
        return HttpResponseRedirect(reverse('eggs_list'))


class ChickenGeneric:
    model = Chicken
    form_class = ChickenForm
    success_url = reverse_lazy('chicken_list')
    # fields = [
    #     'number', 'name', 'group',
    #     'entry', 'departure', 'sex',
    #     'note']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = 'chicken_list'
        return context


class ChickenList(ChickenGeneric, ListView):
    def get_queryset(self):
        return super().get_queryset().select_related('group').order_by('entry')


class ChickenCreate(ChickenGeneric, CreateView):
    pass

class ChickenUpdate(ChickenGeneric, UpdateView):
    def form_valid(self, form):
        self.object.entry = naive_date_to_current_datetime(form.cleaned_data['entry_date'])
        self.object.hatching = naive_date_to_current_datetime(form.cleaned_data['hatching_date'])
        if form.cleaned_data['departure_date']:
            self.object.departure = naive_date_to_current_datetime(form.cleaned_data['departure_date'])
        return super().form_valid(form)


    def get_initial(self):
        out = super().get_initial()
        out['entry_date'] = timezone.localdate(self.object.entry)
        out['hatching_date'] = timezone.localdate(self.object.hatching)
        if self.object.departure:
            out['departure_date'] = timezone.localdate(self.object.departure)
        return out


class ChickenDelete(ChickenGeneric, DeleteView):
    template_name = 'chicken/confirm_delete.html'


class ChickenGroupGeneric:
    model = ChickenGroup
    success_url = reverse_lazy('chickengroup_list')
    fields = ['name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = 'chickengroup_list'
        return context


class ChickenGroupList(ChickenGroupGeneric, ListView):
    pass


class ChickenGroupCreate(ChickenGroupGeneric, CreateView):
    pass


class ChickenGroupUpdate(ChickenGroupGeneric, UpdateView):
    pass


class ChickenGroupDelete(ChickenGroupGeneric, DeleteView):
    template_name = 'chicken/confirm_delete.html'
