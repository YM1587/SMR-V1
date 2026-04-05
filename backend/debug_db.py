import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
import json

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:%24Youngmoney12327@localhost/smartranch')

async def main():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print('--- FEED LOG TABLE ---')
        res = await conn.execute(text("SELECT * FROM feed_log ORDER BY created_at DESC LIMIT 1;"))
        row = res.fetchone()
        if row:
            # Row mapping in asyncpg/sqlalchemy
            cols = res.keys()
            print(dict(zip(cols, row)))
        else:
            print('No logs found.')
            
        print('\n--- SCHEMA ---')
        res = await conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'feed_log';"))
        for row in res.all():
            print(f'{row[0]}: {row[1]}')
            
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())
