import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv, find_dotenv

# --- Carregar variáveis de ambiente ---
load_dotenv(find_dotenv())
groq_api_key = os.getenv("API_GROQ_KEY")

# --- Verificação detalhada ---
st.sidebar.title("Debug Info")
st.sidebar.write(f"Chave carregada: {'Sim' if groq_api_key else 'Não'}")

if groq_api_key:
    st.sidebar.write(f"Tamanho da chave: {len(groq_api_key)} caracteres")
    st.sidebar.write(f"Começa com: {groq_api_key[:10]}...")
else:
    st.sidebar.error("Chave não encontrada!")

# --- Verificar se a chave foi carregada ---
if not groq_api_key:
    st.error("A chave 'API_GROQ_KEY' não foi encontrada. Verifique seu arquivo .env")
    st.stop()

# --- Inicializar cliente Groq ---
try:
    client = Groq(api_key=groq_api_key)
    st.sidebar.success("Cliente Groq inicializado com sucesso!")
except Exception as e:
    st.sidebar.error(f"Erro ao inicializar cliente: {e}")
    st.stop()

# --- Configuração da Página ---
st.set_page_config(page_title="ChatIA", layout="centered")

# --- Estilo Moderno com CSS ---
st.markdown("""
    <style>
        body {
            background-color: #0f1117;
            color: #f0f0f0;
        }
        .stChatMessage {
            padding: 10px 20px;
            border-radius: 10px;
            margin-bottom: 10px;
            max-width: 90%;
            word-wrap: break-word;
        }
        .human {
            background-color: #1f2937;
            text-align: right;
            margin-left: auto;
        }
        .ai {
            background-color: #111827;
            border-left: 4px solid #3b82f6;
        }
        .chat-title {
            font-size: 2em;
            font-weight: bold;
            color: #3b82f6;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-text {
            background-color: #1f2937;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #1f2937;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.markdown('<div class="chat-title">🤖 AI Chat (Groq)</div>', unsafe_allow_html=True)

# --- Seletor de Modelo ---
model_option = st.sidebar.selectbox(
    "Escolha o modelo:",
    ["llama-3.1-8b-instant", "llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma-7b-it"]
)

# --- Configurações de Temperatura ---
temperature = st.sidebar.slider("Temperatura:", 0.0, 1.0, 0.7, 0.1)

# --- Botão para limpar chat ---
if st.sidebar.button("🧹 Limpar Chat"):
    st.session_state.messages = []
    st.rerun()

# --- Inicializa histórico ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Exibir histórico de mensagens ---
for msg in st.session_state.messages:
    role = msg["role"]
    css_class = "human" if role == "user" else "ai"
    icon = "🧑" if role == "user" else "🤖"
    st.markdown(
        f'<div class="stChatMessage {css_class}"><b>{icon}:</b> {msg["content"]}</div>',
        unsafe_allow_html=True
    )

# --- Input de mensagem ---
user_input = st.chat_input("Envie sua dúvida...")

if user_input:
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Exibe imediatamente no frontend
    st.markdown(
        f'<div class="stChatMessage human"><b>🧑:</b> {user_input}</div>',
        unsafe_allow_html=True
    )

    # Preparar mensagens para a API
    messages_for_api = [{"role": msg["role"], "content": msg["content"]} 
                       for msg in st.session_state.messages]

    # Geração da resposta usando a API Groq diretamente
    try:
        with st.spinner("🤖 Gerando resposta..."):
            completion = client.chat.completions.create(
                model=model_option,
                messages=messages_for_api,
                temperature=temperature,
                max_tokens=2048,
                top_p=1,
                stream=False
            )
            
            ai_reply = completion.choices[0].message.content.strip()

        # Armazena resposta
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        # Exibe resposta
        st.markdown(
            f'<div class="stChatMessage ai"><b>🤖:</b> {ai_reply}</div>',
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")
        st.info("Tente: 1) Verificar a chave API 2) Trocar de modelo 3) Verificar conexão")

# --- Informações adicionais no sidebar ---
st.sidebar.markdown("---")
st.sidebar.info("""
**💡 Dicas:**
- Temperatura baixa = respostas mais focadas
- Temperatura alta = respostas mais criativas
- Use o botão 'Limpar Chat' para reiniciar
""")

st.sidebar.markdown("---")
st.sidebar.write("🔑 **Status da API:** ✅ Conectado" if groq_api_key else "❌ Não conectado")