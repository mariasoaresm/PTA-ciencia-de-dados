import duckdb
from agno.tools import Toolkit

class DWQueryTool(Toolkit):
    def __init__(self):
        super().__init__(name="dw_query_tool")

        # 1. Cria um banco de dados na memória (RAM)
        self.con = duckdb.connect(database=':memory:')

        # 2. Carrega os CSVs como se fossem tabelas de banco
        try:
            # O DuckDB lê direto do arquivo na raiz
            self.con.execute("""
                CREATE TABLE produtos AS SELECT * FROM 'DataLake_tratado - produtos_tratados.csv';
                CREATE TABLE pedidos AS SELECT * FROM 'DataLake_tratado - pedidos_tratados.csv';
                CREATE TABLE itens AS SELECT * FROM 'DataLake_tratado - itens_pedidos_tratados.csv';
                CREATE TABLE vendedores AS SELECT * FROM 'DataLake_tratado - vendedores_tratados.csv';
            """)
            print("✅ [DWQueryTool] Sucesso: Tabelas produtos, pedidos, itens e vendedores carregadas.")
        except Exception as e:
            print(f"❌ [DWQueryTool] Erro Crítico: Não encontrei os CSVs na raiz do projeto. Detalhe: {e}")

        self.register(self.run_query)

    def run_query(self, query: str) -> str:
        """
        Executa uma consulta SQL nas tabelas da O-Market (produtos, pedidos, itens, vendedores).
        
        REGRAS PARA O AGENTE (Zero Invenção):
        1. Use esta ferramenta para buscar qualquer dado numérico, data ou status.
        2. Se a consulta retornar 0 linhas, responda "Dado não encontrado". NÃO INVENTE VALORES.
        
        Args:
            query (str): A query SQL válida (ex: SELECT price FROM itens WHERE product_id = '123')
            
        Returns:
            str: O resultado da consulta em formato de tabela texto.
        """

        try:
            # Limpa formatação que a IA possa ter adicionado
            clean_query = query.replace("```sql", "").replace("```", "").strip()

            # Executa a query no DuckDB
            df_result = self.con.execute(clean_query).df()

            # Trava de Segurança: Se não achar nada, avisa explicitamente
            if df_result.empty:
                return "RESULTADO: 0 linhas encontradas. (O dado não existe na planilha)"
            
            # Retorna o dado real formatado
            return df_result.to_markdown(index=False)
        
        except Exception as e:
            return f"ERRO na execução do SQL: {e}"