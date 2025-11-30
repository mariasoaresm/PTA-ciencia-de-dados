# Agente: BI Analyst (Analista de Business Intelligence)

> **Resumo:** O especialista virtual focado em transformar perguntas de negócio em consultas precisas ao banco de dados, fornecendo métricas quantitativas sobre vendas, logística e performance.

---

## Perfil do Agente

* **Função:** Analista de Dados Sênior (SQL Expert).
* **Motor de Inteligência:** Google Gemini.
* **Missão:** Democratizar o acesso aos dados. Ele atua como uma interface entre a linguagem humana ("Quanto vendemos?") e a linguagem de banco de dados (SQL).
* **Personalidade:** Analítico, objetivo e detalhista.

---

## Como Ele Trabalha?

Para garantir respostas corretas, este agente segue um fluxo rigoroso de 3 passos:

1.  **Entendimento do Schema:** Antes de responder, ele verifica a estrutura atual do banco de dados para garantir que as colunas e tabelas existem.
2.  **Tradução para SQL:** Ele converte a pergunta do usuário em uma consulta `DuckDB` (SQL), aplicando regras de negócio pré-definidas.
3.  **Auditoria:** Ele registra a execução da análise para fins de monitoramento e validação.

---

## Mapa de Dados (O que ele consegue ver?)

O agente tem acesso de leitura ao Data Warehouse da O-Market. O conhecimento dele está segregado nas seguintes visões de negócio:

| Visão (Tabela) | O que representa? | Principais Dados |
| :--- | :--- | :--- |
| **`orders`** | **Logística e Prazos** | Status do pedido (Entregue/Cancelado), datas reais vs. estimadas e dias de atraso. |
| **`items`** | **Financeiro do Pedido** | Preço do produto, valor do frete, ID do vendedor e ID do produto. |
| **`sellers`** | **Geolocalização** | Localização dos vendedores (Estado e Cidade). |
| **`products`** | **Características Físicas** | Categoria do produto, peso (g) e dimensões (cm). |

---

## Regras de Negócio Aprendidas

O agente já possui "memória muscular" sobre certas definições da empresa para evitar erros de interpretação:

* **Definição de Atraso:** Um pedido é considerado atrasado estritamente se a coluna `delay_days` for maior que zero.
* **Cálculo de Frete:** Sempre utiliza a coluna `freight` associada à tabela de itens (`items`).
* **Status de Pedido:** Reconhece termos em português como 'entregue' e 'cancelado'.

---

## Exemplos de Capacidades

O que você pode perguntar para este agente?

### 1. Análise Financeira
* *"Qual foi a receita total gerada por vendedores do estado de Minas Gerais?"*
* *"Qual é o ticket médio (preço médio) das vendas desta semana?"*

### 2. Análise Logística
* *"Qual é a taxa percentual de pedidos que sofreram atraso na entrega?"*
* *"Quais estados possuem o frete médio mais caro?"*

### 3. Análise de Produto
* *"Qual categoria de produto tem o maior peso médio de envio?"*

---

## Detalhes Técnicos (Para Desenvolvedores)

* **Código Fonte:** `app/agents/bi_analyst.py`
* **Ferramentas Ativas:**
    * `DWQueryTool`: Permite executar queries `SELECT` no banco DuckDB.
    * `LoggerTool`: Grava logs de execução.
* **Variáveis de Ambiente:** Requer configuração de acesso ao Google Gemini e caminho do banco DuckDB.