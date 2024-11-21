from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini
GOOGLE_API_KEY = "AIzaSyDOr7omU7OOgc2gP83r0QODZpb4EVGq-R8"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Updated prompt to request clean, direct responses
    prompt = f"""Please provide a brief, direct response (maximum 100 words). 
    Avoid using asterisks, bullet points, or special characters.
    Keep responses conversational and natural.
    
    User message: {user_message}"""
    
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        
        # Clean the response text
        clean_response = response.text.replace('*', '').strip()
        return jsonify({'response': clean_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server starting...")
    app.run(debug=True, port=5000)
    print("Server is running at http://localhost:5000")