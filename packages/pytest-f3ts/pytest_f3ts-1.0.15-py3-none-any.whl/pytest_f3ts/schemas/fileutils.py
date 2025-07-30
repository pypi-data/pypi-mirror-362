"""Models for managing filesystem of the `pytest` processes."""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class FileHeirarchy(BaseModel):
    filename: str
    filepath: str
    type: str = "file"
    fileContent: str = ""
    children: List["Optional[FileHeirarchy]"] = []
