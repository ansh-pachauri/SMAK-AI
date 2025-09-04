from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from app.services.whisper_small import transcribe_audio
import os
from app.db.index import prisma
from secret import JWT_SECRET
import jwt
from app.core.auth import middlware
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)







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


class SignUpRequest(BaseModel):
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str
    
# signup route
@app.post("/signup")
async def signup(body: SignUpRequest):
    print("reached after sign up function")
    try:
        user = await prisma.user.create(
        data={
            "email": body.email,
            "password": body.password,
        }
        )
        return {"message": "User created successfully", "user": user.id}

    except Exception as e:
        return {"message": "Error creating user, Pls try later", "error": str(e)}
        
    


# signin route
@app.post("/signin")
async def signin(body: SignInRequest):
    try:
        user = await prisma.user.find_first(
        where={
            "email": body.email,
            "password": body.password,
        }
        )
        
        if(not user):
            return {"message": "Invalid credentials"}
        
        token = jwt.encode({"user_id": user.id}, JWT_SECRET, algorithm="HS256")
        return {"message": "User signed in successfully", "userId": user.id, "token": token}
    except Exception as e:
        return {"message": "Error signing in, Unautheraized user", "error": str(e)}


@app.get("/protected")
async def protected(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Token will automatically be pulled from Swagger UI's Authorize
    token = credentials.credentials
    return {"token": token, "user_id": "You’ll get this from middleware"}



# whisper route for speech to text
# adding middleware
app.middleware("http")(middlware)
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
