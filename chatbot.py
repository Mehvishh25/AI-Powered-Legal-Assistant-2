from flask import Blueprint, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question is required."}), 400

    prompt = f"You are a helpful legal assistant. Answer this in simple terms:\n\n{question}"
    
    try:
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text.strip()})
    except Exception as e:
        return jsonify({"error": f"Failed to get response from Gemini: {str(e)}"}), 500
