import os
import openai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir requisições do frontend

# Carregar a chave da API do OpenAI a partir das variáveis de ambiente
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

def analyze_image(image_bytes):
    try:
        # Converter a imagem para base64
        img_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Enviar a imagem para a API de análise da OpenAI
        # Nota: Certifique-se de que a API utilizada suporta análise de imagens
        response = openai.Image.create(
            prompt="Describe this image in detail.",
            image=img_base64,
            n=1,
            size="1024x1024",
            response_format="json"
        )
        # Retornar a descrição gerada
        return response['choices'][0]['text']
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return "Desculpe, ocorreu um erro ao processar a imagem."

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "Nenhum arquivo de imagem fornecido"}), 400

    image = request.files['image']
    image_bytes = image.read()

    # Analisar a imagem
    description = analyze_image(image_bytes)

    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(debug=True)
