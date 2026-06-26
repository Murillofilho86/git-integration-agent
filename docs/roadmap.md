# Git Integration Agent - Roadmap Oficial

## Visão do Produto

Objetivo:

Analisar uma branch de origem e uma branch de destino para responder:

1. O que mudou?
2. Quais arquivos precisam ser modificados para integrar a feature?
3. Como reproduzir essas alterações na branch destino?
4. Executar a integração assistida por IA.

---

# Sprint 6 - Workspace Structure

Status: Concluída

Objetivo:
Separar análises por repositório.

Entregas:

* Estrutura workspace/<projeto>/<branch>*vs*<target>
* Suporte a múltiplos repositórios

---

# Sprint 7 - Plan Import

Status: Concluída

Objetivo:
Importar resposta estruturada do Claude.

Entregas:

* import-plan
* ai-analysis.json
* execution-plan.json

---

# Sprint 8 - Plan Navigation

Status: Concluída

Objetivo:
Permitir navegação do plano.

Entregas:

* show-plan
* next-task

---

# Sprint 9 - Task Expansion

Status: Concluída

Objetivo:
Expandir tarefas em arquivos concretos.

Entregas:

* expand-task
* classificação Criar/Revisar
* parser de arquivos
* correções de namespaces

---

# Sprint 10 - Repository Explorer

Status: Concluída

Objetivo:
Dar contexto real do repositório.

Entregas:

* inspect-file
* localização física
* descoberta de arquivos

---

# Sprint 11 - Dependency Explorer

Status: Concluída

Objetivo:
Descobrir dependências relacionadas.

Entregas:

* análise textual de dependências
* identificação de arquivos impactados

Observação:
Implementação inicial.
Dependências ainda não são classificadas semanticamente.

---

# Sprint 12 - Integration Scope Builder

Status: Concluída

Objetivo:
Determinar escopo de integração da feature.

Entregas:

* build-scope
* agrupamento por camada
* Domain
* Application
* Infrastructure
* API
* Tests

Resultado:
O agente consegue responder parcialmente:

"Quais arquivos fazem parte desta feature?"

---

# Backlog Priorizado

## Sprint 13 - Scope Consolidation

Status: Planejada

Objetivo:
Eliminar duplicidades e consolidar escopo único da feature.

Resultado esperado:

Feature Beneficiário

Arquivos únicos: XX

Domain: XX
Application: XX
Infrastructure: XX
Api: XX
Tests: XX

---

## Sprint 14 - Change Extraction

Status: Planejada

Objetivo:
Extrair alterações reais entre origem e destino.

Pergunta respondida:

"O que mudou neste arquivo?"

---

## Sprint 15 - Change Classification

Status: Planejada

Objetivo:
Classificar alterações.

Categorias:

* Novo Arquivo
* Arquivo Alterado
* Arquivo Removido
* Contrato Alterado
* Configuração

---

## Sprint 16 - Impact Analysis

Status: Planejada

Objetivo:
Descobrir impacto real das mudanças.

Pergunta respondida:

"Se eu aplicar esta alteração, o que mais precisa mudar?"

---

## Sprint 17 - Integration Plan Generator

Status: Planejada

Objetivo:
Gerar plano técnico executável.

Pergunta respondida:

"Como integrar esta feature?"

---

## Sprint 18 - AI Coding Agent MVP

Status: Planejada

Objetivo:
Gerar instruções de implementação por arquivo.

Pergunta respondida:

"Como reproduzir esta alteração na branch destino?"

---

## Sprint 19 - Assisted Implementation

Status: Planejada

Objetivo:
Gerar implementação assistida.

Saída:

* prompts por arquivo
* prompts por camada
* prompts por feature

---

## Sprint 20 - Autonomous Integration Agent

Status: Planejada

Objetivo:
Executar integração ponta a ponta.

Fluxo:

Analyze
↓
Classify
↓
Import Plan
↓
Build Scope
↓
Extract Changes
↓
Generate Integration Plan
↓
Generate Implementation
↓
Create Pull Request
