import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

# Criando um estado para verificar se o formulário foi preenchido
if "formulario_preenchido" not in st.session_state:
    st.session_state["formulario_preenchido"] = False

# Se ainda não preencheu, mostra os campos de entrada
if not st.session_state["formulario_preenchido"]:
    func = st.sidebar.number_input('Número de funcionários', max_value=1000, value=3)
    horas = st.sidebar.number_input('Horas por dia', min_value=0, max_value=18, value=8)
    dias = st.sidebar.number_input('Dias ao mês', min_value=0, max_value=31, value=22)
    pacotes = st.sidebar.number_input('Quantos pacotes produz mensalmente?', min_value=0, max_value=100000000, value=40000)
    custo_unitario_saquinho_vazio = st.sidebar.number_input('Custo unitário do saquinho vazio em R$', min_value=0.0, max_value=10000000.0, value=0.1)
    lucro_bruto_por_saquinho = st.sidebar.number_input('Lucro Bruto por saquinho embalado em R$', min_value=0.0, max_value=10000000.0, value=1.2)
    custo_medio_funcionario = st.sidebar.number_input('Custo médio por funcionário em R$', min_value=0.0, max_value=100000.0, value=3000.0)
    g_por_saquinho = st.sidebar.number_input('Quantas gramas são embaladas em um saquinho?', min_value=0.0, max_value=1000000.0, value=500.0)
    custo_kg_produto = st.sidebar.number_input('Qual o custo do kg do seu produto em R$?', min_value=0.0, max_value=10000000.0, value=10.0)
    gramas_mais = st.sidebar.number_input('Até quantas g a mais vão em cada saquinho?', min_value=0.0, max_value=10000000.0, value=10.0)

    if dias!= 0 and horas !=0:
        capacidade_produtiva_atual = ((pacotes/60)/dias)/horas
    perda_mes = (pacotes * custo_kg_produto * gramas_mais) / 1000
    mao_obra = func * custo_medio_funcionario
    lucro_bruto = (pacotes * lucro_bruto_por_saquinho - perda_mes) - mao_obra

    # Botão para confirmar os dados e ocultar os campos
    if st.sidebar.button("Enviar Informações"):
        st.session_state["formulario_preenchido"] = True
        st.session_state["func"] = func 
        st.session_state["horas"] = horas
        st.session_state["dias"] = dias
        st.session_state["pacotes"] = pacotes
        st.session_state["custo_unitario_saquinho_vazio"] = custo_unitario_saquinho_vazio
        st.session_state["lucro_bruto_por_saquinho"] = lucro_bruto_por_saquinho
        st.session_state["custo_medio_funcionario"] = custo_medio_funcionario
        st.session_state["g_por_saquinho"] = g_por_saquinho
        st.session_state["custo_kg_produto"] = custo_kg_produto
        st.session_state["gramas_mais"] = gramas_mais
        st.session_state["perda_mes"] = perda_mes
        st.session_state["mao_obra"] = mao_obra
        st.session_state["lucro_bruto"] = lucro_bruto
        st.session_state["capacidade_produtiva_atual_minuto"] = capacidade_produtiva_atual

