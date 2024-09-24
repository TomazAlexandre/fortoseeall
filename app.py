import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from PIL import Image
import base64
import io
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def analyze_image(image_bytes):
    # Converte a imagem para base64
    img_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Faz a requisição para o DALL·E ou API de análise da OpenAI
    response = openai.Image.create(
        model="dalle",
        prompt="Analyze this image in detail.",
        n=1,
        size="1024x1024",
        response_format="json",
        image=img_base64
    )

    # Retorna a descrição da imagem
    return response['choices'][0]['text']

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    image_bytes = image.read()

    # Faz a análise da imagem
    description = analyze_image(image_bytes)

    return jsonify({"description": description})

if __name__ == "__main__":
    app.run(debug=True)