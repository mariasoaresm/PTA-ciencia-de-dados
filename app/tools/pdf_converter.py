import os
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def check_and_convert_csv_to_pdf(project_root: str):
    """
    Verifica a existência de arquivos .pdf para cada .csv crítico.
    Se não existir, gera o PDF automaticamente.
    """
    
    # Lista de arquivos mapeada conforme dw_tool.py 
    target_files = [
        "produtos_tratados",
        "vendedores_tratados",
        "pedidos_tratados",
        "itens_pedidos_tratados"
    ]

    print(f"\n📄 [PDF CHECK] Iniciando verificação de arquivos em: {project_root}")

    for filename in target_files:
        csv_path = os.path.join(project_root, f"{filename}.csv")
        pdf_path = os.path.join(project_root, f"{filename}.pdf")

        # 1. Verifica se o CSV existe
        if not os.path.exists(csv_path):
            print(f"⚠️  CSV não encontrado: {csv_path} - Pulando.")
            continue

        # 2. Verifica se o PDF já existe
        if os.path.exists(pdf_path):
            print(f"✅ PDF já existe: {filename}.pdf")
            continue

        # 3. Conversão (Caso o PDF não exista)
        print(f"⚙️  Gerando PDF faltante para: {filename}...")
        try:
            _convert_csv_to_pdf(csv_path, pdf_path, filename)
            print(f"✅ PDF gerado com sucesso: {pdf_path}")
        except Exception as e:
            print(f"❌ Erro ao converter {filename}: {str(e)}")

def _convert_csv_to_pdf(csv_path: str, pdf_path: str, title: str):
    """
    Lógica interna de geração de PDF usando ReportLab.
    Estilo baseado no DWQueryTool.
    """
    # Lê o CSV (Limita a 100 linhas para performance, ajuste conforme necessidade)
    df = pd.read_csv(csv_path).head(100) 
    
    doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))
    elements = []
    styles = getSampleStyleSheet()

    # Título
    elements.append(Paragraph(f"Relatório Automático: {title.upper()}", styles['Title']))
    elements.append(Spacer(1, 12))

    # Prepara dados para tabela (Header + Rows)
    # Convertendo tudo para string para evitar erros no ReportLab
    data = [df.columns.to_list()] + df.astype(str).values.tolist()

    # Cria tabela
    t = Table(data)
    
    # Aplica o mesmo estilo visual definido no seu dw_tool.py 
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8) # Fonte menor para caber mais dados
    ]))

    elements.append(t)
    doc.build(elements)