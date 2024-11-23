from fastapi import APIRouter
from models import customers
from database import database
from schemas import CustomerCreate, CustomerOut

router = APIRouter()

@router.post("/customers/", response_model=CustomerOut)
async def create_customer(customer: CustomerCreate):
    query = customers.insert().values(**customer.model_dump())
    customer_id = await database.execute(query)
    return {**customer.model_dump(), "id": customer_id}

@router.get("/customers/", response_model=list[CustomerOut])
async def list_customers():
    query = customers.select()
    return await database.fetch_all(query)
