from abc import ABC
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PageableSchema(BaseModel):
    page_number: int
    page_size: int
    total_elements: int

class PageSchema(BaseModel, Generic[T]):
    content: List[T]
    pageable: PageableSchema

class BaseQuerySchema(BaseModel, ABC):
    page: int = 0
    size: int = 10
