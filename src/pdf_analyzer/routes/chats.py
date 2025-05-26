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
    chat_id: UUID,
    message_create: MessageCreate,
    session: SessionDep,
    document_svc: DocumentSvcDep,
    ai_svc: AISvcDep,
):
    human_message = Message(
        content=message_create.content, chat_id=chat_id, sender_type=SenderType.HUMAN
    )

    chat = session.exec(select(Chat).where(Chat.id == chat_id)).one_or_none()
    if not chat:
        raise ValueError(f"Chat with ID {chat_id} does not exist.")
    docs = await document_svc.search(
        human_message.content, [file.id for file in chat.files]
    )

    answer = ai_svc.retrieve_answer(
        human_message.content,
        docs,
    )
    if not answer:
        answer = ""
    ai_message = Message(content=answer, chat_id=chat_id, sender_type=SenderType.AI)

    session.add(human_message)
    session.add(ai_message)
    session.commit()
    session.refresh(ai_message)

    return ai_message


@router.get("/{chat_id}/messages", response_model=list[MessageRead])
async def get_messages(chat_id: UUID, session: SessionDep):
    return session.exec(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp)  # type: ignore
    ).all()
