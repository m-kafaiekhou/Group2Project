from django.urls import path
from .views import HomePage, GalleryPage

app_name = "coffeeshop"
urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("gallery/", GalleryPage.as_view(), name="gallery"),
]
