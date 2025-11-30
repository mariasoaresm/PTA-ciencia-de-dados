# Arquitetura do Sistema O-Market

> **Visão Geral:** O O-Market é um ecossistema de Inteligência Artificial projetado para democratizar o acesso aos dados. Em vez de exigir que usuários aprendam programação ou SQL, o sistema utiliza uma rede de **Agentes Especialistas** coordenados por um **Orquestrador Central**.

---

## O Modelo: "Hub-and-Spoke" (Centro e Raios)

Imagine um hospital. Você (o paciente) não entra na sala de cirurgia direto. Você passa pela **Triagem**. O enfermeiro da triagem decide se você precisa de um cardiologista, um ortopedista ou um clínico geral.

O Sistema O-Market funciona exatamente assim:
1.  **Hub (Centro):** O "Team Leader" atua como a triagem. Ele recebe o pedido e decide para quem repassar.
2.  **Spoke (Raios):** Os Agentes Especialistas (BI, Tech, Home, Lifestyle) estão nas pontas, prontos para resolver problemas específicos.

Isso garante que um especialista em *Móveis* nunca tente responder perguntas sobre *Peças de Carro*, evitando erros e "alucinações".

---

## Diagrama Visual do Fluxo

```mermaid
graph TD
    %% Nós Principais
    User((Usuário))
    Orch[Orquestrador<br/>Team Leader]
    
    %% Subgrafo: Especialistas
    subgraph "Camada de Especialistas"
        BI[BI Analyst<br/>(Negócios)]
        Tech[Tech & Auto<br/>(Técnico)]
        Home[Home & Decor<br/>(Arquitetura)]
        Life[Lifestyle<br/>(Bem-Estar)]
    end
    
    %% Subgrafo: Dados
    subgraph "Camada de Dados & Ferramentas"
        DB[(DuckDB<br/>Dados Numéricos)]
        RAG[Manuais & PDFs<br/>Dados de Texto]
    end

    %% Fluxo
    User -->|Faz uma pergunta| Orch
    Orch -->|Analisa e Delega| BI
    Orch -->|Analisa e Delega| Tech
    Orch -->|Analisa e Delega| Home
    Orch -->|Analisa e Delega| Life

    %% Conexões de Dados
    BI <-->|SQL| DB
    Tech <-->|SQL| DB
    Tech <-->|Busca| RAG
    Home <-->|SQL| DB
    Home <-->|Busca| RAG
    Life <-->|SQL| DB
    Life <-->|Busca| RAG

    %% Retorno
    BI & Tech & Home & Life -.->|Devolve Resposta| Orch
    Orch -.->|Resposta Consolidada| User
    
    %% Estilo
    style Orch fill:#f9f,stroke:#333,stroke-width:2px
    style DB fill:#ff9,stroke:#333
    style RAG fill:#9ff,stroke:#333