from fastapi import APIRouter
from pdf_analyzer.dependencies import SessionDep, DocumentSvcDep, AISvcDep, ChatSvcDep
from pdf_analyzer.models import Chat, ChatFileLink, Message, SenderType
from pdf_analyzer.schemas import ChatCreate, ChatRead, MessageCreate, MessageRead
from sqlmodel import select
from uuid import UUID

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/")
async def create_chat(
    session: SessionDep, chat_svc: ChatSvcDep, chat_create: ChatCreate
) -> UUID:
    res = chat_svc.create_chat(session, chat_create)
    return res.id


@router.get("/", response_model=list[ChatRead])
async def get_chats(session: SessionDep, chat_svc: ChatSvcDep):
    return chat_svc.find_all_chats(session)


@router.post("/{chat_id}/message", response_model=MessageRead)
async def send_message(
    session: SessionDep,
    chat_svc: ChatSvcDep,
    chat_id: UUID,
    message_create: MessageCreate,
):
    ai_message = await chat_svc.send_message(session, chat_id, message_create)
    return ai_message


@router.get("/{chat_id}/messages", response_model=list[MessageRead])
async def get_messages(chat_id: UUID, session: SessionDep, chat_svc: ChatSvcDep):
    return chat_svc.find_messages(session, chat_id)
