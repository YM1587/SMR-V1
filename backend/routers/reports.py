from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, desc, cast, Float
from typing import List, Dict
from datetime import date, timedelta
from decimal import Decimal

from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/fcr/{pen_id}")
async def get_pen_fcr(pen_id: int, db: AsyncSession = Depends(get_db), current_user: models.Farmer = Depends(get_current_user)):
    """
    Calculates Feed Conversion Ratio (FCR) for a specific pen.
    FCR = Total Feed Consumed / Total Weight Gain
    """
    # 1. Total Feed Consumed in this Pen
    feed_query = select(func.sum(models.FeedLog.quantity_kg)).where(models.FeedLog.pen_id == pen_id)
    feed_result = await db.execute(feed_query)
    total_feed = feed_result.scalar() or 0
    
    if total_feed == 0:
        return {"fcr": 0, "message": "No feed records found for this pen."}

    # 2. Total Weight Gain for all animals in this Pen
    # Simplified: (Current Weight - Initial Weight) for each animal
    animals_query = select(models.Animal.animal_id).where(models.Animal.pen_id == pen_id)
    animals_result = await db.execute(animals_query)
    animal_ids = animals_result.scalars().all()
    
    total_gain = 0
    for a_id in animal_ids:
        # Get earliest weight
        first_w = await db.execute(select(models.WeightRecord.weight_kg).where(models.WeightRecord.animal_id == a_id).order_by(models.WeightRecord.date.asc()).limit(1))
        # Get latest weight
        last_w = await db.execute(select(models.WeightRecord.weight_kg).where(models.WeightRecord.animal_id == a_id).order_by(models.WeightRecord.date.desc()).limit(1))
        
        start = first_w.scalar()
        end = last_w.scalar()
        
        if start and end and end > start:
            total_gain += (end - start)

    if total_gain == 0:
        return {"fcr": 0, "message": "Insufficient weight gain data for calculation."}
    
    fcr = float(total_feed) / float(total_gain)
    return {
        "pen_id": pen_id,
        "total_feed_kg": float(total_feed),
        "total_gain_kg": float(total_gain),
        "fcr": round(fcr, 2)
    }

@router.get("/mortality")
async def get_mortality_rate(farmer_id: int, db: AsyncSession = Depends(get_db), current_user: models.Farmer = Depends(get_current_user)):
    """
    Calculates mortality rate: (Deceased Animals / Total Herd Size) * 100
    """
    # Total history of animals
    total_query = select(func.count(models.Animal.animal_id)).where(models.Animal.farmer_id == farmer_id)
    total_result = await db.execute(total_query)
    total_count = total_result.scalar() or 0
    
    if total_count == 0:
        return {"mortality_rate": 0}

    # Count deceased
    deceased_query = select(func.count(models.Animal.animal_id)).where(
        and_(
            models.Animal.farmer_id == farmer_id,
            models.Animal.status == "Disposed",
            models.Animal.disposal_reason == "Deceased"
        )
    )
    deceased_result = await db.execute(deceased_query)
    deceased_count = deceased_result.scalar() or 0
    
    rate = (deceased_count / total_count) * 100
    return {
        "total_animals": total_count,
        "deceased_count": deceased_count,
        "mortality_rate": round(rate, 2)
    }

@router.get("/financial-summary")
async def get_financial_summary(farmer_id: int, db: AsyncSession = Depends(get_db), current_user: models.Farmer = Depends(get_current_user)):
    """
    Returns net expenses grouped by category.
    """
    query = select(
        models.FinancialTransaction.category,
        func.sum(models.FinancialTransaction.amount).label("total_amount")
    ).where(
        and_(
            models.FinancialTransaction.farmer_id == farmer_id,
            models.FinancialTransaction.type == "Expense"
        )
    ).group_by(models.FinancialTransaction.category)
    
    result = await db.execute(query)
    rows = result.all()
    
    summary = {row.category: float(row.total_amount) for row in rows}
    total_expenses = sum(summary.values())
    
    return {
        "categories": summary,
        "total_expenses": total_expenses
    }

@router.get("/batch-performance/{pen_id}")
async def get_batch_performance(pen_id: int, db: AsyncSession = Depends(get_db), current_user: models.Farmer = Depends(get_current_user)):
    """
    Returns financial performance for a specific batch (Pen).
    """
    # 1. Total Expenses for this Pen
    expense_query = select(func.sum(models.FinancialTransaction.amount)).where(
        and_(
            models.FinancialTransaction.related_pen_id == pen_id,
            models.FinancialTransaction.type == "Expense"
        )
    )
    expense_result = await db.execute(expense_query)
    total_expenses = expense_result.scalar() or 0
    
    # 2. Total Income for this Pen (e.g., individual animal sales from this pen, or milk production allocated)
    # For now, let's look at records where related_pen_id is set for Income
    income_query = select(func.sum(models.FinancialTransaction.amount)).where(
        and_(
            models.FinancialTransaction.related_pen_id == pen_id,
            models.FinancialTransaction.type == "Income"
        )
    )
    income_result = await db.execute(income_query)
    total_income = income_result.scalar() or 0
    
    return {
        "pen_id": pen_id,
        "total_expenses": float(total_expenses),
        "total_income": float(total_income),
        "net_performance": float(total_income - total_expenses)
    }
