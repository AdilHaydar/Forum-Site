from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import datetime
# Create your models here.

def min_length(value):
	if len(value) < 6:
		raise ValidationError(_("%(value)s can't be less than 6 characters."), params={'value':value})

class Topic(models.Model):
	owner = models.ForeignKey('user.User',blank=False,null=False,verbose_name='İçerik Sahibi Sahibi',on_delete=models.CASCADE)
	title = models.CharField(max_length=50,verbose_name='Başlık',help_text='Konu başlığı giriniz.',validators=[min_length])
	#min_length özelliği modelde yokmuş forms.CharField da varmış fakat ben bunu modelden direkt türeteceğim için kullanamyabilirim.
	#valid fonkunda bu min_length'i kendim kontrol etmeliyim. https://stackoverflow.com/questions/2470760/django-charfield-with-fixed-length-how
	#validator'a MinLengthValidator() ekledim, bu çözüm olabilir.
	content = RichTextField(verbose_name="İçerik",validators=[min_length])
	fixed = models.BooleanField(null=True,blank=True,editable=False,default='False')
	forum = models.ForeignKey('Forum.SubForum', blank=False, null=False, on_delete = models.CASCADE)
	slug = models.SlugField(max_length=122,default='',unique=True,null=False,verbose_name='Slug Alanı',editable=False)
	views = models.IntegerField(verbose_name = 'Views', default = 0, null = False, blank = False)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	craeted_comment_date = models.DateTimeField(auto_now_add = True)
	lock_topic = models.BooleanField(default = False,verbose_name='Lock')
	
	def get_slug(self):
		return self.slug

	def __str__(self):
		return self.title

	def unique_slug(self,new_slug,orjinal_slug,index):
		if Topic.objects.filter(slug=new_slug):
			new_slug = '%s-%s'%(orjinal_slug,index)
			index += 1
			return self.unique_slug(new_slug=new_slug,orjinal_slug=orjinal_slug,index=index)
		return new_slug

	def save(self, *args, **kwargs):

		if self.slug == '':
			index=1
			new_slug = slugify(self.title)
			self.slug=self.unique_slug(new_slug=new_slug,orjinal_slug=new_slug,index=index)
			
		self.forum.topic_count += 1
		self.forum.save()

		super(Topic, self).save(*args,**kwargs)

		self.owner.topic_count += 1
		self.owner.save()

	def lock(self, *args, **kwargs):
		super(Topic,self).save(*args,**kwargs)

	def move(self, *args, **kwargs):
		self.forum.topic_count += 1
		pre_forum = args[0]
		pre_forum.topic_count -= 1
		pre_forum.save()
		self.forum.save()

		super(Topic,self).save()

	def views_plus(self, *args, **kwargs):
		self.views += 1
		super(Topic, self).save(*args,**kwargs)

	def update_comment_date(self, date, *args, **kwargs):
		self.craeted_comment_date = date
		super(Topic, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		self.forum.topic_count -= 1
		self.forum.save()

		super(Topic, self).delete(*args,**kwargs)

		self.owner.topic_count -= 1
		self.owner.save()

	class Meta:
		verbose_name = 'Topics'
		verbose_name_plural = 'Topics'
		ordering = ['-craeted_comment_date']

class Comment(models.Model):
	owner = models.ForeignKey('user.User', blank=False, null=False, on_delete=models.CASCADE)
	content = RichTextField(validators=[min_length], verbose_name='Comment')
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.topic.forum.comment_count += 1
		self.topic.forum.save()

		super(Comment, self).save(*args,**kwargs)

		self.owner.comment_count += 1
		self.owner.save()

		self.topic.update_comment_date(date = self.created_date)

	def delete(self, *args, **kwargs):
		self.topic.forum.comment_count -= 1
		self.topic.forum.save()

		super(Comment, self).delete(*args,**kwargs)

		self.owner.comment_count -= 1
		self.owner.save()

	class Meta:
		ordering = ['created_date']