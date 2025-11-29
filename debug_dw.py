import duckdb
import os

# Nomes dos arquivos (exatamente como estão na sua pasta)
FILE_PROD = "produtos_tratados.csv"
FILE_ITEMS = "itens_pedidos_tratados.csv"

print("--- 1. VERIFICAÇÃO DE ARQUIVOS ---")
if os.path.exists(FILE_PROD):
    print(f"✅ {FILE_PROD} encontrado.")
else:
    print(f"❌ {FILE_PROD} NÃO encontrado!")

if os.path.exists(FILE_ITEMS):
    print(f"✅ {FILE_ITEMS} encontrado.")
else:
    print(f"❌ {FILE_ITEMS} NÃO encontrado!")

print("\n--- 2. TESTE DE LEITURA (DuckDB) ---")
try:
    con = duckdb.connect(database=':memory:')
    
    # Tenta ler as colunas para ver como o DuckDB está interpretando os tipos
    print(f"Lendo esquema de {FILE_ITEMS}...")
    schema = con.sql(f"DESCRIBE SELECT * FROM read_csv_auto('{FILE_ITEMS}')").fetchall()
    
    # Procura a coluna 'price' para ver o tipo dela
    price_col = [col for col in schema if col[0] == 'price'][0]
    print(f"ℹ️ A coluna 'price' foi lida como: {price_col[1]}")
    
    if price_col[1] == 'VARCHAR':
        print("⚠️ ALERTA: O preço está como TEXTO. Precisamos converter (tratar vírgula/ponto).")
    elif price_col[1] == 'DOUBLE' or price_col[1] == 'BIGINT':
        print("✅ O preço já é número. O erro não é de tipo.")

    print("\n--- 3. TESTE DA QUERY REAL ---")
    # A query exata que o agente tenta fazer
    query = f"""
        SELECT 
            p.product_id,
            p.product_category_name,
            AVG(TRY_CAST(REPLACE(i.price, ',', '.') AS DOUBLE)) as avg_price,
            COUNT(i.order_id) as total_sales
        FROM read_csv_auto('{FILE_PROD}') p
        JOIN read_csv_auto('{FILE_ITEMS}') i ON p.product_id = i.product_id
        WHERE lower(p.product_category_name) LIKE '%telefonia%'
        GROUP BY p.product_id, p.product_category_name
        LIMIT 2
    """
    result = con.execute(query).fetchdf()
    print("✅ Query executada com sucesso!")
    print(result)

except Exception as e:
    print(f"\n❌ ERRO FATAL NO DUCKDB:\n{e}")