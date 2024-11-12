from fastapi import FastAPI
from internal.main import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

origins = [
    "http://localhost:5173",
    "https://paggo-hnclvurgf-fellipes-projects-3dc1e81e.vercel.app",
    "https://paggo-app.vercel.app"
]

local_s3_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'local_s3'))
os.makedirs(local_s3_path, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(api_router)

