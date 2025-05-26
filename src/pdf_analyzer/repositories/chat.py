from pdf_analyzer.models import Chat, ChatFileLink
from sqlmodel import Session, select
from uuid import UUID
from typing import Sequence


class ChatRepository:

    def create_chat(self, session: Session, chat: Chat, file_ids: list[UUID]) -> Chat:
        session.add(chat)

        for file_id in file_ids:
            session.add(ChatFileLink(chat_id=chat.id, file_id=file_id))

        session.commit()
        session.refresh(chat)

        return chat

    def find_all(self, session: Session) -> Sequence[Chat]:
        return session.exec(select(Chat)).all()
