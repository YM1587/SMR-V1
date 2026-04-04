from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

from database import get_db
import models
import schemas
from auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)

@router.post("/", response_model=schemas.Farmer, status_code=status.HTTP_201_CREATED)
async def create_farmer(farmer: schemas.FarmerCreate, db: AsyncSession = Depends(get_db)):
    # Check if username exists
    result = await db.execute(select(models.Farmer).where(models.Farmer.username == farmer.username))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Securely hash the password
    hashed_password = get_password_hash(farmer.password)
    new_farmer = models.Farmer(
        username=farmer.username,
        password_hash=hashed_password,
        full_name=farmer.full_name,
        phone_number=farmer.phone_number,
        farm_name=farmer.farm_name,
        location=farmer.location,
        farm_type=farmer.farm_type
    )
    db.add(new_farmer)
    await db.commit()
    await db.refresh(new_farmer)
    return new_farmer

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Farmer).where(models.Farmer.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "farmer_id": user.farmer_id}

@router.get("/me", response_model=schemas.Farmer)
async def read_farmer_me(current_user: models.Farmer = Depends(get_current_user)):
    return current_user

@router.get("/{farmer_id}", response_model=schemas.Farmer)
async def read_farmer(farmer_id: int, current_user: models.Farmer = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.farmer_id != farmer_id:
         raise HTTPException(status_code=403, detail="Not authorized to view other farmer records")
    result = await db.execute(select(models.Farmer).where(models.Farmer.farmer_id == farmer_id))
    farmer = result.scalars().first()
    if farmer is None:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer
