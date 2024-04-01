import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

key = open('key.txt').read()
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-pro")

cred = credentials.Certificate('gemini-flet-ai-chatbot-firebase-adminsdk-n39tw-693c522268.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class SmartGurucool():
    def __init__(self):
        self.collection_name = 'chat_history'  # Initialize collection_name here

    def SmartGuruResponse(self, user_text, user_name):
        # generating timestamp
        now = datetime.datetime.now()
        timestamp = now.strftime("%b_%d_%Y_%H_%M_%p")
        chat_session = user_name.replace(" ","") + "_" + str(timestamp)
        message_id = "msg_" + str(timestamp)

        # Get conversation history from Firestore
        chat_ref = db.collection(self.collection_name).document(chat_session)
        chat_doc = chat_ref.get()

        # Handle initial conversation (optional)
        if not chat_doc.exists:
            chat_ref.set({})  # Initialize an empty document
            conversation_history = []  # Empty list for initial call
        else:
            conversation_history = list(chat_doc.to_dict().values())  # Convert dict values to list

        # Ensure retrieved history is not empty
        if not conversation_history:
            conversation_history = []  # Set to an empty list if retrieval fails

        # Update conversation history with user message
        chat_ref.update({message_id: user_text})
        conversation_history.append(self.user_text)


        # Generate response using Gemini model
        response = model.generate_content(conversation_history)
        response_text = response._result.candidates[0].content.parts[0].text

        # Save AI response to Firestore with a separate key
        chat_ref.update({f'{message_id}_response': response_text})

        return response_text
