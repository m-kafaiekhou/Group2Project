from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import redirect


def error_404_view(request, exception):
	return render(request, '404.html')
