# Agente: Team Leader (Orquestrador)

> **Resumo:** O ponto central de inteligência do sistema. Este agente não coloca a mão na massa; ele atua como um gerente que entende o pedido do usuário e delega a tarefa para o especialista mais qualificado.

---

## Perfil do Agente

* **Função:** Gerente de Projetos / Roteador de Tarefas.
* **Motor de Inteligência:** Google Gemini.
* **Missão:** Garantir que o usuário nunca precise saber *qual* especialista chamar. O usuário apenas faz a pergunta, e o Team Leader decide quem resolve.
* **Comportamento:** Ele é o único interlocutor direto com o usuário. Ele recebe a dúvida, repassa internamente, aguarda a resposta técnica e a entrega de forma consolidada e cordial.

---

## A Lógica de Triagem (Como ele pensa?)

O Team Leader toma decisões baseadas na **intenção** da pergunta. Ele segue um fluxograma mental rigoroso para evitar erros:

### 1. É uma pergunta sobre o NEGÓCIO? (Visão Macro)
Se o usuário quer saber sobre números agregados da empresa, métricas de performance ou logística geral.
* **Palavras-chave:** "Total de vendas", "Atrasos", "Faturamento", "Frete médio", "KPIs".
* **Ação:** Aciona o **BI Analyst**.

### 2. É uma pergunta sobre um PRODUTO? (Visão Micro)
Se o usuário quer detalhes específicos, preços unitários, manuais ou specs de um item. O Líder analisa o *tipo* de produto e direciona para o departamento correto:

| O que o usuário citou? | Especialista Acionado |
| :--- | :--- |
| Celulares, computadores, peças automotivas | **Tech & Auto Agent** |
| Móveis, decoração, toalhas, panelas | **Home & Decor Agent** |
| Perfumes, maquiagem, itens de bebê, esportes | **Lifestyle Agent** |

---

## Regras de Ouro (Governança)

Para garantir a segurança e eficiência do sistema, este agente possui restrições programadas em seu "DNA":

1.  **Proibição de Execução:** O Team Leader **JAMAIS** executa consultas SQL ou lê documentos PDF diretamente. Ele não tem acesso às ferramentas de dados. Sua única ferramenta é a "delegação".
2.  **Auditoria de Decisão:** Antes de passar a bola, ele registra no log: *"Recebi a pergunta X e decidi chamar o agente Y"*. Isso permite auditar se o roteamento está funcionando corretamente.
3.  **Transparência:** Se ele não entender a pergunta ou se ela fugir do escopo de todos os especialistas, ele deve informar o usuário em vez de tentar adivinhar.

---

## Fluxo de Exemplo

Veja como uma conversa acontece nos bastidores:

1.  **Usuário:** *"A mesa de jantar X cabe na minha sala? E como foram as vendas totais ontem?"*
2.  **Team Leader (Pensamento):**
    * *Parte 1:* "Mesa cabendo na sala" -> Assunto de **Home & Decor**.
    * *Parte 2:* "Vendas totais" -> Assunto de **BI Analyst**.
3.  **Ação:** Ele coordena os dois agentes para trabalharem.
4.  **Resposta Final:** O Team Leader consolida as respostas dos dois e responde ao usuário: *"Sobre a mesa, as dimensões são... Já sobre as vendas de ontem, o total foi de..."*

---

## Detalhes Técnicos (Para Desenvolvedores)

* **Código Fonte:** `app/agents/team.py`
* **Classe Base:** `agno.team.Team`
* **Membros (Agentes Gerenciados):**
    * `bi_analyst_agent`
    * `tech_auto_agent`
    * `home_decorations_agent`
    * `lifestyle_agent`
* **Ferramentas:** Apenas `LoggerTool` (para registro de decisão).