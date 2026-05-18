# ADR-0003 — FastAPI como Framework HTTP

- **Status:** Aceito
- **Data:** 2026-01-15

## Contexto

Precisamos de um framework HTTP em Python que ofereça:

- Validação automática de entrada/saída.
- Documentação OpenAPI/Swagger embutida.
- Performance adequada.
- Boa integração com tipagem moderna do Python.

## Decisão

Usar **FastAPI** (Starlette + Pydantic) como framework HTTP.

## Alternativas consideradas

- **Flask** — minimalista, mas exige libs extras para validação e docs.
- **Django** — pesado demais para o escopo; impõe ORM e estilo MVT.
- **FastAPI** ✅ — tipagem nativa, validação Pydantic, OpenAPI automático.

## Consequências

- Pydantic acopla parcialmente os schemas à camada de apresentação — aceitável,
  pois schemas Pydantic ficam restritos a `apresentacao/`.
- Maior facilidade para gerar SDKs do cliente no futuro.
