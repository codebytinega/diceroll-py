from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import transaction
from inventory.models import Product
from decimal import Decimal


class Sale(models.Model):
    """
    Sale model to track all sales transactions with automatic profit calculation.
    """
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        help_text="Product being sold"
    )
    quantity_sold = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of items sold"
    )
    total_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total selling price (auto-calculated)"
    )
    profit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total profit from this sale (auto-calculated)"
    )
    date_sold = models.DateTimeField(auto_now_add=True)
    sold_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="User who made this sale"
    )
    customer_name = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Optional customer name"
    )
    notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional sale notes"
    )
    
    class Meta:
        ordering = ['-date_sold']
        verbose_name = "Sale"
        verbose_name_plural = "Sales"
    
    def __str__(self):
        return f"Sale #{self.id} - {self.product.name} x{self.quantity_sold}"
    
    def save(self, *args, **kwargs):
        """Override save to calculate total_cost and profit automatically"""
        # Calculate total cost and profit
        self.total_cost = self.product.selling_price * self.quantity_sold
        self.profit = (self.product.selling_price - self.product.buying_price) * self.quantity_sold
        
        # Use transaction to ensure data consistency
        with transaction.atomic():
            # Check if this is a new sale (not an update)
            if not self.pk:
                # Verify stock availability
                if not self.product.can_sell(self.quantity_sold):
                    raise ValueError(f"Insufficient stock. Available: {self.product.quantity}, Requested: {self.quantity_sold}")
                
                # Reduce stock
                self.product.reduce_stock(self.quantity_sold)
            
            super().save(*args, **kwargs)
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage for this sale"""
        if self.total_cost > 0:
            return (self.profit / self.total_cost) * 100
        return 0
    
    @classmethod
    def get_sales_summary(cls, start_date=None, end_date=None):
        """Get sales summary for a date range"""
        queryset = cls.objects.all()
        
        if start_date:
            queryset = queryset.filter(date_sold__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_sold__lte=end_date)
        
        from django.db.models import Sum, Count
        summary = queryset.aggregate(
            total_sales=Sum('total_cost') or 0,
            total_profit=Sum('profit') or 0,
            total_transactions=Count('id')
        )
        
        return summary
    
    @classmethod
    def get_top_selling_products(cls, limit=10):
        """Get top selling products by quantity"""
        from django.db.models import Sum
        return (cls.objects
                .values('product__name', 'product__id')
                .annotate(total_quantity=Sum('quantity_sold'))
                .order_by('-total_quantity')[:limit])
    
    @classmethod
    def get_most_profitable_products(cls, limit=10):
        """Get most profitable products"""
        from django.db.models import Sum
        return (cls.objects
                .values('product__name', 'product__id')
                .annotate(total_profit=Sum('profit'))
                .order_by('-total_profit')[:limit])
