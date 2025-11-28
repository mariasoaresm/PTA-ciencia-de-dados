import os
from dotenv import load_dotenv
from agno.team import Team
from agno.models.groq import Groq

# importa a ferramenta de logging
from app.tools import LoggerTool

# importa agentes especialistas
from .tech_auto import tech_auto_agent
from .home_decorations import home_decorations_agent
from .lifestyle import lifestyle_agent

load_dotenv()

# instruções para o orquestrador
TEAM_INSTRUCTIONS = """
Você é o ORQUESTRADOR do sistema O-Market.
Sua função NÃO é responder a pergunta diretamente, mas sim IDENTIFICAR a intenção e DELEGAR para o agente correto.

Regras de Roteamento:
1. Tech & Auto Agent: Para perguntas sobre eletrônicos, computadores, peças automotivas, voltagem e compatibilidade técnica.
2. Home & Decor Agent: Para perguntas sobre móveis, decoração, eletrodomésticos, dimensões de produtos e construção.
3. Lifestyle Agent: Para perguntas sobre saúde, beleza, moda, roupas, brinquedos, lazer e validade de produtos.

Instruções de Saída:
- Os agentes retornarão dados técnicos em JSON.
- Você deve pegar esse JSON e transformar em uma RESPOSTA FINAL AMIGÁVEL em texto (Markdown).
- Sempre mostre as fontes (sources) que o agente utilizou.
"""

team = Team(
    name="O-Market Orchestrator",
    model=Groq(id="llama-3.3-70b-versatile"), # O Team precisa de um modelo para decidir o roteamento
    members=[tech_auto_agent, home_decorations_agent, lifestyle_agent],
    tools=[LoggerTool()], # O Team usa o Logger para registrar o fluxo
    instructions=TEAM_INSTRUCTIONS,
    show_members_responses=True, # Mostra o JSON interno dos agentes no log
    markdown=True
)