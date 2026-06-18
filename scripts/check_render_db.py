import asyncio
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    engine = create_async_engine(os.environ["DATABASE_URL"])

    async with engine.connect() as conn:
        result = await conn.execute(
            text(
                """
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY tablename
                """
            )
        )

        print([row[0] for row in result.fetchall()])

    await engine.dispose()


asyncio.run(main())