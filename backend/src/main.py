import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.users.presentation.api import user_api_router
from src.tasks.presentation.api import task_api_router
from src.auth.presentation.api import auth_api_router


logger = logging.getLogger(__name__)


app = FastAPI(
    title="ToDoMonolith",
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
)


app.include_router(user_api_router)
app.include_router(task_api_router)
app.include_router(auth_api_router)
