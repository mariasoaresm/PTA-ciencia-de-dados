# Agente: agent_lifestyle

## 1. Identificação
- **Nome:** `agent_lifestyle`
- **Setor:** Estilo de Vida, Saúde, Moda e Lazer
- **Descrição:** Especialista em produtos de uso pessoal, consumo recorrente e entretenimento. Foca na experiência do usuário e segurança.

## 2. Escopo e Responsabilidades
Este agente lida com a "experiência de uso" e segurança pessoal. Deve ser acionado para:
- **Saúde e Segurança:** Validade, composição química, contraindicações (bulas), tabelas nutricionais e faixas etárias.
- **Moda e Tamanho:** Guias de medidas (P/M/G), materiais (algodão vs sintético).
- **Lazer:** Regras de jogos, sinopses de livros/filmes e instruções de brinquedos.

### Categorias Chave (Mapeamento do Banco de Dados)
O agente é responsável exclusivamente pelos produtos nestas categorias:
- **Moda:** `fashion_bolsas_e_acessorios`, `fashion_calcados`, `fashion_underwear_e_moda_praia`, `fashion_roupa_masculina`, `fashion_roupa_feminina`, `fashion_esporte`, `fashion_roupa_infanto_juvenil`, `malas_acessorios`
- **Beleza e Saúde:** `beleza_saude`, `perfumaria`, `bebes`, `fraldas_higiene`
- **Lazer e Cultura:** `brinquedos`, `jogos`, `cool_stuff`, `pet_shop`, `livros_interesse_geral`, `livros_tecnicos`, `livros_importados`, `papelaria`
- **Arte e Mídia:** `instrumentos_musicais`, `musica`, `cds_dvds_musicais`, `dvds_blu_ray`, `artes`, `artes_e_artesanato`, `cine_foto`
- **Consumo:** `alimentos`, `bebidas`, `alimentos_bebidas`, `artigos_de_festas`, `artigos_de_natal`, `flores`
- **Geral:** `indefinido`, `seguros_e_servicos`, `market_place`

## 3. Interfaces (Contrato de API)

### Entradas
- `product_id` (String: SKU ou ID)
- `user_query` (String: Pergunta sobre uso, validade ou tamanho)
- `context` (Dict: Opcional)

### Saída Padronizada (JSON)
⚠️ **IMPORTANTE:** O agente deve retornar estritamente um objeto JSON.

**Esquema de Resposta (Exemplo: Cosmético):**

```json
{
  "request_id": "uuid-v4",
  "agent": "agent_lifestyle",
  "response_text": "Este creme facial contém Retinol e Ácido Hialurônico. É indicado para uso noturno e a validade é de 24 meses após aberto. Não recomendado para gestantes.",
  "confidence": 0.90,
  "sources": [
    {
      "type": "DW",
      "ref": "tabela_skincare:row_123",
      "value": {"price": 120.00, "brand": "Loreal", "volume_ml": 50}
    },
    {
      "type": "PDF",
      "ref": "bula_creme_antiidade.pdf#page=2",
      "snippet": "Composição: Aqua, Retinol, Hyaluronic Acid. Contraindicação: Gestantes."
    }
  ],
  "structured_data": {
    "usage_instructions": "Uso noturno",
    "expiration_months": 24,
    "ingredients": ["Retinol", "Ácido Hialurônico"],
    "warnings": ["Gestantes", "Pele Sensível"]
  },
  "metadata": {
    "model_version": "lifestyle-v1.0",
    "latency_ms": 110
  }
}