# ADR-0001 — Adoção de Arquitetura Limpa

- **Status:** Aceito
- **Data:** 2026-01-15
- **Decisores:** Equipe técnica do Cuidar+

## Contexto

O sistema gerencia operações críticas de uma ILPI (medicação, prontuário, finanças).
Precisamos de uma estrutura que permita:

- Trocar de framework HTTP sem reescrever regras de negócio.
- Trocar SQLite por Postgres no futuro, se a ILPI crescer.
- Testar regras de negócio sem subir banco/HTTP.
- Manter o código compreensível para equipe pequena.

## Decisão

Adotaremos **Arquitetura Limpa** (Clean Architecture), com quatro camadas:
`dominio`, `aplicacao`, `infraestrutura`, `apresentacao`. A regra da dependência
aponta sempre para o domínio.

## Consequências

### Positivas

- Domínio testável sem banco, sem HTTP.
- Possibilidade de troca de tecnologias em camadas externas.
- Casos de uso explicitamente nomeados, facilitando manutenção.

### Negativas

- Mais arquivos e indireção para tarefas simples.
- Curva de aprendizado para devs novos no padrão.

### Mitigações

- Documentação dos padrões em `docs/arquitetura.md`.
- Templates de caso de uso e repositório.
