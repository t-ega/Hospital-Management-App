from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """ registers the filter ('has_group') inside the templates rendered
     so that we can check if the user belongs to a particular group"""
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
