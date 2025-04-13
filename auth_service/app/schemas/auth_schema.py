from pydantic import BaseModel, EmailStr, Field

class SignUpRequest(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="supersecret123")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="supersecret123")

class TokenResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1...")
    token_type: str = Field(..., example="Bearer")

class MessageResponse(BaseModel):
    message: str = Field(..., example="Action completed successfully.")

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Invalid credentials")
