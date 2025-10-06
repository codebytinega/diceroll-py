from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'quantity', 'buying_price', 
        'selling_price', 'profit_per_unit', 'stock_status', 'date_added'
    ]
    list_filter = ['category', 'date_added', 'supplier']
    search_fields = ['name', 'supplier', 'category']
    readonly_fields = ['date_added', 'profit_per_unit', 'profit_percentage', 'total_value']
    list_editable = ['quantity', 'buying_price', 'selling_price']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'supplier')
        }),
        ('Pricing', {
            'fields': ('buying_price', 'selling_price', 'profit_per_unit', 'profit_percentage')
        }),
        ('Stock', {
            'fields': ('quantity', 'total_value')
        }),
        ('Metadata', {
            'fields': ('date_added', 'added_by'),
            'classes': ('collapse',)
        })
    )
    
    def stock_status(self, obj):
        if obj.is_low_stock:
            return format_html(
                '<span style="color: red; font-weight: bold;">⚠️ Low Stock</span>'
            )
        return format_html(
            '<span style="color: green;">✅ In Stock</span>'
        )
    stock_status.short_description = 'Stock Status'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new product
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
