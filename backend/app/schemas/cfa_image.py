from pydantic import BaseModel
from .user import PublicUser
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from .validators import positive_number


class CfaImage(BaseModel):
    id: int
    title: str
    count: int
    description: str
    user: PublicUser


class CfaImageCreateRequest(BaseModel):
    count: Annotated[int, AfterValidator(positive_number)]
    description: str
    title: str


class CfaImagePrice(BaseModel):
    price: float


class CfaImageBuyAdvice(BaseModel):
    is_buy: bool
    why: dict[str, str]
