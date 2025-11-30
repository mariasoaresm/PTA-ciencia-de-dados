import os
from dotenv import load_dotenv
from agno.team import Team
from agno.models.groq import Groq
from app.tools import LoggerTool

# Importa agentes especialistas
from .tech_auto import tech_auto_agent
from .home_decorations import home_decorations_agent
from .lifestyle import lifestyle_agent
from .bi_analyst import bi_analyst_agent  # <--- MUDANÇA 2: Importar o BI

load_dotenv()

# Ajuste fino nas instruções para evitar loop de "quem faz o log"
TEAM_INSTRUCTIONS = """
Você é o ORQUESTRADOR do sistema O-Market.
Sua função é APENAS rotear a pergunta para o especialista correto.

REGRA DE OURO: VOCÊ NÃO TEM FERRAMENTAS DE DADOS. NUNCA TENTE CHAMAR 'get_...' DIRETAMENTE.
SEMPRE DELEGUE A TAREFA PARA O AGENTE ESPECIALISTA.

ROTEAMENTO DE TAREFAS:
1. PERGUNTAS DE NEGÓCIO (Atrasos, Prazos, Fretes, Cancelamentos, KPIs, SQL):
   - AÇÃO: Chame o agente **'BI Analyst'**.
   - EXEMPLO: "Quais categorias atrasam?", "Total de vendas", "Frete médio".

2. PERGUNTAS DE PRODUTO (Specs, Preço unitário, Material, Peso, Garantia):
   - Tecnologia/Auto -> Delegue para **'Tech & Auto Agent'**.
   - Casa/Decoração -> Delegue para **'Home & Decor Agent'**.
   - Saúde/Moda -> Delegue para **'Lifestyle Agent'**.

AUDITORIA FINAL:
- Os especialistas JÁ FAZEM o log individual.
- Sua única tarefa é consolidar a resposta e apresentá-la ao usuário.
- Use `log_execution` APENAS para registrar a *sua* decisão de roteamento.
"""

team = Team(
    name="O-Market Orchestrator",
    # MUDANÇA 3: Configuração correta do Gemini
    model=Groq(id="llama-3.3-70b-versatile", api_key=""),
    members=[bi_analyst_agent, tech_auto_agent, home_decorations_agent, lifestyle_agent],
    tools=[LoggerTool()], 
    instructions=TEAM_INSTRUCTIONS,
    show_members_responses=True, 
    markdown=True
)