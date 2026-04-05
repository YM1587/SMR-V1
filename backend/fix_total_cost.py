import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:%24Youngmoney12327@localhost/smartranch')

async def migrate():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print('Fixing feed_log table...')
        # Drop the existing total_cost if it is NOT a generated column
        # Or just drop and recreate correctly.
        try:
            print('Dropping and recreating total_cost on feed_log...')
            await conn.execute(text("ALTER TABLE feed_log DROP COLUMN IF EXISTS total_cost;"))
            await conn.execute(text("ALTER TABLE feed_log ADD COLUMN total_cost NUMERIC(10, 2) GENERATED ALWAYS AS (quantity_kg * cost_per_kg) STORED;"))
            
            print('Dropping and recreating total_cost on individual_feed_log...')
            await conn.execute(text("ALTER TABLE individual_feed_log DROP COLUMN IF EXISTS total_cost;"))
            await conn.execute(text("ALTER TABLE individual_feed_log ADD COLUMN total_cost NUMERIC(10, 2) GENERATED ALWAYS AS (quantity_kg * cost_per_kg) STORED;"))
            
            print('Migration successful!')
        except Exception as e:
            print(f'Error: {e}')
            
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(migrate())
