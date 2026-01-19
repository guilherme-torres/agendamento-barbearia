from psycopg.rows import class_row
from app.appointments.models import Appointment
from app.database import get_db


class AppointmentRepository:
    async def create(self, data: dict):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Appointment)) as cur:
                await cur.execute("""
                    INSERT INTO appointments
                    (client_id, barber_id, catalog_item_id, appointment_date, appointment_time, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    data["client_id"],
                    data["barber_id"],
                    data["catalog_item_id"],
                    data["appointment_date"],
                    data["appointment_time"],
                    data["status"],
                ))
                return await cur.fetchone()

    async def get(self, id: int):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Appointment)) as cur:
                await cur.execute("""SELECT * FROM appointments WHERE id = %s""", (id,))
                return await cur.fetchone()

    async def get_all(self):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Appointment)) as cur:
                await cur.execute("""SELECT * FROM appointments LIMIT 100""")
                return await cur.fetchall()

    async def delete(self, id: int):
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""DELETE FROM appointments WHERE id = %s RETURNING id""", (id,))
                return await cur.fetchone()

    async def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Appointment)) as cur:
                await cur.execute(f"""
                    UPDATE appointments
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return await cur.fetchone()