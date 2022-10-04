from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey, SmallInteger, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from datetime import datetime
from settings import CURRENCY

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=False, unique=True, index=True)
    email = Column(String(200), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    full_name = column_property(first_name + " " + last_name)
    photo = Column(String(250))
    created = Column(DateTime, default=datetime.now)
    is_banned = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    photo = Column(String(250))
    description = Column(Text)
    price =  Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    currency = Column(String(10), default=CURRENCY)
    quantity = Column(SmallInteger)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)
    amount =  Column(Float(precision=10, decimal_return_scale=2), nullable=False)
    payd =  Column(Float(precision=10, decimal_return_scale=2), default=0)
    currency = Column(String(10), default=CURRENCY)
    date = Column(DateTime, default=datetime.now)
    status = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now)
    customer = relationship('Customer', backref='orders')
    products = relationship('ProductOrder', backref='order')

class ProductOrder(Base):
    __tablename__ = 'product_order'
    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    order_id = Column(Integer, ForeignKey('order.id'))
    quantity = Column(SmallInteger, nullable=False)
    currency = Column(String(10), default=CURRENCY)
    amount =  Column(Integer, nullable=False)
    product = relationship('Product')

class ItemsBasket(Base):
    __tablename__ = 'items_basket'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)
    product_id = Column(Integer, ForeignKey('product.id'), index=True)
    quantity = Column(SmallInteger, nullable=False)
    created = Column(DateTime, default=datetime.now)
    product = relationship('Product', backref='items_basket')
    customer = relationship('Customer', backref='items_basket')

