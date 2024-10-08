from flask import Flask, request, jsonify, send_file, render_template
import openai
from PIL import Image
import io
import os
from gtts import gTTS
import pytesseract  # Biblioteca de OCR para extrair texto da imagem
import pytesseract

# Caminho para o executável do Tesseract no Heroku
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

app = Flask(__name__)

# Configurar a API Key da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    # Serve a página HTML do frontend
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def analyze_image():
    try:
        # Verifica se uma imagem foi enviada
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
        
        # Fazer a chamada à API da OpenAI para gerar a descrição
        response = openai.Completion.create(
            engine="text-davinci-003",  # Ou outro modelo que você preferir
            prompt=prompt,
            max_tokens=100
        )
        description = response.choices[0].text.strip()

        # Gerar áudio a partir da descrição usando gTTS
        tts = gTTS(description, lang='pt')
        audio_path = "description_audio.mp3"
        tts.save(audio_path)

        # Retornar a resposta com a descrição e link para o áudio gerado
        return jsonify({
            "description": description,
            "audio_url": request.host_url + 'audio'
        })

    except Exception as e:
        # Capturar qualquer exceção e retornar um erro no formato JSON
        return jsonify({"error": f"Erro ao processar a imagem: {str(e)}"}), 500

@app.route('/audio')
def get_audio():
    # Enviar o arquivo de áudio gerado
    return send_file('description_audio.mp3', mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
