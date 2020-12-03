from django import template
from ..models import Topic

register = template.Library()

@register.filter(name='last_index')
def last_index(field):
	if len(field.comment_set.union()) != 0:
		return field.comment_set.union()[len(field.comment_set.union())-1].owner
	else:
		return field.owner

@register.filter(name='last_index_date')
def last_index_date(field):
	if len(field.comment_set.union()) != 0:
		return field.comment_set.union()[len(field.comment_set.union())-1].created_date
	else:
		return field.created_date 


