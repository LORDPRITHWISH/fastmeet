import google.generativeai as genai
import os
from fastapi import FastAPI
import uvicorn



# export API_KEY=<YOUR_API_KEY>





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

@app.get("/questiongenerate/")
async def generate(department: str, no: int,dificulty : int):
    response = model.generate_question(prompt)
    return {"response": response.text}

@app.get("/setQuestion")
async def generate(prompt: str):
    response = model.set_question(prompt)
    return {"response": response.text}

if __name__ == "__main__":
    uvicorn.run(app)