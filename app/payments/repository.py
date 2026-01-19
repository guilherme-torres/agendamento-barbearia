from psycopg.rows import class_row
from app.payments.models import Payment
from app.database import get_db


class PaymentRepository:
    async def create(self, data: dict):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Payment)) as cur:
                await cur.execute("""
                    INSERT INTO payments
                    (appointment_id, amount, method, paid_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    data["appointment_id"], 
                    data["amount"], 
                    data["method"], 
                    data["paid_at"], 
                ))
                return await cur.fetchone()

    async def get(self, id: int):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Payment)) as cur:
                await cur.execute("""SELECT * FROM payments WHERE id = %s""", (id,))
                return await cur.fetchone()

    async def get_all(self):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Payment)) as cur:
                await cur.execute("""SELECT * FROM payments LIMIT 100""")
                return await cur.fetchall()

    async def delete(self, id: int):
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""DELETE FROM payments WHERE id = %s RETURNING id""", (id,))
                return await cur.fetchone()

    async def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(Payment)) as cur:
                await cur.execute(f"""
                    UPDATE payments
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return await cur.fetchone()