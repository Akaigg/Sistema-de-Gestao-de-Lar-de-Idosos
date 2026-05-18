# Manual do Usuário — Cuidar+

## 1. Acesso ao sistema

1. Abra o navegador em `http://localhost:8000`.
2. Informe seu **e-mail corporativo** e sua **senha**.
3. No primeiro acesso, o sistema solicita a troca da senha padrão.

## 2. Painel inicial (Dashboard)

Exibe:
- Total de residentes ativos.
- Ocupação dos quartos.
- Medicamentos previstos para hoje.
- Consultas agendadas para hoje.
- Aniversariantes do mês.
- Atalhos rápidos (cadastrar residente, registrar ocorrência, etc.).

## 3. Residentes

- **Cadastrar:** menu lateral → **Residentes** → **Novo**.
- **Editar:** clique no card do residente → aba **Cadastro**.
- **Prontuário:** clique no residente → aba **Prontuário**.
- **Quarto/Leito:** aba **Alocação**.

## 4. Calendário de Medicação

- Acesse **Medicação → Calendário**.
- Filtre por residente / período (dia / semana / mês).
- Clique em um horário para registrar **aplicação** ou **recusa**.
- Cores:
  - 🟢 Aplicado no horário
  - 🟡 Aplicado com atraso
  - 🔴 Em atraso / não aplicado
  - ⚪ Aguardando horário
  - ⚫ Recusado / Suspenso

## 5. Consultas

- Menu **Agenda → Consultas**.
- Botão **Novo agendamento**.
- O dashboard alerta sobre consultas do dia.

## 6. Escalas

- Menu **Funcionários → Escalas**.
- Selecione o mês e clique nos turnos para atribuir cuidadores.
- O sistema impede sobreposição.

## 7. Alimentação

- **Cardápios:** Menu **Alimentação → Cardápios**.
- **Dietas individuais:** dentro do residente → aba **Nutrição**.
- **Registro de refeição:** Menu **Alimentação → Servir refeição**.

## 8. Quartos

- Mapa em **Quartos → Mapa de ocupação**.
- Clique no quarto para ver leitos.
- Arraste e solte residentes para realocar (com confirmação).

## 9. Financeiro

- **Mensalidades** — vincule valores ao residente.
- **Lançamentos** — registre entradas e saídas.
- **Relatórios** — fluxo de caixa e inadimplência.

## 10. Assinatura digital

- Em qualquer documento gerado, clique em **Assinar**.
- Use o mouse ou toque para desenhar a assinatura.
- O sistema grava o PDF com o hash SHA-256 e o nome do funcionário responsável.

## 11. Trilha de auditoria

- Apenas Administradores acessam **Configurações → Auditoria**.
- Filtros por usuário, data, ação.
