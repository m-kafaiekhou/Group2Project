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
    path("chart/year-filter-options/", year_filter_options, name="year-filter-options"),
    path("chart/month-filter-options/", month_filter_options, name="month-filter-options"),
    path("chart/day-filter-options/", day_filter_options, name="day-filter-options"),
    path("chart/sales/year/<int:year>/", yearly_sales_chart, name="year-sales"),
    path("chart/sales/month/<int:month>/", monthly_sales_chart, name="month-sales"),
    path("chart/sales/day/<int:day>/", daily_sales_chart, name="day-sales"),
]