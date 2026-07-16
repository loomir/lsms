from pydantic import BaseModel, EmailStr


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = {
        "from_attributes": True
    }


class RefreshTokenRequest(BaseModel):
    refresh_token: str

    model_config = {
        "from_attributes": True
    }


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    model_config = {
        "from_attributes": True
    }


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str

    model_config = {
        "from_attributes": True
    }
