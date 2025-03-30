from pydantic import BaseModel
from typing import Union, Optional
import json

class RedisMessage(BaseModel):
    type: Optional[str]
    pattern: Optional[str]
    channel: Optional[str]
    data: dict

    def __init__(self, type: Optional[str], pattern: Optional[str], channel: Optional[str], data: Optional[str]):
        super().__init__(type=type, pattern=pattern, channel=channel, data=json.loads(data))

    def get_data_type(self):
        return self.channel.split('.')[0]