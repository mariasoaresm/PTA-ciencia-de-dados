# Agente: Tech & Auto Specialist

> **Resumo:** O especialista "geek" do time. Seu foco é fornecer especificações técnicas precisas sobre computadores, eletrônicos e peças automotivas, garantindo que o usuário entenda o que está comprando.

---

## Perfil do Agente

* **Função:** Consultor Técnico de Tecnologia e Automotivo.
* **Motor de Inteligência:** Google Gemini.
* **Missão:** Clareza técnica. Ele ajuda o cliente a navegar por um mar de especificações (RAM, Gigabytes, Voltagem, Compatibilidade) para encontrar o produto ideal.
* **Diferencial:** É treinado para ser rigoroso com números e categorias, evitando misturar peças de carro com peças de computador.

---

## Áreas de Atuação (Catálogo)

Este agente é responsável pelos departamentos mais técnicos da loja. Ele domina os seguintes grupos de produtos:

| Grupo | Categorias Atendidas |
| :--- | :--- |
| **Computação & Games** | PCs, PC Gamer, Informática, Acessórios, Consoles e Jogos. |
| **Gadgets & Eletrônicos** | Telefonia (Celulares/Smartphones) e Eletrônicos gerais. |
| **Pesados & Mecânica** | Automotivo e Agro/Indústria e Comércio. |

---

## Ferramentas e Superpoderes

Para responder dúvidas técnicas, o agente utiliza duas abordagens complementares:

### 1. O Verificador de Specs (DWQueryTool)
Acessa o banco de dados SQL para buscar dados exatos ("Hard Data").
* **Logística e Peso:** Verifica o peso (`weight_g`) — crucial para frete de peças automotivas ou gabinetes de PC.
* **Preço:** Monitora o valor exato dos produtos.
* **Dimensões:** Confere se o produto tem o tamanho esperado (via `length_cm`).

### 2. O Leitor de Manuais (RAGSearchTool)
Utiliza Inteligência Artificial para ler a documentação textual.
* **Garantia:** Busca termos de garantia e suporte técnico.
* **Manuais Técnicos:** Procura informações de instalação ou compatibilidade em PDFs (quando disponíveis).

---

## Regras de Negócio (O "Cérebro" do Agente)

Para evitar erros comuns em IA, este agente segue protocolos rígidos:

1.  **Isolamento de Categoria:** Ao buscar um "mouse", ele é programado para olhar apenas em `informatica_acessorios`, ignorando categorias de brinquedos ou decoração. Isso é feito através de filtros SQL automáticos.
2.  **Precisão Numérica:** Diferente de perguntas subjetivas (como "qual é mais bonito?"), este agente foca em dados objetivos (qual é mais rápido, mais pesado ou mais barato).

---

## Exemplos de Capacidades

O que você pode perguntar para este agente?

### Comparação Técnica
* *"Qual é o smartphone mais pesado atualmente no estoque?"*
* *"Liste os 3 PCs Gamers com o maior preço."*

### Análise de Mercado
* *"Qual é o preço médio dos produtos na categoria de telefonia?"*
* *"Quantos itens de automotivo temos disponíveis para venda?"*

### Dúvidas de Suporte (Via RAG)
* *"Qual o tempo de garantia deste console?"*
* *"O manual deste acessório automotivo menciona instalação elétrica?"*

---

## Detalhes Técnicos (Para Desenvolvedores)

* **Código Fonte:** `app/agents/tech_auto.py`
* **Filtros SQL (Whitelist):** O agente utiliza a lista `TECH_CATEGORIES` (incluindo `pcs`, `automotivo`, `telefonia`) para injetar cláusulas `WHERE` nas queries.
* **Auditoria:** O uso da ferramenta `LoggerTool` é mandatório para registrar todas as consultas técnicas realizadas.