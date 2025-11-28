import duckdb
import json
import os
from agno.tools import Toolkit

class DWQueryTool(Toolkit):
    def __init__(self):
        super().__init__(name="dw_query_tool")
        # Caminhos dos CSVs (Devem estar na raiz do projeto)
        self.products_csv = "produtos_tratados.csv"
        self.items_csv = "itens_pedidos_tratados.csv"
        
        self.register(self.query_products_by_category)
        self.register(self.get_product_specs_by_id)

    def query_products_by_category(self, category_name: str) -> str:
        """
        Busca produtos por categoria, calculando a média de preço real baseada nos pedidos.
        Útil para responder: "Qual a faixa de preço de produtos de beleza?"
        
        Args:
            category_name (str): Nome da categoria (ex: 'beleza_saude', 'informatica_acessorios', 'moveis_decoracao').
        """
        try:
            if not os.path.exists(self.products_csv) or not os.path.exists(self.items_csv):
                return json.dumps({"error": "Arquivos CSV não encontrados na raiz.", "status": "ERROR"})

            con = duckdb.connect(database=':memory:')
            
            # JOIN PODEROSO: Produtos + Itens (para pegar o preço)
            # Traz o ID, Categoria e a Média de Preço dos itens vendidos
            query = f"""
                SELECT 
                    p.product_id,
                    p.product_category_name,
                    AVG(i.price) as avg_price,
                    COUNT(i.order_id) as total_sales
                FROM read_csv_auto('{self.products_csv}') p
                JOIN read_csv_auto('{self.items_csv}') i ON p.product_id = i.product_id
                WHERE lower(p.product_category_name) LIKE '%{category_name.lower()}%'
                GROUP BY p.product_id, p.product_category_name
                ORDER BY total_sales DESC
                LIMIT 5
            """
            
            result_df = con.execute(query).fetchdf()
            
            if result_df.empty:
                return json.dumps({"status": "NOT_FOUND", "message": f"Nenhuma categoria encontrada parecida com: {category_name}"})
            
            return json.dumps({"status": "SUCCESS", "data": result_df.to_dict(orient="records")}, default=str)

        except Exception as e:
            return json.dumps({"error": str(e), "status": "CRITICAL_ERROR"})

    def get_product_specs_by_id(self, product_id: str) -> str:
        """
        Busca as especificações técnicas exatas (peso, dimensões) de um ID específico.
        Útil para o Agente Técnico validar dados.
        """
        try:
            con = duckdb.connect(database=':memory:')
            
            query = f"""
                SELECT 
                    product_id,
                    product_category_name,
                    product_weight_g,
                    product_length_cm,
                    product_height_cm,
                    product_width_cm,
                    product_description_lenght
                FROM read_csv_auto('{self.products_csv}')
                WHERE product_id = '{product_id}'
            """
            
            result_df = con.execute(query).fetchdf()
            
            if result_df.empty:
                return json.dumps({"status": "NOT_FOUND"})
            
            return json.dumps({"status": "SUCCESS", "specs": result_df.to_dict(orient="records")[0]}, default=str)

        except Exception as e:
            return json.dumps({"error": str(e)})