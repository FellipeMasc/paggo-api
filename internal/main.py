from fastapi import APIRouter
from internal.routes.login import login_router
from internal.routes.sign_up import signup_router
from internal.routes.query_llm import query_llm_router
from internal.routes.post_documents import post_documents_router
from internal.routes.user import user_router

api_router = APIRouter()

api_router.include_router(signup_router)
api_router.include_router(login_router)
api_router.include_router(query_llm_router)
api_router.include_router(post_documents_router)
api_router.include_router(user_router)
