### Arquivo 2: `docs/agents/agent_home_decorations.md`

Este agente foca em **Física e Espaço**. O JSON destaca dimensões e materiais para garantir que o móvel caiba na casa do cliente.

```markdown
# Agente: agent_home_decorations

## 1. Identificação
- **Nome:** `agent_home_decorations`
- **Setor:** Casa, Móveis, Eletro e Construção
- **Descrição:** Especialista em itens para o lar, focando em dimensões físicas, montagem, materiais e consumo energético.

## 2. Escopo e Responsabilidades
Este agente deve garantir que o produto "caiba" e "funcione" no ambiente do usuário.
- **Dimensões e Espaço:** Validar altura, largura, profundidade e peso.
- **Instalação:** Complexidade de montagem, necessidade de ferramentas, voltagem de eletros.
- **Materiais:** Tipo de madeira, tecido, durabilidade e cuidados de limpeza.

### Categorias Chave (Mapeamento do Banco de Dados)
O agente é responsável exclusivamente pelos produtos nestas categorias:
- **Móveis:** `moveis_decoracao`, `moveis_escritorio`, `moveis_sala`, `moveis_cozinha_area_de_servico_jantar_e_jardim`, `moveis_quarto`, `moveis_colchao_e_estofado`
- **Utilidades:** `utilidades_domesticas`, `cama_mesa_banho`
- **Eletros:** `eletrodomesticos`, `eletrodomesticos_2`, `eletroportateis`, `climatizacao`, `la_cuisine`, `portateis_casa_forno_e_cafe`, `portateis_cozinha_e_preparadores_de_alimentos`, `casa_conforto`, `casa_conforto_2`
- **Construção:** `casa_construcao`, `construcao_ferramentas_seguranca`, `construcao_ferramentas_construcao`, `construcao_ferramentas_ferramentas`, `construcao_ferramentas_iluminacao`, `construcao_ferramentas_jardim`, `ferramentas_jardim`

## 3. Interfaces (Contrato de API)

### Entradas
- `product_id` (String: SKU ou ID)
- `user_query` (String: Pergunta sobre medidas, material ou montagem)
- `context` (Dict: Opcional)

### Saída Padronizada (JSON)
⚠️ **IMPORTANTE:** O agente deve retornar estritamente um objeto JSON.

**Esquema de Resposta (Exemplo: Móvel):**

```json
{
  "request_id": "uuid-v4",
  "agent": "agent_home_decorations",
  "response_text": "O Sofá Retrátil tem 2,30m de largura. Ele é feito de madeira de eucalipto e tecido suede. Requer montagem profissional.",
  "confidence": 0.98,
  "sources": [
    {
      "type": "DW",
      "ref": "db_moveis:sku_998",
      "value": {"width_cm": 230, "height_cm": 95, "depth_cm": 110}
    },
    {
      "type": "PDF",
      "ref": "manual_montagem_sofa.pdf#page=1",
      "snippet": "Estrutura: Madeira Eucalipto Reflorestada. Requer montagem: Sim."
    }
  ],
  "structured_data": {
    "dimensions": {
      "width_cm": 230,
      "height_cm": 95,
      "depth_open_cm": 160,
      "depth_closed_cm": 110
    },
    "material": "Suede / Eucalipto",
    "assembly_required": true
  },
  "metadata": {
    "model_version": "home-v1.1",
    "latency_ms": 130
  }
}