import os
import requests
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Carregar as variáveis de ambiente (sua chave do Google)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def buscar_contexto(pergunta):
    # Usar o MESMO modelo de embedding do processor.py
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Carregar o banco que você criou na 'mágica concluída'
    vector_db = Chroma(persist_directory="./vector_db", embedding_function=embeddings)
    
    # Isso vai imprimir o total real de registros guardados no banco
    print(f"Total de registros no banco: {vector_db._collection.count()}")

    # Busca os 10 registros mais parecidos com a pergunta
    docs = vector_db.similarity_search(pergunta, k=10)
    contexto = "\n".join([doc.page_content for doc in docs])
    return contexto

def perguntar_ao_gemini(pergunta, contexto):
    # A URL exata que funcionou no seu Postman!
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    prompt = f"""
    Você é um assistente analista de logística. Use as informações abaixo do relatório para responder à pergunta.
    
    CONTEXTO DO EXCEL:
    {contexto}
    
    PERGUNTA DO USUÁRIO:
    {pergunta}
    
    Resposta:
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Erro na conexão: {response.status_code} - {response.text}"

if __name__ == "__main__":
    print("--- CHAT DA EMPRESA ATIVO ---")
    while True:
        pergunta = input("\nLadislau, o que deseja saber? (ou 'sair'): ")
        if pergunta.lower() == 'sair':
            break
            
        print("Buscando no Excel...")
        contexto = buscar_contexto(pergunta)
        
        print("Consultando a IA...")
        resposta = perguntar_ao_gemini(pergunta, contexto)
        
        print(f"\nRESPOSTA: {resposta}")