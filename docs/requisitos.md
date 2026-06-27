# Requisitos do Sistema "Cuidar+"

> Documento de Especificação de Requisitos do Sistema de Gestão de Lar de Idosos.
> Versão 1.0 — 2026.

---

## 1. Atores do Sistema

| Ator | Descrição |
| --- | --- |
| Administrador | Acesso total. Gerencia usuários, perfis e configurações. |
| Médico | Acessa e edita prontuário, prescrição médica, agenda de consultas. |
| Enfermeiro | Aplica medicação, registra sinais vitais, acompanha prontuário. |
| Cuidador | Vê escala, registra atividades diárias, alimentação e medicação aplicada. |
| Nutricionista | Define cardápios, dietas individuais e restrições alimentares. |
| Financeiro | Lança receitas, despesas, mensalidades e gera relatórios. |
| Recepção | Cadastra visitantes, agendamentos e atendimentos iniciais. |

Todos são *funcionários*. Não há acesso para residentes/familiares neste produto.

---

## 2. Requisitos Funcionais (RF)

### 2.1 Autenticação & Controle de Acesso

- **RF-01** O sistema deve permitir login de funcionários com e-mail e senha.
- **RF-02** O sistema deve bloquear o login após 5 tentativas erradas em 15 min.
- **RF-03** O sistema deve permitir redefinição de senha mediante código temporário.
- **RF-04** O sistema deve registrar logout manual e expirar sessões inativas em 30 min.
- **RF-05** O sistema deve implementar controle de acesso por papel (RBAC).
- **RF-06** O sistema deve permitir ao Administrador criar, editar e desativar contas.
- **RF-07** O sistema deve forçar troca de senha no primeiro acesso.
- **RF-08** O sistema deve manter trilha de auditoria de todas as ações sensíveis.

### 2.2 Cadastro de Residentes

- **RF-09** O sistema deve permitir cadastro completo do residente (dados pessoais,
  documentos, contato de emergência, responsável legal, foto).
- **RF-10** O sistema deve listar residentes com busca por nome, CPF e quarto.
- **RF-11** O sistema deve permitir filtrar residentes por status (ativo, internado,
  licença, desligado, falecido).
- **RF-12** O sistema deve permitir editar dados cadastrais do residente.
- **RF-13** O sistema deve permitir anexar documentos digitalizados ao cadastro.
- **RF-14** O sistema deve registrar grau de dependência (escala de Katz/Lawton).
- **RF-15** O sistema deve registrar contatos de familiares e responsáveis.

### 2.3 Histórico Médico (Prontuário)

- **RF-16** O sistema deve manter prontuário eletrônico por residente.
- **RF-17** O sistema deve permitir registrar alergias, doenças crônicas e cirurgias.
- **RF-18** O sistema deve registrar sinais vitais (PA, FC, FR, SpO₂, T, glicemia).
- **RF-19** O sistema deve gerar gráficos de evolução dos sinais vitais.
- **RF-20** O sistema deve permitir anexar exames laboratoriais e de imagem.
- **RF-21** O sistema deve registrar evoluções médicas e de enfermagem com autor e data.

### 2.4 Controle de Medicamentos (Calendário)

- **RF-22** O sistema deve oferecer um calendário interativo de medicação por residente.
- **RF-23** O sistema deve permitir cadastrar prescrições (medicamento, dose, via,
  horários, frequência, início e término).
- **RF-24** O sistema deve gerar automaticamente os horários no calendário a partir
  da prescrição.
- **RF-25** O sistema deve permitir registrar a aplicação (confirmação, atraso, recusa,
  reação adversa) com responsável e horário real.
- **RF-26** O sistema deve emitir alerta visual quando a medicação estiver em atraso.
- **RF-27** O sistema deve manter um estoque de medicamentos com lote e validade.
- **RF-28** O sistema deve avisar quando o estoque estiver abaixo do mínimo.
- **RF-29** O sistema deve avisar sobre medicamentos próximos do vencimento (30 dias).
- **RF-30** O sistema deve permitir imprimir a "Folha de Medicação" do dia.

### 2.5 Agenda de Consultas

- **RF-31** O sistema deve permitir agendar consultas internas e externas.
- **RF-32** O sistema deve permitir agendar exames e procedimentos.
- **RF-33** O sistema deve enviar alerta de consultas do dia no dashboard.
- **RF-34** O sistema deve permitir cancelar e remarcar consultas com motivo.

