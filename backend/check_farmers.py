import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:%24Youngmoney12327@localhost/smartranch"

async def check_farmers():
    engine = create_async_engine(DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT farmer_id, username, full_name FROM farmer"))
            rows = result.fetchall()
            print("Farmers in DB:")
            for row in rows:
                print(f"ID: {row[0]}, Username: {row[1]}, Full Name: {row[2]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(check_farmers())
