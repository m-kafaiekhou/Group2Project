from django.urls import path
from .views import *

urlpatterns = [
    path('add-category/', AddCategoryView.as_view(), name="add_category"),
    path('add-item/', AddItemView.as_view(), name="add_item"),
    path('order-details/', OrderDetailView.as_view(), name="order_details"),
    path('category-details/', CategoryDetailView.as_view(), name="category_details"),
    path('item-details/', ItemDetailView.as_view(), name="item_details"),
    path('login/', LoginUserView.as_view(), name='login'),
]
