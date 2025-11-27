Nome: agent_lifestyle
Setor: Estilo de Vida, Saúde e Lazer
Responsabilidade:
- Instruções de uso pessoal, validade, faixas etárias e composição.
- Fallback para categorias genéricas ou serviços.

Categorias chave:
- esporte_lazer, beleza_saude, perfumaria, bebes, fraldas_higiene
- brinquedos, jogos, cool_stuff, pet_shop
- fashion_bolsas_e_acessorios, fashion_calcados, fashion_underwear_e_moda_praia, fashion_roupa_masculina, fashion_roupa_feminina, fashion_esporte, fashion_roupa_infanto_juvenil, malas_acessorios
- livros_interesse_geral, livros_tecnicos, livros_importados, papelaria
- instrumentos_musicais, musica, cds_dvds_musicais, dvds_blu_ray, artes, artes_e_artesanato, cine_foto
- alimentos, bebidas, alimentos_bebidas
- artigos_de_festas, artigos_de_natal, flores
- indefinido, seguros_e_servicos, market_place

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
- DWQueryTool (preços, disponibilidade)
- RAGSearch (regras de jogos, bulas, tabelas nutricionais, guias de tamanho)