from pydantic import BaseModel, Field
from uuid import UUID


class FileRead(BaseModel):
    id: UUID | None = Field(
        default=None,
        description="File ID",
    )
    name: str | None = Field(
        default=None,
        description="File name",
    )
