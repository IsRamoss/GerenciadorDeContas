import streamlit as st
import funcoes
import dados
from datetime import date

st.set_page_config(page_title="Gerenciador Financeiro", layout="centered")

st.title("🏦 Sistema de Boletos")

# Menu Lateral
menu = st.sidebar.selectbox("Navegação", ["Início", "Adicionar Conta", "Diário (Hoje)", "Editar"])

if menu == "Início":
    st.write("Bem-vindo ao seu sistema de gestão financeira!")
    st.info("Use o menu lateral para navegar.")

elif menu == "Adicionar Conta":
    st.header("📄 Cadastrar Nova Conta")
    with st.form("form_adicionar"):
        fornecedor = st.text_input("Nome do Fornecedor")
        vencimento = st.date_input("Data de Vencimento", value=date.today())
        tipo = st.selectbox("Tipo de Documento", ["Boleto", "Cheque", "Pix", "Dinheiro"])
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
        status = st.radio("Status", ["Aberto", "Pago"], horizontal=True)
        
        if st.form_submit_button("Salvar Conta"):
            if fornecedor:
                dadosCSV = (fornecedor, str(vencimento), tipo, "S/N", valor, status, "")
                dados.salvarArquivo(dadosCSV)
                st.success("Conta salva com sucesso!")
            else:
                st.error("O nome do fornecedor é obrigatório.")

elif menu == "Diário (Hoje)":
    st.header("📅 Vencimentos de Hoje")
    linhas = dados.lerTudo()
    # Lógica simplificada para exibir em tabela no Streamlit
    if len(linhas) > 1:
        st.table(linhas)
    else:
        st.warning("Nenhuma conta encontrada.")