from django.contrib import admin
from .models import Question, Category

# Register your models here.
#admin.site.register(School)
@admin.register(Category,)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(Question)


# class QCustomModelForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(QCustomModelForm, self).__init__(*args, **kwargs)
#         self.initial['answer'] = some_encoding_method(self.instance.some_field)



class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'category')
	def get_changeform_initial_data(self, request):
		return {'category': 4}