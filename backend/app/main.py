import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.encode_decode import router
import os

app = FastAPI(title="Secure Message Encoder/Decoder PoC")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Serve frontend from ../frontend
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
if os.path.isdir(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    index_path = os.path.join(frontend_path, "index.html") if os.path.isdir(frontend_path) else None
    if index_path and os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Secure Message Encoder/Decoder PoC — start backend and open frontend/index.html"}