### 2.6 Controle Financeiro

- **RF-35** O sistema deve registrar mensalidades por residente.
- **RF-36** O sistema deve registrar receitas e despesas com categoria e centro de custo.
- **RF-37** O sistema deve gerar relatório de inadimplência.
- **RF-38** O sistema deve gerar fluxo de caixa diário, mensal e anual.
- **RF-39** O sistema deve permitir emitir recibos em PDF.
- **RF-40** O sistema deve permitir registrar formas de pagamento (PIX, boleto, dinheiro, cartão).

### 2.7 Gestão de Funcionários

- **RF-41** O sistema deve permitir cadastro de funcionários com cargo, CPF, contato,
  data de admissão e jornada.
- **RF-42** O sistema deve permitir anexar contratos e documentos do funcionário.
- **RF-43** O sistema deve permitir desligar funcionários (mantendo histórico).
- **RF-44** O sistema deve registrar férias, afastamentos e atestados.

### 2.8 Escalas de Cuidadores

- **RF-45** O sistema deve permitir montar escalas semanais e mensais por turno
  (manhã, tarde, noite, plantão 12x36).
- **RF-46** O sistema deve impedir conflito de horários para o mesmo funcionário.
- **RF-47** O sistema deve calcular horas trabalhadas e horas extras.
- **RF-48** O sistema deve permitir trocas de turno mediante aprovação do supervisor.
- **RF-49** O sistema deve enviar notificações de início de turno (no painel).

### 2.9 Controle de Alimentação

- **RF-50** O sistema deve permitir cadastrar cardápios diários e semanais.
- **RF-51** O sistema deve permitir definir dietas individuais (hipossódica,
  diabética, pastosa, líquida, enteral, etc.).
- **RF-52** O sistema deve registrar restrições e alergias alimentares por residente.
- **RF-53** O sistema deve registrar refeições servidas e aceitação do residente.
- **RF-54** O sistema deve permitir registrar ingestão hídrica diária.

### 2.10 Controle de Quartos

- **RF-55** O sistema deve cadastrar quartos com capacidade, tipo (individual,
  duplo, enfermaria) e leitos.
- **RF-56** O sistema deve permitir alocar residentes em leitos.
- **RF-57** O sistema deve exibir mapa visual de ocupação dos quartos.
- **RF-58** O sistema deve registrar manutenção de quartos (status).
- **RF-59** O sistema deve manter histórico de transferências entre quartos.

### 2.11 Assinatura Digital de Documentos

- **RF-60** O sistema deve gerar documentos em PDF (termos, recibos, prescrições,
  declarações) a partir de modelos.
- **RF-61** O sistema deve permitir capturar assinatura via canvas (mouse/touch).
- **RF-62** O sistema deve incorporar a assinatura ao PDF com data/hora e responsável.
- **RF-63** O sistema deve gerar hash SHA-256 do documento assinado para conferência.
- **RF-64** O sistema deve manter repositório dos documentos assinados.

### 2.12 Dashboard, Relatórios e Outros

- **RF-65** O sistema deve oferecer um dashboard com indicadores em tempo real:
  total de residentes, ocupação, medicações do dia, consultas do dia, aniversariantes.
- **RF-66** O sistema deve permitir exportar listagens em CSV.
- **RF-67** O sistema deve permitir busca global (residentes, funcionários, quartos).
- **RF-68** O sistema deve permitir registrar visitas externas (familiares) com data,
  hora e identificação.
- **RF-69** O sistema deve permitir cadastro de fornecedores.
- **RF-70** O sistema deve permitir registrar ocorrências (quedas, intercorrências).

---

## 3. Requisitos Não Funcionais (RNF)

### 3.1 Usabilidade

- **RNF-01** A interface deve usar idioma 100% em português brasileiro.
- **RNF-02** A interface deve seguir um design system consistente (tipografia, cores).
- **RNF-03** Toda ação destrutiva deve exigir confirmação.
- **RNF-04** O sistema deve apresentar mensagens de erro claras e amigáveis.
- **RNF-05** O sistema deve oferecer atalhos de teclado para ações frequentes.
- **RNF-06** O calendário de medicação deve permitir filtros por residente e por dia.
- **RNF-07** O sistema deve oferecer modo claro e modo escuro.
- **RNF-08** Formulários longos devem ser divididos em abas/etapas.
- **RNF-09** A interface deve indicar progresso (loading) em todas as requisições.

### 3.2 Desempenho

