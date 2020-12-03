from django import forms
from .models import Forum, SubForum

class ForumForm(forms.ModelForm):

	class Meta:
		model = Forum
		fields = '__all__'

	def clean_name(self):
		name = self.cleaned_data['name']

		if name.isdigit():
			raise forms.ValidationError('The name cannot only consist of numbers.')

		if '@' in name:
			raise forms.ValidationError('The name cannot contain the @ character.')

		return name

class SubForumForm(forms.ModelForm):

	class Meta:
		model = SubForum
		fields = '__all__'

	def clean_name(self):
		name = self.cleaned_data['name']

		if name.isdigit():
			raise forms.ValidationError('The name cannot only consist of numbers.')

		if '@' in name:
			raise forms.ValidationError('The name cannot contain the @ character.')

		return name

	def clean_description(self):
		description = self.cleaned_data['description']

		if description.isdigit():
			raise forms.ValidationError('The description cannot only consist of numbers.')

		return description

