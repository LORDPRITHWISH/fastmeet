import google.generativeai as genai
import os
from fastapi import FastAPI
import uvicorn
import asyncio
from prisma import Prisma
from prisma.models import User,passwars,Question,Answer,Session



# export API_KEY=<YOUR_API_KEY>




db = Prisma(auto_register=True)

app = FastAPI()

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)





@app.get("/")
async def root():
    return {"message": "Hello World"}




@app.get("/createuser")
async def create_user(username: str, email: str, password: str):
    await db.connect()

    user = await User.prisma().create(
        data={
            'username': username,
            'email': email
        },
    )
    await db.passwars.create(
        data={
            'word': password,
            'user': {
                'connect': {
                    'id': user.id
                }
            }
        },
    )

    await db.disconnect()

    return {"response": "User Created"}







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
async def QuesSet(session: str, question: str, answer: str):
    ses = await db.Session.find_unique(where={"session": session})
    if ses is None:
        return {"response": "Session not found"}
    User = await db.User.find_unique(where={"id": ses.user.id})
    Question = await db.Question.create(
        data={
            'question': question,
            'answer': answer,
            'user': {
                'connect': {
                    'id': User.id
                }
            }
        },
    )
    # return {"response": response.text}



if __name__ == "__main__":
    uvicorn.run(app)