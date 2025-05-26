from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID
from datetime import datetime, timezone
from enum import Enum


class SenderType(Enum):
    HUMAN = "human"
    AI = "ai"


class Message(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    content: str
    sender_type: SenderType
    chat_id: UUID = Field(foreign_key="chat.id")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
        description="UTC timestamp of the message",
    )
