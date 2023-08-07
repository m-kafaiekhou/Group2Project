from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
	path('', include('pages.urls'))
]

handler404 = 'pages.views.error_404_view'
