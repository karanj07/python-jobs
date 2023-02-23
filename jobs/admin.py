from django.contrib import admin
from .models import Job


# Register your models here.

#admin.site.register(School)
@admin.register(Job)

class JobAdmin(admin.ModelAdmin):
	list_display = ('title', 'country')