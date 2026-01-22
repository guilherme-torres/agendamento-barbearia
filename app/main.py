from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import pool
from app.exception_handlers import register_exception_handlers
from app.users.routes import router as user_router
from app.auth.routes import router as auth_router
from app.schedules.routes import router as schedule_router
from app.catalog_items.routes import router as catalog_item_router
from app.appointments.routes import router as appointment_router
from app.payments.routes import router as payment_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(schedule_router)
app.include_router(catalog_item_router)
app.include_router(appointment_router)
app.include_router(payment_router)