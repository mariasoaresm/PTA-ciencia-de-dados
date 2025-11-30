# Agente: Lifestyle & Wellness Specialist

> **Resumo:** O seu consultor pessoal especializado em estilo de vida, abrangendo desde cuidados com a saúde e beleza até moda, hobbies e cuidados com pets.

---

## Perfil do Agente

* **Função:** Especialista em Lifestyle, Moda e Saúde.
* **Motor de Inteligência:** Google Gemini.
* **Missão:** Melhorar a experiência de compra de produtos de uso pessoal. Ele entende que comprar um creme ou um tênis exige mais do que saber o preço; exige saber a composição, o tamanho correto e a finalidade.
* **Personalidade:** Atencioso, atualizado e cuidadoso (especialmente com produtos de saúde e bebê).

---

## Áreas de Atuação (Departamento)

Este agente foi treinado para navegar especificamente pelos departamentos que tocam a vida pessoal e o lazer do cliente. Ele organiza o catálogo nas seguintes frentes:

| Grupo | Categorias Atendidas |
| :--- | :--- |
| **Cuidados Pessoais** | Beleza, Saúde e Perfumaria. |
| **Moda e Estilo** | Calçados, Bolsas, Acessórios, Relógios e Presentes. |
| **Família e Lazer** | Bebês, Brinquedos, Esporte e Lazer. |
| **Pets** | Pet Shop (Cães, Gatos e outros). |

---

## Ferramentas e Superpoderes

Para responder com precisão, o agente combina dados exatos de estoque com conhecimento qualitativo sobre os produtos:

### 1. O Consultor de Preços (DWQueryTool)
Acessa o banco de dados SQL para responder perguntas objetivas e numéricas.
* **Comparação de Preços:** "Qual o perfume mais caro?" ou "Tênis abaixo de R$ 200".
* **Variedade:** "Quantas marcas de shampoo temos disponíveis?"
* **Logística:** Verifica o peso (`weight_g`) de equipamentos de esporte, por exemplo.

### 2. O Especialista Técnico (RAGSearchTool)
Utiliza Inteligência Artificial para ler bulas, rótulos e guias de estilo. **Esta ferramenta é crítica para este agente.**
* **Composição Química:** Analisa ingredientes de cosméticos (ex: "Tem parabenos?", "É hipoalergênico?").
* **Guias de Tamanho:** Ajuda a traduzir medidas de roupas e calçados.
* **Contraindicações:** Busca alertas em produtos de saúde ou itens para bebês.

---

## Regras de Negócio Importantes

O agente segue diretrizes estritas para garantir a segurança e precisão das respostas:

1.  **Segurança em Saúde:** Ao lidar com a categoria `beleza_saude` ou `bebes`, o agente prioriza a busca em documentos oficiais (RAG) para evitar alucinações sobre benefícios médicos.
2.  **Filtro de Categoria:** Ele sempre restringe a busca SQL. Se você pergunta sobre "bolsas", ele ignora produtos de "ferramentas", garantindo que você não receba uma maleta de furadeira quando procura uma bolsa de mão.

---

## Exemplos de Capacidades

Veja como este agente pode ajudar em diferentes cenários:

### Cenário 1: Cosméticos e Saúde
* *"Estou procurando um hidratante facial. Quais opções custam menos de R$ 50,00?"* (SQL)
* *"Verifique se este protetor solar é indicado para pele oleosa com base na descrição do produto."* (RAG)

### Cenário 2: Moda e Acessórios
* *"Qual é a marca de relógio mais vendida na loja?"* (SQL)
* *"Existe algum guia de medidas para estes calçados infantis?"* (RAG)

### Cenário 3: Hobbies e Pets
* *"Qual a ração mais cara disponível no estoque?"* (SQL)
* *"Esse brinquedo é seguro para crianças menores de 3 anos?"* (RAG - Busca na classificação etária/descrição).

---

## Detalhes Técnicos (Para Desenvolvedores)

* **Código Fonte:** `app/agents/lifestyle.py`
* **Lista de Filtros (SQL):** O agente utiliza uma *whitelist* de categorias (`LIFESTYLE_CATEGORIES`) que inclui `perfumaria`, `pet_shop`, `fashion_calcados`, entre outros, para otimizar as queries `WHERE`.
* **Auditoria:** Obrigatória via `LoggerTool` para monitorar a qualidade das sugestões, especialmente em tópicos sensíveis como saúde.