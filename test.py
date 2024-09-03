# import google.generativeai as genai
# import os

# genai.configure(api_key="AIzaSyAEaA_PjfeaEM-0rMPKgjhHcHN0uFEon6Q")

# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )
# response = chat.send_message("I have 2 dogs in my house.")
# print(response.text)
# response = chat.send_message("How many paws are in my house?")
# print(response.text)
# response = chat.send_message("so what was the summary of the convertatuion?")
# print(response.text)

# import ollama
# response = ollama.chat(model='llama3.1', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])









# import asyncio
# from prisma import Prisma
# from prisma.models import User

# async def main() -> None:
#     db = Prisma(auto_register=True)
#     await db.connect()

#     # write your queries here
#     user = await User.prisma().create(
#         data={
#             'username': 'Robert',
#             'email': 'robert@craigie.dev'
#         },
#     )

#     await db.disconnect()

# if __name__ == '__main__':
#     asyncio.run(main())











from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="Whats the weather in San Francisco today? And what is the date?")
print(response)
