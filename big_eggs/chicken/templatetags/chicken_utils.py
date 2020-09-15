from dateutil import relativedelta
from django import template
from django.utils.translation import ngettext

from ..models import Egg

register = template.Library()


@register.filter
def to_class_name(value):
    return value._meta.verbose_name


messages_level = {
    10: "secondary",
    20: "primary",
    25: "success",
    30: "warning",
    40: "danger",
}


@register.filter
def to_bs_level(value):
    """
    Convert django messages levels to Bootstrap messages level

    DEBUG   10
    INFO    20
    SUCCESS 25
    WARNING 30
    ERROR   40
    """
    return messages_level[value]


@register.filter
def relativedelta_to_str(value):
    out = []
    if not isinstance(value, relativedelta.relativedelta):
        return ""
    if value.years:
        out.append(ngettext("ein Jahr", f"{value.years} Jahre", value.years))
    if value.months:
        out.append(ngettext("ein Monat", f"{value.months} Monate", value.months))
    if value.days:
        out.append(ngettext("ein Tag", f"{value.days} Tage", value.days))
    out = ", ".join(out)
    return out


# @register.filter
# def error_to_str(value):
#     error_choices_dict = dict(Egg.Error.choices)
#     return error_choices_dict[value]
