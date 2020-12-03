from django.db import models
from django.utils.text import slugify
# Create your models here.

def upload_to(instance,filename):
    return '%s/%s/%s'%('gayrimenkul',instance.slug,filename)

class Forum(models.Model):
	name = models.CharField(null=False,blank=False,verbose_name='Forum Name',unique=True, max_length=50)

	def __str__(self):
		return self.name

class SubForum(models.Model):
	name = models.CharField(null=False,blank=False,verbose_name='Sub Forum Name',unique=True, max_length=50)
	description = models.CharField(verbose_name='Forum Description', max_length=100, blank=True, null=True)
	icon = models.ImageField(verbose_name='Icon',upload_to=upload_to, null=True, blank=True)
	forum = models.ForeignKey(Forum, on_delete = models.CASCADE)
	comment_count = models.IntegerField(verbose_name = 'Comment Count', default=0, editable=False)
	topic_count = models.IntegerField(verbose_name = 'Topic Count', default=0, editable=False)

	def __str__(self):
		return self.name

class Moderator(models.Model):
	user = models.ForeignKey('user.User', on_delete = models.CASCADE)
	forum = models.ForeignKey(SubForum, on_delete = models.CASCADE)

	def __str__(self):
		return self.user.username





