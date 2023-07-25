from django import template

register = template.Library()

def has_group(user, arg):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=arg)
    return True if group in user.groups.all() else False

register.filter('has_group', has_group)