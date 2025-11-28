import os
from dotenv import load_dotenv
from agno.team import Team
from agno.models.groq import Groq

# Importa a ferramenta de logging
from app.tools import LoggerTool

# Importa agentes especialistas
from .tech_auto import tech_auto_agent
from .home_decorations import home_decorations_agent
from .lifestyle import lifestyle_agent

load_dotenv()

# AUDITORIA

TEAM_INSTRUCTIONS = """
Você é o ORQUESTRADOR do sistema O-Market.
Sua função é: Delegar, Consolidar e AUDITAR.

[ ... Regras de Roteamento ... ]

⚠️ PROTOCOLO DE AUDITORIA (OBRIGATÓRIO):
Ao finalizar a resposta para o usuário, você DEVE executar a ferramenta `log_execution` (do logger_tool).
Preencha os campos:
- agent_name: "O-Market Orchestrator"
- user_query: A pergunta original do usuário.
- response_text: Sua resposta final consolidada.
- sources: A lista de fontes que o agente especialista retornou (se houver).

Não encerre a conversa sem receber a confirmação de "Log salvo com sucesso".
"""

team = Team(
    name="O-Market Orchestrator",
    model=Groq(id="llama-3.3-70b-versatile"), 
    members=[tech_auto_agent, home_decorations_agent, lifestyle_agent],
    tools=[LoggerTool()], # A ferramenta está aqui
    instructions=TEAM_INSTRUCTIONS, # As novas instruções forçam o uso dela
    show_members_responses=True, 
    markdown=True
)