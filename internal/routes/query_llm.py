from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from deps import get_db
from internal.auth.utils import get_current_user
from internal.schemas import QueryBase, User
from langchain_calling.main import query_to_llm

query_llm_router = APIRouter(
    prefix="/query_llm",
    tags=["query_llm"]
)

@query_llm_router.post('', summary="Get LLM data")
async def get_llm(data: QueryBase, user: User = Depends(get_current_user), db=Depends(get_db)):
    document = await db.document.find_unique(where={"id": data.documentId})
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    if document.userId != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this document"
        )
    
    llm_response = query_to_llm(data.query,document.extractedText,document.llmExplanation)
    
    query = await db.query.create(
        data={
            "query": data.query,
            "response": llm_response,
            "document": {
                "connect": {
                    "id": document.id
                }
            }
        }
    )
    
    return {"message": "Hello World"}