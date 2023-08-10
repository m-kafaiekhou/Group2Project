from django.urls import path
from .views import *

urlpatterns = [
    path('add-category/', AddCategoryView.as_view(), name="add_category"),
    path('add-item/', AddItemView.as_view(), name="add_item"),
    path('order-details/', OrderDetailView.as_view(), name="order_details"),
    path('category-details/', CategoryDetailView.as_view(), name="category_details"),
    path('item-details/', ItemDetailView.as_view(), name="item_details"),
    path('category-list/', CategoryListView.as_view(), name="category_list"),
    path('item-list/', ItemListView.as_view(), name="item_list"),
    path('order-list/', OrderListView.as_view(), name="order_list"),
]
