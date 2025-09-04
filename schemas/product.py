from typing import Union

from pydantic import BaseModel, Field
from datetime import  datetime


class Product(BaseModel):
    brand_name: str = Field(title='Brand Name', description='The brand name of the product')
    name: str = Field(title='Product name', description='The name of the product')
    price: Union[int, None] = Field(title='Price', description='The price of the product')
    price_currency: Union[str, None]=Field(title='Price currency', description='The currency part of the product price')
    images: list[str] = Field(title='Product images', description='The list of the product images')

class ScrapingResult(BaseModel):
    dataset: list[Product] = Field(title='Dataset', description='The list of products')

class ProductScrapeRequest(BaseModel):
    url: str

class ProductResponse(BaseModel):
    id :int
    session_id:str
    created_at: datetime
    products: list[Product]
