import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool, LoggerTool

load_dotenv()

HOME_CATEGORIES = [
    "moveis_decoracao", "cama_mesa_banho", "utilidades_domesticas", 
    "moveis_escritorio", "ferramentas_jardim", "construcao_ferramentas_construcao",
    "eletrodomesticos"
]

HOME_INSTRUCTIONS = f"""
Você é o 'agent_home_decorations', Arquiteto e Especialista em Casa e Decoração.

FERRAMENTAS:
- Use `run_sql_query` para buscar dados numéricos (Dimensões, Peso, Preço, Frete).
- Use `rag_search_tool` para manuais de montagem e detalhes de material (PDFs).
- Use `log_execution` para auditoria obrigatória.

DIRETRIZES SQL:
- Tabela `products`: weight_g (peso), length_cm/height_cm/width_cm (dimensões).
- Tabela `items`: price (preço).
- Filtre sempre pela categoria correta.
- Categorias do seu setor: {', '.join(HOME_CATEGORIES)}.

EXEMPLOS SQL:
- "Qual a maior mesa?": SELECT product_id, width_cm FROM products WHERE category = 'moveis_decoracao' ORDER BY width_cm DESC LIMIT 1
- "Preço médio de cama_mesa_banho": SELECT AVG(price) FROM items i JOIN products p ON i.product_id = p.product_id WHERE p.category = 'cama_mesa_banho'
"""

home_decorations_agent = Agent(
    name="Home & Decor Agent",
    role="Especialista em Casa e Decoração",
    model=Groq(id="llama-3.3-70b-versatile"), # Modelo atualizado
    tools=[DWQueryTool(), RAGSearchTool(), LoggerTool()], 
    instructions=HOME_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True,
    add_history_to_messages=True
)