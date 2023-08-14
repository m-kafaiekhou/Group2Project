from django.urls import path
from .views import *

urlpatterns = [
    path('add-category/', AddCategoryView.as_view(), name="add_category"),
    path('add-item/', AddItemView.as_view(), name="add_item"),
    path('order-details/<int:pk>/', OrderDetailView.as_view(), name="order_details"),
    path('category-details/<int:pk>/', CategoryDetailView.as_view(), name="category_details"),
    path('item-details/<int:pk>/', ItemDetailView.as_view(), name="item_details"),
    path('category-list/', CategoryListView.as_view(), name="category_list"),
    path('item-list/', ItemListView.as_view(), name="item_list"),
    path('order-list/', OrderListView.as_view(), name="order_list"),
    path('order-list/<str:stat>/', OrderListView.as_view(), name="order_status"),
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
]


# Chart view urls
urlpatterns += [
    path()
]