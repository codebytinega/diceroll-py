from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from inventory.models import Product
from sales.models import Sale


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get date ranges
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        # Basic stats
        context['total_products'] = Product.objects.count()
        context['low_stock_count'] = Product.objects.filter(quantity__lte=5).count()
        
        # Sales stats
        today_sales = Sale.objects.filter(date_sold__date=today)
        week_sales = Sale.objects.filter(date_sold__date__gte=week_start)
        month_sales = Sale.objects.filter(date_sold__date__gte=month_start)
        
        context['today_sales_count'] = today_sales.count()
        context['today_sales_total'] = today_sales.aggregate(
            total=Sum('total_cost'))['total'] or 0
        context['today_profit'] = today_sales.aggregate(
            total=Sum('profit'))['total'] or 0
        
        context['week_profit'] = week_sales.aggregate(
            total=Sum('profit'))['total'] or 0
        context['month_profit'] = month_sales.aggregate(
            total=Sum('profit'))['total'] or 0
        
        # Low stock products
        context['low_stock_products'] = Product.objects.filter(
            quantity__lte=5).order_by('quantity')[:10]
        
        # Recent sales
        context['recent_sales'] = Sale.objects.select_related('product').order_by('-date_sold')[:5]
        
        # Top selling products
        context['top_products'] = Sale.get_top_selling_products(5)
        
        return context


@login_required
def sales_chart_data(request):
    """API endpoint for sales chart data"""
    # Get last 7 days of sales data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    sales_data = []
    labels = []
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        daily_sales = Sale.objects.filter(
            date_sold__date=current_date
        ).aggregate(total=Sum('total_cost'))['total'] or 0
        
        sales_data.append(float(daily_sales))
        labels.append(current_date.strftime('%m/%d'))
    
    return JsonResponse({
        'labels': labels,
        'data': sales_data
    })


@login_required
def profit_chart_data(request):
    """API endpoint for profit chart data"""
    # Get last 7 days of profit data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    profit_data = []
    labels = []
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        daily_profit = Sale.objects.filter(
            date_sold__date=current_date
        ).aggregate(total=Sum('profit'))['total'] or 0
        
        profit_data.append(float(daily_profit))
        labels.append(current_date.strftime('%m/%d'))
    
    return JsonResponse({
        'labels': labels,
        'data': profit_data
    })
