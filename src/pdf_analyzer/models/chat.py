from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from pdf_analyzer.models.file import File
from uuid import uuid4, UUID


class ChatFileLink(SQLModel, table=True):
    chat_id: UUID = Field(foreign_key="chat.id", primary_key=True)
    file_id: UUID = Field(foreign_key="file.id", primary_key=True)


class Chat(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    name: str
    files: list[File] = Relationship(link_model=ChatFileLink)
