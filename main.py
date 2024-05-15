import streamlit as st
import pandas as pd

def verifica_nativa(especies, arquivo_excel):
    try:
        # Carrega o arquivo Excel
        df = pd.read_excel(arquivo_excel)
        
        # Cria uma lista de resultados para cada espécie
        resultados = []
        for especie in especies:
            if especie.lower() in df['Espécie'].str.strip().str.lower().tolist():
                resultados.append(df.loc[df['Espécie'].str.strip().str.lower() == especie.lower(), 'Nativo'].iloc[0])
            else:
                resultados.append("Não encontrado")
        
        return resultados
    except Exception as e:
        return [f"Erro ao ler arquivo: {e}"] * len(especies)

def verificar_por_planilha(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file, encoding='latin1')

            st.write("Exibindo as primeiras linhas do arquivo:")
            st.write(df.head())

            if 'Espécie' in df.columns:
                especies = df['Espécie'].str.strip().tolist()
                resultados = verifica_nativa(especies, 'especie_base.xlsx')
                df['Nativo'] = resultados
                st.write("### Resultado:")
                # Configura a tabela para ser responsiva e ajustável
                st.dataframe(df, height=min(len(df) * 25, 800), width=1000)
            else:
                st.error("O arquivo não possui uma coluna 'Espécie'.")

        except Exception as e:
            st.error(f"Ocorreu um erro ao ler o arquivo: {e}")

def verificar_por_digitacao():
    st.write("### Verificar por Digitação")
    especies_input = st.text_input("Digite as espécies separadas por vírgula:")
    especies = [especie.strip() for especie in especies_input.split(',')] if especies_input else []
    if especies:
        # Limpa os espaços em branco e remove aspas extras de nomes de espécies com mais de uma palavra
        especies = [especie.strip().replace("'", "").replace('"', '') for especie in especies]
        resultados = verifica_nativa(especies, 'especie_base.xlsx')
        for especie, resultado_especie in zip(especies, resultados):
            st.write(f"A espécie '{especie}' é nativa? {resultado_especie}")
    else:
        st.warning("Digite pelo menos uma espécie para verificar.")

def main():
    st.title("Verificador de Espécies Nativas")
    st.write("Selecione como deseja verificar as espécies:")

    # Adiciona um menu suspenso na barra lateral para o usuário selecionar a opção desejada
    opcao = st.sidebar.selectbox("Selecione uma opção:", ("Verificar por Planilha", "Verificar por Digitação"))

    # Se a opção escolhida for "Verificar por Planilha", exibe o campo de upload de arquivo
    if opcao == "Verificar por Planilha":
        uploaded_file = st.sidebar.file_uploader("Faça o upload do arquivo", type=['csv', 'xlsx'])
        verificar_por_planilha(uploaded_file)
    # Se a opção escolhida for "Verificar por Digitação", chama a função correspondente
    elif opcao == "Verificar por Digitação":
        verificar_por_digitacao()

if __name__ == "__main__":
    main()
