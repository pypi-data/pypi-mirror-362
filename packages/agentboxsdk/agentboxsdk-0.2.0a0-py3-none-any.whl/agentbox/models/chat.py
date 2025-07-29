from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r"^(system|user|assistant|tool)$")
    content: str
