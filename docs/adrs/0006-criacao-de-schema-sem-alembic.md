# ADR-0006 — Criação de Schema sem Alembic na v1

- **Status:** Aceito (revisável)
- **Data:** 2026-01-15

## Contexto

Alembic é a ferramenta padrão de migrations SQLAlchemy. Porém, na v1 do
sistema, o banco é criado uma única vez e mudanças são raras. Adicionar
Alembic agora aumenta complexidade.

## Decisão

Na v1, criar o schema via `Base.metadata.create_all()`. A partir da v2 (quando
houver schema em produção), introduzir Alembic.

## Consequências

- Simplicidade no início.
- Em produção, mudanças exigem script manual de ALTER ou migração baseline
  de Alembic.
