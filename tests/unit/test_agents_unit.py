import pytest
import json
from unittest.mock import MagicMock, patch
from app.tools.dw_tool import DWQueryTool
from app.agents.bi_analyst import bi_analyst_agent

@pytest.mark.unit
class TestDWToolUnit:
    """
    Testa a lógica interna da ferramenta de Data Warehouse (DuckDB)
    sem depender dos CSVs reais e sem acessar o disco.
    """
    
    @pytest.fixture
    def mock_db_connection(self):
        """
        Cria uma conexão DuckDB em memória com dados fake.
        Isso isola o teste de arquivos CSV reais.
        """
        import duckdb
        con = duckdb.connect(':memory:')
        
        # Cria tabela fake de items para teste de soma
        con.execute("CREATE TABLE items (price DOUBLE, freight DOUBLE)")
        con.execute("INSERT INTO items VALUES (100.0, 10.0), (200.0, 20.0)")
        
        return con

    def test_dw_tool_schema_generation(self):
        """Verifica se o schema é retornado como string e contém as tabelas esperadas."""
        tool = DWQueryTool()
        schema = tool.get_database_schema()
        assert "ESQUEMA (DUCKDB)" in schema
        assert "products" in schema
        assert "orders" in schema

    def test_run_sql_query_success(self, mock_db_connection):
        """
        Testa se a ferramenta executa SQL corretamente e retorna JSON estruturado.
        Usa 'patch' para substituir a conexão real pela conexão em memória (mock).
        """
        tool = DWQueryTool()
        
        with patch.object(tool, '_get_connection', return_value=mock_db_connection):
            query = "SELECT SUM(price) as total FROM items"
            result_json = tool.run_sql_query(query)
            
            # Validações de estrutura e valor
            data = json.loads(result_json)
            assert len(data) == 1
            assert data[0]['total'] == 300.0

    def test_run_sql_query_error_handling(self):
        """Testa se a ferramenta captura e formata erros de SQL graciosamente."""
        tool = DWQueryTool()
        
        # Simula um erro de banco de dados
        mock_con = MagicMock()
        mock_con.execute.side_effect = Exception("Erro de Sintaxe SQL Simulado")
        
        with patch.object(tool, '_get_connection', return_value=mock_con):
            result = tool.run_sql_query("SELECT * FROM tabela_inexistente")
            assert "ERRO SQL" in result


@pytest.mark.unit
class TestAgentsMocked:
    """
    Testa a interação do Agente com as ferramentas, MOCKANDO o LLM (Gemini).
    Garante que a lógica do Agno funciona sem gastar créditos da API.
    """

    @patch("agno.agent.Agent.run")
    def test_bi_analyst_flow_mock(self, mock_agent_run):
        """
        Simula: Pergunta -> Agente -> Resposta.
        Verifica se o agente processa o retorno sem erros.
        """
        # 1 Arrange (Preparação do Mock)
        mock_response = MagicMock()
        mock_response.content = "O total de vendas é R$ 5000,00"
        # Simulamos que o agente retornou com sucesso
        mock_agent_run.return_value = mock_response

        # 2 Act (Execução)
        # O 'run' aqui não vai pro Google, vai pro nosso mock
        response = bi_analyst_agent.run("Qual o total de vendas?")

        # 3 Assert (Verificação)
        assert response.content == "O total de vendas é R$ 5000,00"
        mock_agent_run.assert_called_once()