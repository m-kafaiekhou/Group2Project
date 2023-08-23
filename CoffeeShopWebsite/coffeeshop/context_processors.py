from .models import HomePage
from .models import Footer


def homepage_context(request):
def footer_context(request):
    return {"footer": Footer.objects.all()}
