import asyncio
from database import engine
from sqlalchemy import text
import models

async def check():
    async with engine.connect() as conn:
        # Find Joy
        res = await conn.execute(text("SELECT animal_id, name, tag_number FROM animal WHERE name ILIKE 'Joy' LIMIT 1"))
        joy = res.fetchone()
        if not joy:
            print("Joy not found")
            return
        
        animal_id = joy[0]
        print(f"Found Joy: animal_id={animal_id}, tag={joy[2]}")
        
        # Check breeding records
        res = await conn.execute(text(f"SELECT breeding_id, breeding_date, pregnancy_status FROM breeding_record WHERE female_id = {animal_id} ORDER BY breeding_date DESC"))
        records = res.fetchall()
        print(f"Breeding records for Joy: {records}")

if __name__ == "__main__":
    asyncio.run(check())
