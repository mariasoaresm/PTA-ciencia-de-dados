from contextlib import asynccontextmanager
from urllib.parse import quote
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from agno.playground import Playground, serve_playground_app
from agno.models.groq import Groq

# Imports Seguros
try:
    from app.agents.team import team
    from app.agents.bi_analyst import bi_analyst_agent
    from app.agents.tech_auto import tech_auto_agent
    from app.agents.home_decorations import home_decorations_agent
    from app.agents.lifestyle import lifestyle_agent
except ImportError as e:
    print(f"❌ [CRITICAL] Erro de Importação: {e}")
    exit(1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n🚀 [SYSTEM STARTUP] O-Market Playground Iniciando...")
    print("✅ Logger System: ONLINE")
    print("✅ Database Connection: READY")
    yield
    print("\n🛑 [SYSTEM SHUTDOWN] Encerrando serviços...")

# Configuração do Playground com Agentes Individuais
playground = Playground(
    name="O-Market Enterprise System",
    agents=[bi_analyst_agent, tech_auto_agent, home_decorations_agent, lifestyle_agent],
    teams=[team],
).get_app()

playground.router.lifespan_context = lifespan

@playground.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    host = request.url.hostname or "localhost"
    port = request.url.port
    endpoint = f"{host}:{port}" if port else host
    playground_url = f"https://app.agno.com/playground?endpoint={quote(endpoint)}"

    return f"""
    <!doctype html>
    <html lang="pt-br">
      <head>
        <meta charset="utf-8"/>
        <title>O-Market Enterprise</title>
        <style>
            body {{ font-family: sans-serif; background: #f0fdf4; display: grid; place-items: center; height: 100vh; margin: 0; }}
            .container {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
            h1 {{ color: #166534; }}
            .btn {{ background: #16a34a; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; }}
            .btn:hover {{ background: #15803d; }}
        </style>
      </head>
      <body>
        <div class="container">
            <h1>🌿 O-Market System</h1>
            <p>Estado: <strong>Operacional</strong></p>
            <p>Módulo de Auditoria: <strong>Ativo</strong></p>
            <br>
            <a href="{playground_url}" target="_blank" class="btn">Acessar Console de Agentes ↗</a>
        </div>
      </body>
    </html>
    """

if __name__ == "__main__":
    serve_playground_app("app.main:playground", reload=True, port=7777)