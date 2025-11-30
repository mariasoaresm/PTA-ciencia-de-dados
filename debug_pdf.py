from app.tools.dw_tool import DWQueryTool
import json

def testar_geracao_pdf():
    print("🚀 Iniciando teste de geração de PDF...")
    
    # 1. Instancia a ferramenta
    dw_tool = DWQueryTool()
    
    # 2. Chama a função diretamente
    resultado = dw_tool.generate_pdf_reports()
    
    # 3. Exibe o resultado
    print("\n📄 Resultado da execução:")
    try:
        res_json = json.loads(resultado)
        print(json.dumps(res_json, indent=2, ensure_ascii=False))
        
        if res_json.get("status") == "SUCCESS":
            print(f"\n✅ SUCESSO! Verifique a pasta: {dw_tool.output_pdf_dir}")
        else:
            print("\n❌ ERRO: Algo deu errado na geração.")
            
    except Exception as e:
        print(f"Erro ao ler resposta: {resultado}")

if __name__ == "__main__":
    testar_geracao_pdf()