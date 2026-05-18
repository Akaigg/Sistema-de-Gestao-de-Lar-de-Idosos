# ADR-0007 — Código 100% em Português

- **Status:** Aceito
- **Data:** 2026-01-15

## Contexto

Requisito do cliente: equipe e domínio são brasileiros. Termos técnicos do
domínio (residente, prontuário, prescrição, escala) são mais claros em PT-BR.

## Decisão

Todo o código (variáveis, classes, funções, comentários, mensagens) será
escrito em **português brasileiro**, exceto:

- Palavras-chave da linguagem (`class`, `def`, `import`, `return`).
- Decoradores e nomes de frameworks (`@app.get`).
- Constantes consagradas universalmente (`HTTP_OK`, `HTTP_NOT_FOUND` — mantemos).

## Consequências

- Vocabulário ubíquo (DDD) preservado.
- Onboarding de devs PT-BR mais rápido.
- Mistura com APIs em inglês é inevitável e aceitável nas bordas.
