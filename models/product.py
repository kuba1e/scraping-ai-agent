from datetime import datetime

from sqlalchemy import Integer, Column, String, JSON, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from  sqlalchemy.sql import func

from db.database import Base

class Product(Base):
    __tablename__ = 'scraped_product'

    id = Column(Integer, primary_key=True)
    scraped_products_result_id = Column(Integer, ForeignKey('scraped_products_result.id'))
    name= Column(String, nullable=True)
    brand_name = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    price_currency = Column(String, nullable=True)
    images = Column(JSON, default=list)
    scraped_products_result = relationship('ScrapedProductsResult', back_populates='products')

class ScrapedProductsResult(Base):
    __tablename__ = 'scraped_products_result'

    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    products = relationship('Product', back_populates='scraped_products_result', lazy='joined')
