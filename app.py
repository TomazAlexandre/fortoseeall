import openai
from flask import Flask, render_template, request, jsonify
from PIL import Image
from flask_cors import CORS
import base64
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)


# Rota principal para renderizar o frontend
@app.route('/')
def index():
    return render_template('index.html')

def analyze_image(image_bytes):
    # Convertendo a imagem para base64
    img_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Fazendo a requisição para o modelo de análise de imagem
    response = openai.Image.create(
        prompt="Describe this image in detail.",
        image=img_base64,
        n=1,
        size="1024x1024",
        response_format="json"
    )
    
    return response['choices'][0]['text']


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_bytes = image.read()

    # Chamando a função para analisar a imagem
    description = analyze_image(image_bytes)

    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(debug=True)
