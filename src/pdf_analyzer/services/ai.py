from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("system", "{data}"),
        ("human", "{text}"),
    ]
)


class Output(BaseModel):
    answer: str | None = Field(
        default=None,
        description="Answer on the question",
    )


class AIService:

    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.structured_llm = llm.with_structured_output(schema=Output)

    def retrieve_answer(self, question: str, docs: list[Document]) -> str | None:
        data = "\n\n".join(doc.page_content for doc in docs)
        prompt = prompt_template.invoke({"text": question, "data": data})
        llm_result = self.structured_llm.invoke(prompt)
        
        return Output.model_validate(llm_result).answer if llm_result else None
