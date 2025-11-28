import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from app.tools import DWQueryTool, RAGSearchTool

load_dotenv()

# Instruções copiadas e adaptadas da sua documentação
TECH_INSTRUCTIONS = """
Você é o 'agent_tech_auto', especialista em Tecnologia e Automotivo.
Sua missão é validar especificações técnicas rigorosas (voltagem, compatibilidade, dimensões).

FERRAMENTAS:
1. USE 'dw_query_tool' para buscar dados exatos (preço, dimensões, voltagem) no banco.
2. USE 'rag_search_tool' para buscar em manuais técnicos e verificar compatibilidade.

REGRAS DE RESPOSTA:
- Você DEVE responder estritamente em JSON.
- Se o DW e o RAG divergirem, confie no DW para números e no RAG para instruções de uso.
- Formato obrigatório:
{
  "request_id": "uuid",
  "agent": "agent_tech_auto",
  "response_text": "Texto explicativo aqui...",
  "confidence": 0.95,
  "sources": [{"type": "DW", "ref": "...", "value": "..."}, {"type": "PDF", "ref": "...", "snippet": "..."}]
}
"""

tech_auto_agent = Agent(
    name="Tech & Auto Agent",
    role="Especialista Técnico e Automotivo",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DWQueryTool(), RAGSearchTool()],
    instructions=TECH_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True
)