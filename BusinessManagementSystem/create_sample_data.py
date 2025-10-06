#!/usr/bin/env python
"""
Script to create sample data for the Business Management System
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BusinessManagementSystem.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Product
from sales.models import Sale

def create_sample_data():
    print("Creating sample data...")
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Sample products
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'category': 'electronics',
            'buying_price': Decimal('800.00'),
            'selling_price': Decimal('1200.00'),
            'quantity': 15,
            'supplier': 'Apple Inc.'
        },
        {
            'name': 'Samsung Galaxy S24',
            'category': 'electronics',
            'buying_price': Decimal('700.00'),
            'selling_price': Decimal('1000.00'),
            'quantity': 8,
            'supplier': 'Samsung Electronics'
        },
        {
            'name': 'Nike Air Max',
            'category': 'clothing',
            'buying_price': Decimal('80.00'),
            'selling_price': Decimal('150.00'),
            'quantity': 25,
            'supplier': 'Nike Store'
        },
        {
            'name': 'Adidas Ultraboost',
            'category': 'clothing',
            'buying_price': Decimal('90.00'),
            'selling_price': Decimal('180.00'),
            'quantity': 12,
            'supplier': 'Adidas Official'
        },
        {
            'name': 'MacBook Air M3',
            'category': 'electronics',
            'buying_price': Decimal('1000.00'),
            'selling_price': Decimal('1500.00'),
            'quantity': 5,  # Low stock
            'supplier': 'Apple Inc.'
        },
        {
            'name': 'Organic Coffee Beans',
            'category': 'food',
            'buying_price': Decimal('12.00'),
            'selling_price': Decimal('25.00'),
            'quantity': 50,
            'supplier': 'Local Coffee Roasters'
        },
        {
            'name': 'Wireless Headphones',
            'category': 'electronics',
            'buying_price': Decimal('45.00'),
            'selling_price': Decimal('89.99'),
            'quantity': 3,  # Low stock
            'supplier': 'Tech Wholesale'
        },
        {
            'name': 'Gaming Mouse',
            'category': 'electronics',
            'buying_price': Decimal('25.00'),
            'selling_price': Decimal('59.99'),
            'quantity': 20,
            'supplier': 'Gaming Gear Co.'
        },
        {
            'name': 'Yoga Mat',
            'category': 'sports',
            'buying_price': Decimal('15.00'),
            'selling_price': Decimal('35.00'),
            'quantity': 18,
            'supplier': 'Fitness Equipment Ltd.'
        },
        {
            'name': 'Water Bottle',
            'category': 'sports',
            'buying_price': Decimal('8.00'),
            'selling_price': Decimal('19.99'),
            'quantity': 2,  # Low stock
            'supplier': 'Hydration Solutions'
        }
    ]
    
    # Create products
    created_products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                **product_data,
                'added_by': admin_user
            }
        )
        created_products.append(product)
        if created:
            print(f"Created product: {product.name}")
    
    # Create sample sales (last 30 days)
    print("\nCreating sample sales...")
    
    customer_names = [
        'John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Brown', 
        'David Wilson', 'Lisa Garcia', 'Tom Anderson', 'Maria Rodriguez',
        'James Taylor', 'Jennifer Martinez', 'Robert Lee', 'Amanda White'
    ]
    
    # Generate sales for the last 30 days
    for i in range(50):  # Create 50 sales
        # Random date in the last 30 days
        days_ago = random.randint(0, 30)
        sale_date = datetime.now() - timedelta(days=days_ago)
        
        # Random product (only those with stock)
        available_products = [p for p in created_products if p.quantity > 0]
        if not available_products:
            break
            
        product = random.choice(available_products)
        
        # Random quantity (1-3, but not more than available stock)
        max_quantity = min(3, product.quantity)
        if max_quantity <= 0:
            continue
            
        quantity = random.randint(1, max_quantity)
        
        # Random customer
        customer = random.choice(customer_names) if random.random() > 0.3 else None
        
        try:
            # Create the sale
            sale = Sale.objects.create(
                product=product,
                quantity_sold=quantity,
                customer_name=customer,
                sold_by=admin_user,
                notes=f"Sample sale #{i+1}" if random.random() > 0.7 else None
            )
            
            # Update the sale date (since auto_now_add prevents this)
            Sale.objects.filter(id=sale.id).update(date_sold=sale_date)
            
            print(f"Created sale: {product.name} x{quantity} - ${sale.total_cost}")
            
        except ValueError as e:
            print(f"Skipped sale for {product.name}: {e}")
            continue
    
    print(f"\nSample data creation completed!")
    print(f"Total products: {Product.objects.count()}")
    print(f"Total sales: {Sale.objects.count()}")
    print(f"Low stock products: {Product.objects.filter(quantity__lte=5).count()}")

if __name__ == '__main__':
    create_sample_data()