from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Optional[int] = None
    is_active: bool = True
    subscriptions: List['Subscription'] = []

    class Config:
        from_attributes: True


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


class SubscriptionType(str, Enum):
    single = 'single'
    family = 'family'


class SubscriptionBase(BaseModel):
    type: SubscriptionType = None


class SubscriptionCreate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    id: int
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True


class BaseBook(BaseModel):
    title: str
    description: Optional[str] = None
    author_id: int
    price: int
    published_year: int


class CreateBook(BaseBook):
    pass


class UpdateBook(BaseBook):
    pass


class Book(BaseBook):
    id: int

    class Config:
        from_attributes = True


class BaseAuthor(BaseModel):
    first_name: str
    last_name: str


class CreateAuthor(BaseAuthor):
    pass


class UpdateAuthor(BaseAuthor):
    pass


class Author(BaseAuthor):
    id: int

    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    amount: float
    status: str


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    user_id: int
    subscription_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
