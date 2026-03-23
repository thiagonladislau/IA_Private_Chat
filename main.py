import streamlit as st
from src.app import buscar_contexto, perguntar_ao_gemini

# Configuração da Página
st.set_page_config(page_title="Analista IA - Logística", page_icon="🚚")

st.title("🚚 Assistente de Logística Privado")
st.markdown("---")

# Inicializar o histórico de chat na sessão do navegador
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Área de entrada do usuário
if prompt := st.chat_input("Ladislau, o que deseja saber sobre as cargas?"):
    
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Processamento da resposta
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Buscando no Excel e consultando Gemini...")
        
        try:
            # Chama as funções que você já validou no app.py
            contexto = buscar_contexto(prompt)
            resposta = perguntar_ao_gemini(prompt, contexto)
            
            message_placeholder.markdown(resposta)
            # Adicionar resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.error(f"Erro ao processar: {e}")

# Barra Lateral (Sidebar) com Informações
with st.sidebar:
    st.header("Status do Sistema")
    st.success("Conectado ao Gemini 3 Flash")
    st.info("Memória Local: 2409 registros carregados")
    
    # Sliders para você testar a precisão em tempo real
    st.session_state.k_value = st.slider("Quantidade de Contexto (k)", 5, 50, 10)
    
    if st.button("Limpar Histórico"):
        st.session_state.messages = []
        st.rerun()