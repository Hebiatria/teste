import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import math
import locale

# Define o locale para português do Brasil
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')

# Carrega os dados da OMS
dados_boys = pd.read_csv("bmi_boys.csv", sep=";", decimal=",")
dados_girls = pd.read_csv("bmi_girls.csv", sep=";", decimal=",")

# Título
st.title("🩺 Avaliação Nutricional Infantil")
st.subheader("Baseado nos padrões da OMS 2007 para 5 a 19 anos")

# Dados antropométricos
st.header("📏 Dados antropométricos")

sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
altura = st.number_input("Altura (cm)", min_value=0.0, format="%.2f")

# Datas
st.header("📅 Datas")

min_data = date(1900, 1, 1)
data_nascimento = st.date_input("Data de nascimento", min_value=min_data)
data_afericao = st.date_input("Data da aferição", value=date.today(), min_value=min_data)

# Exibir datas formatadas
st.caption(f"🗓️ Nascimento: {data_nascimento.strftime('%d/%m/%Y')}")
st.caption(f"🗓️ Aferição: {data_afericao.strftime('%d/%m/%Y')}")

# Calcular idade
idade = relativedelta(data_afericao, data_nascimento)
idade_anos = idade.years
idade_meses = idade.months
idade_meses_total = idade_anos * 12 + idade_meses

# Calcular IMC
if altura > 0:
    imc = peso / ((altura / 100) ** 2)
else:
    imc = None

# Função para calcular Z-score real
def calcular_zscore_real(imc, idade_meses, sexo):
    df = dados_boys if sexo == "Masculino" else dados_girls
    linha = df[df["Month"] == idade_meses]
    if linha.empty:
        return None
    L = linha["L"].values[0]
    M = linha["M"].values[0]
    S = linha["S"].values[0]
    if L == 0:
        z = math.log(imc / M) / S
    else:
        z = ((imc / M) ** L - 1) / (L * S)
    return round(z, 2)

# Botão de cálculo
if st.button("✅ Calcular"):
    st.success("Cálculo realizado com sucesso!")

    st.write(f"📅 Idade: {idade_anos} anos e {idade_meses} meses")
    st.write(f"📏 Altura: {altura:.2f} cm")
    st.write(f"⚖️ Peso: {peso:.2f} kg")

    if imc:
        st.write(f"🧮 IMC: {imc:.2f}")
        zscore = calcular_zscore_real(imc, idade_meses_total, sexo)
        if zscore is None:
            st.warning("Idade fora da faixa da OMS (61 a 228 meses).")
        else:
            st.write(f"📊 Z-score do IMC para idade: {zscore:.2f}")
            if zscore < -3:
                st.error("🔴 Magreza severa")
            elif zscore < -2:
                st.warning("🟠 Magreza")
            elif zscore < 1:
                st.success("🟢 IMC normal")
            elif zscore < 2:
                st.warning("🟡 Sobrepeso")
            else:
                st.error("🔴 Obesidade")
    else:
        st.error("Altura inválida para cálculo do IMC.")

# Rodapé
st.caption("Referência: [OMS 2007 - Crescimento 5 a 19 anos](https://www.who.int/tools/growth-reference-data-for-5to19-years)")