from django.urls import path
from .views import *


urlpatterns = [
    path("order-details/<int:pk>/", OrderDetailView.as_view(), name="order_details"),
    path("order-details/<int:pk>/quantity/", OrderItemUpdateView.as_view(), name="order_item_update"),
    # path("category-details/<int:pk>/", CategoryDetailView.as_view(), name="category_details"),
    # path("item-details/<int:pk>/", ItemDetailView.as_view(), name="item_details"),
    # path("category-list/", CategoryListView.as_view(), name="category_list"),
    # path("item-list/", ItemListView.as_view(), name="item_list"),
    path("order-list/", OrderListView.as_view(), name="order_list"),
    path("order-list/<str:stat>/", OrderListView.as_view(), name="order_status"),
    path("orderitem-delete/<int:pk>/<int:order_pk>/", OrderItemDeleteView.as_view(), name="orderitem_delete"),
    path("", DashboardView.as_view(), name="dashboard"),
]


# Chart view urls
urlpatterns += [
    path("chart/year-filter-options/", year_filter_options, name="year-filter-options"),
    path("chart/month-filter-options/", month_filter_options, name="month-filter-options"),
    path("chart/day-filter-options/", day_filter_options, name="day-filter-options"),
    path("chart/sales/this-year/", yearly_sales_chart, name="this-year-sales"),
    path("chart/sales/this-month/", monthly_sales_chart, name="month-sales"),
    path("chart/sales/this-day/", daily_sales_chart, name="day-sales"),
    path("chart/sales/daily-time-sale/", sales_by_time_of_day, name="daily-time-sale"),
    path("chart/sales/total/", total_sales, name="total-sales"),
    path("chart/sales/top-selling/", top_10_selling_items, name="top-selling"),
    path("chart/sales/best-customers/", top_10_customers, name="best-customers"),
    path("chart/sales/category-sale/", sales_by_category, name="category-sale"),
    path("chart/sales/employee-sales/", sales_by_employee, name="employee-sales"),
    path("chart/sales/peak-hour/", peak_business_hour, name="peak-hour"),
    path("chart/sales/popular-items/", most_popular_items, name="popular-items"),
    path("chart/sales/status/<str:status>/", order_status_report, name="status"),
    path("chart/sales/customer-history/", customer_order_history, name="customer-history"),
    # Customer Demographic
    path("chart/sales/customer-data/", customer_data, name="customer-data"),
    path("chart/sales/customer-items-bought/", number_of_items_bought, name="customer-items-bought"),
]
