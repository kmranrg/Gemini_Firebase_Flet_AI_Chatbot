import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime

# gemini setup
key = open('key.txt').read()
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-pro")

# firebase setup
cred = credentials.Certificate('gemini-flet-ai-chatbot-firebase-adminsdk-n39tw-693c522268.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# timestamp
now = datetime.datetime.now()
timestamp = now.strftime("%b_%d_%Y_%H_%M_%S_%p")

class SmartGurucool():
    def __init__(self):
        self.collection_name = 'chat_history'
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

    def SmartGuruResponse(self, user_text, user_name):
        chat_session = user_name.replace(" ","")
        now = datetime.datetime.now()
        timestamp = now.strftime("%b_%d_%Y_%H_%M_%S_%p")
        message_id = "msg_" + str(timestamp)

        # Get conversation history from Firestore
        chat_ref = db.collection(self.collection_name).document(chat_session)
        chat_doc = chat_ref.get()

        self.conversation_history.append({"role": "user", "content": user_text})

        # Handle initial conversation (optional)
        if not chat_doc.exists:
            chat_ref.set({})  # Initialize an empty document

            # Update conversation history with user message
            chat_ref.update({message_id: user_text})
            
            # Generate response using Gemini model
            response = model.generate_content(user_text)
            response_text = response._result.candidates[0].content.parts[0].text
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
        else:
            messages = list(chat_doc.to_dict().values())  # fetching from firebase db (reference)

            # Update conversation history with user message
            chat_ref.update({message_id: user_text})
            
            # Generate response using Gemini model
            response = model.generate_content([message["content"] for message in self.conversation_history])
            response_text = response._result.candidates[0].content.parts[0].text
            self.conversation_history.append({"role": "assistant", "content": response_text})

        # Save AI response to Firestore with a separate key
        chat_ref.update({f'{message_id}_response': response_text})
        print(self.conversation_history)

        return response_text

