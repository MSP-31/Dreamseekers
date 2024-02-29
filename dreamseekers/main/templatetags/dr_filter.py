from django import template
import os

register = template.Library()

# dr_filter

#sub 연산 필터
@register.filter
def sub(value, arg):
    return value - arg

# 파일 경로의 마지막부분 반환
@register.filter
def basename(value):
    return os.path.basename(value)