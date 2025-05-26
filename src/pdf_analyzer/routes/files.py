from fastapi import APIRouter, UploadFile
from pdf_analyzer.dependencies import SessionDep, DocumentSvcDep
from pdf_analyzer.models import File
from pdf_analyzer.schemas import FileRead
from sqlmodel import select
from uuid import UUID

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload/")
async def upload_file(
    file: UploadFile, name: str, session: SessionDep, document_svc: DocumentSvcDep
) -> UUID:
    db_file = File(name=name, content=await file.read())
    session.add(db_file)
    session.commit()
    session.refresh(db_file)

    await document_svc.save(db_file)

    return db_file.id


@router.get("/", response_model=list[FileRead])
async def get_files(session: SessionDep):
    return session.exec(select(File)).all()
