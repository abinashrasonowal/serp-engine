from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Price:
    """Value object for product price."""
    amount: float
    currency: str = "INR"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Price amount cannot be negative")

    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"


@dataclass
class Rating:
    """Value object for product rating."""
    value: float
    count: int = 0

    def __post_init__(self):
        if not 0 <= self.value <= 5:
            raise ValueError("Rating must be between 0 and 5")
        if self.count < 0:
            raise ValueError("Rating count cannot be negative")

    def __str__(self) -> str:
        return f"{self.value} ({self.count} reviews)"


@dataclass
class Store:
    """Entity representing a store offering a product."""
    name: str
    title: str
    link: str
    price: str
    image_url: str
    rating: float
    rating_count: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "title": self.title,
            "link": self.link,
            "price": self.price,
            "image_url": self.image_url,
            "rating": self.rating,
            "ratingCount": self.rating_count,
        }


@dataclass
class Product:
    """Entity representing a scraped product."""
    product_id: str
    title: str
    product_link: str
    image_url: str
    position: int
    stores: list[Store] = field(default_factory=list)
    description: str = ""
    features: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.product_id:
            raise ValueError("Product ID is required")
        if not self.title:
            raise ValueError("Product title is required")

    def to_dict(self) -> dict:
        return {
            "position": self.position,
            "title": self.title,
            "product_link": self.product_link,
            "image_url": self.image_url,
            "product_id": self.product_id,
            "stores": [store.to_dict() for store in self.stores],
            "description": self.description,
            "features": self.features,
        }


@dataclass
class SearchResult:
    """Entity representing search results."""
    query: str
    products: list[Product] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "shopping_result": [product.to_dict() for product in self.products],
        }
