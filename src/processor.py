import pandas as pd
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import DocArrayInMemorySearch

load_dotenv()

file_path = 'data/RelatorioAnalise_20260209.xlsx'

def carregar_dados_empresa(file_path):
    # Carregando seu Excel de Fevereiro
    df = pd.read_excel(file_path)
    # Removendo linhas em branco para nao sujar a IA
    df = df.dropna(how='all')

    documentos = [] 

    # Transformando cada linha do Excel em um "Documento" que a IA entende
    for index, row in df.iterrows():
        detalhes = [f"{col}: {row[col]}" for col in df.columns]
        conteudo_completo = "\n".join(detalhes)


        doc = Document(page_content=conteudo_completo, metadata={"linha": index, "fonte": "Relatorio_fevereiro_Completo"})
        documentos.append(doc)
        
    print(f"Sucesso! {len(documentos)} registros processados para a memória da IA.")
    return documentos



def criar_banco_vetorial(documentos):
    print("Criando memória local... aguarde.")
    try:
        # Este modelo roda no seu CPU, sem precisar de API Key ou internet
        # É excelente para garantir que os 2408 registros sejam processados sem erro 404
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_db = Chroma.from_documents(
            documents=documentos,
            embedding=embeddings,
            persist_directory="./vector_db"
        )
            
        print("Mágica concluída: Memória criada com sucesso!")
        return vector_db
    except Exception as e:
                                    
        print(f"Erro ao criar memória: {e}")

# --- FINAL DO ARQUIVO 

if __name__ == "__main__":
    # 1. Defina o caminho do seu arquivo
    caminho = 'data/RelatorioAnalise_20260209.xlsx'
    
    print("Iniciando o processamento...") # Isso ajuda a saber se o script começou
    
    try:
        # 2. Carrega os 2408 registros
        meus_docs = carregar_dados_empresa(caminho)
        
        # 3. Cria a memória vetorial (Isso pode demorar uns 30 segundos)
        print("Criando banco de vetores... aguarde.")
        criar_banco_vetorial(meus_docs)
        
        print("Processo finalizado com sucesso!")
        
    except Exception as e:
        print(f"Ops! Tivemos um problema: {e}")