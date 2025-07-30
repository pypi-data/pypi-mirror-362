"""Test Attachment Schema"""
from typing import Optional

from pydantic import BaseModel


class AttachmentBase(BaseModel):
    """Test Attachment Base schema."""

    name: Optional[str]
    filepath: Optional[str]


class AttachmentCreate(AttachmentBase):
    """Test Attachment Create schema."""

    name: str
    filepath: str


class AttachmentUpdate(AttachmentBase):
    """Test Attachment Update schema."""

    pass


class AttachmentInDBBase(AttachmentBase):
    """Test Attachment Database base schema."""

    id: int
    run_id: int

    class Config:
        orm_mode = True


class Attachment(AttachmentInDBBase):
    """Test Attachment schema."""

    pass


class AttachmentInDB(AttachmentInDBBase):
    pass
