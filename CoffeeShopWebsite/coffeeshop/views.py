from django.shortcuts import render
from django.views import View


class HomePageView(View):
    def get(self, request):
        # a class method should written to get top rated items
        top_rated_items = []
        return render(
            request, "coffeeshop/home.html", {"top_rated_items": top_rated_items}
        )
