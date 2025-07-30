"""Git/Balena Commit Schema"""
from typing import Optional

from pydantic import BaseModel


class CommitBase(BaseModel):
    balena_id: Optional[int] = None
    balena_commit_hash: Optional[str] = None
    balena_uuid: Optional[str] = None
    balena_created_at: Optional[str] = None
    balena_revision: Optional[int] = None
    git_commit_hash: Optional[str] = None
    git_slug: Optional[str] = None


class CommitCreate(CommitBase):
    balena_id: int
    balena_commit_hash: str
    balena_uuid: str
    balena_created_at: str
    balena_revision: int


class CommitUpdate(CommitBase):
    """Git/Balena Commit Update schema."""

    pass


class CommitInDBBase(CommitBase):
    """Git/Balena Commit Database base schema."""

    id: int

    class Config:
        orm_mode = True


class Commit(CommitInDBBase):
    """Git/Balena Commit schema."""

    pass


class CommitInDB(CommitInDBBase):
    pass
