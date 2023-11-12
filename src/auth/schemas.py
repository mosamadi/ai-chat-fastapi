import re
from typing import Any
from pydantic import BaseModel,EmailStr,Field,field_validator,ConfigDict


STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,128}$")

class BaseUser(BaseModel):
    email: EmailStr
    full_name: str

class UserInfo(BaseUser):
    model_config = ConfigDict(from_attributes=True)
    id: int
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6,max_length=128)

class UserCreation(BaseUser):
    password: str = Field(min_length=6,max_length=128)
    
    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password
    


class AccessTokenResponse(BaseUser):
    access_token: str



class TokenData(BaseModel):
    email : EmailStr