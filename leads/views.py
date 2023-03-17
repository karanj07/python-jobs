from django.shortcuts import render
from django.contrib import messages #import messages
from django.http import HttpResponseRedirect
from django.views import View
from verify_email import verify_email
from subprocess import run, PIPE
import sys
#import json

from django.db.models import Count 


class leadsVerify(View):
	def get(self, request):
		context={res:{}}
		
		return render(request, "leads/verify.html", context)

	def post(self, request):
		emails_list = request.POST.get("emails_list")
		emails_list = emails_list.replace("\r\n", ",")

		result = run([sys.executable, "-c", "import sys; from verify_email import verify_email; res=verify_email(sys.argv[1].split(',')); int_res=['Yes' if i else 'No' for i in res]; print(','.join(int_res))", emails_list], shell=False, stdout=PIPE, universal_newlines=True)
		
		result_list = result.stdout
		result_list = result_list.split(",")
		emails_dict = dict(zip(emails_list.split(','), result_list))
		print(emails_dict)
		# for email in emails_list:
		# 	res = verify_email(email)
		# 	print(email, res)
		
		return render(request, "leads/verify.html", {"res":emails_dict})
