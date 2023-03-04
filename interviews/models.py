from django.db import models
from ckeditor.fields import RichTextField 


# Create your models here.


class Category(models.Model):
	class Meta:
		ordering = ['id']
		verbose_name_plural = "categories"

	def __str__(self):
		return self.name

	name = models.CharField(max_length=200)
	order = models.IntegerField(default=0)

class Question(models.Model):
	question = models.TextField(default="", blank=True)
	answer = RichTextField(default="", blank=True) # blank=true - field is not required
	category = models.ForeignKey(Category, default=0, on_delete=models.SET_DEFAULT)
	is_starred = models.BooleanField(default=False)
	is_trivial = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)