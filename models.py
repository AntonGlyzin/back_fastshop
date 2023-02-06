from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey, SmallInteger, Text, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, column_property
from datetime import datetime
from settings import CURRENCY

Base = declarative_base()

class Customer(Base):
    '''
    type_key: ['registration', 
            'reset_password']
    '''
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
    key = Column(String(250))
    type_key = Column(String(100))
    is_banned = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

class PeaceCustomer(Base):
    __tablename__ = 'peace_customer'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)
    active = Column(Boolean, default=False)
    peace = Column(Text, nullable=False)
    customer = relationship('Customer', backref='peaces')

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200))
    photo = Column(String(250))
    description = Column(Text)
    price =  Column(Numeric(10,2), nullable=False)
    currency = Column(String(10), default=CURRENCY)
    quantity = Column(SmallInteger)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey('category.id'), index=True)
    category = relationship('Category', backref='products')
    tags = relationship('Tags', secondary='product_tags', back_populates='products')

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    photo = Column(String(250))

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), nullable=False)
    products = relationship('Product', secondary='product_tags', back_populates='tags')

class MapProductTags(Base):
    __tablename__ = 'product_tags'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    tags_id = Column(Integer, ForeignKey('tags.id'))

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), index=True)
    amount =  Column(Numeric(10,2), nullable=False)
    payd =  Column(Numeric(10,2), default=0)
    currency = Column(String(10), default=CURRENCY)
    status = Column(Integer, default=0)
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
    amount =  Column(Numeric(10,2), nullable=False)
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

