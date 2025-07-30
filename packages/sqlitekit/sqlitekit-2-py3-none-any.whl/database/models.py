from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
import pendulum

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    items = relationship('Item', back_populates='category')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: pendulum.now('UTC'))
    updated_at = Column(DateTime, default=lambda: pendulum.now('UTC'), onupdate=lambda: pendulum.now('UTC'))
    is_active = Column(Boolean, default=True)
    tags = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items')
    details = relationship('ItemDetail', back_populates='item', cascade="all, delete-orphan")

class ItemDetail(Base):
    __tablename__ = 'item_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.id', ondelete="CASCADE"))
    key = Column(String)
    value = Column(Text)
    is_active = Column(Boolean, default=True)
    item = relationship('Item', back_populates='details')
