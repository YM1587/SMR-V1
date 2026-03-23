import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:%24Youngmoney12327@localhost/smartranch")

async def run_migration():
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        print("Creating alert table...")
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS alert (
                    id SERIAL PRIMARY KEY,
                    farmer_id INT NOT NULL REFERENCES farmer(farmer_id) ON DELETE CASCADE,
                    type VARCHAR(20) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    severity VARCHAR(20) NOT NULL,
                    related_animal_id INT REFERENCES animal(animal_id) ON DELETE SET NULL,
                    is_active INT DEFAULT 1,
                    is_dismissed INT DEFAULT 0,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """))
            print("Alert table created successfully!")
        except Exception as e:
            print(f"Error creating alert table: {e}")

    await engine.dispose()
    print("Migration complete!")

if __name__ == "__main__":
    asyncio.run(run_migration())
