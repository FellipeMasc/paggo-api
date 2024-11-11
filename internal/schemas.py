from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    email: str
    
class UserAuth(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    access_token: str
    refresh_token: str
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    filename: str
    extractedText: str
    llmExplanation: Optional[str] 
    
class DocumentOut(DocumentBase):
    id: int
    uploadedAt: datetime
    class Config:
        from_attributes = True
    
class QueryBase(BaseModel):
    query: str
    documentId: int


class ResponseBase(BaseModel):
    responseText: str
    
class ResponseOut(ResponseBase):
    id: int
    createdAt: str
    class Config:
        from_attributes = True
    
class QueryOut(QueryBase):
    id: int
    createdAt: datetime
    response: str
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    documents: List[DocumentOut] = []
    queries: List[QueryOut] = []
    class Config:
        from_attributes = True

class Document(DocumentBase):
    id: int
    userId: int
    user: UserOut
    queries: List[QueryOut] = []
    class Config:
        from_attributes = True

class Query(QueryBase):
    id: int
    userId: int
    user: UserOut
    document: DocumentOut
    response: Optional[ResponseOut]
    class Config:
        from_attributes = True

        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    class Config:
        from_attributes = True


    