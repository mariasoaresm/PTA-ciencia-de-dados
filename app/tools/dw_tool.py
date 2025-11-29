import duckdb
import json
import os
from typing import Optional
from agno.tools import Toolkit

class DWQueryTool(Toolkit):
    def __init__(self):
        super().__init__(name="dw_query_tool")
        
        # 1. Configuração de Caminhos
        current_file = os.path.abspath(__file__)
        app_dir = os.path.dirname(os.path.dirname(current_file))
        project_root = os.path.dirname(app_dir)
        
        self.files = {
            "products": os.path.join(project_root, "produtos_tratados.csv").replace("\\", "/"),
            "items": os.path.join(project_root, "itens_pedidos_tratados.csv").replace("\\", "/"),
            "orders": os.path.join(project_root, "pedidos_tratados.csv").replace("\\", "/"),
            "sellers": os.path.join(project_root, "vendedores_tratados.csv").replace("\\", "/")
        }

        self.register(self.get_database_schema)
        self.register(self.run_sql_query)

    def _get_connection(self):
        """
        Cria conexão DuckDB com tratamento robusto de números (Ponto ou Vírgula).
        """
        con = duckdb.connect(database=':memory:')
        
        # PRODUTOS - Tratamento Híbrido: Troca vírgula por ponto, mas mantém ponto se já existir.
        con.execute(f"""
            CREATE OR REPLACE VIEW products AS 
            SELECT 
                product_id, 
                product_category_name as category, 
                TRY_CAST(REPLACE(CAST(product_weight_g AS VARCHAR), ',', '.') AS DOUBLE) as weight_g,
                TRY_CAST(REPLACE(CAST(product_length_cm AS VARCHAR), ',', '.') AS DOUBLE) as length_cm,
                TRY_CAST(REPLACE(CAST(product_height_cm AS VARCHAR), ',', '.') AS DOUBLE) as height_cm,
                TRY_CAST(REPLACE(CAST(product_width_cm AS VARCHAR), ',', '.') AS DOUBLE) as width_cm
            FROM read_csv_auto('{self.files['products']}')
        """)

        # ITENS - Tratamento Híbrido para Preço e Frete
        # Se vier "10.50" -> Fica "10.50" (ok)
        # Se vier "10,50" -> Vira "10.50" (ok)
        con.execute(f"""
            CREATE OR REPLACE VIEW items AS 
            SELECT 
                order_id, product_id, seller_id,
                TRY_CAST(REPLACE(CAST(price AS VARCHAR), ',', '.') AS DOUBLE) as price,
                TRY_CAST(REPLACE(CAST(freight_value AS VARCHAR), ',', '.') AS DOUBLE) as freight
            FROM read_csv_auto('{self.files['items']}')
        """)

        # PEDIDOS
        con.execute(f"""
            CREATE OR REPLACE VIEW orders AS 
            SELECT 
                order_id, order_status,
                CAST(order_estimated_delivery_date AS DATE) as estimated_date,
                CAST(order_delivered_customer_date AS DATE) as delivered_date,
                (CAST(order_delivered_customer_date AS DATE) - CAST(order_estimated_delivery_date AS DATE)) as delay_days
            FROM read_csv_auto('{self.files['orders']}')
        """)

        # VENDEDORES
        con.execute(f"""
            CREATE OR REPLACE VIEW sellers AS 
            SELECT seller_id, seller_city, seller_state
            FROM read_csv_auto('{self.files['sellers']}')
        """)
        
        return con

    def get_database_schema(self) -> str:
        return """
        ESQUEMA (DUCKDB):
        1. products (product_id, category, weight_g, length_cm)
        2. items (order_id, product_id, seller_id, price, freight)
        3. orders (order_id, order_status, estimated_date, delivered_date, delay_days)
        4. sellers (seller_id, seller_city, seller_state)
        
        NOTA: Colunas numéricas já foram tratadas. Pode fazer SUM, AVG diretamente.
        """

    def run_sql_query(self, query: str) -> str:
        """Executa SQL arbitrário."""
        try:
            con = self._get_connection()
            # print(f"🔍 EXECUTANDO SQL: {query}") # Debug útil
            
            df = con.execute(query).fetchdf()
            
            if df.empty:
                return "A consulta rodou com sucesso mas não retornou resultados."
            
            return df.to_json(orient='records', date_format='iso')

        except Exception as e:
            return f"ERRO SQL: {str(e)}. Verifique a sintaxe e nomes das colunas."