- **RNF-10** Operações comuns devem responder em até 300 ms localmente.
- **RNF-11** A página de calendário deve carregar até 60 dias em até 1 segundo.
- **RNF-12** O sistema deve suportar até 200 residentes simultâneos sem degradação.
- **RNF-13** O backend deve usar `WAL mode` no SQLite para concorrência.
- **RNF-14** Consultas frequentes devem usar índices apropriados.

### 3.3 Confiabilidade & Integridade

- **RNF-15** O banco deve usar transações em todas as operações multi-tabela.
- **RNF-16** O sistema deve realizar backup automático diário do SQLite.
- **RNF-17** O sistema não deve permitir exclusão física de registros médicos
  (soft delete).
- **RNF-18** Falhas no servidor não devem corromper o banco (uso de WAL + sync).
- **RNF-19** Logs estruturados devem ser gerados em todas as camadas.

### 3.4 Segurança

- **RNF-20** Senhas devem ser armazenadas com bcrypt (custo ≥ 12).
- **RNF-21** Autenticação deve usar JWT assinado com chave de 256 bits.
- **RNF-22** Tokens devem expirar em até 30 minutos.
- **RNF-23** O sistema deve aplicar CORS restritivo.
- **RNF-24** O sistema deve mitigar XSS (sanitização em entradas e saídas).
- **RNF-25** O sistema deve usar prepared statements (proteção SQL injection).
- **RNF-26** O sistema deve usar CSP (Content Security Policy).
- **RNF-27** Senha deve seguir política mínima (8 caracteres, mista).
- **RNF-28** Trilha de auditoria deve ser imutável (append-only).
- **RNF-29** O sistema deve registrar IP e user-agent nos logs de login.
- **RNF-30** O sistema deve oferecer logout em todos os dispositivos.

### 3.5 Manutenibilidade

- **RNF-31** O código deve seguir Arquitetura Limpa, separando regras de negócio.
- **RNF-32** O código deve estar 100% em português (variáveis, classes, comentários).
- **RNF-33** O projeto deve manter cobertura de testes ≥ 60% no domínio.
- **RNF-34** O projeto deve seguir PEP-8 (formatação com `ruff`).
- **RNF-35** Cada camada não deve importar de camada mais externa (regra da dependência).
- **RNF-36** Documentação de API gerada automaticamente (OpenAPI/Swagger).
- **RNF-37** ADRs devem ser registrados para toda decisão estrutural.

### 3.6 Portabilidade

- **RNF-38** O sistema deve rodar em Windows, Linux e macOS.
- **RNF-39** O sistema deve rodar com Python 3.11+ sem dependências nativas pesadas.
- **RNF-40** O banco deve ser portável (arquivo único SQLite).

### 3.7 Disponibilidade

- **RNF-41** O sistema deve manter uptime ≥ 99% em horário comercial.
- **RNF-42** O sistema deve reiniciar automaticamente em caso de falha (systemd/NSSM).

### 3.8 Compatibilidade

- **RNF-43** A interface deve suportar Chrome, Firefox e Edge (últimas 2 versões).
- **RNF-44** A interface deve ser responsiva (desktop, tablet e celular).

### 3.9 Acessibilidade

- **RNF-45** A interface deve seguir diretrizes WCAG 2.1 nível AA.
- **RNF-46** Contraste mínimo de 4.5:1 entre texto e fundo.
- **RNF-47** Todos os campos devem ter `label` associado.
- **RNF-48** Navegação completa via teclado deve ser possível.

### 3.10 Auditoria & Conformidade

- **RNF-49** O sistema deve permitir exportar a trilha de auditoria.
- **RNF-50** Dados pessoais devem seguir princípios da LGPD (minimização, finalidade).
- **RNF-51** O sistema deve registrar consentimento de uso de imagem do residente.
- **RNF-52** Documentos assinados devem ter hash verificável.

### 3.11 Internacionalização

- **RNF-53** Datas no padrão `DD/MM/AAAA HH:mm` e fuso `America/Sao_Paulo`.
- **RNF-54** Valores monetários em Real (R$) com duas casas decimais.

---

## 4. Restrições

- **R-01** O sistema só é acessível por funcionários autenticados.
- **R-02** O banco de dados deve ser SQLite, acessado localmente.
- **R-03** O backend deve ser escrito em Python.
- **R-04** O código deve estar inteiramente em português.
- **R-05** O projeto deve adotar Arquitetura Limpa.
