import json
from agno.tools import Toolkit

class RAGSearchTool(Toolkit):
    def __init__(self):
        super().__init__(name="rag_search_tool")
        self.register(self.search_manuals)

    def search_manuals(self, query_text: str) -> str:
        """
        Busca semântica simulada em manuais técnicos.
        """
        print(f"📚 [RAG] Buscando conhecimento para: '{query_text}'")
        
        results = []
        q = query_text.lower()

        # Simulações baseadas nas categorias do seu dataset Olist
        if "beleza" in q or "saude" in q or "creme" in q:
            results.append({
                "doc_ref": "guia_beleza_segura.pdf",
                "snippet": "Produtos da categoria beleza_saude devem conter selo da Anvisa. Validade média de cosméticos é 24 meses.",
                "score": 0.89
            })
        
        if "informatica" in q or "mouse" in q or "teclado" in q:
            results.append({
                "doc_ref": "manual_acessorios_tech.pdf",
                "snippet": "A maioria dos itens de informatica_acessorios possui garantia de 3 meses. Verifique compatibilidade USB 3.0.",
                "score": 0.92
            })

        if "moveis" in q or "decoracao" in q:
             results.append({
                "doc_ref": "instrucoes_moveis.pdf",
                "snippet": "Para categoria moveis_decoracao, as dimensões (length, height, width) são da embalagem. O produto montado pode variar 2cm.",
                "score": 0.95
            })

        if not results:
            return json.dumps({"status": "NO_RESULTS", "message": "Nenhum documento técnico encontrado."})

        return json.dumps({"status": "SUCCESS", "results": results}, indent=2)