"""
Streamlit web interface for duck-console
"""
import os
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from duck_console.core.duck_engine import DuckEngine
from duck_console.core.file_reader import read_csv
from duck_console.utils.io_helpers import sanitize_table_name


def init_session_state():
    """Initialize Streamlit session state"""
    if 'engine' not in st.session_state:
        os.makedirs('data', exist_ok=True)
        st.session_state.engine = DuckEngine('data/database.duckdb')


def render_table_list():
    """Render list of available tables"""
    st.header("📊 Tabelas Disponíveis")

    table_names = st.session_state.engine.get_table_names()
    if not table_names:
        st.info("Nenhuma tabela carregada ainda")
        return

    for table in table_names:
        with st.expander(f"📋 {table}"):
            info = st.session_state.engine.get_table_info(table)
            st.dataframe(
                st.session_state.engine.get_table_schema(table),
                use_container_width=True
            )
            st.caption(f"Total de registros: {info.row_count:,}")


def handle_file_upload():
    """Handle file upload in sidebar"""
    with st.sidebar:
        st.header("📁 Importar Dados")

        uploaded_file = st.file_uploader(
            "Escolha um arquivo CSV/TXT", 
            type=['csv', 'txt']
        )

        if uploaded_file is not None:
            default_name = sanitize_table_name(uploaded_file.name)
            table_name = st.text_input("Nome da tabela", value=default_name)

            if st.button("Carregar Arquivo", type="primary"):
                try:
                    df = read_csv(uploaded_file)
                    info = st.session_state.engine.create_table_from_df(table_name, df)
                    st.success(f"✅ Tabela '{table_name}' criada com sucesso!")
                    st.info(
                        f"📊 {info.row_count:,} linhas x {len(info.columns)} colunas"
                    )
                except Exception as e:
                    st.error(f"❌ Erro ao carregar arquivo: {str(e)}")


def render_query_editor():
    """Render SQL query editor section"""
    st.header("💻 Editor SQL")

    query = st.text_area(
        "Digite sua consulta SQL:",
        height=150,
        placeholder="SELECT * FROM sua_tabela LIMIT 10;",
        help="Execute queries SQL diretamente no DuckDB"
    )

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        execute = st.button("▶️ Executar Query", type="primary")
    with col2:
        clear = st.button("🗑️ Limpar")

    if execute and query:
        try:
            result = st.session_state.engine.execute_query(query)
            st.success(f"✅ Query executada com sucesso! ({len(result):,} linhas)")

            st.markdown("---")
            st.header("📈 Resultados")
            st.dataframe(result, use_container_width=True)

            col_exp1, col_exp2, col_exp3 = st.columns([1, 1, 4])
            with col_exp1:
                csv = result.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Exportar CSV",
                    data=csv,
                    file_name="resultado.csv",
                    mime="text/csv",
                )

            with col_exp2:
                if st.button("📊 Estatísticas"):
                    st.subheader("Estatísticas descritivas")
                    st.dataframe(result.describe(), use_container_width=True)

        except Exception as e:
            st.error("❌ Erro na execução da query:")
            st.code(str(e))

    if clear:
        st.rerun()


def show_sql_examples():
    """Show SQL example queries"""
    with st.expander("💡 Exemplos de Queries SQL"):
        st.markdown("""
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
        SHOW TABLES;
        ```
        """)


def main():
    """Main Streamlit app"""
    st.set_page_config(
        page_title="Duck Console",
        page_icon="🦆",
        layout="wide"
    )

    st.title("🦆 Duck Console")
    st.markdown("**Console SQL interativo com DuckDB**")
    st.markdown("---")

    init_session_state()
    handle_file_upload()
    st.markdown("---")
    render_table_list()
    render_query_editor()
    show_sql_examples()

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
            <small>Duck Console | Powered by DuckDB + Streamlit 🦆</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()