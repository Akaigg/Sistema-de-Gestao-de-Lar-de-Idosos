# ADR-0004 — Autenticação com JWT + Bcrypt

- **Status:** Aceito
- **Data:** 2026-01-15

## Contexto

Precisamos autenticar funcionários e autorizar ações por papel. O sistema é
*single-page-app-like* — uma vez logado, o cliente faz várias requisições.

## Decisão

- Senhas: **bcrypt** com custo 12 (`passlib[bcrypt]`).
- Sessão: **JWT** HS256, assinado com chave aleatória de 256 bits
  (env `CHAVE_SECRETA_JWT`).
- Expiração curta (30 min) + *refresh token* (7 dias) armazenado em cookie HttpOnly.
- Autorização por papel via dependência `requer_papel("admin", "medico")`.

## Consequências

- Stateless: servidor não guarda sessão.
- Necessidade de mecanismo de revogação (lista de tokens revogados — `tokens_revogados`).
- Refresh em cookie HttpOnly mitiga XSS.
