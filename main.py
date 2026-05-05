import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date, datetime

# Configuração da página
st.set_page_config(page_title="Gestão Financeira", layout="centered")

# 1. Conexão com o Google Sheets
# Certifique-se de que o URL está nos "Secrets" do Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    # Lê a planilha. O parâmetro ttl=0 evita que o Streamlit use cache antigo
    return conn.read(ttl=0)

st.title("🏦 Sistema de Boletos & Google Sheets")

# Menu Lateral
menu = st.sidebar.selectbox("Navegação", ["Início", "Adicionar Conta", "Diário (Hoje)"])

if menu == "Início":
    st.write("Bem-vindo ao seu sistema na nuvem!")
    st.info("Os dados agora são salvos diretamente na sua Planilha Google.")

elif menu == "Adicionar Conta":
    st.header("📄 Cadastrar Nova Conta")
    
    with st.form("form_adicionar"):
        fornecedor = st.text_input("Nome do Fornecedor")
        vencimento = st.date_input("Data de Vencimento", value=date.today())
        tipo = st.selectbox("Tipo de Documento", ["Boleto", "Cheque", "Pix", "Dinheiro"])
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
        status = st.radio("Status", ["Aberto", "Pago"], horizontal=True)
        num_doc = st.text_input("Nº do Documento", value="S/N")
        cod_barras = st.text_input("Código de Barras", value="Não informado")
        
        if st.form_submit_button("Salvar na Planilha"):
            if fornecedor:
                # Lê os dados atuais
                df_existente = carregar_dados()
                
                # Cria a nova linha
                nova_linha = pd.DataFrame([{
                    "Fornecedor": fornecedor,
                    "Vencimento": vencimento.strftime('%Y-%m-%d'),
                    "Tipo": tipo,
                    "numDoc": num_doc,
                    "Valor": valor,
                    "Status": status,
                    "codBarras": cod_barras
                }])
                
                # Adiciona a nova linha ao final do DataFrame
                df_atualizado = pd.concat([df_existente, nova_linha], ignore_index=True)
                
                # Atualiza a planilha no Google
                conn.update(data=df_atualizado)
                st.success(f"Conta de {fornecedor} salva com sucesso!")
            else:
                st.error("O nome do fornecedor é obrigatório.")

elif menu == "Diário (Hoje)":
    st.header("📅 Vencimentos de Hoje")
    hoje_str = date.today().strftime('%Y-%m-%d')
    
    df = carregar_dados()
    
    if not df.empty:
        # Filtra as contas que vencem hoje e estão em aberto
        contas_hoje = df[(df['Vencimento'] == hoje_str) & (df['Status'] == 'Aberto')]
        
        if not contas_hoje.empty:
            st.dataframe(contas_hoje)
        else:
            st.success("Tudo em dia! Nenhuma conta vence hoje.")
    else:
        st.warning("A planilha está vazia.")