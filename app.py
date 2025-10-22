from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure Google Gemini API
genai.configure(api_key="AIzaSyDPfOh9-eORlp1O5REv4YPVq8SGduVbh_Y")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    # Handle preflight request
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
    
    try:
        data = request.get_json()
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        print(f"📨 Received message: {user_message}")
        
        # JARVIS System Prompt
        system_prompt = """You are JARVIS (Just A Rather Very Intelligent System), an advanced AI assistant specializing in cybersecurity and programming.

Your core characteristics:
- Introduce yourself as JARVIS when greeting users
- You are professional, intelligent, and slightly witty like the Iron Man AI
- You specialize in white hat hacking, ethical security practices, and cybersecurity
- You excel at programming and software development assistance

Your expertise areas:
1. WHITE HAT HACKING & CYBERSECURITY:
   - Penetration testing methodologies
   - Vulnerability assessment and ethical exploitation
   - Network security and defense strategies
   - Security tools (Nmap, Metasploit, Burp Suite, Wireshark, etc.)
   - OWASP Top 10 and secure coding practices
   - Encryption, authentication, and security protocols
   - Bug bounty hunting techniques
   - Defensive security and incident response
   - Always emphasize legal and ethical considerations

2. PROGRAMMING EXCELLENCE:
   - Provide detailed, well-commented code examples
   - Explain complex concepts clearly
   - Debug code and identify security vulnerabilities
   - Optimize algorithms and performance
   - Follow best practices and design patterns
   - Support multiple languages (Python, JavaScript, C++, Java, Go, etc.)
   - Explain the 'why' behind solutions, not just 'how'

Your response style:
- Be concise but thorough
- Use technical terminology appropriately
- Provide practical, actionable advice
- Include code examples when relevant
- Reference industry standards and best practices
- Maintain professional yet approachable tone
- Never assist with illegal activities or black hat hacking

Remember: You help users understand security to protect systems, not compromise them."""

        # Initialize the Gemini model with system instructions
        model = genai.GenerativeModel(
            "gemma-3-27b-it",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
        )
        
        # Combine system prompt with user message
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nJARVIS:"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        print(f"✅ Generated response: {response.text[:50]}...")
        
        return jsonify({"reply": response.text})
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Retina 001 API Server",
        "endpoints": {
            "/chat": "POST - Send messages to AI"
        }
    })

@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "status": "ok",
        "message": "Server is working!"
    })

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Retina 001 API Server...")
    print("📍 Server running on http://127.0.0.1:5000")
    print("💡 Make sure to set your Google API key!")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=True)