from django.shortcuts import render
from django.db.models import Q
from .models import CafeItem
from .search import SearchMenu

# Create your views here.
def menu(request) :
    cafeitem = CafeItem.objects.all()
    form = SearchMenu()
    if 'search' in request.GET:
        form = SearchMenu(request.GET)
        if form.is_valid():
            cd = form.cleaned_data['search']
            cafeitem = cafeitem.filter(Q(name__icontains=cd) | Q(description__icontains=cd))
    return render(request, 'menu/menu.html', {'cafeitem':cafeitem, 'form' : form})