
from uuid import UUID
from pydantic import BaseModel
from typing import Optional
# from sqlalchemy.dialects.postgresql import UUID


class SignupModel(BaseModel):
    # id: Optional[UUID]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "test@email.com",
                "password": "testpassword",
                "username": "testusername",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = "e43dc5e4f7290075ec72cbdc32d2c2957c6e258763c216f071cf7c49440ec433"

class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "testusername",
                "password": "testpassword"
            }
        }

class OrderModel(BaseModel):
    id: Optional[UUID]
    quantity: int
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'SMALL'
    user_id: Optional[UUID]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "PENDING",
                "pizza_size": "SMALL",
                "user_id": "e43dc5e4-f729-0075-ec72-cbdc32d2c295"
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[str] = 'PENDING'

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "DELIVERED"
            }
        }
