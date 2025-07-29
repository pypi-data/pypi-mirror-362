"""
Data models for Notify Africa SDK
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class SMSResponse:
    """Response model for SMS operations"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None
    balance: Optional[float] = None
    credits_spent: Optional[int] = None
    sms_id: Optional[str] = None


@dataclass
class BulkSMSResponse:
    """Response model for bulk SMS operations"""
    success: bool
    message: str
    total_messages: int
    successful_messages: int
    failed_messages: int
    balance: Optional[float] = None
    total_credits: Optional[int] = None
    messages: Optional[List[Dict[str, Any]]] = None


@dataclass
class DeliveryStatus:
    """Delivery status model"""
    sms_id: str
    recipient: str
    status: str
    status_description: str
    delivered_at: Optional[datetime] = None
    credits: Optional[int] = None


@dataclass
class SenderID:
    """Sender ID model"""
    id: int
    name: str
    status: str
    purpose: str
    access: str
    created_at: datetime