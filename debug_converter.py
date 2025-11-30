import os
from app.tools.pdf_converter import check_and_convert_csv_to_pdf

# Define o caminho da raiz (onde este script está)
project_root = os.path.dirname(os.path.abspath(__file__))

print(f"--- 🧪 Testando Conversor de PDF na pasta: {project_root} ---")

# Executa a função
try:
    check_and_convert_csv_to_pdf(project_root)
    print("\n✅ Teste finalizado. Verifique se os arquivos .pdf apareceram na raiz.")
except Exception as e:
    print(f"\n❌ Erro durante o teste: {e}")