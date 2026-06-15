import aiosqlite

from datetime import datetime

DB_PATH = "data/db.sqlite3"


async def add_slot(date: str, time: str):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO slots(date, time)
            VALUES(?, ?)
            """,
            (date, time)
        )

        await db.commit()


async def get_free_slots():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT date, time
            FROM slots
            WHERE is_booked = 0
            ORDER BY date, time
            """
        )

        return await cursor.fetchall()

import aiosqlite

DB_PATH = "data/db.sqlite3"


async def save_slots(
        date: str,
        times: list[str]
):

    async with aiosqlite.connect(DB_PATH) as db:

        added = 0

        for time in times:

            try:

                await db.execute(
                    """
                    INSERT INTO slots(date, time)
                    VALUES(?, ?)
                    """,
                    (date, time)
                )

                added += 1

            except Exception:
                pass

        await db.commit()

        return added

async def get_all_slots():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT date, time
            FROM slots
            WHERE is_booked = 0
            ORDER BY date, time
            """
        )

        return await cursor.fetchall()

async def get_slots_by_date(date: str):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT id, time
            FROM slots
            WHERE date = ?
            AND is_booked = 0
            ORDER BY time
            """,
            (date,)
        )

        return await cursor.fetchall()

async def get_available_dates():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT DISTINCT date
            FROM slots
            WHERE is_booked = 0
            ORDER BY date
            """
        )

        return await cursor.fetchall()

async def delete_slots(slot_ids: list[int]):

    async with aiosqlite.connect(DB_PATH) as db:

        for slot_id in slot_ids:

            await db.execute(
                """
                DELETE FROM slots
                WHERE id = ?
                """,
                (slot_id,)
            )

        await db.commit()

async def get_order_dates():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT DISTINCT date
            FROM slots
            WHERE is_booked = 0
            ORDER BY date
            """
        )

        return await cursor.fetchall()

async def get_order_times(date: str):

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT time
            FROM slots
            WHERE date = ?
            AND is_booked = 0
            ORDER BY time
            """,
            (date,)
        )

        return await cursor.fetchall()

async def book_slot(
        date: str,
        time: str
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            UPDATE slots
            SET is_booked = 1
            WHERE date = ?
            AND time = ?
            """,
            (
                date,
                time
            )
        )

        await db.commit()

async def add_completed_order(
        amount: int
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO completed_orders(
                amount,
                created_at
            )
            VALUES(?, ?)
            """,
            (
                amount,
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )
        )

        await db.commit()

async def get_month_profit():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT SUM(amount)
            FROM completed_orders
            WHERE strftime(
                '%Y-%m',
                created_at
            ) =
            strftime(
                '%Y-%m',
                'now'
            )
            """
        )

        result = await cursor.fetchone()

        return result[0] or 0

async def add_completed_order(
        amount: int
):

    async with aiosqlite.connect(DB_PATH) as db:

        await db.execute(
            """
            INSERT INTO completed_orders(
                amount,
                created_at
            )
            VALUES(?, ?)
            """,
            (
                amount,
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
            )
        )

        await db.commit()

async def get_month_profit():

    async with aiosqlite.connect(DB_PATH) as db:

        cursor = await db.execute(
            """
            SELECT SUM(amount)
            FROM completed_orders
            WHERE strftime(
                '%Y-%m',
                created_at
            ) =
            strftime(
                '%Y-%m',
                'now'
            )
            """
        )

        result = await cursor.fetchone()

        return result[0] or 0