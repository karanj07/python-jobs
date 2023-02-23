from django.shortcuts import render

from .forms import JobModelForm
from .models import Job
from django.views import View
from django.contrib import messages #import messages

from django.core.mail import send_mail
from django.conf import settings

import requests
from bs4 import BeautifulSoup

import feedparser
import json
import re
from datetime import datetime
# Create your views here.


def index(request):
	#dests = Job.objects.all()
	feeds = feedparser.parse('https://www.upwork.com/ab/feed/topics/rss?securityToken=967ba2da29bea39ad7d100fbbac891a11b8baed891c5801a5c7a5b92087a44a7bda689a99ec83cedb0cafb2d2a012d9a4f413689b0269c8ab81ec219502e5db6&userUid=424228385627422720&orgUid=424228385635811329')

	entries = []

	return render(request, "jobs/all.html", {'jobs':entries})

def upworkAll(request):
	#dests = Job.objects.all()
	feeds = feedparser.parse('https://www.upwork.com/ab/feed/topics/rss?securityToken=967ba2da29bea39ad7d100fbbac891a11b8baed891c5801a5c7a5b92087a44a7bda689a99ec83cedb0cafb2d2a012d9a4f413689b0269c8ab81ec219502e5db6&userUid=424228385627422720&orgUid=424228385635811329')

	entries = []

	past_jobs = Job.objects.filter(source="upwork").order_by('-id')[:200].all()

	mixed_entries = []
	for j in past_jobs:
		json_decode = feedparser.FeedParserDict(json.loads(j.feed_json))
		json_decode["is_saved"] = True
		mixed_entries.append(json_decode)

	for feed in feeds.entries:
		skip = False
		for j in past_jobs:
			if j.url == feed.link:
				skip = True
				break

		if skip == False:
			mixed_entries.insert(0, feed)

	for feed in mixed_entries:
		feed_title = feed.title.lower()
		if feed.title != None and ("tutor" in feed_title or "graphic design" in feed_title or "automation" in feed_title or "bot" in feed_title):
			continue

		content_lowercase = feed.summary.lower()
		content_lowercase = content_lowercase.replace('\n', ' ').replace('\r', '')
		if content_lowercase != None and "pakistan" in content_lowercase:
			continue

		m = re.search('<b>skills</b>:(.*)country', content_lowercase)
		#if m:print(m.group(1))
		if m != None and ("machine learning" in m.group(1) or 
			"crypto" in m.group(1) or 
			"php" in m.group(1) or 
			"wordpress" in m.group(1)or 
			"scrap" in m.group(1) or 
			"selenium" in m.group(1) 
			):continue

		m = re.search('<b>budget</b>:(.*)<br /><b>posted', content_lowercase)
		budget = None
		if m:budget = int(''.join(filter(str.isdigit, m.group(1))))
		if budget != None and budget < 300:continue
		
		m = re.search('<b>country</b>:(.*)<br />', content_lowercase)
		country = ''
		if m:country=m.group(1)
		published_obj = datetime.strptime(feed["published"], '%a, %d %b %Y %X %z')
		dt_string = published_obj.strftime("%Y-%m-%d %H:%M:%S.%f %z")
		upworkJob = Job(title = feed.title, description = feed.summary, source="upwork")
		upworkJob.country = country
		upworkJob.job_date = dt_string
		upworkJob.url = feed.link
		upworkJob.feed_json = json.dumps(feed)
		#print(feed.title if "is_saved" not in feed else "exists" + feed.title)
		if "is_saved" not in feed:upworkJob.save()

		feed["published_obj"] = published_obj
		feed["published_ts"] = published_obj.timestamp()
		entries.append(feed)

	entries.sort(key=lambda r: -r.published_ts)
	
	return render(request, "jobs/all-upwork.html", {'jobs':entries})

def indeedAll(request):
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0'}
	
	req = requests.get("http://in.indeed.com/jobs?q=django&l=Gurgaon%2C+Haryana&sort=date&fromage=7&vjk=1e6aae454849931b", headers=headers)
	web_s = req.text
	soup = BeautifulSoup(web_s, "html.parser") # Parse
	page_title = soup.title.string # Get Value of Title tag
	entries = []
	unordered_list = soup.find("ul", {"class": "jobsearch-ResultsList"})
	if unordered_list != None:
		children = unordered_list.findChildren("li", recursive=False)
		print(len(children))
		for child in children:
			job_h = child.find("h2")
			job_a = job_h.find("a") if job_h != None else None
			job_title = job_a.find("span") if job_a != None else None
			job_date = child.find("span", {"class": "date"})
			print(job_date)
			if job_title != None and job_date != None:
				job_title_text = job_title.get_text()
				job_date_text = job_date.get_text()
				entries.append({"title":job_title_text, "date": job_date_text})

	return render(request, "jobs/all-indeed.html", {'jobs':entries, 'title':page_title})

class CreateJob(View):
	def get(self, request):
		context={'form':JobModelForm}
		return render(request, "jobs/create.html", context)

	def post(self, request):
		context={'form':JobModelForm}

		form = JobModelForm(request.POST)
		if form.is_valid():
			form.save()

			mail_response = send_mail('New Job Form',
			'This is some test Job message', 
			settings.EMAIL_HOST_USER,
			['karanj89@gmail.com'], 
			fail_silently=False)
			if mail_response == 1:
				messages.success(request, 'Mail sent successfully.')

			messages.success(request, 'Request added successfully.')
		else:
			messages.error(request, 'Invalid form submission.')
			messages.error(request, form.errors)

		return render(request, "jobs/create.html", context)



def JobDetail(request, pk):
	obj = Job.objects.get(pk=pk)

	return render(request, "jobs/single.html", {'job':obj})

