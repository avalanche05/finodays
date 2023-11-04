from pydantic import BaseModel

from .cfa_image import CfaImage
from .user import PublicUser


class Cfa(BaseModel):
    token: str
    cfa_image: CfaImage
    user: PublicUser
