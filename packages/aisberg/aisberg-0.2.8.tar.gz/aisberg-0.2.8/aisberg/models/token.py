from pydantic import BaseModel
from typing import List


class TokenInfo(BaseModel):
    message: str
    id: str
    username: str
    email: str
    groups: List[str]
    roles: List[str]
