from django import template

register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__



messages_level = {
    10: 'secondary',
    20: 'primary',
    25: 'success',
    30: 'warning',
    40: 'danger',
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