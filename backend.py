import google.generativeai as genai

key = open('key.txt').read()
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-pro")

class SmartGurucool():
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are a helpful assistant."},
        ]

    def SmartGuruResponse(self, user_text):
        self.user_text = user_text

        while True:
            # if user says stop, then breaking the loop
            if self.user_text == "stop":
                break

            # storing the user question in the messages list
            self.messages.append({"role": "user", "content": self.user_text})

            # getting the response from Gemini model by providing the conversation history
            response = model.generate_content([message["content"] for message in self.messages])

            # appending the generated response so that AI remembers past responses
            response_text = response._result.candidates[0].content.parts[0].text
            self.messages.append({"role": "assistant", "content": response_text})

            # returning the response
            # print("Chatbot:", response_text)
            return response_text

# smart_guru = SmartGurucool()

# print("\n\t\t---------------------------------")
# print("\n\t\t\t ANURAG SMARTBOT")
# print("\n\t\t---------------------------------\n\n")

# while True:
#     user_message = input("You: ")
#     if user_message.lower() == "quit":
#         break
#     smart_guru.SmartGuruResponse(user_message)
#     print('\n-----------------------------------------------------------------\n')
