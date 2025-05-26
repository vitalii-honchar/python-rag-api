from sqlmodel import create_engine
from pydantic_settings import BaseSettings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from pdf_analyzer.services import DocumentService, AIService, ChatService
from langchain.chat_models import init_chat_model
from pdf_analyzer.repositories import FileRepository, ChatRepository, MessageRepository


class AppSettings(BaseSettings):
    db_url: str
    openai_api_key: str
    debug: bool = False
    vector_store_collection_name: str = "pdf_analyzer_documents"
    embedding_model: str = "text-embedding-3-large"

    class Config:
        env_file = ".env"
        env_prefix = "PDF_ANALYZER_"


class AppContext:

    def __init__(self, settings: AppSettings):
        self.db_engine = create_engine(settings.db_url, echo=settings.debug)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.openai_api_key, model=settings.embedding_model  # type: ignore
        )
        self.vector_store = PGVector(
            collection_name=settings.vector_store_collection_name,
            connection=settings.db_url.replace(
                "postgresql://", "postgresql+psycopg://"
            ),
            embeddings=self.embeddings,
            use_jsonb=True,
            async_mode=True,
        )
        self.file_repository = FileRepository()
        self.chat_repository = ChatRepository()
        self.message_repository = MessageRepository()
        self.document_svc = DocumentService(
            self.vector_store, self.text_splitter, self.file_repository
        )
        self.chat_svc = ChatService(self.chat_repository, self.message_repository)
        self.llm = init_chat_model(
            "gpt-4o-mini", model_provider="openai", api_key=settings.openai_api_key
        )
        self.ai_svc = AIService(self.llm)


def create_app_context() -> AppContext:
    return AppContext(AppSettings())  # type: ignore
