import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

# Initialize GenAI Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.json
    user_prompt = data.get('prompt')

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        # API Integration: Sending request to Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Optimize this prompt for better LLM results: {user_prompt}"
        )
        return jsonify({"optimized": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)