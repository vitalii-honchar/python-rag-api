from pydantic import BaseModel, Field
from pdf_analyzer.schemas.file import FileRead
from uuid import UUID


class ChatCreate(BaseModel):
    file_ids: list[UUID] = Field(
        default=[],
        description="List of file IDs to associate with the chat",
    )


class ChatRead(BaseModel):
    id: UUID | None = Field(
        default=None,
        description="Chat ID",
    )
    name: str | None = Field(
        default=None,
        description="Chat name",
    )
    files: list[FileRead] = Field(
        default=[],
        description="List of files associated with the chat",
    )
