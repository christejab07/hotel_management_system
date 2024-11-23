from fastapi import APIRouter, HTTPException
from models import reservations, rooms, customers
from database import database
from schemas import ReservationCreate, ReservationOut
from datetime import datetime

router = APIRouter()


# make a reservation
@router.post("/reservations/", response_model=ReservationOut)
async def create_reservation(reservation: ReservationCreate):
    # Ensure the room exists and is available
    room_query = rooms.select().where(
        rooms.c.id == reservation.room,
        rooms.c.is_available == True,  # Explicit check for availability
    )
    room = await database.fetch_one(room_query)
    if not room:
        raise HTTPException(
            status_code=400, detail="Room is not available or does not exist."
        )

    # Ensure the customer exists
    customer_query = customers.select().where(customers.c.id == reservation.customer)
    customer = await database.fetch_one(customer_query)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer does not exist.")

    # Prepare reservation data
    reservation_data = reservation.model_dump(exclude={"id", "created_at"})

    # Use a transaction to ensure atomicity
    async with database.transaction():
        # Create the reservation
        reservation_query = reservations.insert().values(**reservation_data)
        reservation_id = await database.execute(reservation_query)

        # Mark the room as unavailable
        update_room_query = (
            rooms.update()
            .where(rooms.c.id == reservation.room)
            .values(is_available=False)
        )
        await database.execute(update_room_query)

    # Return the created reservation
    return {
        **reservation.model_dump(),
        "id": reservation_id,
        "created_at": datetime.now().date(),  # Corrected datetime usage
    }


# List all reservations
@router.get("/reservations/", response_model=list[ReservationOut])
async def list_reservations():
    query = reservations.select()
    results = await database.fetch_all(query)

    return [
        {
            "id": reservation["id"],
            "room": reservation["room"],
            "customer": {
                "id": reservation["id"]
            },
            "check_in": reservation["check_in"],
            "check_out": reservation["check_out"],
            "status": reservation["status"],
            "created_at": reservation["created_at"],
        }
        for reservation in results
    ]
