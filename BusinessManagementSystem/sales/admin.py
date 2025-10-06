from django.contrib import admin
from django.utils.html import format_html
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product', 'quantity_sold', 'total_cost', 
        'profit', 'profit_margin_display', 'date_sold', 'sold_by'
    ]
    list_filter = ['date_sold', 'product__category', 'sold_by']
    search_fields = ['product__name', 'customer_name', 'notes']
    readonly_fields = ['total_cost', 'profit', 'date_sold', 'profit_margin']
    date_hierarchy = 'date_sold'
    
    fieldsets = (
        ('Sale Information', {
            'fields': ('product', 'quantity_sold', 'customer_name')
        }),
        ('Calculated Fields', {
            'fields': ('total_cost', 'profit', 'profit_margin'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'sold_by', 'date_sold'),
            'classes': ('collapse',)
        })
    )
    
    def profit_margin_display(self, obj):
        margin = obj.profit_margin
        if margin > 50:
            color = 'green'
        elif margin > 20:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, margin
        )
    profit_margin_display.short_description = 'Profit Margin'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new sale
            obj.sold_by = request.user
        super().save_model(request, obj, form, change)
