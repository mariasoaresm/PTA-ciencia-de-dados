from agno.agent import Agent
from agno.models.groq import Groq
from agno.team import Team
from dotenv import load_dotenv
import sys
import os

# Adiciona o diretório raiz ao path para evitar erros de módulo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.agents.home_decoration import home_decor_agent
from app.agents.lifestyle import lifestyle_agent
from app.agents.tech_auto import tech_auto_agent
from app.tools.logger_tool import AuditLogger

load_dotenv()

# --- DEFINIÇÃO DO TIME ---
market_team = Team(
    name="O-Market-Orchestrator",
    
    # AQUI ESTAVA O ERRO: O parâmetro correto nesta versão é 'members'
    members=[home_decor_agent, lifestyle_agent, tech_auto_agent],
    
    model=Groq(id="llama-3.3-70b-versatile"),
    
    instructions=[
        "Você é o Orquestrador de Atendimento da O-Market.",
        "Sua função é: Receber a pergunta do usuário e delegar para o agente especialista correto.",
        "NÃO tente responder perguntas sobre produtos, estoques ou preços você mesmo. Delegue.",
        
        "🧠 REGRAS DE ROTEAMENTO:",
        "1. Se o assunto for MÓVEIS, CASA, FERRAMENTAS ou ELETRODOMÉSTICOS -> Chame o `agent_home_decor`.",
        "2. Se o assunto for SAÚDE, BELEZA, ESPORTES, BEBÊS ou ROUPAS -> Chame o `agent_lifestyle`.",
        "3. Se o assunto for TECNOLOGIA, CELULARES, COMPUTADORES ou CARROS -> Chame o `agent_tech_auto`.",
        
        "Se a pergunta for genérica (ex: 'Olá'), responda cordialmente e pergunte como ajudar.",
        "Sempre apresente a resposta final de forma clara."
    ],
    markdown=True
)

if __name__ == "__main__":
    # Tenta registrar o log de boot
    try:
        AuditLogger.log_event("SYS_START", "Orchestrator", "SYSTEM_BOOT", {"status": "online"})
    except:
        pass 
    
    print("\n🛒 --- Bem-vindo ao O-Market Specialist (Powered by Groq & DuckDB) ---")
    print("Sou o Orquestrador. Pergunte sobre qualquer produto das nossas planilhas.")
    print("Exemplos: 'Qual o preço do sofá?', 'Esse celular tem estoque?', 'Qual o prazo de entrega do batom?'")
    print("Digite 'sair' para encerrar.\n")
    
    while True:
        try:
            user_input = input("👤 Você: ")
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("👋 Até logo!")
                break
            
            # O Team processa a entrada e decide qual agente chamar
            market_team.print_response(user_input, stream=True)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Erro no sistema: {e}")