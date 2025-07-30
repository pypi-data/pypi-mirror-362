"""Models for messaging between the Test Executor and `pytest` processes."""

from typing import Dict, Optional

from pydantic import BaseModel

from .config import TestCase


class LimitsBase(BaseModel):
    """Test Limits Base Model."""

    test_name: Optional[str] = None
    version: Optional[str] = None
    test_cases: Optional[Dict[str, TestCase]] = None
    # runner_settings: Optional[GUISettings] = None


class LimitsCreate(LimitsBase):
    """Test Limits Create"""

    test_name: str
    version: str
    test_cases: Dict[str, TestCase]
    # runner_settings: GUISettings


class LimitsUpdate(LimitsBase):
    """Git/Balena Limits Update schema."""

    pass


class LimitsInDBBase(LimitsBase):
    """Git/Balena Limits Database base schema."""

    id: int

    class Config:
        orm_mode = True


class Limits(LimitsInDBBase):
    """Git/Balena Limits schema."""

    pass


class LimitsInDB(LimitsInDBBase):
    pass
