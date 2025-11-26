# Arquitetura do Sistema Multiagente - O-Market Specialist

## 1. Visão Geral
O sistema utiliza uma arquitetura de orquestração centralizada. O **Agente Orquestrador** recebe a pergunta do usuário e, baseado nas palavras-chave e intenção, roteia para um dos **Agentes Especialistas por Setor**.

## 2. Diagrama de Alto Nível
```mermaid
flowchart LR
    User[Usuário / UI] --> O(Orquestrador)
    
    %% Roteamento
    O --> A1[agent_home_decor]
    O --> A2[agent_lifestyle]
    O --> A3[agent_tech_auto]
    
    %% Fontes de Dados
    subgraph Knowledge Base
        DW[(Data Warehouse - SQL)]
        RAG[(Vector DB / PDFs)]
    end
    
    %% Conexões
    A1 & A2 & A3 --> DW
    A1 & A2 & A3 --> RAG