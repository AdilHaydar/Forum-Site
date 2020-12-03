from django import template
from Topic.models import Topic
from ..models import SubForum, Forum


register = template.Library()

@register.filter(name='link_map')
def link_map(path):
	p = path.split('/')
	for index,item in enumerate(p):
		if item == '':
			del p[index]
	if len(p) == 1:
		return "<a href='/'>Forum Site</a>"
	if len(p) == 2:
		return ("<a href='/'>Forum Site</a> > <a href='/forums/{}'>{}</a>").format(p[1],p[1])
	if len(p) == 3 and p[1] != 'panel':
		return ("<a href='/'>Forum Site</a> > <a href='/forums/{}'>{}</a> > <a href='/forums/{}/{}'>{}</a>").format(p[1],p[1],p[1],p[2],p[2])
	else:
		return "<a href='/'>Forum Site</a>"
		