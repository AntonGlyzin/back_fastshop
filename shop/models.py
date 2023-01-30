from email.policy import default
from re import I
from django.db import models
from django.utils.translation import gettext_lazy as _
from settings import CURRENCY, TIME_ZONE
from utils import EmailWorked
from django.utils import timezone

class Customer(models.Model):
    CHOOSE_TYPE_KEY = [('registration', 'registration'), ('reset_password', 'reset_password') ]
    username = models.CharField(unique=True, max_length=200, verbose_name=_('Username'))
    email = models.CharField(unique=True, max_length=200, verbose_name=_('E-mail'))
    password = models.CharField(verbose_name=_('Пароль'), max_length=250)
    first_name = models.CharField(max_length=100, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=100, verbose_name=_('Фамилия'))
    photo = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Ссылка на фото'))
    created = models.DateTimeField(verbose_name=_('Дата регистрации'), default=timezone.now())
    key = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Ключ'))
    type_key = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Тип ключа'), choices=CHOOSE_TYPE_KEY)
    is_banned = models.BooleanField(verbose_name=_('Бан'), default=False)
    is_active = models.BooleanField(default=False, verbose_name=_('Активность'))

    def __str__(self):
        return f'{self.email}'

    class Meta:
        managed = False
        db_table = 'customer'
        verbose_name = _('покупателя')
        verbose_name_plural = _('Покупатели')


class PeaceCustomer(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name=_('Покупатель'), related_name='peaces_customer')
    active = models.BooleanField(default=False, verbose_name=_('Активность'))
    peace = models.TextField(blank=True, null=True, verbose_name=_('Место доставки'))

    def __str__(self):
        return _('Доставка для ')+f' {self.customer.email}'

    class Meta:
        managed = False
        db_table = 'peace_customer'
        verbose_name = _('место доставки')
        verbose_name_plural = _('Места доставки')


class ItemsBasket(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name=_('Покупатель'), related_name='items_basket')
    product = models.ForeignKey('Product', models.CASCADE, verbose_name=_('Продукт'))
    quantity = models.SmallIntegerField(verbose_name=_('Количество'))
    created = models.DateTimeField(verbose_name=_('Дата добавления'), default=timezone.now())

    def __str__(self):
        return f'{self.product.title}'

    class Meta:
        managed = False
        db_table = 'items_basket'
        verbose_name = _('товар в корзину')
        verbose_name_plural = _('Товары в корзине')


class Order(models.Model):
    CHOOSE_PAYED = [(0, _('В ожидание')), (1, _('Оплачено'))]
    customer = models.ForeignKey(Customer, models.PROTECT, verbose_name=_('Покупатель'), related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))
    payd = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Оплачено'))
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    status = models.IntegerField(default=0, verbose_name=_('Статус'), choices=CHOOSE_PAYED)
    created = models.DateTimeField(default=timezone.now(), verbose_name=_('Дата'))

    def save(self, **kwargs):
        if self.status and self.payd != self.amount:
            self.payd = self.amount
            try:
                EmailWorked.send_notify_payd_tocustomer(self.customer.email)
            except Exception as err:
                print(err)
        return super().save(**kwargs)

    def __str__(self):
        return _('Заказ №')+f'{self.id}'

    class Meta:
        managed = False
        db_table = 'order'
        verbose_name = _('заказ')
        verbose_name_plural = _('Заказы')


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    photo = models.ImageField(max_length=255, blank=True, null=True, verbose_name=_('Фото'), upload_to='fastshop/product')
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    quantity = models.SmallIntegerField(verbose_name=_('Количество'), default=1)
    created = models.DateTimeField(default=timezone.now(), verbose_name=_('Дата добавления'))
    updated = models.DateTimeField(verbose_name=_('Дата обнавления'), auto_now=timezone.now())
    is_active = models.BooleanField(default=True, verbose_name=_('Активность'))

    @property
    def amount_products(self):
        return self.price*self.quantity

    def __str__(self):
        return f'{self.title}'

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = _('товар')
        verbose_name_plural = _('Товары')


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, verbose_name=_('Товар'), related_name='products_order')
    order = models.ForeignKey(Order, models.CASCADE, verbose_name=_('Заказ'), related_name='products_order')
    quantity = models.SmallIntegerField(verbose_name=_('Количество'), default=0)
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))

    def __str__(self):
        return f'{self.product.title}'

    class Meta:
        managed = False
        db_table = 'product_order'
        verbose_name = _('заказанный товар')
        verbose_name_plural = _('Заказанные товары')