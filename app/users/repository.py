from psycopg.rows import class_row
from app.database import get_db
from app.users.models import User


class UserRepository:
    async def create(self, data: dict):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("""
                    INSERT INTO users
                    (name, email, password_hash, phone)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                    RETURNING *
                """, (
                    data["name"], 
                    data["email"], 
                    data["password_hash"], 
                    data["phone"]
                ))
                return await cur.fetchone()

    async def get(self, id: int):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("""SELECT * FROM users WHERE id = %s""", (id,))
                return await cur.fetchone()

    async def get_all(self, limit: int = 100, offset: int = 0):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("""
                    SELECT * FROM users
                    ORDER BY id LIMIT %s OFFSET %s
                """, (limit, offset))
                return await cur.fetchall()

    async def delete(self, id: int):
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""DELETE FROM users WHERE id = %s RETURNING id""", (id,))
                return await cur.fetchone()

    async def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute(f"""
                    UPDATE users
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return await cur.fetchone()
            
    async def get_by_email(self, email: str):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(User)) as cur:
                await cur.execute("""SELECT * FROM users WHERE email = %s""", (email,))
                return await cur.fetchone()