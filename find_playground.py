import agno
import os

print(f"📍 Procurando 'class Playground' dentro de: {os.path.dirname(agno.__file__)}")
print("-" * 50)

# Caminho base da biblioteca instalada
base_dir = os.path.dirname(agno.__file__)

encontrou = False

# Varre todas as pastas e arquivos da biblioteca
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "class Playground" in content:
                        # Descobre o caminho de importação relativo
                        rel_path = os.path.relpath(path, os.path.dirname(base_dir))
                        import_path = rel_path.replace(os.sep, ".").replace(".py", "").replace(".__init__", "")
                        
                        print(f"✅ ENCONTRADO EM: {path}")
                        print(f"💡 Tente importar assim: from {import_path} import Playground")
                        encontrou = True
            except Exception as e:
                pass

if not encontrou:
    print("❌ A classe 'Playground' não foi encontrada em nenhum lugar da biblioteca 'agno'.")
    print("Possível solução: Talvez precise instalar 'phidata' ou um pacote extra 'agno[ui]'.")