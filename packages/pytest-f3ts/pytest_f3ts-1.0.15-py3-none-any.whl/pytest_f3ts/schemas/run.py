"""Test Run Schema"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .limits import Limits
from .result import Result


class RunBase(BaseModel):
    """Test Run Base schema."""

    operator_id: Optional[int] = None
    serial_number: Optional[str] = None
    slot_id: Optional[str] = None
    api_url: Optional[str] = None
    test_plan_version: Optional[str] = None
    start: Optional[str] = None
    duration: Optional[float] = None
    passed: Optional[bool] = None
    log_file: Optional[str] = None
    num_failed: Optional[int] = None
    num_passed: Optional[int] = None
    num_skipped: Optional[int] = None


class RunCreate(RunBase):
    """Test Run Create schema."""

    operator_id: int
    slot_id: str
    api_url: str
    start: str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


class RunUpdate(RunBase):
    """Test Run Update schema."""

    pass


class RunInDBBase(RunBase):
    """Test Run Database base schema."""

    id: int
    plan_id: int
    limits_id: Optional[int]
    results_id: Optional[int] = None
    results: Optional[List[Result]] = None
    limits: Optional[Limits] = None

    class Config:
        orm_mode = True


class Run(RunInDBBase):
    """Test Run schema."""

    pass


class RunInDB(RunInDBBase):
    pass
