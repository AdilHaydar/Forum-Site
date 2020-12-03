from django import forms
from .models import Topic, Comment
from bs4 import BeautifulSoup

class TopicForm(forms.ModelForm):

	class Meta:
		model = Topic
		fields = ['title','content']

	def clean_title(self):
		title = self.cleaned_data['title']
		if title.isdigit():
			raise forms.ValidationError("Do not enter a title consisting only of numbers.")
		return title

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['content']

	def clean_content(self):

		content = self.cleaned_data['content']
		soup = BeautifulSoup(content,'html.parser')
		content_len = soup.text
		if len(content_len) <= 6:
			raise forms.ValidationError(" Comment can't be less than 6 characters.")
		return content