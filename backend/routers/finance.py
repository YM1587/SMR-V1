from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(
    prefix="/finance",
    tags=["Finance"]
)

@router.post("/", response_model=schemas.FinancialTransaction, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: schemas.FinancialTransactionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if transaction.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized to create transactions for other farmers")
        
    new_transaction = models.FinancialTransaction(**transaction.dict())
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

@router.get("/farmer/{farmer_id}", response_model=List[schemas.FinancialTransaction])
async def read_transactions(
    farmer_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    result = await db.execute(
        select(models.FinancialTransaction)
        .where(models.FinancialTransaction.farmer_id == current_user.farmer_id)
        .order_by(models.FinancialTransaction.date.desc())
    )
    return result.scalars().all()
