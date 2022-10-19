from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import Product, ItemsBasket, Customer, Order, ProductOrder
from django.utils.safestring import mark_safe
from django.db.models import Value, F
from django.db.models.functions import Concat

admin.site.site_header = _('Админка интернет-магазина')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['get_html_photo']
    list_display = ['id', 'title', 'quantity', 'price', 'currency', 'get_sum_product']
    list_display_links = ['id', 'title',]
    search_fields = ['id', 'title__icontains', ]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'quantity', 'price', 'currency')
        }),
        (_('Изображение'), {
            'fields': ('photo', 'get_html_photo'),
        }),
    )

    @admin.display(ordering=F('quantity')*F('price'), description=_('Продуктов на сумму'))
    def get_sum_product(self, object):
        return f'{object.amount_products} {object.currency}'

    def get_html_photo(self, object):
        if object.photo.url:
            return mark_safe(f"<img src='{object.photo.url}' width=213>")

    get_html_photo.short_description = _("")


class ItemsBasketInline(admin.TabularInline):
    model = ItemsBasket
    can_delete = False
    readonly_fields = ['product', 'quantity', 'created']
    list_per_page = 20


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    can_delete = False
    readonly_fields = ['product', 'quantity', 'amount', 'currency']


class OrderInline(admin.TabularInline):
    model = Order
    can_delete = False
    inlines = [ProductOrderInline, ]
    readonly_fields = ['payd', 'amount', 'currency', 'created']
    list_per_page = 20


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_no = '<img src="/static/admin/img/icon-no.svg" alt="False">'
    icon_yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    list_per_page = 20
    list_display = ['username', 'email', 'full_name','get_active', 'get_ban']
    list_display_links = ['username', 'email',]
    search_fields = ['username__icontains', 'email__icontains', ]
    list_filter = ['is_active', 'is_banned']
    inlines = [ItemsBasketInline, OrderInline, ]
    save_on_top = True
    exclude = ['password']
    search_help_text = 'username / email'
    readonly_fields = ['username', 'email', 'first_name', 
                    'last_name', 'photo', 'key', 'type_key']

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'photo', 'key', 'type_key')
        }),
        (_('Активность / Бан'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_banned'),
        }),
    )

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
    icon_no = '<img src="/static/admin/img/icon-no.svg" alt="False">'
    icon_yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    inlines = [ProductOrderInline, ]
    search_fields = ['id', ]
    search_help_text = _('Номер заказа')
    list_per_page = 20
    save_on_top = True
    list_display = ['get_order_number', 'get_status']
    list_filter = ['status',]
    readonly_fields = ['customer', 'amount', 'currency', 'payd', 'created']

    @admin.display(ordering='id')
    def get_order_number(self, object):
        return _(f'Заказ №{object.id}')

    @admin.display(ordering='status')
    def get_status(self, object):
        if object.status:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    get_status.short_description = _("Оплачено")
    get_order_number.short_description = _("Номер заказа")