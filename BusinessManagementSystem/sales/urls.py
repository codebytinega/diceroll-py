from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleListView.as_view(), name='sale_list'),
    path('add/', views.SaleCreateView.as_view(), name='sale_add'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('history/', views.SalesHistoryView.as_view(), name='sales_history'),
]