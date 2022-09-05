from django import template

register = template.Library()


@register.filter
def filter_by_user(item, user):
    if item.author == user:
        return item.name
