{
  "request_id": "uuid-v4",
  "agent": "nome_do_agente",
  "response_text": "O produto tem preço médio de R$ 100,50 e o vendedor principal é a Loja X.",
  "confidence": 1.0,
  "structured": {
    "price": 100.50,
    "seller_id": "seller_123",
    "delivery_days": 5
  },
  "sources": [
    {
      "type": "DW", 
      "ref": "tabela_itens", 
      "query_used": "SELECT price FROM itens WHERE product_id='123'",
      "value_found": {"price": 100.50}
    },
    {
      "type": "DW", 
      "ref": "tabela_pedidos", 
      "query_used": "SELECT tempo_entrega_dias FROM pedidos WHERE order_id='abc'",
      "value_found": {"delivery_days": 5}
    }
  ]
}