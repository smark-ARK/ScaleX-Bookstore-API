from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from starlette.types import ASGIApp

from app.routers import auth, book

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://*",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(book.router)


@app.get("/")
def home():
    return {"message": "Hello World!"}
