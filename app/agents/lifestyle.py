import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool, LoggerTool

load_dotenv()

# 1. Definição explícita das categorias para ajudar no filtro SQL correto
LIFESTYLE_CATEGORIES = [
    "beleza_saude", "bebes", "esporte_lazer", "perfumaria", 
    "pet_shop", "brinquedos", "relogios_presentes",
    "fashion_bolsas_e_acessorios", "fashion_calcados"
]

# 2. Instruções atualizadas com f-string para incluir as categorias
LIFESTYLE_INSTRUCTIONS = f"""
Você é o 'agent_lifestyle', Especialista em Saúde, Moda e Bem-Estar.

FERRAMENTAS:
- Use `run_sql_query` para buscar preços, marcas e pesos.
- Use `rag_search_tool` para buscar composição, contraindicações (bulas) e guias (PDFs).
- Use `log_execution` para auditoria obrigatória.

DIRETRIZES SQL:
- Tabela `products`: category, weight_g.
- Tabela `items`: price.
- SEMPRE filtre pela categoria mais provável para evitar resultados errados.
- Suas Categorias: {', '.join(LIFESTYLE_CATEGORIES)}.

EXEMPLOS SQL:
- "Produto mais caro de beleza": SELECT p.product_id, i.price FROM items i JOIN products p ON i.product_id = p.product_id WHERE p.category = 'beleza_saude' ORDER BY i.price DESC LIMIT 1
- "Quantos produtos de esporte?": SELECT COUNT(*) FROM products WHERE category = 'esporte_lazer'
"""

lifestyle_agent = Agent(
    name="Lifestyle Agent",
    role="Especialista em Lifestyle e Saúde",
    model=Groq(id="llama-3.3-70b-versatile", api_key=""),
    tools=[DWQueryTool(), RAGSearchTool(), LoggerTool()], 
    instructions=LIFESTYLE_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True,
    add_history_to_messages=True
)