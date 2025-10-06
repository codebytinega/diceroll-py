from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from inventory.models import Product
from sales.models import Sale


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/home.html'


class SalesReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/sales_report.html'


class ProfitReportView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/profit_report.html'


class ProductPerformanceView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/product_performance.html'


@login_required
def export_sales_csv(request):
    """Export sales data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Product', 'Quantity', 'Total Cost', 'Profit', 'Customer', 'Sold By'])
    
    sales = Sale.objects.select_related('product', 'sold_by').order_by('-date_sold')
    for sale in sales:
        writer.writerow([
            sale.date_sold.strftime('%Y-%m-%d %H:%M'),
            sale.product.name,
            sale.quantity_sold,
            sale.total_cost,
            sale.profit,
            sale.customer_name or 'N/A',
            sale.sold_by.username if sale.sold_by else 'N/A'
        ])
    
    return response


@login_required
def export_sales_pdf(request):
    """Export sales data to PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "Sales Report")
    
    # Date
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 70, f"Generated on: {timezone.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Headers
    y = height - 100
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Product")
    p.drawString(300, y, "Qty")
    p.drawString(350, y, "Total")
    p.drawString(400, y, "Profit")
    
    # Data
    y -= 20
    p.setFont("Helvetica", 9)
    sales = Sale.objects.select_related('product').order_by('-date_sold')[:50]  # Limit for PDF
    
    for sale in sales:
        if y < 50:  # Start new page if needed
            p.showPage()
            y = height - 50
        
        p.drawString(50, y, sale.date_sold.strftime('%m/%d/%Y'))
        p.drawString(150, y, sale.product.name[:20])  # Truncate long names
        p.drawString(300, y, str(sale.quantity_sold))
        p.drawString(350, y, f"${sale.total_cost:.2f}")
        p.drawString(400, y, f"${sale.profit:.2f}")
        y -= 15
    
    p.save()
    return response
