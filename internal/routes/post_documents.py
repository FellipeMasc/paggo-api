from fastapi import FastAPI, APIRouter,Response, Depends, UploadFile, File
from deps import get_db
from internal.auth.utils import get_current_user
from internal.schemas import QueryBase, User
from ocr.main import extract_text_from_file
from download_upload_utils.main import save_file_to_s3
from langchain_calling.main import explain_text


post_documents_router = APIRouter(
    prefix="/post_documents",
    tags=["post_documents"]
)

@post_documents_router.post('', summary="Post documents")
async def post_documents(file : UploadFile ,user: User = Depends(get_current_user), db=Depends(get_db)):
    filename = file.filename
    text = ""
    file_bytes = await file.read()
    text = extract_text_from_file(file_bytes, file.content_type == "application/pdf") 
    
    explanation = explain_text(text)
    document = await db.document.create(
        data={
            "filename": filename,
            "extractedText": text,
            "llmExplanation": explanation,
            "user": {
                "connect": {
                    "id": user.id
                }
            }
        }
    )
    save_file_to_s3(file_bytes, "user_id_"+str(user.id)+"_document_id_"+str(document.id)+"_"+filename)
    
    return Response(status=200, content="Document uploaded successfully")