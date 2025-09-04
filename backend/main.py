from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from app.services.whisper_small import transcribe_audio
import os
from app.db.index import prisma
import jwt

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


JWT_SECRET = "secret"




app = FastAPI(
    title="SMAK AI API",
    description="A FastAPI application for SMAK AI",
    version="1.0.0"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await prisma.connect()

@app.on_event("shutdown")
async def on_shutdown() -> None:
    await prisma.disconnect()



# signup route
@app.post("/signup")
async def signup(email: str, password: str):
    
    user = await prisma.user.create(
        data={
            "email": email,
            "password": password,
        }
    )
    return {"message": "User created successfully", "user": user}


# signin route
@app.post("/signin")
async def signin(email: str, password: str):
    user = await prisma.user.find_first(
        where={
            "email": email,
            "password": password,
        }
    )
    
    if(not user):
        return {"message": "Invalid credentials"}
    
    token = jwt.encode({"user_id": user.id}, JWT_SECRET, algorithm="HS256")
    return {"message": "User signed in successfully", "userId": user.id, "token": token}


# whisper route for speech to text
@app.post("/whisper")
async def whisper(file: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    text = transcribe_audio(file_path)
    return {"message": "Audio transcribed successfully", "text": text}

@app.get("/health")
async def health_check():   
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
