from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to access API

openai.api_key = "sk-proj-JXnDf2Bf10_GrfC94m1QGxkWuf-4jeY9CMU-rVIWr_I8KXGznzPAtVIxgpA6YhcoL81IDxtYy1T3BlbkFJ1wh-sAWgjBCRLGg9jPm7MvodteajAmCQcmxqpL7PZmImCpyH3enDPkoGzokzTXghUohmVVwJAAY"  # Replace with your OpenAI key

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    query = data.get("query")

    # Get response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": query}]
    )
    reply = response["choices"][0]["message"]["content"]

    # Convert text to Marathi speech
    tts = gTTS(reply, lang='mr')
    audio_path = "static/response.mp3"
    tts.save(audio_path)

    return jsonify({"audio_url": f"/static/response.mp3"})

@app.route('/static/response.mp3')
def serve_audio():
    return send_file("static/response.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
