from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pregunta del usuario en lenguaje natural.")
