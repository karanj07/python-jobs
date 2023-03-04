from django import forms
from django.forms import ModelForm
from .models import Question




class QuestionModelForm(ModelForm):
	class Meta:
		model = Question
		#fields = '__all__'
		fields = ('question', 'answer', 'category',)