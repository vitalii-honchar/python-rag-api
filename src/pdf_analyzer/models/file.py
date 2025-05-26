from sqlmodel import SQLModel, Field
from sqlalchemy import Column, LargeBinary
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID


class File(SQLModel, table=True):
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )
    name: str
    content: bytes = Field(sa_column=Column(LargeBinary))
