import openai  
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ler_arquivo(arquivo):
    with open(arquivo,'r', encoding='utf-8') as file:
        return file.read()
    
def resumo(texto):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Resumo o seguinte texto: {texto}",
        temperature=0.4,
        max_tokens=2048,
        n=1,
        stop=None
    )
    return response['choises'][0]['text']


arquivo = 'artigo.txt'
texto = ler_arquivo(arquivo)
print(resumo(texto))
