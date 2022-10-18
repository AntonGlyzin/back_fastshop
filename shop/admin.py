from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import Product, ItemsBasket, Customer, Order, ProductOrder
# Register your models here.
admin.site.site_header = _('Админка интернет-магазина')
admin.site.site_title = _('My Site Title')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ItemsBasket)
class ItemsBasketAdmin(admin.ModelAdmin):
    pass

class ProductInline(admin.TabularInline):
    model = Product

class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    # inlines = [ProductInline, ]

class OrderInline(admin.TabularInline):
    model = Order
    inlines = [ProductOrderInline, ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductOrderInline, ]

