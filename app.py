import os
from dotenv import load_dotenv, find_dotenv


import streamlit as st
from langchain_groq import ChatGroq
load_dotenv(find_dotenv())
api_key = os.getenv("API_GROQ_KEY")
# --- Configuração da Página ---
st.set_page_config(page_title="ChatIA", layout="centered")
# --- Testa se carregou corretamente ---
if not api_key:
    raise ValueError("A chave 'API_GROQ_KEY' não foi encontrada. Verifique seu arquivo .env")

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
    </style>
""", unsafe_allow_html=True)

# --- Título ---
st.markdown('<div class="chat-title">🤖 AI Chat</div>', unsafe_allow_html=True)

# --- Inicializa histórico ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LLM ---
llm = ChatGroq(model="deepseek-r1-distill-llama-70b", api_key=api_key)

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

    # Geração da resposta
    response = llm.invoke(user_input)
    ai_reply = response.content.strip()

    # Armazena resposta
    st.session_state.messages.append({"role": "ai", "content": ai_reply})

    # Exibe resposta
    st.markdown(
        f'<div class="stChatMessage ai"><b>🤖:</b> {ai_reply}</div>',
        unsafe_allow_html=True
    )
