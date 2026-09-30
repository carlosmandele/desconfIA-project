import os
import streamlit as st


# Configuração da página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 


# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🤖")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em ...")


    #


    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar...")

    st.markdown("---")
    st.markdown("Conheça outras soluções nossas...:")

    # Link para o site da "company"....
    st.markdown("🔗 [Company](https://www.desconfIAproject.com.br)")
    
    # Botão de link para enviar e-mail ao suporte da Company
    st.link_button(" E-mail Para o Suporte Company no Caso de Dúvidas", "mailto:suporte@desconfIAproject.com.br")


# Título principal do app
st.title("Desconf-IA Project: ")

# Subtítulo adicional
st.subheader("Assistente Pessoal de...")

# Texto auxiliar abaixo do título
st.caption("Faça sua pergunta sobre..., explicações e referências.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


