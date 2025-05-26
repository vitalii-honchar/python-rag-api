from fastapi import FastAPI
from pdf_analyzer.app_context import AppContext, AppSettings
from pdf_analyzer.routes import chats, files

app = FastAPI()

app.include_router(files.router)
app.include_router(chats.router)
