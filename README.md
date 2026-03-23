# 🚚 Assistente de Logística Privado (RAG + Gemini 3 Flash)

Este projeto é um **Assistente de Inteligência Artificial Especializado em Devoluções**, desenvolvido para realizar consultas complexas em grandes volumes de dados (Excel/CSV) com foco em privacidade e performance.

O sistema utiliza a arquitetura **RAG (Retrieval-Augmented Generation)**, garantindo que a IA consulte apenas documentos privados e locais antes de gerar respostas, evitando alucinações e mantendo a segurança dos dados corporativos.

---

## 🖼️ Interface do Sistema
Abaixo, capturas de tela do assistente em operação:

![Dashboard de Logística](screenshot)
*Interface desenvolvida com Streamlit apresentando o status da conexão e registros carregados.*

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **LLM:** Google Gemini 3 Flash (via API)
* **Banco Vetorial:** ChromaDB (Persistência Local)
* **Embeddings:** HuggingFace (Processamento local via CPU)
* **Interface:** Streamlit
* **Manipulação de Dados:** Pandas

---

## 🚀 Diferenciais Técnicos
* **Privacidade de Dados:** Os documentos são vetorizados localmente. Apenas o contexto relevante é enviado à API.
* **Busca Semântica:** Utiliza `k-neighbors` para encontrar informações por similaridade, não apenas palavras-chave.
* **Escalabilidade:** Capaz de processar milhares de registros com baixo consumo de memória.

---

## ⚙️ Como Executar o Projeto

1. **Instale as dependências:**
   ```bash
   pip install streamlit langchain langchain-community chromadb requests pandas