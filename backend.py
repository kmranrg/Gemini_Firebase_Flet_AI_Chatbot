import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

key = open('key.txt').read()
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-pro")

cred = credentials.Certificate('gemini-flet-ai-chatbot-firebase-adminsdk-n39tw-693c522268.json') 
firebase_admin.initialize_app(cred)
db = firestore.client()

class SmartGurucool():
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]
        self.collection_name = 'chat_history'

    def SmartGuruResponse(self, user_text):
        self.user_text = user_text

        while True:
            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break

            # Get conversation history from Firestore
            chat_ref = db.collection(self.collection_name)
            chat_docs = chat_ref.get()

            conversation_history = []
            for doc in chat_docs:
                conversation_history.append(doc.to_dict()['message'])

            # Update conversation history with user message
            conversation_history.append(self.user_text)

            # Generate response using Gemini model
            response = model.generate_content(conversation_history)
            response_text = response._result.candidates[0].content.parts[0].text

            # Save conversation (including response) to Firestore
            chat_ref.add({'message': response_text})

            # returning the response
            return response_text
