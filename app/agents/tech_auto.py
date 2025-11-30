import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool, LoggerTool 

load_dotenv()

TECH_CATEGORIES = [
    "informatica_acessorios", "pcs", "pc_gamer", "eletronicos",
    "consoles_games", "automotivo", "telefonia", "agro_industria_e_comercio"
]

TECH_INSTRUCTIONS = f"""
Você é o 'agent_tech_auto', Especialista em Tecnologia.

FERRAMENTAS:
- Use `run_sql_query` para buscar dados técnicos (peso, preço, specs).
- Use `rag_search_tool` para manuais e garantias.
- Use `log_execution` para auditoria.

DIRETRIZES SQL:
- Tabela `products` tem: weight_g (peso), length_cm (tamanho).
- Tabela `items` tem: price (preço).
- Filtre sempre pela categoria correta usando `WHERE category = '...'`.

EXEMPLOS:
- "Mais pesado de telefonia": SELECT product_id, weight_g FROM products WHERE category = 'telefonia' ORDER BY weight_g DESC LIMIT 1
- "Preço médio de pc_gamer": SELECT AVG(price) FROM items i JOIN products p ON i.product_id = p.product_id WHERE p.category = 'pc_gamer'
"""

tech_auto_agent = Agent(
    name="Tech & Auto Agent",
    role="Especialista em Tecnologia",
    model=Groq(id="llama-3.3-70b-versatile", api_key=""),
    tools=[DWQueryTool(), RAGSearchTool(), LoggerTool()], 
    instructions=TECH_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True,
    add_history_to_messages=True
)