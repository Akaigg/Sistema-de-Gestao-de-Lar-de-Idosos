# ADR-0005 — Frontend em HTML/CSS/JS Vanilla

- **Status:** Aceito
- **Data:** 2026-01-15

## Contexto

A interface precisa ser interativa, mas o sistema é simples e roda localmente.
Bundlers (Webpack, Vite) e frameworks (React, Vue) trariam complexidade de
build e dependências de Node.js — desnecessárias para o porte do projeto.

## Decisão

Usar **HTML5 + CSS3 + JavaScript ES Modules vanilla**, servido como
estáticos pelo próprio FastAPI. Bibliotecas via CDN apenas para componentes
pontuais (FullCalendar, Chart.js, Lucide, SignaturePad).

## Consequências

### Positivas

- Sem etapa de build: editar arquivo e recarregar.
- Sem cadeia de dependências npm.
- Aprendizado mais simples para devs novos.

### Negativas

- Sem reatividade automática (componentes são montados manualmente).
- Reuso por composição manual de templates.

### Mitigações

- Estrutura modular: cada página tem seu JS isolado.
- Funções auxiliares em `js/comum.js`.
