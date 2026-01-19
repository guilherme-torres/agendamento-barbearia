from psycopg.rows import class_row
from app.schedules.models import Schedule
from app.database import get_db


class ScheduleRepository:
    async def create(self, data: dict):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Schedule)) as cur:
                await cur.execute("""
                    INSERT INTO schedules
                    (barber_id, day_of_week, start_time, end_time, break_start, break_end, tolerance)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    data["barber_id"], 
                    data["day_of_week"], 
                    data["start_time"], 
                    data["end_time"], 
                    data["break_start"],
                    data["break_end"],
                    data["tolerance"],
                ))
                return await cur.fetchone()

    async def get(self, id: int):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Schedule)) as cur:
                await cur.execute("""SELECT * FROM schedules WHERE id = %s""", (id,))
                return await cur.fetchone()

    async def get_all(self):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Schedule)) as cur:
                await cur.execute("""SELECT * FROM schedules LIMIT 100""")
                return await cur.fetchall()

    async def delete(self, id: int):
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""DELETE FROM schedules WHERE id = %s RETURNING id""", (id,))
                return await cur.fetchone()

    async def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Schedule)) as cur:
                await cur.execute(f"""
                    UPDATE schedules
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return await cur.fetchone()