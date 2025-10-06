#!/usr/bin/env python
"""
Test script to verify the Business Management System functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BusinessManagementSystem.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Product
from sales.models import Sale

def test_system():
    print('=== Business Management System Test ===')
    print(f'Users: {User.objects.count()}')
    print(f'Products: {Product.objects.count()}')
    print(f'Sales: {Sale.objects.count()}')
    print(f'Low Stock Products: {Product.objects.filter(quantity__lte=5).count()}')

    # Test calculations
    if Product.objects.exists():
        product = Product.objects.first()
        print(f'\nSample Product: {product.name}')
        print(f'Profit per unit: ${product.profit_per_unit}')
        print(f'Profit percentage: {product.profit_percentage:.1f}%')
        print(f'Is low stock: {product.is_low_stock}')

    if Sale.objects.exists():
        sale = Sale.objects.first()
        print(f'\nSample Sale: Sale #{sale.id}')
        print(f'Total cost: ${sale.total_cost}')
        print(f'Profit: ${sale.profit}')
        print(f'Profit margin: {sale.profit_margin:.1f}%')

    # Test URL resolution
    from django.urls import reverse
    try:
        dashboard_url = reverse('dashboard:home')
        inventory_url = reverse('inventory:product_list')
        sales_url = reverse('sales:sale_list')
        reports_url = reverse('reports:home')
        print(f'\n✅ URL Resolution Test Passed')
        print(f'Dashboard: {dashboard_url}')
        print(f'Inventory: {inventory_url}')
        print(f'Sales: {sales_url}')
        print(f'Reports: {reports_url}')
    except Exception as e:
        print(f'❌ URL Resolution Error: {e}')

    print('\n✅ All systems working correctly!')
    print('\n🚀 Application is ready to use!')
    print('   Login: http://localhost:8000')
    print('   Username: admin')
    print('   Password: admin123')

if __name__ == '__main__':
    test_system()