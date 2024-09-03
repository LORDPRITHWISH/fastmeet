import google.generativeai as genai
import os
from fastapi import FastAPI
import uvicorn



# export API_KEY=<YOUR_API_KEY>








from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()








app = FastAPI()

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)





@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/modgenerate/{prompt}")
async def generate(prompt: str):
    response = model.generate_content(prompt)
    return {"response": response.text}

@app.get("/chatgenerate/{prompt}")
async def generate(prompt: str):
    response = chat.send_message(prompt)
    return {"response": response.text}

@app.get("/questiongenerate/{prompt}")
async def generate(prompt: str):
    response = model.generate_question(prompt)
    return {"response": response.text}

@app.get("/setQuestion/{prompt}")
async def generate(prompt: str):
    response = model.set_question(prompt)
    return {"response": response.text}

if __name__ == "__main__":
    uvicorn.run(app)