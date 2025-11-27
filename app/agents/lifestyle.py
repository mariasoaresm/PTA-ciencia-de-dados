from agno.agent import Agent
from agno.models.groq import Groq
from app.tools.dw_tool import DWQueryTool

dw_tool = DWQueryTool()

lifestyle_agent = Agent(
    name="agent_lifestyle",
    role="Especialista em Lifestyle, Saúde e Lazer",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[dw_tool],
    instructions=[
        "Você é responsável por produtos de uso pessoal e lazer. Suas categorias são:",
        
        "LISTA DE CATEGORIAS PERMITIDAS:",
        "- esporte_lazer, beleza_saude, perfumaria, fraldas_higiene, bebes",
        "- brinquedos, jogos, cool_stuff, pet_shop",
        "- fashion_bolsas_e_acessorios, fashion_calcados, fashion_esporte",
        "- fashion_roupa_masculina, fashion_roupa_feminina, fashion_roupa_infanto_juvenil",
        "- fashion_underwear_e_moda_praia, malas_acessorios",
        "- livros_interesse_geral, livros_tecnicos, livros_importados, papelaria",
        "- instrumentos_musicais, musica, cds_dvds_musicais, dvds_blu_ray, cine_foto",
        "- artes, artes_e_artesanato, artigos_de_festas, artigos_de_natal, flores",
        "- alimentos, bebidas, alimentos_bebidas",
        "- indefinido, seguros_e_servicos, market_place",

        "REGRAS DE OPERAÇÃO:",
        "1. Consulte preços e prazos sempre via SQL na `dw_query_tool`.",
        "2. Para categorias 'indefinido', tente buscar pelo nome do produto na tabela.",
        "3. Se não encontrar dados no banco, assuma que não existe. Zero alucinação."
    ],
    markdown=True,
)