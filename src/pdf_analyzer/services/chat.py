from dataclasses import dataclass
from pdf_analyzer.schemas import ChatCreate
from pdf_analyzer.repositories import ChatRepository, MessageRepository
from pdf_analyzer.models import Chat
from sqlmodel import Session


@dataclass
class ChatService:
    chat_repository: ChatRepository
    message_repository: MessageRepository

    def create_chat(self, session: Session, chat_create: ChatCreate):
        chat = Chat(name="New Chat", files=[])
        return self.chat_repository.create(session, chat, chat_create.file_ids)

    def find_all_chats(self, session: Session):
        return self.chat_repository.find_all(session)
