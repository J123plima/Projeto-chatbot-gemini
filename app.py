import streamlit as st
from google import genai
from google.genai import types

#MAIS TARDE VAMOS COLAR CODIGO AQUI

def converter_para_gemini(historico):
    mensagens_gemini = []


    for mensagem in historico:
        papel = mensagem["role"]
        conteudo = mensagem["content"]


        if papel == "assistant":
            papel_gemini = "model"
        else:
            papel_gemini = "user"


        mensagens_gemini.append(
            types.Content(
                role=papel_gemini,
                parts=[types.Part.from_text(text=conteudo)]
            )
        )


    return mensagens_gemini


def gerar_resposta():
    resposta = cliente.models.generate_content(
        model=MODELO,
        contents=converter_para_gemini(st.session_state.historico),
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.4,
        )
    )


    return resposta.text



MODELO = "gemini-2.5-flash"
persona = open("homem_aranha_persona.txt", "r", encoding="utf-8")
INSTRUCAO_SISTEMA = persona.read()
persona.close()

st.set_page_config("Chatbot com gimini", "🕷️🕸️🕷️")
st.title("Chatbot do Homem Aranha 🕷️🕸️")

chave_api = st.sidebar.text_input("Digite sua chave de API", type="password")

if not chave_api:
    st.warning("É preciso de uma chave de API")
    st.stop()

cliente = genai.Client(api_key= chave_api)

if "historico" not in st.session_state:
    st.session_state.historico = []

for mensagem in st.session_state.historico: #percorre o historico 
    with st.chat_message(mensagem["role"]): # mostra no chat_message o usuario e a pergunta/resposta
        st.markdown(mensagem["content"])

entrada_usuario = st.chat_input("Digite sua pergunta")

if entrada_usuario:
    st.session_state.historico.append({
       "role":"user",
       "content":entrada_usuario  
    })


    with st.chat_message("user"):
        st.markdown(entrada_usuario)

    with st.chat_message("assistant"):
        resposta_ai = gerar_resposta()
        st.markdown(resposta_ai)

    st.session_state.historico.append({
       "role":"assistant",
       "content":resposta_ai  
    })