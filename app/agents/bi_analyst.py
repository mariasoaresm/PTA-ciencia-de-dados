import os
from dotenv import load_dotenv
from agno.agent import Agent
# MUDANÇA: Usando Gemini
from agno.models.google import Gemini
from app.tools import DWQueryTool, LoggerTool

load_dotenv()

# Instruções refinadas para evitar erros de SQL em português
BI_INSTRUCTIONS = """
Você é o Analista de Dados Sênior (SQL Expert) da O-Market.
Sua missão é transformar perguntas de negócio em consultas SQL DuckDB.

FERRAMENTAS:
1. `get_database_schema`: Use no início para ver as tabelas (views).
2. `run_sql_query`: Escreva o SQL para responder.
3. `log_execution`: Registre sua análise no final.

SCHEMA SIMPLIFICADO:
- `products`: category, weight_g, length_cm
- `items`: price, freight, seller_id
- `orders`: order_status (valores em PT: 'entregue', 'cancelado'), delay_days
- `sellers`: seller_state, seller_city

ESTRATÉGIA SQL:
- "Qual estado tem frete mais caro?" -> JOIN items + sellers.
- "Taxa de atraso?" -> Contar delay_days > 0 na tabela orders.
- "Total de vendas?" -> SUM(price) na tabela items.

IMPORTANTE:
- Se a pergunta for sobre "atraso", lembre-se que `delay_days > 0` significa atraso.
- Se a pergunta for sobre "frete", use a coluna `freight` da tabela `items`.
"""

bi_analyst_agent = Agent(
    name="BI Analyst",
    role="Analista de Dados SQL",
    model=Gemini(id="gemini-2.5-flash"), # Modelo atualizado
    tools=[DWQueryTool(), LoggerTool()], 
    instructions=BI_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True,
    add_history_to_messages=True
)