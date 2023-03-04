from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name='intvques'),
    path('<int:pk>/', views.categoryQuestions, name='catques'),
    path('<int:pk>/<int:ques_id>/', views.categoryQuestions, name='catques'),
]
