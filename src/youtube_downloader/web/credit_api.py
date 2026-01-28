"""
Credit management API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from .database import get_db
from .models_db import User, CreditTransaction
from .auth_api import get_current_user

router = APIRouter(prefix="/api/v1/credits", tags=["Credits"])


# Pydantic models
class CreditBalance(BaseModel):
    """Credit balance response."""
    credits: int
    
    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    """Transaction response."""
    id: str
    amount: int
    type: str
    description: Optional[str]
    balance_after: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class CreditHistoryResponse(BaseModel):
    """Credit history response."""
    total: int
    transactions: List[TransactionResponse]


class EstimateRequest(BaseModel):
    """Estimate request."""
    quality: str
    audio_quality: Optional[str] = None


class EstimateResponse(BaseModel):
    """Estimate response."""
    credits_required: int
    quality: str
    audio_quality: Optional[str]


# Credit cost mapping
QUALITY_CREDITS = {
    "360p": 1,
    "480p": 2,
    "720p": 3,
    "1080p": 5,
    "1440p": 8,
    "2160p": 12,
    "best": 5,  # Default to 1080p cost
}

AUDIO_CREDITS = {
    "64kbps": 1,
    "128kbps": 1,
    "192kbps": 2,
    "256kbps": 2,
    "320kbps": 2,
    "best": 2,  # Default to high quality
}


def calculate_credits(quality: str, audio_quality: Optional[str] = None) -> int:
    """
    Calculate required credits for download.
    
    Args:
        quality: Video quality
        audio_quality: Audio quality (optional)
        
    Returns:
        Required credits
    """
    credits = QUALITY_CREDITS.get(quality, 5)  # Default to 1080p
    
    if audio_quality:
        credits += AUDIO_CREDITS.get(audio_quality, 2)
    
    return credits


# API endpoints
@router.get("/balance", response_model=CreditBalance)
async def get_balance(
    current_user: User = Depends(get_current_user)
):
    """
    Get current credit balance.
    
    Returns:
        Current credit balance
    """
    return CreditBalance(credits=current_user.credits)


@router.get("/history", response_model=CreditHistoryResponse)
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get credit transaction history.
    
    Args:
        limit: Number of transactions to return
        offset: Offset for pagination
        
    Returns:
        Transaction history
    """
    # Get total count
    total = db.query(CreditTransaction).filter(
        CreditTransaction.user_id == current_user.id
    ).count()
    
    # Get transactions
    transactions = db.query(CreditTransaction).filter(
        CreditTransaction.user_id == current_user.id
    ).order_by(
        desc(CreditTransaction.created_at)
    ).limit(limit).offset(offset).all()
    
    return CreditHistoryResponse(
        total=total,
        transactions=[
            TransactionResponse(
                id=t.id,
                amount=t.amount,
                type=t.type,
                description=t.description,
                balance_after=t.balance_after,
                created_at=t.created_at
            )
            for t in transactions
        ]
    )


@router.post("/estimate", response_model=EstimateResponse)
async def estimate_cost(
    request: EstimateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Estimate download cost.
    
    Args:
        request: Estimate request with quality settings
        
    Returns:
        Estimated credits required
    """
    credits = calculate_credits(request.quality, request.audio_quality)
    
    return EstimateResponse(
        credits_required=credits,
        quality=request.quality,
        audio_quality=request.audio_quality
    )


def deduct_credits(
    user: User,
    credits: int,
    description: str,
    db: Session
) -> bool:
    """
    Deduct credits from user account.
    
    Args:
        user: User object
        credits: Credits to deduct
        description: Transaction description
        db: Database session
        
    Returns:
        True if successful, False if insufficient credits
    """
    if user.credits < credits:
        return False
    
    # Deduct credits
    user.credits -= credits
    
    # Create transaction record
    transaction = CreditTransaction(
        user_id=user.id,
        amount=-credits,
        type="usage",
        description=description,
        balance_after=user.credits
    )
    
    db.add(transaction)
    db.commit()
    
    return True


def refund_credits(
    user: User,
    credits: int,
    description: str,
    db: Session
):
    """
    Refund credits to user account.
    
    Args:
        user: User object
        credits: Credits to refund
        description: Transaction description
        db: Database session
    """
    # Add credits back
    user.credits += credits
    
    # Create transaction record
    transaction = CreditTransaction(
        user_id=user.id,
        amount=credits,
        type="refund",
        description=description,
        balance_after=user.credits
    )
    
    db.add(transaction)
    db.commit()
