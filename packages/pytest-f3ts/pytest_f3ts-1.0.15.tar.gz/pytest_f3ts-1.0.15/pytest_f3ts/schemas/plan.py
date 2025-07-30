"""Test Plan Schema"""
from typing import Dict, Optional

from pydantic import BaseModel

from .commit import Commit
from .config import FixtureSettings, GUISettings
from .limits import LimitsBase


class PlanBase(BaseModel):
    """Test Plan Base schema."""

    name: Optional[str] = None
    customer_name: Optional[str] = None
    project_name: Optional[str] = None
    part_number: Optional[str] = None
    version: Optional[str] = None
    path: Optional[str] = None
    limits_settings: Optional[LimitsBase] = None
    runner_settings: Optional[GUISettings] = None
    fixture_settings: Optional[Dict[str, FixtureSettings]] = None


class PlanCreate(PlanBase):
    """Test Plan Create schema."""

    path: str = "."


class PlanUpdate(PlanBase):
    """Test Plan Update schema."""

    pass


class PlanInDBBase(PlanBase):
    """Test Plan Database base schema."""

    id: int
    uuid: str
    owner_id: int
    commit_id: int = None
    commit: Optional[Commit] = None

    class Config:
        orm_mode = True


class Plan(PlanInDBBase):
    """Test Plan schema."""

    pass


class PlanInDB(PlanInDBBase):
    pass
