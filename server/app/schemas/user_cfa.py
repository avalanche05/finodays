from typing import List
from .cfa_image import CfaImage

from pydantic import BaseModel


class UserCfa(BaseModel):
    cfa_image: CfaImage
    count: int
    tokens: List[str]
