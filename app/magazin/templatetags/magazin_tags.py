from django import template
from django.db.models import Count

from magazin.models import *

register = template.Library()


@register.simple_tag(name='get_categories')     # name можно задавать имя тега
def get_categories():
    # if not filter:
    #     return Category.objects.all()
    # else:
    #     return Category.objects.filter(pk=filter)
    return Category.objects.all()


@register.inclusion_tag('magazin/list_categories.html')
def show_categories(sort='name', cat_selected=''):
    cats = Category.objects.order_by(sort).annotate(Count('product'))
    return {'cats': cats, 'cat_selected': cat_selected}

