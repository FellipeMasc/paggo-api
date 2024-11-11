from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Response
from deps import get_db
from internal.auth.utils import get_current_user
from internal.schemas import DocumentOut, User, QueryOut
from fastapi.responses import StreamingResponse, FileResponse
from download_upload_utils.main import request_file_from_s3
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from PIL import ImageFile, Image
from textwrap import wrap

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@user_router.get('/documents', summary="Get documents from an active user", response_model=List[DocumentOut])
async def get_user_details(user: User = Depends(get_current_user),db = Depends(get_db)):
    documents = await db.document.find_many(where={"userId": user.id})
    response = []
    for doc in documents:
        response.append({
            "id": doc.id,
            "filename": doc.filename,
            "extractedText": doc.extractedText,
            "llmExplanation": doc.llmExplanation,
            "uploadedAt": doc.uploadedAt,
            "userId": doc.userId
        })
    return response

@user_router.get('/queries/{document_id}', summary="Get queries from a document of an active user", response_model=List[QueryOut])
async def get_queries_from_document(document_id: int, user: User = Depends(get_current_user), db = Depends(get_db)):
    document = await db.document.find_unique(where={"id": document_id})
    
    if document.userId != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this document's queries")
    
    queries = await db.query.find_many(where={"documentId": document_id})
    response = []
    for query in queries:
        response.append({
            "id": query.id,
            "query": query.query,
            "documentId": query.documentId,
            "createdAt": query.createdAt,
            "response": query.response
        })
    return response

@user_router.get('/download_raw_document/{document_id}', summary="Get the initial file of the document that was uploaded")
async def download_raw_document(document_id: int, user: User = Depends(get_current_user), db = Depends(get_db)):
    document = await db.document.find_unique(where={"id": document_id})
    
    if document.userId != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this document")
    
    file_name = "user_id_"+str(user.id)+"_document_id_"+str(document.id)+"_"+document.filename
    media_type = "application/pdf" if document.filename.endswith(".pdf") else "image/png"
    #get from s3
    file = request_file_from_s3(file_name)
    
    return Response(content=file, media_type=media_type, headers={"Content-Disposition": "attachment; filename="+document.filename})

@user_router.get('/download_llm_document/{document_id}', summary="Get the document with LLM explanation and queries")
async def download_llm_document(document_id: int, user: User = Depends(get_current_user), db = Depends(get_db)):
    document = await db.document.find_unique(where={"id": document_id})
    
    if document.userId != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this document")
    
    file_name = "user_id_"+str(user.id)+"_document_id_"+str(document.id)+"_"+document.filename
    #get from 's3' local
    file = request_file_from_s3(file_name)
    
    queries = await db.query.find_many(where={"documentId": document_id})
    
    image = ImageReader(BytesIO(file))

    output = PdfWriter()
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    image_pil = Image.open(BytesIO(file))
    image_width, image_height = image_pil.size
    page_width, page_height = A4
    x = (page_width - image_width) / 2
    y = (page_height - image_height) / 2
    can.drawImage(image, x, y, width=image_width, height=image_height)
    can.showPage()  
    extracted_text_height = 820
    extracted_text = wrap(document.extractedText, width=80)
    can.drawString(10, extracted_text_height, "Texto extraído:")
    extracted_text_height -= 12
    for line in extracted_text:
        can.drawString(10, extracted_text_height, line)
        extracted_text_height -= 12
    explanation = wrap(document.llmExplanation, width=80)
    extracted_text_height-=20
    can.drawString(10, extracted_text_height, "Explicação do texto por um modelo de linguagem natural:")
    extracted_text_height -= 12
    for line in explanation:
        can.drawString(10, extracted_text_height, line)
        extracted_text_height -= 12
    response_height = 820
    for i, query in enumerate(queries):
        if i % 2 == 0:
            can.showPage()  
        query_height = response_height - 20
        can.drawString(10, query_height, f"Query: {query.query}")
        response_lines = wrap(query.response, width=80)
        response_height = query_height - 32
        can.drawString(10, response_height, f"Response:")
        response_height -= 12
        for line in response_lines:
            can.drawString(10, response_height, line)
            response_height -= 12

    can.save()
    packet.seek(0) 

    new_pdf = PdfReader(packet)
    for page in new_pdf.pages:
        output.add_page(page)

    final_pdf = BytesIO()
    output.write(final_pdf)
    final_pdf.seek(0) 
    
    return Response(content=final_pdf.read(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=appended_document_with_queries.pdf"})