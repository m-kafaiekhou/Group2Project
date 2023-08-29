from django.contrib import admin
from .models import (
    Review,
    Footer,
    HomePage,
    CarouselItem,
    Service,
    Page,
    Navbar,
    Dashboard,
)


admin.site.register(Review)
admin.site.register(Footer)
admin.site.register(HomePage)
admin.site.register(CarouselItem)
admin.site.register(Service)
admin.site.register(Page)
admin.site.register(Navbar)
