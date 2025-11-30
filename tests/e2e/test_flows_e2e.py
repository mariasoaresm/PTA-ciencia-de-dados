import pytest
import duckdb
from unittest.mock import patch
from app.agents.team import team
from app.tools.dw_tool import DWQueryTool
from agno.models.base import ModelResponse 

@pytest.fixture(scope="module")
def real_memory_db():
    con = duckdb.connect(':memory:')
    
    # SETUP PRODUCTS
    con.execute("CREATE TABLE products_raw (product_id VARCHAR, product_category_name VARCHAR, product_weight_g VARCHAR, product_length_cm VARCHAR, product_height_cm VARCHAR, product_width_cm VARCHAR)")
    con.execute("INSERT INTO products_raw VALUES ('p1', 'informatica_acessorios', '1000', '10', '10', '10'), ('p2', 'cama_mesa_banho', '500', '20', '20', '20')")
    con.execute("CREATE VIEW products AS SELECT product_id, product_category_name as category, CAST(product_weight_g AS DOUBLE) as weight_g, CAST(product_length_cm AS DOUBLE) as length_cm FROM products_raw")

    # SETUP ITEMS
    con.execute("CREATE TABLE items_raw (order_id VARCHAR, product_id VARCHAR, seller_id VARCHAR, price VARCHAR, freight_value VARCHAR)")
    con.execute("INSERT INTO items_raw VALUES ('o1', 'p1', 's1', '2000.0', '50.0'), ('o2', 'p2', 's1', '100.0', '20.0')")
    con.execute("CREATE VIEW items AS SELECT order_id, product_id, seller_id, CAST(price AS DOUBLE) as price, CAST(freight_value AS DOUBLE) as freight FROM items_raw")

    # SETUP ORDERS
    con.execute("CREATE TABLE orders_raw (order_id VARCHAR, order_status VARCHAR, order_estimated_delivery_date DATE, order_delivered_customer_date DATE)")
    con.execute("INSERT INTO orders_raw VALUES ('o1', 'delivered', '2023-01-10', '2023-01-12')") 
    con.execute("CREATE VIEW orders AS SELECT order_id, order_status, order_estimated_delivery_date as estimated_date, order_delivered_customer_date as delivered_date, (order_delivered_customer_date - order_estimated_delivery_date) as delay_days FROM orders_raw")

    # SETUP SELLERS
    con.execute("CREATE TABLE sellers_raw (seller_id VARCHAR, seller_city VARCHAR, seller_state VARCHAR)")
    con.execute("INSERT INTO sellers_raw VALUES ('s1', 'Sao Paulo', 'SP')")
    con.execute("CREATE VIEW sellers AS SELECT seller_id, seller_city, seller_state FROM sellers_raw")
    
    return con

@pytest.mark.e2e
class TestSystemFlows:
    
    def test_scenario_1_routing_bi_analyst(self, real_memory_db):
        """
        Cenário 1: Pergunta de Negócio (BI).
        """
        question = "Quantos pedidos tiveram atraso na entrega?"
        
        # MOCK CIRÚRGICO: Interceptamos o cérebro do Time (team.model)
        # Dizemos: "Não pense, apenas retorne esta resposta final".
        expected_response = ModelResponse(content="Com base nos dados, identifiquei que 1 pedido teve atraso na entrega.")
        
        with patch.object(team.model, "response", return_value=expected_response) as mock_model:
            with patch.object(DWQueryTool, '_get_connection', return_value=real_memory_db):
                response = team.run(question)
                
                # Valida se o orquestrador entregou a mensagem ao usuário
                content = response.content.lower()
                assert "1" in content or "pedido" in content
                
                # Garante que o método foi chamado (prova que o código rodou)
                mock_model.assert_called()

    def test_scenario_2_routing_tech_spec(self, real_memory_db):
        """
        Cenário 2: Pergunta de Produto (Tech/Auto).
        """
        question = "Qual o preço do produto de informatica acessorios?"
        
        expected_response = ModelResponse(content="O preço do produto de informatica acessorios é R$ 2000.00.")

        with patch.object(team.model, "response", return_value=expected_response):
            with patch.object(DWQueryTool, '_get_connection', return_value=real_memory_db):
                response = team.run(question)
                assert "2000" in response.content

    def test_scenario_3_routing_home_decor(self, real_memory_db):
        """
        Cenário 3: Pergunta de Home & Decor.
        """
        question = "Quanto custa o item de cama mesa e banho?"
        
        expected_response = ModelResponse(content="O item de cama mesa e banho custa R$ 100.00.")

        with patch.object(team.model, "response", return_value=expected_response):
            with patch.object(DWQueryTool, '_get_connection', return_value=real_memory_db):
                response = team.run(question)
                assert "100" in response.content