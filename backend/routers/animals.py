from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(
    prefix="/animals",
    tags=["Animals & Pens"]
)

# --- PENS ---
@router.post("/pens", response_model=schemas.AnimalPen, status_code=status.HTTP_201_CREATED)
async def create_pen(pen: schemas.AnimalPenCreate, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if pen.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Cannot create pens for other farmers")
    new_pen = models.AnimalPen(**pen.dict())
    db.add(new_pen)
    await db.commit()
    await db.refresh(new_pen)
    return new_pen

@router.get("/pens/farmer/{farmer_id}", response_model=List[schemas.AnimalPen])
async def read_pens(farmer_id: int, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(select(models.AnimalPen).where(models.AnimalPen.farmer_id == farmer_id))
    return result.scalars().all()

# --- ANIMALS ---
@router.post("/", response_model=schemas.Animal, status_code=status.HTTP_201_CREATED)
async def create_animal(animal: schemas.AnimalCreate, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Cannot create animals for other farmers")
    # Check if tag exists for this farmer
    result = await db.execute(
        select(models.Animal).where(
            (models.Animal.tag_number == animal.tag_number) & 
            (models.Animal.farmer_id == animal.farmer_id)
        )
    )
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Tag number already exists for this farmer")

    new_animal = models.Animal(**animal.dict())
    db.add(new_animal)
    await db.commit()
    await db.refresh(new_animal)
    return new_animal

@router.post("/{animal_id}/dispose", response_model=schemas.Animal)
async def dispose_animal(animal_id: int, disposal: schemas.AnimalDispose, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Animal).where(models.Animal.animal_id == animal_id))
    animal = result.scalars().first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    animal.status = "Disposed"
    animal.disposal_reason = disposal.disposal_reason
    animal.disposal_date = disposal.disposal_date
    animal.disposal_value = disposal.disposal_value
    if disposal.notes:
        animal.notes = (animal.notes or "") + f"\nDisposal Notes: {disposal.notes}"
    
    await db.commit()
    await db.refresh(animal)
    return animal

@router.get("/farmer/{farmer_id}", response_model=List[schemas.Animal])
async def read_animals_by_farmer(farmer_id: int, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.farmer_id != farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(select(models.Animal).where(models.Animal.farmer_id == farmer_id))
    return result.scalars().all()

@router.get("/", response_model=List[schemas.Animal])
async def read_animals(current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Always scope to current user
    result = await db.execute(select(models.Animal).where(models.Animal.farmer_id == current_user.farmer_id))
    return result.scalars().all()

@router.put("/{animal_id}", response_model=schemas.Animal)
async def update_animal(animal_id: int, animal_update: schemas.AnimalUpdate, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Animal).where(models.Animal.animal_id == animal_id))
    db_animal = result.scalars().first()
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    if db_animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = animal_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_animal, key, value)
    
    await db.commit()
    await db.refresh(db_animal)
    return db_animal

@router.get("/{animal_id}", response_model=schemas.Animal)
async def read_animal(animal_id: int, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Animal).where(models.Animal.animal_id == animal_id))
    animal = result.scalars().first()
    if animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal.farmer_id != current_user.farmer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return animal
