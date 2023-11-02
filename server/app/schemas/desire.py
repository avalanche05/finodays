from pydantic import BaseModel

from .cfa_image import CfaImage
from .user import PublicUser
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from .validators import positive_number

class Desire(BaseModel):
    id: int
    cfa_image: CfaImage
    count: int
    price: float
    buyer: PublicUser


class DesireCreateRequest(BaseModel):
    cfa_image_id: int
    count: Annotated[int, AfterValidator(positive_number)]
    price: Annotated[float, AfterValidator(positive_number)]


class DesireSellRequest(BaseModel):
    count: Annotated[int, AfterValidator(positive_number)]
