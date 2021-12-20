from django import template

register = template.Library()


def getallattrs(value):
    return dir(value)


register.filter('getallattrs', getallattrs)
