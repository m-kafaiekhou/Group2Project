from django.urls import path
from .views import HomePage, GalleryPage

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("gallery/", GalleryPage.as_view(), name="gallery"),
]
