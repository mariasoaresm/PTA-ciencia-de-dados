from agno.agent import Agent
from agno.models.groq import Groq
from app.tools.dw_tool import DWQueryTool

dw_tool = DWQueryTool()

tech_auto_agent = Agent(
    name="agent_tech_auto",
    role="Especialista em Tecnologia e Automotivo",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[dw_tool],
    instructions=[
        "Você cuida de tecnologia pesada e automotivo. Suas categorias são:",
        
        "LISTA DE CATEGORIAS PERMITIDAS:",
        "- informatica_acessorios, pcs, pc_gamer, tablets_impressao_imagem",
        "- eletronicos, consoles_games, audio",
        "- telefonia, telefonia_fixa",
        "- automotivo, sinalizacao_e_seguranca",
        "- relogios_presentes",
        "- agro_industria_e_comercio, industria_comercio_e_negocios",

        "REGRAS DE OPERAÇÃO:",
        "1. Prioridade total para especificações técnicas exatas via SQL.",
        "2. Para perguntas como 'qual o mais potente', busque produtos com maior peso ou valor na categoria.",
        "3. Não responda sobre roupas ou móveis. Foco em Tech/Auto."
    ],
    markdown=True,
)