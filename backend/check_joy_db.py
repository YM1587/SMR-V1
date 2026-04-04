import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

# Database URL from your environment or standard dev setup
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/smart_ranch"

async def check():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            # Find Joy
            res = await conn.execute(text("SELECT animal_id, name, tag_number FROM animal WHERE name ILIKE 'Joy' LIMIT 1"))
            joy = res.fetchone()
            if not joy:
                print("--- RESULT: Joy not found ---")
                return
            
            animal_id = joy[0]
            print(f"--- RESULT: Found Joy: id={animal_id}, tag={joy[2]} ---")
            
            # Check breeding records
            res = await conn.execute(text(f"SELECT breeding_id, breeding_date, pregnancy_status FROM breeding_record WHERE female_id = {animal_id} ORDER BY breeding_date DESC"))
            records = res.fetchall()
            print(f"--- RESULT: Breeding records: {records} ---")
    except Exception as e:
        print(f"--- ERROR: {e} ---")

if __name__ == "__main__":
    asyncio.run(check())
