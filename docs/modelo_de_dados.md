# Modelo de Dados — Cuidar+

Resumo das tabelas principais. (Diagrama ER detalhado em `docs/diagramas/`.)

## Núcleo

| Tabela | Descrição |
| --- | --- |
| `funcionarios` | Funcionários (usuários do sistema). |
| `papeis` | Papéis (roles) RBAC. |
| `funcionarios_papeis` | Pivot funcionário ↔ papel. |
| `residentes` | Residentes do lar. |
| `responsaveis` | Familiares / responsáveis legais. |
| `residentes_responsaveis` | Pivot residente ↔ responsável. |

## Quartos

| Tabela | Descrição |
| --- | --- |
| `quartos` | Quartos físicos. |
| `leitos` | Leitos dentro dos quartos. |
| `alocacoes_leito` | Histórico de alocação de residente em leito. |

## Medicação

| Tabela | Descrição |
| --- | --- |
| `medicamentos` | Catálogo de medicamentos. |
| `estoque_medicamentos` | Lote, validade, quantidade. |
| `prescricoes` | Prescrição médica de um residente. |
| `horarios_prescricao` | Horários gerados para cada prescrição. |
| `aplicacoes_medicamento` | Cada aplicação realizada (ou recusada). |

## Prontuário

| Tabela | Descrição |
| --- | --- |
| `historicos_medicos` | Cabeçalho do prontuário. |
| `alergias` | Alergias por residente. |
| `condicoes_cronicas` | Doenças crônicas. |
| `sinais_vitais` | Aferições. |
| `evolucoes` | Notas de evolução (médica / enfermagem). |
| `consultas` | Agenda de consultas / exames. |
| `exames_anexos` | PDFs / imagens. |

## Alimentação

| Tabela | Descrição |
| --- | --- |
| `cardapios` | Cardápios diários. |
| `refeicoes_servidas` | Refeições servidas com aceitação. |
| `dietas` | Dietas individuais. |
| `restricoes_alimentares` | Restrições por residente. |
| `ingestao_hidrica` | Registros de hidratação. |

## Escalas

| Tabela | Descrição |
| --- | --- |
| `escalas` | Escala (cabeçalho — mês/turno). |
| `turnos` | Turnos atribuídos. |
| `trocas_turno` | Solicitações de troca. |

## Financeiro

| Tabela | Descrição |
| --- | --- |
| `mensalidades` | Mensalidades por residente. |
| `lancamentos_financeiros` | Receitas e despesas. |
| `categorias_financeiras` | Categorias. |
| `fornecedores` | Fornecedores. |

## Documentos

| Tabela | Descrição |
| --- | --- |
| `modelos_documento` | Templates (termos, recibos). |
| `documentos_assinados` | Documentos gerados e assinados. |

## Operacional

| Tabela | Descrição |
| --- | --- |
| `visitas` | Visitas externas registradas. |
| `ocorrencias` | Quedas, intercorrências. |
| `log_auditoria` | Trilha de auditoria. |
| `tokens_revogados` | JWTs revogados. |
| `tentativas_login` | Anti-bruteforce. |
