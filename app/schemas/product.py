from pydantic import BaseModel
from typing import List, Optional

class ProductImage(BaseModel):
    url: str

class ProductOption(BaseModel):
    name: str
    values: List[str]

class Product(BaseModel):
    id: str
    name: str
    price: float
    description: Optional[str] = None
    images: List[ProductImage] = []
    options: List[ProductOption] = []

class ProductList(BaseModel):
    items: List[Product]
    total: int 