import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:%24Youngmoney12327@localhost/smartranch')

async def main():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print('Detecting existing check constraints on breeding_record...')
        # Get existing check constraints
        res = await conn.execute(text("""
            SELECT conname 
            FROM pg_constraint 
            WHERE conrelid = 'breeding_record'::regclass AND contype = 'c';
        """))
        constraints = [row[0] for row in res.all()]
        print(f'Found constraints: {constraints}')
        
        for con in constraints:
            if 'pregnancy_status' in con:
                print(f'Dropping old constraint: {con}')
                await conn.execute(text(f"ALTER TABLE breeding_record DROP CONSTRAINT \"{con}\";"))
        
        print('Adding new standardized pregnancy_status check constraint...')
        # Explicitly allow 'Pregnant', 'Failed', 'Unknown', 'Calved'
        await conn.execute(text("""
            ALTER TABLE breeding_record 
            ADD CONSTRAINT breeding_record_pregnancy_status_check 
            CHECK (pregnancy_status IN ('Pregnant', 'Failed', 'Unknown', 'Calved'));
        """))
        
        print('Constraint update successful!')
        
        print('Syncing existing data (Confirmed -> Pregnant)...')
        await conn.execute(text("UPDATE breeding_record SET pregnancy_status = 'Pregnant' WHERE pregnancy_status = 'Confirmed';"))
        
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())
