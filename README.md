# Sistema de Gestão de Lar de Idosos — "Cuidar+"

Sistema interno de gestão para Lares de Idosos (Casas de Repouso / ILPI — Instituições
de Longa Permanência para Idosos). Acesso exclusivo de funcionários autorizados.

## Visão Geral

O **Cuidar+** centraliza, em um único produto, todas as operações de uma instituição
de cuidado a idosos: cadastro de residentes, prontuário/histórico médico, controle
diário de medicamentos (com calendário interativo), agenda de consultas, gestão
financeira, gestão de funcionários, escalas de cuidadores, controle de alimentação,
gestão de quartos e assinatura digital de documentos.

## Tecnologias

| Camada | Tecnologia |
| --- | --- |
| Linguagem backend | Python 3.11+ |
| Framework HTTP | FastAPI |
| Banco de dados | SQLite (acesso local) |
| ORM | SQLAlchemy 2.x |
| Autenticação | JWT (PyJWT) + Bcrypt |
| Frontend | HTML5 + CSS3 + JavaScript (Vanilla, modular) |
| Calendário | FullCalendar (CDN) |
| Gráficos | Chart.js (CDN) |
| Ícones | Lucide Icons |

## Arquitetura

Adotamos **Arquitetura Limpa (Clean Architecture)** com quatro camadas independentes
e dependências apontando sempre para o domínio:

```
apresentacao ──▶ aplicacao ──▶ dominio ◀── infraestrutura
```

- `dominio/` — Entidades, regras de negócio puras e interfaces de repositório
- `aplicacao/` — Casos de uso (orquestra o domínio), DTOs e contratos de serviços
- `infraestrutura/` — Implementações concretas: banco, segurança, e-mail, PDFs
- `apresentacao/` — API FastAPI, schemas Pydantic, middlewares, dependências

Veja [`docs/arquitetura.md`](docs/arquitetura.md) e os
[ADRs](docs/adrs/) para detalhes.

## Como executar

```bash
# 1. Crie um ambiente virtual
python -m venv .venv
.venv\Scripts\activate             # Windows

# 2. Instale as dependências
pip install -r backend/requirements.txt

# 3. Crie o banco e o usuário administrador padrão
python -m backend.scripts.inicializar_banco

# 3b. (Opcional) Popule o banco com dados fictícios de demonstração
python -m backend.scripts.popular_dados_ficticios
# Para apagar e repopular do zero: RECRIAR=1 python -m backend.scripts.popular_dados_ficticios

# 4. Suba o servidor
uvicorn backend.main:app --reload --port 8000

# 5. Abra no navegador
# http://localhost:8000
```

Credencial padrão criada pelo script de inicialização:

- **Usuário:** `admin@cuidarmais.com.br`
- **Senha:** `Admin@2026` (altere no primeiro acesso)

Os dados fictícios criam também funcionários de demonstração (médicos, enfermeiros,
cuidadores, nutricionista, financeiro e recepção), todos com a senha `Cuidar@2026`.
Exemplo: `patricia.nogueira@cuidarmais.com.br` / `Cuidar@2026`.

## Estrutura de pastas

```
.
├── backend/
│   ├── dominio/              # Núcleo do negócio (sem dependências externas)
│   ├── aplicacao/            # Casos de uso
│   ├── infraestrutura/       # Banco, segurança, serviços externos
│   ├── apresentacao/         # API HTTP (FastAPI)
│   ├── scripts/              # Scripts utilitários (inicialização, seeds)
│   ├── testes/
│   ├── main.py
│   └── requirements.txt
├── frontend/                 # Cliente web (servido pelo FastAPI)
├── docs/                     # Requisitos, arquitetura, ADRs, manuais
├── dados/                    # Diretório do arquivo SQLite (criado em runtime)
└── README.md
```

## Documentação

- [Requisitos Funcionais e Não Funcionais](docs/requisitos.md)
- [Arquitetura](docs/arquitetura.md)
- [Manual do Usuário](docs/manual_do_usuario.md)
- [Decisões Arquiteturais (ADRs)](docs/adrs/)
- [Modelo de Dados](docs/modelo_de_dados.md)

## Segurança

- Senhas armazenadas com **bcrypt** (custo 12)
- Autenticação via **JWT** com expiração curta + refresh token
- Controle de acesso por **perfil/papel** (RBAC): Administrador, Enfermeiro,
  Cuidador, Nutricionista, Médico, Financeiro, Recepção
- Trilha de auditoria (`tabela log_auditoria`) registra criações, edições e exclusões
- Senhas com política mínima (8+ caracteres, maiúscula, minúscula, número, símbolo)
- Bloqueio de conta após 5 tentativas erradas em 15 minutos
- Sessão expira por inatividade (30 min)
- Validação de entrada em todos os endpoints via Pydantic
- HTTPS recomendado em produção (reverse proxy Nginx/Caddy)

## Licença

Uso interno. Todos os direitos reservados.
