# ADR-0002 — Uso de SQLite como Banco de Dados

- **Status:** Aceito
- **Data:** 2026-01-15

## Contexto

O sistema será usado **localmente** dentro do lar de idosos, por uma equipe
pequena (até ~30 funcionários simultâneos). Não há necessidade de cluster,
replicação ou acesso remoto. Backups simples (cópia de arquivo) são suficientes.

## Decisão

Usar **SQLite** como banco principal, com:

- Modo `WAL` (Write-Ahead Logging) habilitado para concorrência de leitura/escrita.
- `PRAGMA foreign_keys = ON` para integridade referencial.
- Uma instância única, arquivo em `dados/cuidarmais.db`.

## Consequências

### Positivas

- Zero configuração: sem servidor a manter.
- Backup trivial (copiar o `.db`).
- Performance excelente para o volume previsto.
- Roda em qualquer SO.

### Negativas

- Concorrência de escrita limitada (uma escrita por vez).
- Tipos mais permissivos que Postgres.

### Mitigações

- WAL mode + transações curtas.
- Validação rígida na camada de domínio/aplicação.
- Possível migração futura a Postgres mantendo as portas do domínio intactas.
