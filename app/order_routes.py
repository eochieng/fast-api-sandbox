from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from app.models import Order, User
from app.schemas import OrderModel, OrderStatusModel
from app.database import Session, engine


order_router = APIRouter(
    prefix='/orders',
    tags=['orders'],
)

session = Session(bind=engine)

# get order by id
@order_router.get("/orders/{id}", status_code=status.HTTP_200_OK)
async def get_order(id: UUID, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
    if not user.is_staff and order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return order

# Get all orders
@order_router.get("/orders", status_code=status.HTTP_200_OK)
async def get_all_orders(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    orders = session.query(Order).filter(Order.user_id == db_user.id).all()
    return orders

# create a new order
@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    current_user = Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == current_user).first()
    order_data = dict(order)
    order_data.update({'user_id': db_user.id})
    order = Order(**order_data)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

# update an order
@order_router.put("/order/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_order(id: UUID, order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    order_data = dict(order)
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
    if not user.is_staff and order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    order.quantity = order_data.get('quantity')
    order.order_status = order_data.get('order_status')
    order.pizza_size = order_data.get('pizza_size')
    session.commit()
    session.refresh(order)
    return order

# update order status
@order_router.put("/order/{id}/status", status_code=status.HTTP_202_ACCEPTED)
async def update_order_status(id: UUID, order: OrderStatusModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    order_data = dict(order)
    user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
    if not user.is_staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.order_status = order_data.get('order_status')
    session.commit()
    session.refresh(order)
    return order

# delete an order
@order_router.delete("/order/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: UUID, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    order = session.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user = session.query(User).filter(User.username == Authorize.get_jwt_subject()).first()
    if not user.is_staff and order.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    session.delete(order)
    session.commit()
    return "Order deleted"