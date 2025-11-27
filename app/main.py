# from agno.playground import Playground, serve_playground_app
# from fastapi.responses import HTMLResponse, RedirectResponse
# from contextlib import asynccontextmanager
# from fastapi import Request
# from urllib.parse import quote
# from .agents import team

# app = Playground(
#     name="Example Playground",
#     description="A playground for testing agents.",
#     teams=[team]
# ).get_app()

# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# def home(request: Request):
#     host = request.url.hostname or "localhost"
#     port = request.url.port
#     endpoint = f"{host}:{port}" if port else host
#     playground_url = f"https://app.agno.com/playground?endpoint={quote(endpoint)}"

#     return f"""
#     <!doctype html>
#     <html lang="pt-br">
#       <head>
#         <meta charset="utf-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1" />
#         <title>Agent Playground</title>
#         <style>
#           :root {{ color-scheme: light dark; }}
#           body {{
#             font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, "Helvetica Neue", Arial, "Apple Color Emoji", "Segoe UI Emoji";
#             margin: 0; padding: 0; display: grid; min-height: 100dvh; place-items: center;
#             background: radial-gradient(1000px 600px at 50% -20%, rgba(99,102,241,.15), transparent);
#           }}
#           .card {{
#             width: min(680px, 92vw);
#             border: 1px solid color-mix(in oklab, CanvasText 12%, transparent);
#             border-radius: 20px; padding: 28px; backdrop-filter: blur(6px);
#             box-shadow: 0 10px 30px color-mix(in oklab, CanvasText 12%, transparent);
#           }}
#           h1 {{ margin: 0 0 8px; font-size: clamp(24px, 4vw, 34px); }}
#           p  {{ margin: 0 0 18px; line-height: 1.5; opacity: .85; }}
#           a.button {{
#             display: inline-block; padding: 12px 18px; border-radius: 12px; text-decoration: none;
#             border: 1px solid color-mix(in oklab, CanvasText 10%, transparent);
#           }}
#         </style>
#       </head>
#       <body>
#         <main class="card">
#           <h1>Agent Playground</h1>
#           <p>Abra o playground em uma nova aba para testar seus agentes.</p>
#           <p><strong>URL:</strong> <code>{playground_url}</code></p>
#           <p>Selecione "Teams" e em "Endpoint" digite: <code>http://{endpoint}/v1</code> ou <code>http://localhost:{port}/v1<code></p>
#           <p style="margin-top:14px">
#             <a class="button" href="{playground_url}" target="_blank" rel="noopener">Abrir Playground ↗</a>
#           </p>
#           <p style="margin-top:22px; opacity:.7">
#             Dica: a documentação da API está em <a href="/docs">/docs</a>.
#           </p>
#         </main>
#       </body>
#     </html>
#     """

# @app.on_event("startup")
# async def lifespan():
#     host = "127.0.0.1"
#     port = "7777"
#     endpoint = f"{host}:{port}"
#     local_url = f"http://{endpoint}"
#     cloud_url = f"https://app.agno.com/playground?endpoint={quote(endpoint)}"

#     print("INFO Starting playground on", local_url)
#     print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Agent Playground ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
#     print("┃                                                                             ┃")
#     print(f"┃  Playground URL: {cloud_url:<54}┃")
#     print("┃                                                                             ┃")
#     print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

# Mudamos de 'agno.playground' para 'phi.playground' para contornar o erro
from agno.playground import Playground, serve_playground_app
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from urllib.parse import quote
from dotenv import load_dotenv
import os
import sys

# Garante que acha os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importa seu time do Agno
from app.orchestrator import market_team as team

load_dotenv()

# Inicializa o Playground
playground = Playground(
    name="O-Market Specialist Playground",
    teams=[team]
)

app = playground.get_app()

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request):
    host = request.url.hostname or "localhost"
    port = request.url.port or 7777
    endpoint = f"{host}:{port}"
    playground_url = f"https://app.phidata.com/playground?endpoint={quote(endpoint)}"

    return f"""
    <!doctype html>
    <html lang="pt-br">
      <head>
        <title>O-Market AI</title>
        <style>
          body {{ background: #111; color: #fff; font-family: sans-serif; display: grid; place-items: center; height: 100vh; margin: 0; }}
          .card {{ background: #222; padding: 40px; border-radius: 12px; text-align: center; border: 1px solid #333; }}
          a.button {{ display: inline-block; padding: 15px 30px; background: #4ade80; color: #000; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }}
        </style>
      </head>
      <body>
        <main class="card">
          <h1>🤖 O-Market Specialist</h1>
          <p>Playground Ativo via Phidata/Agno.</p>
          <a class="button" href="{playground_url}" target="_blank">Abrir Interface ↗</a>
        </main>
      </body>
    </html>
    """

if __name__ == "__main__":
    serve_playground_app("app.main:app", reload=True, port=7777)