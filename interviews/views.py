from django.shortcuts import render
from .models import Question, Category
from .forms import QuestionModelForm
from django.contrib import messages #import messages
from django.http import HttpResponseRedirect
#import json

from django.db.models import Count 
# Create your views here.

def index(request):
	#dests = Job.objects.all()
	categories = Category.objects.annotate(number_of_ques = Count("questions")).order_by("id").all()
	
	return render(request, "interviews/all.html", {'categories':categories})



def categoryQuestions(request, pk, ques_id=None):
	if ques_id:
		ques = Question.objects.get(pk=ques_id)
		form_data = {'question': ques.question, 'answer':ques.answer, 'category':ques.category}
	else:
		form_data = {'category': pk}

	questions = Question.objects.filter(category=pk).order_by("id")
	post_form = QuestionModelForm(request.POST)
	if request.POST:
		if ques_id and post_form.is_valid():
			#print(request.POST)
			ques.question = request.POST.get("question")
			ques.answer = request.POST.get("answer")
			ques.save()
			messages.success(request, 'Question updated successfully.')
			return HttpResponseRedirect("/interview-questions/"+str(pk))
		elif post_form.is_valid():
			post_form.save()
			messages.success(request, 'Question added successfully.')
		else:
			messages.error(request, 'Invalid form submission.')
			messages.error(request, post_form.errors)

	return render(request, "interviews/category-questions.html", {'questions':questions,'cat_id':pk, 'form':QuestionModelForm(initial=form_data)})


