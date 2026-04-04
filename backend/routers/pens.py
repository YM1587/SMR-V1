from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(
    prefix="/pens",
    tags=["Pens"]
)

@router.get("/", response_model=List[schemas.AnimalPen])
async def get_pens(
    farmer_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    result = await db.execute(
        select(models.AnimalPen)
        .where(models.AnimalPen.farmer_id == current_user.farmer_id)
    )
    return result.scalars().all()

@router.post("/", response_model=schemas.AnimalPen, status_code=status.HTTP_201_CREATED)
async def create_pen(
    pen: schemas.AnimalPenCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if pen.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized to create pens for other farmers")
        
    new_pen = models.AnimalPen(**pen.dict())
    db.add(new_pen)
    await db.commit()
    await db.refresh(new_pen)
    return new_pen
