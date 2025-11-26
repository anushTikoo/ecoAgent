from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()

#Database connection import
from database.session import lifespan

app = FastAPI(title="ecoAgent API", lifespan=lifespan)

origins = [ os.getenv("FRONTEND_URL") ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ecoAgent Backend", "status": "running"}