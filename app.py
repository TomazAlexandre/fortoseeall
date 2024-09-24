import openai
from flask import Flask, request, jsonify
from PIL import Image
import io
import base64

# Defina sua chave de API OpenAI
openai.api_key = ""

app = Flask(__name__)

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
    
    # A resposta retorna a descrição da imagem
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
