import tempfile

from langchain_core.vectorstores import VectorStore
from langchain_core.documents import Document
from langchain_text_splitters.base import TextSplitter
from pdf_analyzer.models import File
from dataclasses import dataclass
from langchain.document_loaders import PyPDFLoader
from uuid import UUID


@dataclass
class DocumentService:

    vector_store: VectorStore
    text_splitter: TextSplitter

    async def save(self, file: File):
        documents = self.__convert_to_documents(file)
        all_splits = self.text_splitter.split_documents(documents)
        self.__add_metadata(all_splits, file)
        await self.vector_store.aadd_documents(all_splits)

    async def search(self, text: str, file_ids: list[UUID] = []) -> list[Document]:
        documents_filter = None
        if file_ids:
            documents_filter = {
                "file_id": {"$in": [str(file_id) for file_id in file_ids]}
            }
        return await self.vector_store.asimilarity_search(text, filter=documents_filter)

    def __add_metadata(self, documents: list[Document], file: File):
        for doc in documents:
            doc.metadata["file_name"] = file.name
            doc.metadata["file_id"] = str(file.id)

    def __convert_to_documents(self, file: File) -> list[Document]:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp_file:
            tmp_file.write(file.content)
            tmp_file.flush()

            loader = PyPDFLoader(tmp_file.name)
            return loader.load()
