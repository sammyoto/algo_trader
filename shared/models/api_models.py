from pydantic import BaseModel
from typing import Generic, TypeVar, Union, Optional, List
from enum import Enum

T = TypeVar("T")

class Status(int, Enum):
    FAILED = 400
    SUCCESS = 200

class APIResponse(BaseModel, Generic[T]):
    status: Status
    message: str
    body: Optional[T]