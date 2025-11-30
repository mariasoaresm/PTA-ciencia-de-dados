# Agente: Home & Decor Specialist

> **Resumo:** O seu consultor digital de arquitetura e decoração, especializado em verificar se o produto cabe no seu ambiente e como ele é montado.

---

## Perfil do Agente

* **Função:** Arquiteto e Especialista em Casa & Decoração.
* **Motor de Inteligência:** Google Gemini.
* **Missão:** Unir a estética à funcionalidade. Ele garante que o usuário compre o móvel certo, com as medidas certas e o material adequado, evitando devoluções por problemas de tamanho ou compatibilidade.
* **Diferencial:** Capacidade híbrida de analisar dados técnicos (dimensões) e dados documentais (manuais de montagem).

---

## Áreas de Atuação (Escopo)

Este agente é treinado para ignorar produtos que não sejam do seu departamento. Ele foca exclusivamente nas seguintes categorias:

| Categoria | O que inclui? |
| :--- | :--- |
| **Móveis e Decoração** | Sofás, estantes, mesas, decoração geral. |
| **Cama, Mesa e Banho** | Têxteis, toalhas, lençóis e acessórios. |
| **Escritório e Home Office** | Cadeiras ergonômicas, escrivaninhas, organização. |
| **Utilidades Domésticas** | Itens de cozinha e organização do lar. |
| **Jardim e Construção** | Ferramentas manuais, itens de jardinagem e construção civil. |
| **Eletrodomésticos** | Itens elétricos voltados para o lar. |

---

## Ferramentas e Superpoderes

Diferente de um analista comum, este agente possui duas "caixas de ferramentas" distintas para responder perguntas completas:

### 1. A Régua Digital (DWQueryTool)
Utiliza o banco de dados SQL para validar **números e métricas**.
* **Verificação de Espaço:** Acessa `length_cm` (comprimento), `width_cm` (largura) e `height_cm` (altura).
* **Logística:** Verifica o peso (`weight_g`) para estimar dificuldade de manuseio.
* **Financeiro:** Consulta preços e custos de frete.

### 2. O Bibliotecário Técnico (RAGSearchTool)
Utiliza Inteligência Artificial para ler documentos (PDFs e textos) que não estão em tabelas.
* **Manuais de Instrução:** Busca informações sobre montagem e instalação.
* **Materiais:** Responde dúvidas sobre composição (ex: "É madeira maciça ou MDF?").

---

## Exemplos de Capacidades

O que você pode perguntar para este agente?

### Planejamento de Espaço (Foco em Dimensões)
* *"Tenho um espaço de 2 metros na minha sala. Qual a maior mesa de jantar que cabe ali?"*
* *"Essa cadeira de escritório passa em uma porta de 80cm de largura?"*

### Detalhes do Produto (Foco em RAG/Documentos)
* *"Como é feita a montagem desse guarda-roupa? Preciso de parafusadeira?"*
* *"Qual o material do tampo dessa mesa? É resistente à água?"*

### Análise Comparativa (Foco em Custo-Benefício)
* *"Qual é o preço médio dos kits de cama e banho disponíveis?"*
* *"Liste as ferramentas de jardim mais leves (menor peso) para idosos."*

---

## Detalhes Técnicos (Para Desenvolvedores)

* **Código Fonte:** `app/agents/home_decorations.py`
* **Restrições de Sistema:**
    * O agente aplica filtros automáticos nas queries SQL (`WHERE category = ...`) para garantir que não sugira produtos de outros departamentos (como automotivo ou beleza).
    * Requer acesso a uma *Vector Store* (para o RAG) e ao *DuckDB* (para o SQL).
* **Auditoria:** Todas as consultas são registradas via `LoggerTool` para controle de qualidade das recomendações.