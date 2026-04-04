from pydantic import BaseModel
from typing import List, Any

class Store(BaseModel):
    name: str
    title: str
    link: str
    price: str
    image_url: str
    rating: float
    ratingCount: int

class ImmersiveResult(BaseModel):
    position: int
    title: str
    product_link: str
    image_url: str
    product_id: str
    stores: List[Store]
    description: str
    features: dict[Any, Any]

class SearchResult(BaseModel):
    query: str
    shopping_result: List[ImmersiveResult]