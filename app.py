from flask import Flask, request, jsonify, send_file, render_template
import openai
from PIL import Image
import io
import os
from gtts import gTTS
import pytesseract  

app = Flask(__name__)

# Configurar a API Key da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem foi enviada"}), 400
    
    # Obter a imagem do request
    image = request.files['image']
    img = Image.open(io.BytesIO(image.read()))

    # Usar OCR (Tesseract) para extrair texto da imagem, se houver texto nela
    extracted_text = pytesseract.image_to_string(img)

    # Se não houver texto extraído, usar uma descrição genérica para a imagem
    if not extracted_text.strip():
        extracted_text = "uma imagem interessante"

    # Enviar a entrada de texto extraído ou descrição genérica para a OpenAI
    prompt = f"Descreva o seguinte conteúdo: {extracted_text}. A descrição deve ser clara e detalhada."
    
    try:
        # Fazer a chamada à API da OpenAI para gerar a descrição
        response = openai.Completion.create(
            engine="text-davinci-003",  # Ou outro modelo que você preferir
            prompt=prompt,
            max_tokens=100
        )
        description = response.choices[0].text.strip()

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar descrição: {str(e)}"}), 500

    # Gerar áudio a partir da descrição usando gTTS
    tts = gTTS(description, lang='pt')
    audio_path = "description_audio.mp3"
    tts.save(audio_path)

    return jsonify({
        "description": description,
        "audio_url": request.host_url + 'audio'
    })

@app.route('/audio')
def get_audio():
    return send_file('description_audio.mp3', mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
