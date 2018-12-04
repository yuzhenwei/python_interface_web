from django import template
from django.utils.safestring import mark_safe
from DB import models

register = template.Library()   #register的名字是固定的,不可改变

####################以上行是固定不变要写的#############################


######################定义过滤器####################
# @register.filter
# def filter_multi(v1,v2):
#     return  v1 * v2

######################定义标签#####################

@register.simple_tag    
def search_item():
    item_list = models.Project_info.objects.all()
    return item_list