from flask import Flask, request, jsonify, send_file, render_template
import openai
from PIL import Image
import io
import os
from gtts import gTTS

app = Flask(__name__)

# Configurar a API Key da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    # Serve a página HTML do frontend
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem foi enviada"}), 400
    
    # Obter a imagem do request
    image = request.files['image']
    img = Image.open(io.BytesIO(image.read()))

    # Gerar descrição da imagem (aqui, é um exemplo fixo, você pode substituir com a API da OpenAI)
    description = "Este é um exemplo de descrição gerada pela análise da imagem."

    # Gerar áudio a partir da descrição usando gTTS
    tts = gTTS(description, lang='pt')
    audio_path = "description_audio.mp3"
    tts.save(audio_path)

    # Retornar a resposta com a descrição e link para o áudio gerado
    return jsonify({
        "description": description,
        "audio_url": request.host_url + 'audio'
    })

@app.route('/audio')
def get_audio():
    # Enviar o arquivo de áudio gerado
    return send_file('description_audio.mp3', mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
