from pydantic import BaseModel
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from .validators import positive_number


class User(BaseModel):
    id: int
    email: str
    username: str
    name: str
    balance: float


class PublicUser(BaseModel):
    id: int
    email: str
    username: str
    name: str


class UserCreateRequest(BaseModel):
    email: str
    password: str
    username: str
    name: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserDepositRequest(BaseModel):
    value: Annotated[float, AfterValidator(positive_number)]


class UserWithdrawRequest(BaseModel):
    value: Annotated[float, AfterValidator(positive_number)]