else:
    # Criando um alerta piscante sobre a perda de dinheiro
    st.markdown(
        """
        <style>
        @keyframes blink {
            0% { color: red; opacity: 1; }
            50% { color: darkred; opacity: 0.5; }
            100% { color: red; opacity: 1; }
        }
        
        .blinking-text {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            animation: blink 1s infinite;
        }
        </style>
        """ + f'<h3 class="blinking-text">⚠️ ALERTA: Você está perdendo mensalmente R$ {st.session_state["perda_mes"]:.2f} em produtos desperdiçados! ⚠️</h3>',
        unsafe_allow_html=True
    )
    # Após preenchimento, exibe apenas a seleção da máquina na sidebar
    select = st.sidebar.selectbox('Selecione a máquina:', ['', 'Semiautomática', 'Automática'])
    if select == 'Semiautomática':
        valor_semi = st.sidebar.number_input('Valor da máquina em R$', min_value=0.0, max_value=10000000.0, value=0.0)
        funcionarios_semi = st.session_state["func"]/2 
        producao_semi_minuto = 10
        producao_semi_hora = 10*60
        producao_semi_dia = producao_semi_hora*st.session_state["horas"]
        producao_semi_mes = producao_semi_dia*st.session_state["dias"]
        producao_atual_hora = st.session_state["capacidade_produtiva_atual_minuto"]*60
        producao_atual_dia = producao_atual_hora*st.session_state["horas"]
        producao_atual_mes = producao_atual_dia*st.session_state["dias"] 
        reducao_desperdicio_g = 8
        reducao_custo_desperdicio = (reducao_desperdicio_g*st.session_state["custo_kg_produto"])/1000
        lucro_bruto_semi = st.session_state["lucro_bruto_por_saquinho"]+reducao_custo_desperdicio
        mao_obra_semi = funcionarios_semi*st.session_state["custo_medio_funcionario"]
        lucro_total_semi = (producao_semi_mes*lucro_bruto_semi)-mao_obra_semi
        lucratividade = f'{((lucro_total_semi*100)/st.session_state["lucro_bruto"]):.0f}%'

        lucratividade_semi = (valor_semi*-1)+lucro_total_semi-st.session_state["lucro_bruto"]
        lista_semi = []
        lista_semi.append(valor_semi*-1)
        lista_semi.append(lucratividade_semi)

        lucro_atual = 0
        lista_atual = []
        lista_atual.append(lucro_atual)
        lucro_atual = st.session_state["lucro_bruto"]
        lista_atual.append(st.session_state["lucro_bruto"])

        meses = []
        meses.append('Aquisição')
        for i in range (1, 13):
            meses.append(f'{i}º mês')

        for i in range(1,12):
            lucratividade_semi = lucratividade_semi+lucro_total_semi-st.session_state["lucro_bruto"]
            lista_semi.append(lucratividade_semi)
            lucro_atual = lucro_atual+st.session_state["lucro_bruto"]
            lista_atual.append(lucro_atual)
        
        ordem = ['Aquisição', '1º mês', '2º mês', '3º mês', '4º mês', '5º mês', '6º mês', '7º mês', '8º mês', '9º mês', '10º mês', '11º mês', '12º mês']

        df = pd.DataFrame({'Meses': meses, 'Lucro Atual': lista_atual, 'Lucro com Máquina Semiautomática': lista_semi})
        df['Meses'] = pd.Categorical(df['Meses'], categories=ordem, ordered=True)
        df = df.sort_values('Meses')    
        # Financiamento para semi automática
        total = valor_semi
        sinal = total*0.25
        tx_juros = 0.035
        parcelas = 24
        valor_financiado = total-sinal
        parcela_mes = (tx_juros*(1+tx_juros)**24)/((1+tx_juros)**parcelas-1)*valor_financiado
        juros = (parcela_mes*parcelas)-valor_financiado
        total_semi = sinal+juros+valor_financiado
        lucro_financiamento = ((sinal+parcela_mes)*-1)+lucro_total_semi-st.session_state["lucro_bruto"]
        lista_financiamento = []
        lista_financiamento.append((sinal+parcela_mes)*-1)
        lista_financiamento.append(lucro_financiamento)
        for i in range(1,12):
            lucro_financiamento = lucro_financiamento+lucro_total_semi-st.session_state["lucro_bruto"]
            lista_financiamento.append(lucro_financiamento)
        df2 = pd.DataFrame({'Meses': meses, 'Lucro Atual': lista_atual, 'Lucro com Máquina Semiautomática': lista_financiamento})
        df['Meses'] = pd.Categorical(df['Meses'], categories=ordem, ordered=True)
        df = df.sort_values('Meses')

        col1, col2, = st.columns(2)
        col3, col4 = st.columns(2)

        sl = st.sidebar.selectbox('Máquina Financiada ou À vista:', ['', 'Financiada', 'À vista'])
        
        reducao_mao_obra = px.bar(x=['Mão de Obra Atual', 'Mão de Obra com Máquina Semiautomática'], y=[st.session_state["mao_obra"], mao_obra_semi], labels={'x':'', 'y':'Custo com mão de obra em R$'}, title='Redução de custos com mão de obra')
        col1.plotly_chart(reducao_mao_obra)

        reducao_de_desperdicio = px.bar(x=['Desperdício Atual', 'Desperdício com Máquina Semiautomática'], y=[st.session_state["perda_mes"], st.session_state["perda_mes"]*0.2], labels={'x':'', 'y':'Custo com desperdício em R$'}, title='Redução de desperdício em R$')
        col2.plotly_chart(reducao_de_desperdicio)
        
        if sl == 'À vista':
            # Criando o gráfico com Plotly
            fig = px.line(df, x='Meses', y=['Lucro Atual', 'Lucro com Máquina Semiautomática'], 
              labels={'value': 'Lucro (R$)', 'Meses': 'Período'}, 
              title="Comparação de Lucro Atual vs Lucro com Máquina Semiautomática")
            col4.plotly_chart(fig)
        
        fig = px.line(x = ['1 Mês', '2 meses', '3 meses', '4 meses', '5 meses', '6 meses', '7 meses', '8 meses', '9 meses', '10 meses', '11 meses', '12 meses'], y = [[producao_atual_mes, producao_atual_mes*2, producao_atual_mes*3, producao_atual_mes*4, producao_atual_mes*5, producao_atual_mes*6, producao_atual_mes*7, producao_atual_mes*8, producao_atual_mes*9, producao_atual_mes*10, producao_atual_mes*11, producao_atual_mes*12],[producao_semi_mes, producao_semi_mes*2, producao_semi_mes*3, producao_semi_mes*4, producao_semi_mes*5, producao_semi_mes*6, producao_semi_mes*7, producao_semi_mes*8, producao_semi_mes*9, producao_semi_mes*10, producao_semi_mes*11, producao_semi_mes*12]], labels={'value':'Produção de pacotes', 'x': ''}, title='Produção atual')
        fig.data[0].name = 'Produção Atual'
        fig.data[1].name = 'Produção Semiautomática' 
        col3.plotly_chart(fig)

        if sl == 'Financiada':
            # Criando o gráfico com Plotly
            fig = px.line(df2, x='Meses', y=['Lucro Atual', 'Lucro com Máquina Semiautomática'], 
                labels={'value': 'Lucro (R$)', 'Meses': 'Período'}, 
                title="Comparação de Lucro Atual vs Lucro com Máquina Semiautomática")
            col4.plotly_chart(fig)

    elif select == 'Automática':
        valor_aut = st.sidebar.number_input('Valor da máquina em R$', min_value=0.0, max_value=10000000.0, value=0.0)
        funcionarios_aut = st.session_state["func"]/3 
        producao_aut_minuto = 12
        producao_aut_hora = 12*60
        producao_aut_dia = producao_aut_hora*st.session_state["horas"]
        producao_aut_mes = producao_aut_dia*st.session_state["dias"]
        producao_atual_hora = st.session_state["capacidade_produtiva_atual_minuto"]*60
        producao_atual_dia = producao_atual_hora*st.session_state["horas"]
        producao_atual_mes = producao_atual_dia*st.session_state["dias"] 
        reducao_desperdicio_g = 8
        reducao_custo_desperdicio = (reducao_desperdicio_g*st.session_state["custo_kg_produto"])/1000
        lucro_bruto_aut = st.session_state["lucro_bruto_por_saquinho"]+reducao_custo_desperdicio
        mao_obra_aut = funcionarios_aut*st.session_state["custo_medio_funcionario"]
        lucro_total_aut = (producao_aut_mes*lucro_bruto_aut)-mao_obra_aut
        lucratividade = f'{((lucro_total_aut*100)/st.session_state["lucro_bruto"]):.0f}%'

        lucratividade_aut = (valor_aut*-1)+lucro_total_aut-st.session_state["lucro_bruto"]
        lista_aut = []
        lista_aut.append(valor_aut*-1)
        lista_aut.append(lucratividade_aut)

        lucro_atual = 0
        lista_atual = []
        lista_atual.append(lucro_atual)
        lucro_atual = st.session_state["lucro_bruto"]
        lista_atual.append(st.session_state["lucro_bruto"])

        meses = []
        meses.append('Aquisição')
        for i in range (1, 13):
            meses.append(f'{i}º mês')

        for i in range(1,12):
            lucratividade_aut = lucratividade_aut+lucro_total_aut-st.session_state["lucro_bruto"]
            lista_aut.append(lucratividade_aut)
            lucro_atual = lucro_atual+st.session_state["lucro_bruto"]
            lista_atual.append(lucro_atual)
        
        ordem = ['Aquisição', '1º mês', '2º mês', '3º mês', '4º mês', '5º mês', '6º mês', '7º mês', '8º mês', '9º mês', '10º mês', '11º mês', '12º mês']

        df = pd.DataFrame({'Meses': meses, 'Lucro Atual': lista_atual, 'Lucro com Máquina Automática': lista_aut})
        df['Meses'] = pd.Categorical(df['Meses'], categories=ordem, ordered=True)
        df = df.sort_values('Meses')
        
        
        # Financiamento para automática
        total = valor_aut
        sinal = total*0.25
        tx_juros = 0.035
        parcelas = 24
        valor_financiado = total-sinal
        parcela_mes = (tx_juros*(1+tx_juros)**24)/((1+tx_juros)**parcelas-1)*valor_financiado
        juros = (parcela_mes*parcelas)-valor_financiado
        total_aut = sinal+juros+valor_financiado
        lucro_financiamento = ((sinal+parcela_mes)*-1)+lucro_total_aut-st.session_state["lucro_bruto"]
        lista_financiamento = []
        lista_financiamento.append((sinal+parcela_mes)*-1)
        lista_financiamento.append(lucro_financiamento)
        for i in range(1,12):
            lucro_financiamento = lucro_financiamento+lucro_total_aut-st.session_state["lucro_bruto"]
            lista_financiamento.append(lucro_financiamento)
        print(len(meses), len(lista_atual), len(lista_financiamento))
        df2 = pd.DataFrame({'Meses': meses, 'Lucro Atual': lista_atual, 'Lucro com Máquina Automática': lista_financiamento})
        df['Meses'] = pd.Categorical(df['Meses'], categories=ordem, ordered=True)
        df = df.sort_values('Meses')

        col1, col2, = st.columns(2)
        col3, col4 = st.columns(2)

        sl = st.sidebar.selectbox('Máquina Financiada ou À vista:', ['', 'Financiada', 'À vista'])
        
        reducao_mao_obra = px.bar(x=['Mão de Obra Atual', 'Mão de Obra com Máquina Automática'], y=[st.session_state["mao_obra"], mao_obra_aut], labels={'x':'', 'y':'Custo com mão de obra em R$'}, title='Redução de custos com mão de obra')
        col1.plotly_chart(reducao_mao_obra)

        reducao_de_desperdicio = px.bar(x=['Desperdício Atual', 'Desperdício com Máquina Automática'], y=[st.session_state["perda_mes"], st.session_state["perda_mes"]*0.2], labels={'x':'', 'y':'Custo com desperdício em R$'}, title='Redução de desperdício em R$')
        col2.plotly_chart(reducao_de_desperdicio)
        
        if sl == 'À vista':
            # Criando o gráfico com Plotly
            fig = px.line(df, x='Meses', y=['Lucro Atual', 'Lucro com Máquina Automática'], 
              labels={'value': 'Lucro (R$)', 'Meses': 'Período'}, 
              title="Comparação de Lucro Atual vs Lucro com Máquina Automática")
            col4.plotly_chart(fig)
        
        fig = px.line(x = ['1 Mês', '2 meses', '3 meses', '4 meses', '5 meses', '6 meses', '7 meses', '8 meses', '9 meses', '10 meses', '11 meses', '12 meses'], y = [[producao_atual_mes, producao_atual_mes*2, producao_atual_mes*3, producao_atual_mes*4, producao_atual_mes*5, producao_atual_mes*6, producao_atual_mes*7, producao_atual_mes*8, producao_atual_mes*9, producao_atual_mes*10, producao_atual_mes*11, producao_atual_mes*12],[producao_aut_mes, producao_aut_mes*2, producao_aut_mes*3, producao_aut_mes*4, producao_aut_mes*5, producao_aut_mes*6, producao_aut_mes*7, producao_aut_mes*8, producao_aut_mes*9, producao_aut_mes*10, producao_aut_mes*11, producao_aut_mes*12]], labels={'value':'Produção de pacotes', 'x': ''}, title='Produção atual')
        fig.data[0].name = 'Produção Atual'
        fig.data[1].name = 'Produção Automática' 
        col3.plotly_chart(fig)

        if sl == 'Financiada':
            # Criando o gráfico com Plotly
            fig = px.line(df2, x='Meses', y=['Lucro Atual', 'Lucro com Máquina Automática'], 
                labels={'value': 'Lucro (R$)', 'Meses': 'Período'}, 
                title="Comparação de Lucro Atual vs Lucro com Máquina Automática")
            col4.plotly_chart(fig)

    