import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.Client()

mensagens = [
    {'role': 'user', 'content': 'Crie uma história de dois parágrafos sobre uma viagem a Marte'}
]
resposta = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=mensagens,
    max_tokens=50,
    temperature=0.7,
    stream=True,
)

for stream_resp in resposta:
    texto = stream_resposta.choices[0].delta.content
    if texto:
        print(texto, end='')

resposta_completa = ''
for stream_resposta in resposta:
    texto = stream_resposta.choices[0].delta.content
    if texto:
        resposta_completa += texto
        print(texto, end='')