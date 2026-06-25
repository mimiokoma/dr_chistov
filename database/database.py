import aiosqlite


async def init_db():
    async with aiosqlite.connect("data/db.sqlite3") as db:
        await db.execute("""
                         CREATE TABLE IF NOT EXISTS slots
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             date
                             TEXT
                             NOT
                             NULL,
                             time
                             TEXT
                             NOT
                             NULL,
                             is_booked
                             INTEGER
                             DEFAULT
                             0,

                             UNIQUE
                         (
                             date,
                             time
                         )
                             )
                         """)

        await db.execute("""
                         CREATE TABLE IF NOT EXISTS completed_orders
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT,
                             amount
                             INTEGER
                             NOT
                             NULL,
                             created_at
                             TEXT
                             NOT
                             NULL
                         )
                         """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT,
            date TEXT,
            time TEXT,
            client_name TEXT,
            client_phone TEXT,
            address TEXT,
            source TEXT,
            price TEXT,
            comment TEXT,
            photos TEXT,
            status TEXT DEFAULT 'new',
            message_id INTEGER,
            chat_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()