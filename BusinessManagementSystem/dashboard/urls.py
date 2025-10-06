from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('api/sales-chart-data/', views.sales_chart_data, name='sales_chart_data'),
    path('api/profit-chart-data/', views.profit_chart_data, name='profit_chart_data'),
]