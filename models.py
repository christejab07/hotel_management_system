from time import timezone
from sqlalchemy import Date, Table, Column, Integer, String, Float, Boolean, ForeignKey, text
from database import metadata

# Room model
rooms = Table(
    "rooms",
    metadata,
    Column("id", Integer, primary_key=True, index=True),  # Auto-increment ID
    Column("room_number", String, unique=True, nullable=False),  # Room number
    Column("room_type", String, nullable=False),  # Type of room (e.g., Single, Double)
    Column("price", Float, nullable=False),  # Room price
    Column("capacity", Integer, nullable=False),  # Maximum capacity
    Column("is_available", Boolean, default=True),  # Room availability
)

# Customer model
customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True, index=True),  # Auto-increment ID
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("phone_number", String, nullable=False),
)

# Reservation model
reservations = Table(
    "reservations",
    metadata,
    Column("id", Integer, primary_key=True, index=True),  # Auto-increment ID
    Column("room", Integer, ForeignKey("rooms.id"), nullable=False),  # Room ID (FK)
    Column("customer", Integer, ForeignKey("customers.id"), nullable=False),  # Customer ID (FK)
    Column("check_in", Date, nullable=False),  # Check-in date (Date only)
    Column("check_out", Date, nullable=False),  # Check-out date (Date only)
    Column("status", String, nullable=False, default="pending"),  # Reservation status
    Column("created_at", Date, server_default=text("(DATE('now'))"))
)
