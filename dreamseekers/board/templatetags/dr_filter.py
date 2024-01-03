from django import template

register = template.Library()

#sub 연산 필터
@register.filter
def sub(value, arg):
    return value - arg