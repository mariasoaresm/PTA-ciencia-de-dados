import duckdb
import json
import os
from typing import List, Optional, Dict, Any, Union
from agno.tools import Toolkit

class DWQueryTool(Toolkit):
    def __init__(self):
        super().__init__(name="dw_query_tool")
        
        # Define o caminho absoluto (Robustez de Path)
        base_path = os.getcwd()
        if base_path.endswith("app") or base_path.endswith("tools"):
            base_path = os.path.dirname(os.path.dirname(base_path))
            
        self.products_csv = os.path.join(base_path, "produtos_tratados.csv")
        self.items_csv = os.path.join(base_path, "itens_pedidos_tratados.csv")
        self.orders_csv = os.path.join(base_path, "pedidos_tratados.csv")
        self.sellers_csv = os.path.join(base_path, "vendedores_tratados.csv")

        self.register(self.get_product_specs_by_id)
        self.register(self.get_avg_price_by_category)
        self.register(self.get_max_min_info) # Corrige o erro "Mais Pesado"
        self.register(self.get_avg_freight_by_product) # Capacidade Futura

    def _check_files(self, required_files: List[str]) -> Optional[str]:
        """Verifica se todos os arquivos requeridos pela query existem."""
        for filename in required_files:
            if filename == self.products_csv and not os.path.exists(filename): return f"Arquivo ausente: {os.path.basename(filename)}"
            if filename == self.items_csv and not os.path.exists(filename): return f"Arquivo ausente: {os.path.basename(filename)}"
            if filename == self.orders_csv and not os.path.exists(filename): return f"Arquivo ausente: {os.path.basename(filename)}"
            if filename == self.sellers_csv and not os.path.exists(filename): return f"Arquivo ausente: {os.path.basename(filename)}"
        return None

    def _safe_query(self, query: str, required_files: List[str]) -> Dict[str, Any]:
        """Executa uma query DuckDB com tratamento de exceção defensivo e verifica arquivos."""
        error = self._check_files(required_files)
        if error:
            return {"error": error, "status": "FILE_SYSTEM_ERROR"}
        
        try:
            con = duckdb.connect(database=':memory:')
            result_df = con.execute(query).fetchdf()
            
            if result_df.empty:
                return {"status": "NOT_FOUND", "message": "Nenhum registro encontrado para a consulta."}
            
            # Limpa NaN/None e retorna JSON serializável
            data = result_df.fillna(0).to_dict(orient="records")
            return {"status": "SUCCESS", "data": data}

        except Exception as e:
            error_msg = f"Erro CRÍTICO no DuckDB/SQL: {str(e)}"
            return {"error": error_msg, "status": "DATABASE_ERROR"}

    # --- FUNÇÕES DE BUSCA ---

    def get_avg_price_by_category(self, category_name: str) -> str:
        """Calcula preço médio, resolvendo o erro de AVG(VARCHAR)."""
        # A magia do saneamento de preço
        price_cleaner = "REPLACE(REPLACE(REPLACE(CAST(i.price AS VARCHAR), 'R$', ''), '.', ''), ',', '.') AS DOUBLE"
        
        query = f"""
            SELECT 
                p.product_category_name,
                AVG(TRY_CAST({price_cleaner})) as avg_price,
                COUNT(i.order_id) as total_sales
            FROM read_csv_auto('{self.products_csv}') p
            JOIN read_csv_auto('{self.items_csv}') i ON p.product_id = i.product_id
            WHERE lower(p.product_category_name) LIKE '%{category_name.lower()}%'
            GROUP BY 1
            LIMIT 10
        """
        return json.dumps(self._safe_query(query, [self.products_csv, self.items_csv]), default=str)

    def get_max_min_info(self, attribute: str, mode: str, category_filter: str) -> str:
        """
        RESOLUÇÃO DO ERRO 'MAIS PESADO': Encontra o MAX ou MIN de um atributo em uma categoria.
        """
        attribute = attribute.lower()
        mode = mode.upper()
        
        # 1. TRATAMENTO DO ATRIBUTO
        if attribute == 'price':
            table = self.items_csv
            clean_col = f"TRY_CAST(REPLACE(REPLACE(REPLACE(i.price, 'R$', ''), '.', ''), ',', '.') AS DOUBLE)"
            join_clause = f"JOIN read_csv_auto('{self.products_csv}') p ON p.product_id = i.product_id"
            target_table = "i" # Alias da tabela que tem o preço
        elif attribute == 'weight':
            table = self.products_csv
            clean_col = "TRY_CAST(product_weight_g AS DOUBLE)"
            join_clause = ""
            target_table = "p" # Alias da tabela que tem o peso
        else:
            return json.dumps({"error": f"Atributo desconhecido: {attribute}", "status": "INVALID_INPUT"}, default=str)

        # 2. QUERY SQL
        # NOTA: O WHERE é aplicado no product_category_name que está na tabela de produtos (p)
        query = f"""
            SELECT
                p.product_id, 
                p.product_category_name,
                {clean_col} AS cleaned_value
            FROM read_csv_auto('{self.products_csv}') p
            {join_clause}
            WHERE lower(p.product_category_name) LIKE '%{category_filter.lower()}%'
            ORDER BY cleaned_value {'DESC' if mode == 'MAX' else 'ASC'}
            NULLS LAST
            LIMIT 1
        """
        
        # 3. Execução
        return json.dumps(self._safe_query(query, [self.products_csv, self.items_csv]), default=str)

    def get_avg_freight_by_product(self, product_id: str) -> str:
        """Capacidade futura: Calcula o valor médio do frete para um produto específico."""
        # NOTA: Assumindo que freight_value é DOUBLE ou similar
        query = f"""
            SELECT 
                AVG(freight_value) as avg_freight
            FROM read_csv_auto('{self.items_csv}')
            WHERE product_id = '{product_id}'
        """
        return json.dumps(self._safe_query(query, [self.items_csv]), default=str)

    def get_product_specs_by_id(self, product_id: str) -> str:
        """Busca specs por ID."""
        query = f"""
            SELECT product_id, product_category_name, product_weight_g, 
                   product_length_cm, product_height_cm, product_width_cm
            FROM read_csv_auto('{self.products_csv}')
            WHERE product_id = '{product_id}'
        """
        return json.dumps(self._safe_query(query, [self.products_csv]), default=str)