from django.contrib import admin
from .models import Topic, Comment
# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ['owner', 'title', 'fixed', 'forum']
	list_display_links = ['title']
	search_fields = ['owner','title','forum']
	list_filter = ['fixed','forum']

	class Meta:
		model = Topic

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['owner','topic','created_date']
	list_display_links = ['owner','topic']
	search_fields = ['owner','topic']
	list_filter = ['owner','topic','created_date']

	class Meta:
		model = Comment
