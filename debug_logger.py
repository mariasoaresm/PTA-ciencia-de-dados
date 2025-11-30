from app.tools.logger_tool import LoggerTool
import shutil
import os

print("--- 🔬 INICIANDO TESTE DE ROBUSTEZ DO LOGGER ---")

# Inicializa a ferramenta
logger = LoggerTool(base_evidence_path="evidence_test")

# Teste 1: Caso Perfeito (Happy Path)
print("\n1. Testando entrada perfeita...")
res = logger.log_execution(
    agent_name="TestAgent",
    user_query="Teste 1",
    response_text="Sucesso",
    sources=[{"type": "DW", "content": "dados"}],
    latency_ms=120.5
)
print(f"   Resultado: {res}")

# Teste 2: O Agente mandou Latência como String (O ERRO QUE VOCÊ TEVE)
print("\n2. Testando latência como string ('150ms')...")
res = logger.log_execution(
    agent_name="TestAgent",
    user_query="Teste 2",
    response_text="Latencia errada",
    latency_ms="150ms" # Isso quebraria o código antigo
)
print(f"   Resultado: {res}")

# Teste 3: O Agente mandou Sources tudo errado (String solta)
print("\n3. Testando sources como string solta...")
res = logger.log_execution(
    agent_name="TestAgent",
    user_query="Teste 3",
    response_text="Source errada",
    sources="Apenas um texto solto, não uma lista"
)
print(f"   Resultado: {res}")

# Limpeza (opcional)
# shutil.rmtree("evidence_test")
print("\n✅ TESTES CONCLUÍDOS. Se você viu 3 sucessos acima, o logger está blindado.")