from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


# Room schemas
class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=10)
    room_type: str
    price: float
    capacity: int
    is_available: Optional[bool] = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    room_number: Optional[str]
    room_type: Optional[str]
    price: Optional[float]
    capacity: Optional[int]
    is_available: Optional[bool]


class RoomOut(RoomBase):
    id: int  # Auto-generated ID

    class Config:
        from_attributes = True


# Customer schemas
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str


class CustomerCreate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class CustomerSchema(BaseModel):
    id: int


# Reservation schemas
class ReservationBase(BaseModel):
    room: int  # Room ID
    customer: CustomerSchema
    check_in: date  # Check-in date (Date only)
    check_out: date  # Check-out date (Date only)
    status: Optional[str] = "pending"


class ReservationCreate(ReservationBase):
    pass


class ReservationOut(ReservationBase):
    id: int
    created_at: date  # Created date (Date only)

    class Config:
        from_attributes = True
