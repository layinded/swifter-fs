from sqlmodel import SQLModel

# ✅ Generic message response
class Message(SQLModel):
    message: str
