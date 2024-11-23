from fastapi import FastAPI
from database import database, metadata, engine
from routers import rooms, customers, reservations
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

# Initialize the database metadata
metadata.create_all(bind=engine)


# Lifespan context manager
async def lifespan(app: FastAPI):
    await database.connect()  # Connect to the database
    yield
    await database.disconnect()  # Disconnect from the database


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(rooms.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(reservations.router, prefix="/api")

# Templates for rendering
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
