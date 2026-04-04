from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

@router.post("/pen", response_model=schemas.FeedLog, status_code=status.HTTP_201_CREATED)
async def create_pen_feed_log(
    log: schemas.FeedLogCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    # Verify pen ownership
    pen_res = await db.execute(select(models.AnimalPen).where(models.AnimalPen.pen_id == log.pen_id))
    pen = pen_res.scalars().first()
    if not pen or pen.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized to log feed for this pen")

    new_log = models.FeedLog(**log.dict())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

@router.post("/individual", response_model=schemas.IndividualFeedLog, status_code=status.HTTP_201_CREATED)
async def create_individual_feed_log(
    log: schemas.IndividualFeedLogCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    # Verify animal ownership
    anim_res = await db.execute(select(models.Animal).where(models.Animal.animal_id == log.animal_id))
    animal = anim_res.scalars().first()
    if not animal or animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized to log feed for this animal")

    new_log = models.IndividualFeedLog(**log.dict())
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

@router.get("/farmer/{farmer_id}/pen", response_model=List[schemas.FeedLog])
async def read_farmer_pen_feed_logs(
    farmer_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        select(models.FeedLog)
        .join(models.AnimalPen)
        .where(models.AnimalPen.farmer_id == current_user.farmer_id)
        .order_by(models.FeedLog.date.desc())
    )
    return result.scalars().all()

@router.get("/farmer/{farmer_id}/individual", response_model=List[schemas.IndividualFeedLog])
async def read_farmer_individual_feed_logs(
    farmer_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        select(models.IndividualFeedLog)
        .join(models.Animal)
        .where(models.Animal.farmer_id == current_user.farmer_id)
        .order_by(models.IndividualFeedLog.date.desc())
    )
    return result.scalars().all()

@router.get("/individual/animal/{animal_id}", response_model=List[schemas.IndividualFeedLog])
async def read_animal_individual_feed_logs(
    animal_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: models.Farmer = Depends(get_current_user)
):
    # Verify animal ownership
    anim_res = await db.execute(select(models.Animal).where(models.Animal.animal_id == animal_id))
    animal = anim_res.scalars().first()
    if not animal or animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(
        select(models.IndividualFeedLog)
        .where(models.IndividualFeedLog.animal_id == animal_id)
        .order_by(models.IndividualFeedLog.date.desc())
    )
    return result.scalars().all()
