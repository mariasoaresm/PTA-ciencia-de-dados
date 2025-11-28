import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool

load_dotenv()

LIFESTYLE_INSTRUCTIONS = """
Você é o 'agent_lifestyle', especialista em Beleza, Saúde, Moda e Lazer.
Sua missão é focar na experiência de uso, segurança e validade.

FERRAMENTAS:
1. USE 'dw_query_tool' para preços e disponibilidade.
2. USE 'rag_search_tool' para composição, contraindicações (bulas) e guias de tamanho.

REGRAS DE RESPOSTA:
- Responda estritamente em JSON.
- Se for saúde/beleza, priorize avisos de segurança.
- Formato obrigatório JSON (igual ao padrão do sistema).
"""

lifestyle_agent = Agent(
    name="Lifestyle Agent",
    role="Especialista em Lifestyle e Saúde",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DWQueryTool(), RAGSearchTool()],
    instructions=LIFESTYLE_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True
)