from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Sale
from .forms import SaleForm
from inventory.models import Product


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    paginate_by = 20
    
    def get_queryset(self):
        return Sale.objects.select_related('product', 'sold_by').order_by('-date_sold')


class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/sale_detail.html'
    context_object_name = 'sale'


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sales/sale_form.html'
    success_url = reverse_lazy('sales:sale_list')
    
    def form_valid(self, form):
        try:
            form.instance.sold_by = self.request.user
            response = super().form_valid(form)
            messages.success(
                self.request, 
                f'Sale recorded successfully! Profit: ${form.instance.profit:.2f}'
            )
            return response
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class SalesHistoryView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sales_history.html'
    context_object_name = 'sales'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Sale.objects.select_related('product', 'sold_by')
        
        # Date filtering
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date_sold__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date_sold__date__lte=end_date)
            except ValueError:
                pass
        
        # Product filtering
        product_id = self.request.GET.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(product__name__icontains=search_query) |
                Q(customer_name__icontains=search_query) |
                Q(notes__icontains=search_query)
            )
        
        return queryset.order_by('-date_sold')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter values
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['selected_product'] = self.request.GET.get('product', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Get products for filter
        context['products'] = Product.objects.all().order_by('name')
        
        # Calculate summary for filtered results
        filtered_sales = self.get_queryset()
        context['summary'] = filtered_sales.aggregate(
            total_sales=Sum('total_cost') or 0,
            total_profit=Sum('profit') or 0,
            total_transactions=filtered_sales.count()
        )
        
        return context
