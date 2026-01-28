"""
SQLAlchemy database models.
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .database import Base


def generate_uuid():
    """Generate UUID as string."""
    return str(uuid.uuid4())


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    credits = Column(Integer, default=5, nullable=False)  # 신규 가입 보너스 5 크레딧
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    credit_transactions = relationship("CreditTransaction", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    downloads = relationship("Download", back_populates="user", cascade="all, delete-orphan")


class CreditTransaction(Base):
    """Credit transaction model."""
    __tablename__ = "credit_transactions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # 양수: 충전, 음수: 사용
    type = Column(String(50), nullable=False)  # 'purchase', 'bonus', 'usage', 'refund'
    description = Column(Text)
    balance_after = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="credit_transactions")


class Payment(Base):
    """Payment model."""
    __tablename__ = "payments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(String(255), unique=True, nullable=False, index=True)
    amount = Column(Integer, nullable=False)  # 결제 금액 (원)
    credits = Column(Integer, nullable=False)  # 구매한 크레딧
    status = Column(String(50), nullable=False)  # 'pending', 'completed', 'failed', 'refunded'
    payment_key = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="payments")


class Download(Base):
    """Download model."""
    __tablename__ = "downloads"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(String(36), nullable=False, index=True)
    video_url = Column(Text, nullable=False)
    video_title = Column(Text)
    quality = Column(String(20), nullable=False)
    credits_used = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)  # 'pending', 'downloading', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="downloads")
