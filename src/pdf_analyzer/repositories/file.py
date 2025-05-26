from pdf_analyzer.models import File
from sqlmodel import Session, select
from typing import Sequence


class FileRepository:

    def create_file(self, session: Session, file: File) -> File:
        session.add(file)
        session.commit()
        session.refresh(file)
        return file

    def find_all(self, session: Session) -> Sequence[File]:
        return session.exec(select(File)).all()
