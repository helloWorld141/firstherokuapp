from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

def index(req):
	return render(req, 'index.html', {'url': settings.HOST})