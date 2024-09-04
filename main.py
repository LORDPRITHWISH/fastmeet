import google.generativeai as genai
import os
from fastapi import FastAPI
import uvicorn
import asyncio
from prisma import Prisma
from prisma.models import User,passwars,Organization,Interview ,Question,Sesson,InterList
# import uuid
from datetime import datetime



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
async def generator(sesson: str,department: str, no: int,dificulty : int):
    response = model.generate_question(f'''Generate a question bank for a interviews in wich i will be interwiewing a {department} with the skill set {dificulty} ,
    give me  30 questins starting from easy to hard ranking them on a dificulty of 1 to 10.
    assign key to each to mach the question to the claimed experties of the candidates .
    Use the JSON format given below.
    {"question": "question 1", "answer": "answer 1", "keywords": {"key 1","key 2"}, "dificulty":"level"}
    {"question": "question 2", "answer": "answer 2", "keywords": {"key 1","key 2"}, "dificulty":"level"}''')
    return response


@app.get("/makeOrganization")
async def OrgSet(name: str, session: str):
    ses = await db.Session.find_unique(where={"session": session})
    user = await db.User.find_unique(where={"id": ses.userId})
    Organization = await db.Organization.create(
        data={
            'name': name,
            'User': {
                    'connect': {
                        'id': user.id
                    }
                }
        },
    )
    # await db
    return {"response": "Organization Created"}




@app.get("/login")
async def create_session(user_id: int = None):
    await db.connect()

    # session_id = str(uuid.uuid4())  # Generate a UUID for the session ID
    created_at = datetime.now()  # Capture the current time for session creation
    user = await db.user.find_unique(where={"id": user_id})
    # Create the session in the database
    session = await Sesson.prisma().create(
        data={
            'createdAt': created_at,
            "userId"
            'user': {
                'connect': {'id': user.id}
            } if user_id else None
        }
    )

    await db.disconnect()
    
    return {"response": "Session Created", "session": session.session}



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