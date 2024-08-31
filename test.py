import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyAEaA_PjfeaEM-0rMPKgjhHcHN0uFEon6Q")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)
response = chat.send_message("I have 2 dogs in my house.")
print(response.text)
response = chat.send_message("How many paws are in my house?")
print(response.text)
response = chat.send_message("so what was the summary of the convertatuion?")
print(response.text)

# import ollama
# response = ollama.chat(model='llama3.1', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])