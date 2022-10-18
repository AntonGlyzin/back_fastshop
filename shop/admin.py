from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import Product, ItemsBasket, Customer, Order, ProductOrder
from django.utils.safestring import mark_safe
from django.db.models import Value
from django.db.models.functions import Concat
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
    icon_no = '<img src="/static/admin/img/icon-no.svg" alt="False">'
    icon_yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    list_display = ['username', 'email', 'full_name','get_active', 'get_ban']
    list_display_links = ['username', 'email',]
    search_fields = ['username', 'email',]
    list_filter = ['is_active', 'is_banned']
    inlines = [OrderInline, ]
    exclude = ['password']
    readonly_fields = ['username', 'email', 'first_name', 
                    'last_name', 'photo', 'key', 'type_key']

    @admin.display(ordering='is_active')
    def get_active(self, object):
        if object.is_active:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    @admin.display(ordering='is_banned')
    def get_ban(self, object):
        if object.is_banned:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    @admin.display(ordering=Concat('last_name', Value(' '), 'first_name'))
    def full_name(self, object):
        return object.last_name + ' ' + object.first_name

    get_active.short_description = _("Активен")
    get_ban.short_description = _("Бан")
    full_name.short_description = _("Полное имя")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductOrderInline, ]

