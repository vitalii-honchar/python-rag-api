from sqlmodel import Session
from fastapi import Depends
from typing import Annotated
from pdf_analyzer.app_context import create_app_context
from pdf_analyzer.services import DocumentService, AIService


ctx = create_app_context()


def get_session():
    with Session(ctx.db_engine) as session:
        yield session


def get_document_svc() -> DocumentService:
    return ctx.document_svc


def get_ai_svc() -> AIService:
    return ctx.ai_svc


SessionDep = Annotated[Session, Depends(get_session)]
DocumentSvcDep = Annotated[DocumentService, Depends(get_document_svc)]
AISvcDep = Annotated[AIService, Depends(get_ai_svc)]
