from .models import HomePage


def homepage_context(request):
    return {
        "homepage": HomePage.objects.all(),
    }
