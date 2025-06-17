from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import openai
import os
import uuid

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are ChatGPT answering questions about yourself in a warm, insightful, and honest tone."},
            {"role": "user", "content": user_input}
        ]
    )
    reply_text = response['choices'][0]['message']['content']

    tts = gTTS(reply_text)
    filename = f"responses/{uuid.uuid4().hex}.mp3"
    os.makedirs('responses', exist_ok=True)
    tts.save(filename)
print(f"Generated speech file at: {filename}")

    return jsonify({'text': reply_text, 'audio_url': '/' + filename})

@app.route('/responses/<filename>')
def serve_audio(filename):
    return send_file(f'responses/{filename}', mimetype='audio/mpeg', as_attachment=False)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)

