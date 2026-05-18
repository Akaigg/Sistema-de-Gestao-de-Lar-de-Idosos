# Arquitetura do Sistema — Cuidar+

## 1. Visão Geral

O sistema segue **Arquitetura Limpa (Clean Architecture)**, popularizada por
Robert C. Martin. O objetivo é manter as **regras de negócio** independentes
de detalhes de tecnologia (framework, banco, UI), permitindo testar e evoluir
o domínio sem reescrever camadas externas.

```
                    ┌───────────────────────────────────────────┐
                    │            apresentacao/                  │
                    │  FastAPI · Pydantic · Middlewares · HTTP  │
                    └──────────────────┬────────────────────────┘
                                       │ depende de
                    ┌──────────────────▼────────────────────────┐
                    │             aplicacao/                    │
                    │   Casos de uso · DTOs · Orquestração      │
                    └──────────────────┬────────────────────────┘
                                       │ depende de
                    ┌──────────────────▼────────────────────────┐
                    │              dominio/                     │
                    │    Entidades · VOs · Regras de negócio    │
                    │    Interfaces (Portas) de repositório     │
                    └──────────────────▲────────────────────────┘
                                       │ implementa
                    ┌──────────────────┴────────────────────────┐
                    │           infraestrutura/                 │
                    │  SQLAlchemy · SQLite · JWT · Bcrypt · PDF │
                    └───────────────────────────────────────────┘
```

### Regra da dependência

> *"O fluxo de dependência aponta sempre para o domínio."*

- `dominio` **não importa de ninguém**.
- `aplicacao` importa apenas `dominio`.
- `infraestrutura` implementa interfaces de `dominio` (e pode usar `aplicacao`
  para DTOs).
- `apresentacao` importa `aplicacao` (e `infraestrutura` apenas para *wiring*
  via injeção de dependência).

## 2. Camadas

### 2.1 `dominio/`

Núcleo do sistema. Entidades de negócio (Residente, Medicamento, Prescrição,
Funcionario, Quarto, etc.), objetos de valor (CPF, Email, Endereco, Periodo)
e **portas** (interfaces de repositório) — *nenhuma* dependência de framework.

### 2.2 `aplicacao/`

Casos de uso (use cases): "Cadastrar Residente", "Registrar Aplicação de
Medicamento", "Montar Escala". Cada caso de uso recebe suas dependências por
injeção (interfaces vindas do domínio) e expõe um método público `executar`.

### 2.3 `infraestrutura/`

Implementações concretas:

- `banco_de_dados/` — modelos ORM (SQLAlchemy), sessão, migrations.
- `repositorios/` — implementações das portas do domínio (SQLAlchemy → entidade).
- `seguranca/` — bcrypt, JWT, geração de tokens.
- `servicos_externos/` — geração de PDF, e-mail (placeholder), hash.

### 2.4 `apresentacao/`

- `api/rotas/` — rotas FastAPI separadas por contexto.
- `schemas/` — modelos Pydantic de entrada e saída HTTP.
- `middlewares/` — autenticação, CORS, logging, tratamento global de erros.
- `dependencias/` — fábricas de dependências (DI) que conectam os casos de uso
  às implementações de infraestrutura.

## 3. Fluxo de uma Requisição

Exemplo: `POST /api/residentes`.

1. **Frontend** envia JSON com dados do residente.
2. `apresentacao/api/rotas/residentes.py` valida via schema Pydantic.
3. A rota chama `CadastrarResidente` (caso de uso), via Depends.
4. O caso de uso usa `RepositorioResidentes` (interface do domínio).
5. Em runtime, a interface é satisfeita por `RepositorioResidentesSQLAlchemy`
   (infraestrutura).
6. Resultado é convertido em DTO/schema e devolvido.

## 4. Persistência

- **SQLite** com modo WAL (`PRAGMA journal_mode = WAL`).
- Um arquivo único em `dados/cuidarmais.db`.
- Migrations declarativas controladas via SQLAlchemy `metadata.create_all`
  (poderia evoluir para Alembic em versão futura — ver ADR-006).

## 5. Segurança

- Autenticação via **JWT** com chave configurável (env `CHAVE_SECRETA_JWT`).
- Hashing de senha com **bcrypt** custo 12.
- RBAC declarativo via dependência `requer_papel(...)`.
- Auditoria registrada em `log_auditoria` a cada ação sensível
  (middleware/decorador).

## 6. Frontend

Implementado em HTML/CSS/JS *vanilla* (modular, ES modules). Comunica-se com
o backend via `fetch` JSON. Bibliotecas via CDN:

- FullCalendar — calendário de medicação e consultas.
- Chart.js — gráficos do dashboard e sinais vitais.
- Lucide Icons — ícones.
- SignaturePad — assinatura digital.

## 7. Testes

- `testes/unitarios/` — testes do domínio e casos de uso (sem dependências externas).
- `testes/integracao/` — testes ponta-a-ponta da API via `TestClient`.

Cobertura-alvo: 60% no domínio (RNF-33).

## 8. Observabilidade

- Logs estruturados via `logging` padrão (JSON em produção).
- Trilha de auditoria persistida em tabela.
- Endpoint `/saude` para *health check*.

## 9. Deploy

Para produção interna:

```
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 2
```

Recomendado por trás de um proxy reverso (Caddy/Nginx) com TLS e cabeçalhos
de segurança (HSTS, CSP).
