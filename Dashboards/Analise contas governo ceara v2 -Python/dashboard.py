import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import requests
import psycopg2
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import io
import kaleido.scopes.plotly

# Configuração inicial do Streamlit
st.set_page_config(layout='wide')

# Função para obter o período de data desejado
def obter_data_formatada(option):
    today = datetime.now()
    
    if option == 1:
        start_date = today
    elif option == 2:
        start_date = today - timedelta(days=15)
    elif option == 3:
        start_date = today - timedelta(days=30)
    elif option == 4:
        start_date = today - timedelta(days=180)
    elif option == 5:
        start_date = today - timedelta(days=365)
    else:
        raise ValueError("Opção inválida")
    
    end_date = today  # Data de fim é sempre hoje para essas opções
    return start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y')

# Função para consultar dados da API
def consultar_dados(url):
    try:
        response = requests.get(url, headers={'accept': 'application/json'})
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            st.error(f'Erro na requisição: {response.status_code}')
            return []
    except requests.RequestException as e:
        st.error(f"Erro ao fazer requisição à API: {e}")
        return []

# Função para inserir dados no banco de dados
def inserir_dados_banco(dados_concatenados):
    conn = psycopg2.connect(
        host='localhost',
        database='trabalho_m3_teste',
        user='postgres',
        password='123'
    )
    crsr = conn.cursor()

    # Limpar a tabela antes do insert
    crsr.execute('TRUNCATE TABLE public.contrato_convenio')

    for index, row in dados_concatenados.iterrows():
        crsr.execute('''INSERT INTO contrato_convenio (id, cod_concedente, cod_financiador, cod_gestora, cod_orgao, cod_secretaria, descricao_modalidade, descricao_objeto, descricao_tipo, descricao_url,
            data_assinatura, data_processamento, data_termino, flg_tipo, isn_parte_destino,
            isn_sic, num_spu, valor_contrato, isn_modalidade, isn_entidade, tipo_objeto,
            num_spu_licitacao, descricao_justificativa, valor_can_rstpg, data_publicacao_portal,
            descricao_url_pltrb, descricao_url_ddisp, descricao_url_inexg, cod_plano_trabalho,
            num_certidao, descriaco_edital, cpf_cnpj_financiador, num_contrato, valor_original_concedente,
            valor_original_contrapartida, valor_atualizado_concedente, valor_atualizado_contrapartida,
            created_at, updated_at, plain_num_contrato, calculated_valor_aditivo, calculated_valor_ajuste,
            calculated_valor_empenhado, calculated_valor_pago, contract_type, infringement_status,
            cod_financiador_including_zeroes, accountability_status, plain_cpf_cnpj_financiador,
            descricao_situacao, data_publicacao_doe, descricao_nome_credor, isn_parte_origem, data_auditoria,
            data_termino_original, data_inicio, data_rescisao, confidential, gestor_contrato,
            data_finalizacao_prestacao_contas) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (row.get('id'), row.get('cod_concedente'), row.get('cod_financiador'), row.get('cod_gestora'), row.get('cod_orgao'), row.get('cod_secretaria'),
                        row.get('descricao_modalidade'), row.get('descricao_objeto'), row.get('descricao_tipo'), row.get('descricao_url'),
                        row.get('data_assinatura'), row.get('data_processamento'), row.get('data_termino'), row.get('flg_tipo'), row.get('isn_parte_destino'),
                        row.get('isn_sic'), row.get('num_spu'), row.get('valor_contrato'), row.get('isn_modalidade'), row.get('isn_entidade'), row.get('tipo_objeto'),
                        row.get('num_spu_licitacao'), row.get('descricao_justificativa'), row.get('valor_can_rstpg'), row.get('data_publicacao_portal'),
                        row.get('descricao_url_pltrb'), row.get('descricao_url_ddisp'), row.get('descricao_url_inexg'), row.get('cod_plano_trabalho'),
                        row.get('num_certidao'), row.get('descriaco_edital'), row.get('cpf_cnpj_financiador'), row.get('num_contrato'), row.get('valor_original_concedente'),
                        row.get('valor_original_contrapartida'), row.get('valor_atualizado_concedente'), row.get('valor_atualizado_contrapartida'),
                        row.get('created_at'), row.get('updated_at'), row.get('plain_num_contrato'), row.get('calculated_valor_aditivo'), row.get('calculated_valor_ajuste'),
                        row.get('calculated_valor_empenhado'), row.get('calculated_valor_pago'), row.get('contract_type'), row.get('infringement_status'),
                        row.get('cod_financiador_including_zeroes'), row.get('accountability_status'), row.get('plain_cpf_cnpj_financiador'),
                        row.get('descricao_situacao'), row.get('data_publicacao_doe'), row.get('descricao_nome_credor'), row.get('isn_parte_origem'), row.get('data_auditoria'),
                        row.get('data_termino_original'), row.get('data_inicio'), row.get('data_rescisao'), row.get('confidential'), row.get('gestor_contrato'),
                        row.get('data_finalizacao_prestacao_contas')
                        ))

    conn.commit()
    crsr.close()
    conn.close()


# Função para gerar gráficos
def gerar_graficos(dados_concat):
    # Agrupar e somar valores pagos e empenhados por credor
    df_credor_pago = dados_concat.groupby('descricao_nome_credor')['calculated_valor_pago'].sum().reset_index()
    df_credor_pago = df_credor_pago.sort_values(by='calculated_valor_pago', ascending=False).head(5)

    df_credor_empenhado = dados_concat.groupby('descricao_nome_credor')['calculated_valor_empenhado'].sum().reset_index()
    df_credor_empenhado = df_credor_empenhado.sort_values(by='calculated_valor_empenhado', ascending=False).head(5)

    df_tipo_objeto = dados_concat.groupby('tipo_objeto')['calculated_valor_empenhado'].sum().reset_index()
    df_tipo_objeto = df_tipo_objeto.sort_values(by='calculated_valor_empenhado', ascending=False)

    df_valor_contrato = dados_concat.groupby('descricao_nome_credor')['valor_contrato'].sum().reset_index()
    df_valor_contrato = df_valor_contrato.sort_values(by='valor_contrato', ascending=False).head(5)


    df_tipo = dados_concat['descricao_tipo'].value_counts().reset_index()
    df_tipo.columns = ['descricao_tipo', 'count']
 
    credor_por_gestor = dados_concat.groupby('gestor_contrato')['descricao_nome_credor'].nunique().reset_index()
    credor_por_gestor = credor_por_gestor.sort_values(by='descricao_nome_credor', ascending=False).head(5)

    col1, col2 = st.columns(2)
    col3 = st.columns(1)
    col4, col5 = st.columns(2)
    col6 = st.columns(1)
    col9, col8 = st.columns(2)

    # Gráfico de maiores valores empenhados por credor
    fig_empenhado = px.bar(df_credor_empenhado, x='descricao_nome_credor', y='calculated_valor_empenhado',
                           color='descricao_nome_credor', title='Top 5 maiores valores empenhados por credor',
                           text='calculated_valor_empenhado')
    fig_empenhado.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col1.plotly_chart(fig_empenhado)

    # Gráfico de maiores valores pagos por credor
    fig_pago = px.bar(df_credor_pago, x='descricao_nome_credor', y='calculated_valor_pago',
                      color='descricao_nome_credor', title='Top 5 maiores valores pagos por credor',
                      text='calculated_valor_pago')
    fig_pago.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col2.plotly_chart(fig_pago)

    # Gráfico de valor por tipo de contrato
    fig_contract = px.bar(dados_concat, x='contract_type', y='valor_contrato', 
                      title='Valor por tipo de contrato', 
                      text=dados_concat['valor_contrato'], 
                      color='contract_type',
                      color_discrete_sequence=px.colors.qualitative.Plotly) 
    fig_contract.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col4.plotly_chart(fig_contract)

    # Gráfico de valor por tipo de objeto nos 5 maiores contratos
    fig_objeto = px.bar(df_tipo_objeto, x='tipo_objeto', y='calculated_valor_empenhado',
                           color='tipo_objeto', title='Top 5 maiores valores empenhados por objeto',
                           text='calculated_valor_empenhado')
    fig_objeto.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col3[0].plotly_chart(fig_objeto)

    # Gráfico de porcentagem de tipos de contrato
    contagem = dados_concat['contract_type'].value_counts()
    porcentagem = contagem / contagem.sum() * 100
    cores = px.colors.qualitative.Plotly[:len(porcentagem)]
    fig_contagem = px.pie(names=porcentagem.index, values=porcentagem.values, title='Porcentagem de Tipos de Contrato',
                      color_discrete_sequence=cores)
    col5.plotly_chart(fig_contagem)

    #Grafico valor contrato por credor
    fig_valor_contrato = px.bar(df_valor_contrato, x='descricao_nome_credor', y='valor_contrato',
                            color='descricao_nome_credor', title='Top 5 maiores valores de contrato por credor',
                            text='valor_contrato')
    fig_valor_contrato.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col6[0].plotly_chart(fig_valor_contrato)

   # Gráfico de quantidade de contratos por tipo
    fig_tipo = px.bar(df_tipo, x='descricao_tipo', y='count',
                    title='Quantidade de contratos por tipo',
                    text='count',color='descricao_tipo', color_discrete_sequence=cores)
    fig_tipo.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col8.plotly_chart(fig_tipo)

    #Gráfico de Quantidade de Credores por Gestor de Contrato
    fig_credor_gestor = px.bar(credor_por_gestor, x='gestor_contrato', y='descricao_nome_credor',
                           title='Quantidade de credores por gestor de contrato',
                           text='descricao_nome_credor')
    fig_credor_gestor.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    col9.plotly_chart(fig_credor_gestor)

    return fig_empenhado, fig_pago, fig_contract, fig_objeto, fig_contagem, fig_valor_contrato, fig_credor_gestor, fig_tipo


# Função para enviar email com gráficos anexados
def enviar_email(email_destinatario, figuras):
    # Configurações do servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'seu email'
    smtp_password = 'senha'

    # Criação do email
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email_destinatario
    msg['Subject'] = 'Relatório de gráficos'

    # Corpo do email
    body = "Segue em anexo o relatório com os gráficos gerados."
    msg.attach(MIMEText(body, 'plain'))

    # Salvando figuras localmente
    paths = []
    for i, fig in enumerate(figuras):
        path = f"figura_{i}.png"
        fig.write_image(path)
        paths.append(path)

    # Anexando figuras ao email
    for path in paths:
        with open(path, 'rb') as fp:
            img = MIMEImage(fp.read())
            img.add_header('Content-Disposition', 'attachment', filename=path)
            msg.attach(img)

    # Envio do email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email_destinatario, msg.as_string())
        st.success("Email enviado com sucesso!")
    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")

# Função principal do Streamlit
def main():
    st.title('Consulta de Convênios e Contratos')

    # Opções de período
    option = st.sidebar.selectbox(
        'Selecione o período:',
        ('Dia atual', 'Últimos 15 dias', 'Últimos 30 dias', 'Últimos 180 dias', 'Último ano')
    )

    # Mapeamento das opções para números
    option_map = {
        'Dia atual': 1,
        'Últimos 15 dias': 2,
        'Últimos 30 dias': 3,
        'Últimos 180 dias': 4,
        'Último ano': 5
    }

    try:
        data_inicio, data_fim = obter_data_formatada(option_map[option])

        # Consulta de convênios
        url_convenios = f'https://api-dados-abertos.cearatransparente.ce.gov.br/transparencia/contratos/convenios?page=1&data_assinatura_inicio={data_inicio}&data_assinatura_fim={data_fim}'
        convenios = consultar_dados(url_convenios)

        # Consulta de contratos
        url_contratos = f'https://api-dados-abertos.cearatransparente.ce.gov.br/transparencia/contratos/contratos?page=1&data_assinatura_inicio={data_inicio}&data_assinatura_fim={data_fim}'
        contratos = consultar_dados(url_contratos)

        df_contratos = pd.DataFrame(contratos)
        df_convenios = pd.DataFrame(convenios)

        # Verifica se há dados nos DataFrames antes de continuar
        if not df_contratos.empty or not df_convenios.empty:
            # Concatenação dos DataFrames
            dados_concat = pd.concat([df_contratos, df_convenios], ignore_index=True)

            # Verificando se a coluna 'descricao_nome_credor' existe
            if 'descricao_nome_credor' in dados_concat.columns:
                # Selecionando colunas necessárias
                dados_concat = dados_concat[['valor_contrato', 'calculated_valor_pago', 'calculated_valor_empenhado', 'descricao_modalidade', 'descricao_tipo', 'contract_type', 'descricao_nome_credor', 'gestor_contrato', 'data_inicio', 'tipo_objeto']]
                
                dados_concat['calculated_valor_empenhado'] = pd.to_numeric(dados_concat['calculated_valor_empenhado'], errors='coerce')
                dados_concat['calculated_valor_pago'] = pd.to_numeric(dados_concat['calculated_valor_pago'], errors='coerce')
                dados_concat['valor_contrato'] = pd.to_numeric(dados_concat['valor_contrato'], errors='coerce')
                dados_concat['data_inicio'] = pd.to_datetime(dados_concat['data_inicio'], errors='coerce')

                # Inserir dados no banco
                inserir_dados_banco(dados_concat)

                # Gerar gráficos
                fig_empenhado, fig_pago, fig_contract, fig_objeto, fig_contagem, fig_valor_contrato, fig_credor_gestor, fig_tipo = gerar_graficos(dados_concat)

                # Botão para enviar email
                if st.button('Enviar email com os gráficos'):
                    # Aqui, passamos todos os gráficos como uma lista/tupla para a função enviar_email
                    email_destinatario = 'kmk.052006@gmail.com'  # Email destinatário já pré-definido
                    enviar_email(email_destinatario, [fig_empenhado, fig_pago, fig_contract, fig_objeto, fig_contagem, fig_valor_contrato, fig_credor_gestor, fig_tipo])
            else:
                st.error("A coluna 'descricao_nome_credor' não está presente nos dados.")
        else:
            st.warning("Não há dados suficientes para gerar gráficos.")
    except ValueError as e:
        st.error(e)

if __name__ == "__main__":
    main()
