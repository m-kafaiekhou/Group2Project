from .models import HomePage, Footer, Page, Navbar
from menus.models import CafeItem, Category


def homepage_context(request):
    return {"homepage": HomePage.objects.all()}


def footer_context(request):
    return {"footer": Footer.objects.all()}


def pages_context(request):
    return {"pages": Page.objects.all()}


def navbar_context(request):
    return {"navbars": Navbar.objects.all()}


def autocomplete_context(request):
    return {"autocomp_cafeitems": CafeItem.objects.all()}
