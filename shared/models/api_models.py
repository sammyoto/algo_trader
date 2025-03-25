from pydantic import BaseModel
from typing import Union, Optional, List
from enum import Enum

class APIResponse(BaseModel):
    status: str
    message: str