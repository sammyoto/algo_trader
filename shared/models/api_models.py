from pydantic import BaseModel
from typing import Union, Optional, List
from enum import Enum

class Status(int, Enum):
    FAILED = 400
    SUCCESS = 200

class APIResponse(BaseModel):
    status: Status
    message: str