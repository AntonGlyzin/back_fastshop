from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from shop.models import (Product, ItemsBasket, Customer, 
                         Order, ProductOrder, PeaceCustomer,
                         Category, Tags, MapProductTags)
from django.utils.safestring import mark_safe
from django.db.models import Value, F
from django.db.models.functions import Concat
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum, Count


admin.site.site_header = _('Админка интернет-магазина')
admin.site.disable_action('delete_selected')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['get_html_photo', 'created', 'updated', ]
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['id', 'title', 'quantity', 'price', 'currency', 'get_sum_product',  ]
    list_display_links = ['id', 'title',]
    search_fields = ['id', 'title__icontains', ]
    search_help_text = 'ID / Название'
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('title', 'slug','category','description', 'quantity', 
                       'price', 'currency', 'created', 'updated')
        }),
        (_('Изображение'), {
            'fields': ('photo', 'get_html_photo'),
        }),
    )

    @admin.display(ordering=F('quantity')*F('price'), description=_('Продуктов на сумму'))
    def get_sum_product(self, object):
        return f'{object.amount_products} {object.currency}'

    @admin.display(description='')
    def get_html_photo(self, object):
        if object.photo.url:
            return mark_safe(f"<img src='{object.photo.url}' width=213>")

    def get_queryset(self, request):
        return super().get_queryset(request)        
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        change_list = response.context_data['cl']
        queryset = change_list.queryset
        response.context_data['total_product'] = self.get_total(queryset)
        return response

    def get_total(self, queryset):
        prod = (Product.objects
                        .filter(is_active=True, id__in=[item.id for item in queryset])
                        .values('currency')
                        .annotate(total_sum=Sum(F('quantity')*F('price')), total_count=Sum("quantity"))
        )
        return prod


class ItemsBasketInline(admin.TabularInline):
    model = ItemsBasket
    can_delete = False
    readonly_fields = ['product', 'quantity', 'created']
    list_per_page = 20
    ordering = ['-created']
    extra = 0


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    can_delete = False
    readonly_fields = ['product', 'quantity', 'amount', 'currency']
    extra = 0


class OrderInline(admin.TabularInline):
    icon_no = '<img src="/static/admin/img/icon-no.svg" alt="False">'
    icon_yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    model = Order
    can_delete = False
    readonly_fields = ['created', 'payd', 'amount', 'currency', 'get_status', ]
    exclude = ['status']
    list_per_page = 20
    ordering = ['-created']
    show_change_link = True
    extra = 0

    @admin.display(description=_("Оплачено"))
    def get_status(self, obj):
        if obj.status:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)


class PeaceCustomerInline(admin.TabularInline):
    model = PeaceCustomer
    can_delete = False
    readonly_fields = ['active', 'peace', ]
    list_per_page = 20
    extra = 0

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_no = '<img src="/static/admin/img/icon-no.svg" alt="False">'
    icon_yes = '<img src="/static/admin/img/icon-yes.svg" alt="True">'
    list_per_page = 20
    list_display = ['username', 'email', 'full_name','get_active', 'get_ban']
    list_display_links = ['username', 'email',]
    search_fields = ['username__iexact', 'email__icontains', ]
    list_filter = ['is_active', 'is_banned']
    inlines = [PeaceCustomerInline, OrderInline, ItemsBasketInline]
    save_on_top = True
    exclude = ['password']
    search_help_text = 'username / email'
    readonly_fields = ['username', 'email', 'first_name', 
                    'last_name', 'key', 'type_key', 'get_link_photo', 'get_html_photo']

    fieldsets = (
        (_('Общая информация'.upper()), {
            'fields': ('username', 'email', 'first_name', 'last_name', 'get_link_photo', 'get_html_photo', 'key', 'type_key', )
        }),
        (_('Активность / Бан'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_banned'),
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(ordering='is_active', description=_("Активен"))
    def get_active(self, object):
        if object.is_active:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    @admin.display(ordering='is_banned', description=_("Бан"))
    def get_ban(self, object):
        if object.is_banned:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    @admin.display(ordering=Concat('last_name', Value(' '), 'first_name'))
    def full_name(self, object):
        return object.last_name + ' ' + object.first_name

    @admin.display(description=_("Фото"))
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo}' width=213>")

    @admin.display(description=_("Ссылка на фото"))
    def get_link_photo(self, object):
        if object.photo:
            txt = _('Открыть фото')
            return mark_safe(f"<a href='{object.photo}' >{txt}</a>")

    def has_add_permission(self, request):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_delete'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

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
    date_hierarchy = 'created'

    @admin.display(ordering='id', description=_("Номер заказа"))
    def get_order_number(self, object):
        return _(f'Заказ №{object.id}')

    def has_add_permission(self, request):
        return False

    @admin.display(ordering='status', description=_("Оплачено"))
    def get_status(self, object):
        if object.status:
           return  mark_safe(self.icon_yes)
        else:
            return  mark_safe(self.icon_no)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        order = Order.objects.get(id=object_id)
        if order.status:
            self.readonly_fields = ['status', 'customer', 'amount', 'currency', 'payd', 'created']
            extra_context['show_delete'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        else:
            self.readonly_fields = ['customer', 'amount', 'currency', 'payd', 'created']
        return super().changeform_view(request, object_id, form_url, extra_context)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo']
    prepopulated_fields = {"slug": ("name",)}