from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.index, name='all_jobs'),
    path('upwork/', views.upworkAll, name='all_upwork'),
    path('indeed/', views.indeedAll, name='all_indeed'),
    path('<int:pk>', views.JobDetail, name='single_job'),
    path('create/', views.CreateJob.as_view(), name='create_job'),
]
