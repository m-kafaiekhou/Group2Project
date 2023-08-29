from .models import HomePage, Footer, Page


def homepage_context(request):
    return {"homepage": HomePage.objects.all()}


def footer_context(request):
    return {"footer": Footer.objects.all()}


def pages_context(request):
    return {"pages": Page.objects.all()}

