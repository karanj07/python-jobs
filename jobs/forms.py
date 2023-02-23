from django import forms
from django.forms import ModelForm
from .models import Job
from django.urls import reverse_lazy
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit




class JobModelForm(ModelForm):
	class Meta:
		model = Job
		#fields = '__all__'
		fields = ('title', 'description', 'country',)