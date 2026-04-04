import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/smart_ranch"

async def inspect():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as conn:
            # Check table columns for breeding_record
            print("--- BreedingRecord Columns ---")
            res = await conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'breeding_record'
            """))
            for row in res.fetchall():
                print(f"{row[0]}: {row[1]}")
            
            # Check Joy specifically
            print("\n--- Joy's Records ---")
            res = await conn.execute(text("SELECT animal_id FROM animal WHERE name ILIKE 'Joy' LIMIT 1"))
            joy = res.fetchone()
            if joy:
                joy_id = joy[0]
                res = await conn.execute(text(f"SELECT * FROM breeding_record WHERE female_id = {joy_id}"))
                records = res.fetchall()
                print(f"Count: {len(records)}")
                for r in records:
                    print(r)
            else:
                print("Joy not found")
                
    except Exception as e:
        print(f"--- ERROR: {e} ---")

if __name__ == "__main__":
    asyncio.run(inspect())
