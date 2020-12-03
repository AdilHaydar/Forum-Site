from django.contrib import admin
from .models import Forum, SubForum, Moderator
# Register your models here.

class ForumAdmin(admin.ModelAdmin):
    pass

class SubForumAdmin(admin.ModelAdmin):
	pass

class ModeratorAdmin(admin.ModelAdmin):
	pass

admin.site.register(SubForum, SubForumAdmin)

admin.site.register(Forum, ForumAdmin)

admin.site.register(Moderator, ModeratorAdmin)

