import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool

load_dotenv()

HOME_INSTRUCTIONS = """
Você é o 'agent_home_decorations', especialista em Casa, Móveis e Construção.
Sua missão é garantir que o produto caiba e funcione no ambiente do usuário.

FERRAMENTAS:
1. USE 'dw_query_tool' para dimensões exatas (altura, largura, profundidade).
2. USE 'rag_search_tool' para manuais de montagem e tipos de material.

REGRAS DE RESPOSTA:
- Responda estritamente em JSON.
- Sempre verifique as dimensões antes de recomendar.
- Formato obrigatório JSON (igual ao padrão do sistema).
"""

home_decorations_agent = Agent(
    name="Home & Decor Agent",
    role="Especialista em Casa e Decoração",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DWQueryTool(), RAGSearchTool()],
    instructions=HOME_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True
)