from psycopg.rows import class_row
from app.catalog_items.models import CatalogItem
from app.database import get_db


class CatalogItemRepository:
    async def create(self, data: dict):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(CatalogItem)) as cur:
                await cur.execute("""
                    INSERT INTO catalog_items
                    (barber_id, name, description, price, duration)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    data["barber_id"], 
                    data["name"], 
                    data["description"], 
                    data["price"], 
                    data["duration"],
                ))
                return await cur.fetchone()

    async def get(self, id: int):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(CatalogItem)) as cur:
                await cur.execute("""SELECT * FROM catalog_items WHERE id = %s""", (id,))
                return await cur.fetchone()

    async def get_all(self):
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(CatalogItem)) as cur:
                await cur.execute("""SELECT * FROM catalog_items LIMIT 100""")
                return await cur.fetchall()

    async def delete(self, id: int):
        async with get_db() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""DELETE FROM catalog_items WHERE id = %s RETURNING id""", (id,))
                return await cur.fetchone()

    async def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        async with get_db() as conn:
            async with conn.cursor(row_factory=class_row(CatalogItem)) as cur:
                await cur.execute(f"""
                    UPDATE catalog_items
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return await cur.fetchone()