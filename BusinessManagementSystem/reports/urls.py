from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportsView.as_view(), name='home'),
    path('sales-report/', views.SalesReportView.as_view(), name='sales_report'),
    path('profit-report/', views.ProfitReportView.as_view(), name='profit_report'),
    path('product-performance/', views.ProductPerformanceView.as_view(), name='product_performance'),
    path('export/csv/', views.export_sales_csv, name='export_csv'),
    path('export/pdf/', views.export_sales_pdf, name='export_pdf'),
]