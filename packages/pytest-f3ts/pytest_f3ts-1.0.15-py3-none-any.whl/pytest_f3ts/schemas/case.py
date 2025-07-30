"""Test Case Schema"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CaseBase(BaseModel):
    """Test Case Base schema."""

    name: Optional[str] = None
    config: Optional[str] = None
    user_properties: Optional[str] = None
    duration: Optional[int] = None
    result: Optional[bool] = None


class CaseCreate(CaseBase):
    """Test Case Create schema."""

    name: str
    config: str
    user_properties: str
    start: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


class CaseUpdate(CaseBase):
    """Test Case Update schema."""

    result: bool
    pass


class CaseInDBBase(CaseBase):
    """Test Case Database base schema."""

    name: str
    run_id: int

    class Config:
        orm_mode = True


class Case(CaseInDBBase):
    """Test Case schema."""

    pass


class CaseInDB(CaseInDBBase):
    pass
