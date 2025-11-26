Nome: agent_tech_auto
Setor: Tecnologia e Automotivo
Responsabilidade:
- Especificações técnicas rígidas (hardware, software, voltagem).
- Compatibilidade de peças automotivas e industriais.

Categorias chave:
- informatica_acessorios, pcs, pc_gamer, tablets_impressao_imagem, eletronicos, consoles_games, audio
- telefonia, telefonia_fixa
- automotivo, sinalizacao_e_seguranca
- relogios_presentes
- agro_industria_e_comercio, industria_comercio_e_negocios

Entradas:
- product_id
- pergunta_texto
- contexto_usuario (opcional)

Saídas:
- resposta_texto
- fontes: [DW|PDF]
- score_confianca (0-1)
- evidencias: [{tipo, ref, trecho}]

Ferramentas permitidas:
- DWQueryTool (specs técnicas numéricas, voltagem, potência)
- RAGSearch (datasheets, manuais técnicos, listas de compatibilidade)