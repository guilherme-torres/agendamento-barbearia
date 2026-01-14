from psycopg.rows import class_row
from app.database import get_db
from app.users.models import User


class UserRepository:
    def create(self, data: dict):
        with get_db() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute("""
                    INSERT INTO users
                    (first_name, last_name, email, password_hash, phone)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                    RETURNING *
                """, (
                    data["first_name"], 
                    data["last_name"], 
                    data["email"], 
                    data["password_hash"], 
                    data["phone"]
                ))
                return cur.fetchone()

    def get(self, id: int):
        with get_db() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute("""SELECT * FROM users WHERE id = %s""", (id,))
                return cur.fetchone()

    def get_all(self):
        with get_db() as conn:
            with conn.cursor(row_factory=class_row(User)) as cur:
                cur.execute("""SELECT * FROM users LIMIT 100""")
                return cur.fetchall()

    def delete(self, id: int):
        with get_db() as conn:
            with conn.cursor(class_row=User) as cur:
                cur.execute("""DELETE FROM users WHERE id = %s RETURNING id""", (id,))
                return cur.fetchone()

    def update(self, id: int, data: dict):
        columns = ", ".join([f"{k} = %s" for k in data.keys()])
        values = list(data.values())
        values.append(id)
        with get_db() as conn:
            with conn.cursor(class_row=User) as cur:
                cur.execute(f"""
                    UPDATE users
                    SET {columns}
                    WHERE id = %s 
                    RETURNING *
                """, values)
                return cur.fetchone()