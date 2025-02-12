import boto3
from gtts import gTTS
from io import BytesIO
import base64
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

# Configuração do Rekognition
rekognition_client = boto3.client('rekognition')

def describe_image(image_bytes):
    """
    Usa o Amazon Rekognition para detectar rótulos (labels) em uma imagem.
    """
    try:
        response = rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )
        labels = [label['Name'] for label in response['Labels']]
        logger.info(f"Rótulos detectados: {labels}")
        return labels
    except Exception as e:
        logger.error(f"Erro ao descrever a imagem: {e}")
        return None

def generate_narrative_description(labels):
    """
    Gera uma descrição narrativa a partir dos rótulos detectados.
    """
    try:
        # Lógica personalizada para combinações de rótulos
        if "Family" in labels and "Park" in labels:
            description = "A imagem mostra uma família em um parque, aproveitando um dia ao ar livre."
        elif "Woman" in labels and "Tree" in labels:
            description = "A imagem mostra uma mulher perto de uma árvore, possivelmente em um ambiente natural."
        elif "Grass" in labels and "Vegetation" in labels:
            description = "A cena ocorre em uma área com grama e vegetação abundante."
        elif "Photography" in labels and "Person" in labels:
            description = "A imagem parece ser uma fotografia de uma pessoa, capturando um momento especial."
        elif "Adult" in labels and "Park" in labels:
            description = "Um adulto está em um parque, desfrutando do ambiente ao ar livre."
        elif "People" in labels and "Grass" in labels:
            description = "Várias pessoas estão em um campo com grama, talvez em um piquenique ou evento."
        elif "Tree" in labels and "Vegetation" in labels:
            description = "A imagem mostra uma árvore cercada por vegetação, indicando um ambiente natural."
        elif "Family" in labels and "Grass" in labels:
            description = "Uma família está reunida em um campo com grama, aproveitando um momento juntos."
        elif "Woman" in labels and "Grass" in labels:
            description = "Uma mulher está em um campo com grama, possivelmente relaxando ou caminhando."
        elif "Person" in labels and "Tree" in labels:
            description = "Uma pessoa está perto de uma árvore, talvez descansando ou apreciando a natureza."
        elif "People" in labels and "Clothing" in labels:
            description = "Várias pessoas estão usando roupas, possivelmente em um evento ou reunião."
        elif "Person" in labels and "Clothing" in labels:
            description = "Varias pessoas, talvez em uma ocasião especial."
        elif "Vest" in labels and "Clothing" in labels:
            description = "A imagem mostra alguém usando um colete, possivelmente em um ambiente casual ou profissional."
        else:
            # Descrição genérica caso nenhuma combinação específica seja encontrada
            description = "A imagem contém os seguintes elementos: " + ", ".join(labels) + "."
        
        logger.info(f"Descrição narrativa gerada: {description}")
        return description
    except Exception as e:
        logger.error(f"Erro ao gerar descrição narrativa: {e}")
        return None

def text_to_speech(text):
    """
    Converte o texto em áudio usando gTTS.
    """
    try:
        tts = gTTS(text=text, lang='pt')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
        logger.info("Áudio gerado com sucesso.")
        return audio_base64
    except Exception as e:
        logger.error(f"Erro ao converter texto em áudio: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload():
    """
    Endpoint para upload de imagens.
    """
    if 'image' not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400

    image = request.files['image']
    image_bytes = image.read()

    # Gera os rótulos da imagem
    labels = describe_image(image_bytes)
    if not labels:
        return jsonify({"error": "Erro ao processar a imagem"}), 500

    # Gera a descrição narrativa
    description = generate_narrative_description(labels)
    if not description:
        return jsonify({"error": "Erro ao gerar descrição narrativa"}), 500

    # Converte a descrição em áudio
    audio_base64 = text_to_speech(description)
    if not audio_base64:
        return jsonify({"error": "Erro ao gerar áudio"}), 500

    return jsonify({
        "description": description,
        "audio": audio_base64
    })

if __name__ == '__main__':
    app.run(debug=True)