from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    """
    Product model to store inventory items with pricing and stock information.
    """
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food & Beverages'),
        ('books', 'Books'),
        ('home', 'Home & Garden'),
        ('sports', 'Sports & Outdoors'),
        ('toys', 'Toys & Games'),
        ('beauty', 'Beauty & Personal Care'),
        ('automotive', 'Automotive'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, help_text="Product name")
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='other',
        help_text="Product category"
    )
    buying_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Cost price per unit"
    )
    selling_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Selling price per unit"
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity"
    )
    supplier = models.CharField(max_length=200, help_text="Supplier name")
    date_added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="User who added this product"
    )
    
    class Meta:
        ordering = ['-date_added']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return f"{self.name} ({self.category})"
    
    @property
    def profit_per_unit(self):
        """Calculate profit per unit"""
        return self.selling_price - self.buying_price
    
    @property
    def profit_percentage(self):
        """Calculate profit percentage"""
        if self.buying_price > 0:
            return ((self.selling_price - self.buying_price) / self.buying_price) * 100
        return 0
    
    @property
    def is_low_stock(self):
        """Check if product is low in stock (≤ 5 units)"""
        return self.quantity <= 5
    
    @property
    def total_value(self):
        """Calculate total inventory value at buying price"""
        return self.buying_price * self.quantity
    
    def can_sell(self, quantity):
        """Check if we can sell the requested quantity"""
        return self.quantity >= quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock quantity after a sale"""
        if self.can_sell(quantity):
            self.quantity -= quantity
            self.save()
            return True
        return False
