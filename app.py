import os
import streamlit as st
import keras
import numpy as np


# Configurações da página
st.set_page_config(
    page_title="DesconfIA - Detector de Smishing ",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "texto_input" not in st.session_state:
    st.session_state["texto_input"] = ""

if "historico_mensagens" not in st.session_state:
    st.session_state["historico_mensagens"] = []

# Carregando o modelo - carrega o modelo uma única vez em cache para performance
@st.cache_resource
def carregar_modelo():
    return keras.models.load_model("modelo_extraid")


def preparar_entrada_modelo(texto):
    tokenizer = modelo.preprocessor.tokenizer
    # Implementação Python do WordPiece para dispensar tensorflow-text
    tokens = tokenizer._tokenize_python([texto])[0]
    sequence_length = modelo.preprocessor.sequence_length

    token_ids = [
        tokenizer.cls_token_id,
        *tokens[: sequence_length - 2],
        tokenizer.sep_token_id,
    ]
    padding_length = sequence_length - len(token_ids)
    token_ids.extend([tokenizer.pad_token_id] * padding_length)
    padding_mask = (
        [1] * (sequence_length - padding_length) + [0] * padding_length
    )

    return {
        "token_ids": np.asarray([token_ids], dtype=np.int32),
        "padding_mask": np.asarray([padding_mask], dtype=np.int32),
    }


try:
    modelo = carregar_modelo()
    st.success("Olá! Seja bem-vindo ao desconfIA!")
except Exception as e:
    st.error(f"Erro ao carregar o modelo. Detalhes: {e}")
    st.stop()

# Cabeçalho de mensagens de erros
st.title("🛡️ Detector de Smishing ")
st.subheader("Assistente Pessoal de...")
st.caption("Faça sua pergunta sobre..., explicações e referências.")

# Barra lateral contendo informações sobre o assistente, links e explicações adicionais
with st.sidebar:
    
    # Título da barra lateral
    st.title("🛡️ DesconfIA")
    
    # Texto explicativo sobre o assistente
    st.markdown("Um assistente de IA focado em ...")

    st.markdown("---")
    st.markdown(
        "Este assistente foi desenvolvido para auxiliar usuários e instituições a identificar "
        "tentativas de golpes digitais, engenharia social e links malisiosos em tempo real."
        "Ele utiliza técnicas avançadas de aprendizado de máquinas para analisar o conteúdo das mensagens e fornecer "
        "uma avaliação sobre a probabilidade de serem fraudulentas."
    )

    st.markdown("---")
    st.markdown("Conheça outras soluções nossas:")
    # Link para o site do "projeto"
    st.markdown("🔗 [desconfIA Project](https://www.desconfIAproject.com.br)")
    # Link para enviar e-mail ao suporte
    st.link_button("E-mail para o suporte em caso de dúvidas", "[suporte](mailto:suporte@desconfIAproject.com.br)")
    
# Entrada do usuário
texto_usuario = st.text_area("Texto da Mensagem:", placeholder="Digite ou cole o SMS aqui...")

if st.button("Analisar Mensagem", type="primary"):
    if texto_usuario.strip() == "":
        st.warning("Por favor, digite alguma mensagem para análise.")
    else:
        with st.spinner("Analisando..."):
            processed_input = preparar_entrada_modelo(texto_usuario)
            prob_smishing = float(
                modelo(processed_input, training=False).numpy()[0][0]
            )
            prob_legitima = 1.0 - prob_smishing

            # Decisão com base no limiar ótimo que calculamos (0.5343)
            LIMIAR_OTIMO = 0.5343
            e_smishing = prob_smishing >= LIMIAR_OTIMO

        # Visualização dos resultados
        st.subheader("Resultados do Diagnóstico:")
        if e_smishing:
            st.error(f"🚨 **ALERTA DE SMISHING (GOLPE)!** (Confiança: {prob_smishing * 100:.2f}%)")
        else:
            st.success(f"🟢 **Mensagem Legítima (Segura)** (Confiança: {prob_legitima * 100:.2f}%)")

        # Métricas visuais das probabilidades
        col1, col2 = st.columns(2)
        col1.metric("Probabilidade de Smishing", f"{prob_smishing * 100:.2f}%")
        col2.metric("Probabilidade de Legítima", f"{prob_legitima * 100:.2f}%")