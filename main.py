import streamlit as st
import duckdb
import pandas as pd
from io import StringIO
import os

# =====================================
# Configuração da página
# =====================================
st.set_page_config(
    page_title="Duck Console Web",
    page_icon="🦆",
    layout="wide"
)

# =====================================
# Cabeçalho
# =====================================
st.title("🦆 Duck Console Web")
st.markdown("**Console SQL interativo com DuckDB**")
st.markdown("---")

# =====================================
# Inicializar conexão DuckDB
# =====================================
if 'conn' not in st.session_state:
    os.makedirs('data', exist_ok=True)
    st.session_state.conn = duckdb.connect('data/database.duckdb')
    st.session_state.tables = []

# =====================================
# Sidebar - Upload de Arquivos
# =====================================
with st.sidebar:
    st.header("📁 Importar Dados")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])

    if uploaded_file is not None:
        table_name = st.text_input(
            "Nome da tabela",
            value=uploaded_file.name.replace('.csv', '').replace('-', '_').replace(' ', '_')
        )

        if st.button("Carregar CSV", type="primary"):
            try:
                # Ler CSV
                df = pd.read_csv(uploaded_file)

                # Criar ou substituir tabela no DuckDB
                st.session_state.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                st.session_state.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

                # Atualizar lista de tabelas
                if table_name not in st.session_state.tables:
                    st.session_state.tables.append(table_name)

                st.success(f"✅ Tabela '{table_name}' criada com sucesso!")
                st.info(f"📊 {len(df)} linhas x {len(df.columns)} colunas")

            except Exception as e:
                st.error(f"❌ Erro ao carregar CSV: {str(e)}")

st.markdown("---")

# =====================================
# Listar tabelas disponíveis
# =====================================
st.header("📊 Tabelas Disponíveis")

try:
    tables_df = st.session_state.conn.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='main'
    """).fetchdf()

    if not tables_df.empty:
        for table in tables_df['table_name']:
            with st.expander(f"📋 {table}"):
                # Mostrar schema
                schema = st.session_state.conn.execute(f"DESCRIBE {table}").fetchdf()
                st.dataframe(schema, use_container_width=True)

                # Contagem de registros
                count = st.session_state.conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()[0]
                st.caption(f"Total de registros: {count}")
    else:
        st.info("Nenhuma tabela carregada ainda")

except Exception:
    st.warning("Aguardando primeira tabela...")

# =====================================
# Área principal - Editor SQL
# =====================================
st.header("💻 Editor SQL")

query = st.text_area(
    "Digite sua consulta SQL:",
    height=150,
    placeholder="SELECT * FROM sua_tabela LIMIT 10;",
    help="Execute queries SQL diretamente no DuckDB"
)

# Botões de ação
col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    execute_button = st.button("▶️ Executar Query", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Limpar", use_container_width=True)

# =====================================
# Execução da Query
# =====================================
if execute_button and query:
    try:
        result = st.session_state.conn.execute(query).fetchdf()
        st.success(f"✅ Query executada com sucesso! ({len(result)} linhas retornadas)")

        st.markdown("---")
        st.header("📈 Resultados")
        st.dataframe(result, use_container_width=True, height=400)

        # Botões adicionais
        col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 4])
        with col_exp1:
            csv = result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar CSV",
                data=csv,
                file_name="resultado.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_exp2:
            if st.button("📊 Estatísticas", use_container_width=True):
                st.subheader("Estatísticas descritivas")
                st.dataframe(result.describe(), use_container_width=True)

    except Exception as e:
        st.error("❌ Erro na execução da query:")
        st.code(str(e), language="text")

if clear_button:
    st.rerun()

# =====================================
# Rodapé
# =====================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>Duck Console Web | Powered by Streamlit + DuckDB + Pandas 🦆</small>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# Exemplos de Queries
# =====================================
with st.expander("💡 Exemplos de Queries SQL"):
    st.markdown(
        """
        ```sql
        -- Selecionar todos os dados
        SELECT * FROM sua_tabela LIMIT 10;

        -- Agregações
        SELECT coluna1, COUNT(*), AVG(coluna2)
        FROM sua_tabela
        GROUP BY coluna1;

        -- Filtros
        SELECT * FROM sua_tabela
        WHERE coluna1 > 100
        ORDER BY coluna2 DESC;

        -- Join entre tabelas
        SELECT a.*, b.coluna
        FROM tabela1 a
        JOIN tabela2 b ON a.id = b.id;

        -- Listar todas as tabelas
        SHOW TABLES;```
        """)