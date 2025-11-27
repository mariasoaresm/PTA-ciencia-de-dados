from agno.tools import Toolkit

class RAGSearchTool(Toolkit):
    def __init__(self):
        super().__init__(name="rag_search_tool")
        self.register(self.search_documents)

    def search_documents(self, query_text: str, top_k: int = 3) -> str:
        """
        Busca informações em documentos técnicos (PDFs, Manuais).
        Atualmente configurado como placeholder para cumprir requisito de arquitetura.
        
        Args:
            query_text (str): O termo a ser buscado (ex: "como montar a mesa").
            top_k (int): Número de trechos a retornar.
            
        Returns:
            str: Trechos encontrados ou aviso de ausência.
        """
        # AQUI entraria a lógica de conectar num VectorDB (ChromaDB, PGVector).
        # Como estamos focados em planilhas (DW) por enquanto, retornamos um aviso
        # para garantir o princípio de "Não Inventar".
        
        return "AVISO: Nenhum documento PDF (Base de Conhecimento) foi indexado ainda. Consulte a DWQueryTool para dados."