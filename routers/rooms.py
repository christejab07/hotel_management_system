from fastapi import APIRouter
from models import rooms
from database import database
from schemas import RoomCreate, RoomOut, RoomUpdate

router = APIRouter()

@router.post("/rooms/", response_model=RoomOut)
async def create_room(room: RoomCreate):
    query = rooms.insert().values(**room.model_dump())
    room_id = await database.execute(query)
    return {**room.model_dump(), "id": room_id}

@router.get("/rooms/", response_model=list[RoomOut])
async def list_available_rooms():
    query = rooms.select().where(rooms.c.is_available == True)
    return await database.fetch_all(query)

@router.put("/rooms/{room_id}/", response_model=RoomOut)
async def update_room(room_id: int, room: RoomUpdate):
    query = rooms.update().where(rooms.c.id == room_id).values(**room.model_dump(exclude_unset=True))
    await database.execute(query)
    query = rooms.select().where(rooms.c.id == room_id)
    return await database.fetch_one(query)
