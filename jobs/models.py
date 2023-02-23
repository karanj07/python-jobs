from django.db import models
from ckeditor.fields import RichTextField 

# Create your models here.


class Job(models.Model):
	title = models.CharField(max_length=200)
	description = RichTextField(default="", blank=True) # blank=true - field is not required
	url = models.CharField(max_length=200)
	source = models.CharField(max_length=50)
	country = models.CharField(max_length=100)
	location = models.CharField(max_length=500)
	min_amount = models.IntegerField(default=0)
	max_amount = models.IntegerField(default=0)
	currency = models.CharField(max_length=20)
	is_hourly = models.BooleanField(default=False)
	is_remote = models.BooleanField(default=False)
	proposals = models.CharField(max_length=50)
	feed_json = models.TextField(default="", blank=True)
	job_date = models.CharField(max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


# Create your models here.
