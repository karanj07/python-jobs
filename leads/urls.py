from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
  #  path('', views.index, name='all_leads'),
    path('verify/', views.leadsVerify.as_view(), name='leads_verify'),
]
