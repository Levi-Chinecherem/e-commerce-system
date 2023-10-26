from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem

# Customizations for the admin site
admin.site.site_header = 'Bigi Burger Administration'
admin.site.site_title = 'Bigi Burger Admin'
admin.site.index_title = 'Admin Dashboard'

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'created_at', 'is_completed')
    list_filter = ('is_completed',)
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]

# Register your models with the custom admin classes
admin.site.register(Category)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Order, OrderAdmin)
