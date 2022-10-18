from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from settings import CURRENCY

class Customer(models.Model):
    CHOOSE_TYPE_KEY = [('registration', 'registration'), ('reset_password', 'reset_password') ]
    username = models.CharField(unique=True, max_length=200, verbose_name=_('Username'))
    email = models.CharField(unique=True, max_length=200, verbose_name=_('E-mail'))
    password = models.CharField(max_length=-1, verbose_name=_('Пароль'))
    first_name = models.CharField(max_length=100, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=100, verbose_name=_('Фамилия'))
    photo = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Ссылка на фото'))
    created = models.DateTimeField(verbose_name=_('Дата регистрации'), auto_now_add=True)
    key = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Ключ'))
    type_key = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Тип ключа'), choices=CHOOSE_TYPE_KEY)
    is_banned = models.BooleanField(verbose_name=_('Бан'), default=False)
    is_active = models.BooleanField(default=False, verbose_name=_('Активность'))

    class Meta:
        managed = False
        db_table = 'customer'
        verbose_name = _('покупателя')
        verbose_name_plural = _('Покупатели')
        


class ItemsBasket(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, verbose_name=_('Покупатель'))
    product = models.ForeignKey('Product', models.CASCADE, verbose_name=_('Продукт'))
    quantity = models.SmallIntegerField(verbose_name=_('Количество'))
    created = models.DateTimeField(verbose_name=_('Дата добавления'), auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'items_basket'
        verbose_name = _('товар в корзину')
        verbose_name_plural = _('Товары в корзине')


class Order(models.Model):
    customer = models.ForeignKey(Customer, models.PROTECT, verbose_name=_('Покупатель'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))
    payd = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Оплачено'))
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    status = models.IntegerField(default=0, verbose_name=_('Статус'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата'))

    class Meta:
        managed = False
        db_table = 'order'
        verbose_name = _('заказ')
        verbose_name_plural = _('Заказы')


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Название'))
    photo = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Ссылка на фото'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Описание'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    quantity = models.SmallIntegerField(verbose_name=_('Количество'), default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата добавления'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Дата обнавления'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активность'))

    class Meta:
        managed = False
        db_table = 'product'
        verbose_name = _('товар')
        verbose_name_plural = _('Товары')


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, models.PROTECT, blank=True, null=True, verbose_name=_('Товар'))
    order = models.ForeignKey(Order, models.PROTECT, blank=True, null=True, verbose_name=_('Заказ'))
    quantity = models.SmallIntegerField(verbose_name=_('Количество'), default=1)
    currency = models.CharField(max_length=10, default=CURRENCY, verbose_name=_('Валюта'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Сумма'))

    class Meta:
        managed = False
        db_table = 'product_order'
        verbose_name = _('заказанный товар')
        verbose_name_plural = _('Заказанные товары')