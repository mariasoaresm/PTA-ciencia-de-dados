import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
# Removemos LoggerTool daqui, ele será chamado apenas pelo Orquestrador (Team)
from app.tools import DWQueryTool, RAGSearchTool, LoggerTool 

load_dotenv()

# --- Em app/agents/tech_auto.py ---

TECH_CATEGORIES = [
    "informatica_acessorios", "pcs", "pc_gamer", "eletronicos",
    "consoles_games", "automotivo", "telefonia", "agro_industria_e_comercio"
]

TECH_INSTRUCTIONS = f"""
Você é o 'agent_tech_auto', Engenheiro Especialista em Tecnologia.

PROTOCOLO RÍGIDO DE EXECUÇÃO:
1. ANÁLISE: Identifique a intenção (Preço? Specs? MÁXIMO/MÍNIMO?).
2. MAPEAMENTO: Se o usuário usar um termo geral como 'computação' ou 'eletrônicos', traduza-o para as categorias exatas: {', '.join(TECH_CATEGORIES)}.
3. COLETA DE DADOS:
   - Use 'get_max_min_info' quando o usuário perguntar por "mais pesado" (use atributo 'weight') ou "mais caro" (use 'price').
   - Use 'get_avg_price_by_category' para preços médios.
4. AUDITORIA (OBRIGATÓRIO):
   - Chame `log_execution` antes de responder, passando a lista de fontes.

FALLBACK:
Se o DW retornar NOT_FOUND, informe ao usuário a lista de categorias válidas.
"""

tech_auto_agent = Agent(
    name="Tech & Auto Agent",
    role="Especialista Sênior em Tecnologia",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DWQueryTool(), RAGSearchTool(), LoggerTool()], 
    instructions=TECH_INSTRUCTIONS,
    markdown=True,
    show_tool_calls=True,
    add_history_to_messages=True
)