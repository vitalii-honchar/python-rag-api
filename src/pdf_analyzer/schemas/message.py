from pydantic import BaseModel, Field
from pdf_analyzer.models import SenderType
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    content: str = Field(
        description="Message content",
    )


class MessageRead(BaseModel):
    id: UUID = Field(
        description="Message ID",
    )
    chat_id: UUID = Field(
        description="Chat ID",
    )
    content: str = Field(
        description="Message content",
    )
    timestamp: datetime = Field(
        description="Message timestamp",
    )
    sender_type: SenderType = Field(
        description="Sender type (ai or human)",
    )
