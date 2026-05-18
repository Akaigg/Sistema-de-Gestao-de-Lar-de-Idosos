"""Funções utilitárias de conversão entre Modelos ORM e Entidades de Domínio."""

from __future__ import annotations

from datetime import time
from typing import Optional

from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.dominio.entidades.residente import (
    Residente,
    StatusResidente,
    GrauDependencia,
)
from backend.dominio.entidades.responsavel import Responsavel
from backend.dominio.entidades.quarto import (
    Quarto,
    Leito,
    TipoQuarto,
    StatusQuarto,
    StatusLeito,
)
from backend.dominio.entidades.medicamento import (
    Medicamento,
    Prescricao,
    AplicacaoMedicamento,
    LoteMedicamento,
    StatusAplicacao,
    ViaAdministracao,
)
from backend.dominio.entidades.prontuario import (
    SinaisVitais,
    Evolucao,
    Alergia,
    CondicaoCronica,
    Consulta,
    StatusConsulta,
    TipoConsulta,
)
from backend.dominio.entidades.alimentacao import (
    Cardapio,
    Dieta,
    Refeicao,
    IngestaoHidrica,
    TipoRefeicao,
    TipoDieta,
)
from backend.dominio.entidades.escala import Escala, Turno, TipoTurno
from backend.dominio.entidades.financeiro import (
    Mensalidade,
    LancamentoFinanceiro,
    StatusPagamento,
    FormaPagamento,
    TipoLancamento,
)
from backend.dominio.entidades.documento import DocumentoAssinado, ModeloDocumento
from backend.dominio.entidades.ocorrencia import (
    Ocorrencia,
    TipoOcorrencia,
    GravidadeOcorrencia,
)
from backend.dominio.entidades.visita import Visita
from backend.dominio.entidades.auditoria import LogAuditoria

from backend.infraestrutura.banco_de_dados.modelos import (
    FuncionarioModel,
    PapelFuncionarioModel,
    ResidenteModel,
    ResponsavelModel,
    QuartoModel,
    LeitoModel,
    MedicamentoModel,
    PrescricaoModel,
    AplicacaoMedicamentoModel,
    LoteMedicamentoModel,
    SinaisVitaisModel,
    EvolucaoModel,
    AlergiaModel,
    CondicaoCronicaModel,
    ConsultaModel,
    CardapioModel,
    DietaModel,
    RefeicaoModel,
    IngestaoHidricaModel,
    EscalaModel,
    TurnoModel,
    MensalidadeModel,
    LancamentoFinanceiroModel,
    ModeloDocumentoModel,
    DocumentoAssinadoModel,
    OcorrenciaModel,
    VisitaModel,
    LogAuditoriaModel,
)


def _horarios_csv_para_lista(csv: str) -> list[time]:
    horarios: list[time] = []
    for h in csv.split(","):
        h = h.strip()
        if not h:
            continue
        hora, minuto = h.split(":")
        horarios.append(time(int(hora), int(minuto)))
    return horarios


def _horarios_lista_para_csv(horarios: list[time]) -> str:
    return ",".join(f"{h.hour:02d}:{h.minute:02d}" for h in horarios)


# -------- Funcionário --------

def funcionario_para_entidade(modelo: FuncionarioModel) -> Funcionario:
    return Funcionario(
        identificador=modelo.id,
        nome_completo=modelo.nome_completo,
        email=modelo.email,
        senha_hash=modelo.senha_hash,
        cpf=modelo.cpf,
        cargo=modelo.cargo,
        telefone=modelo.telefone,
        data_admissao=modelo.data_admissao,
        data_desligamento=modelo.data_desligamento,
        ativo=modelo.ativo,
        deve_trocar_senha=modelo.deve_trocar_senha,
        ultimo_acesso=modelo.ultimo_acesso,
        papeis=[PapelFuncionario(p.papel) for p in modelo.papeis],
    )


def funcionario_para_modelo(entidade: Funcionario, modelo: Optional[FuncionarioModel] = None) -> FuncionarioModel:
    modelo = modelo or FuncionarioModel()
    modelo.nome_completo = entidade.nome_completo
    modelo.email = entidade.email
    modelo.senha_hash = entidade.senha_hash
    modelo.cpf = entidade.cpf
    modelo.cargo = entidade.cargo
    modelo.telefone = entidade.telefone
    modelo.data_admissao = entidade.data_admissao
    modelo.data_desligamento = entidade.data_desligamento
    modelo.ativo = entidade.ativo
    modelo.deve_trocar_senha = entidade.deve_trocar_senha
    modelo.ultimo_acesso = entidade.ultimo_acesso
    return modelo


# -------- Residente --------

def residente_para_entidade(modelo: ResidenteModel) -> Residente:
    return Residente(
        identificador=modelo.id,
        nome_completo=modelo.nome_completo,
        data_nascimento=modelo.data_nascimento,
        cpf=modelo.cpf,
        sexo=modelo.sexo,
        data_entrada=modelo.data_entrada,
        grau_dependencia=GrauDependencia(modelo.grau_dependencia),
        status=StatusResidente(modelo.status),
        rg=modelo.rg,
        cartao_sus=modelo.cartao_sus,
        convenio=modelo.convenio,
        numero_convenio=modelo.numero_convenio,
        religiao=modelo.religiao,
        estado_civil=modelo.estado_civil,
        naturalidade=modelo.naturalidade,
        profissao_anterior=modelo.profissao_anterior,
        observacoes=modelo.observacoes,
        foto_caminho=modelo.foto_caminho,
        consentimento_imagem=modelo.consentimento_imagem,
        data_saida=modelo.data_saida,
        motivo_saida=modelo.motivo_saida,
    )


def residente_para_modelo(entidade: Residente, modelo: Optional[ResidenteModel] = None) -> ResidenteModel:
    modelo = modelo or ResidenteModel()
    modelo.nome_completo = entidade.nome_completo
    modelo.data_nascimento = entidade.data_nascimento
    modelo.cpf = entidade.cpf
    modelo.sexo = entidade.sexo
    modelo.data_entrada = entidade.data_entrada
    modelo.grau_dependencia = entidade.grau_dependencia.value
    modelo.status = entidade.status.value
    modelo.rg = entidade.rg
    modelo.cartao_sus = entidade.cartao_sus
    modelo.convenio = entidade.convenio
    modelo.numero_convenio = entidade.numero_convenio
    modelo.religiao = entidade.religiao
    modelo.estado_civil = entidade.estado_civil
    modelo.naturalidade = entidade.naturalidade
    modelo.profissao_anterior = entidade.profissao_anterior
    modelo.observacoes = entidade.observacoes
    modelo.foto_caminho = entidade.foto_caminho
    modelo.consentimento_imagem = entidade.consentimento_imagem
    modelo.data_saida = entidade.data_saida
    modelo.motivo_saida = entidade.motivo_saida
    return modelo


# -------- Responsável --------

def responsavel_para_entidade(modelo: ResponsavelModel) -> Responsavel:
    return Responsavel(
        identificador=modelo.id,
        nome_completo=modelo.nome_completo,
        cpf=modelo.cpf,
        parentesco=modelo.parentesco,
        telefone=modelo.telefone,
        email=modelo.email,
        endereco_resumido=modelo.endereco_resumido,
        eh_responsavel_legal=modelo.eh_responsavel_legal,
        eh_contato_emergencia=modelo.eh_contato_emergencia,
        observacoes=modelo.observacoes,
    )


def responsavel_para_modelo(entidade: Responsavel, modelo: Optional[ResponsavelModel] = None) -> ResponsavelModel:
    modelo = modelo or ResponsavelModel()
    modelo.nome_completo = entidade.nome_completo
    modelo.cpf = entidade.cpf
    modelo.parentesco = entidade.parentesco
    modelo.telefone = entidade.telefone
    modelo.email = entidade.email
    modelo.endereco_resumido = entidade.endereco_resumido
    modelo.eh_responsavel_legal = entidade.eh_responsavel_legal
    modelo.eh_contato_emergencia = entidade.eh_contato_emergencia
    modelo.observacoes = entidade.observacoes
    return modelo


# -------- Quarto / Leito --------

def leito_para_entidade(modelo: LeitoModel) -> Leito:
    return Leito(
        identificador=modelo.id,
        numero=modelo.numero,
        status=StatusLeito(modelo.status),
        residente_id=modelo.residente_id,
        observacoes=modelo.observacoes,
    )


def quarto_para_entidade(modelo: QuartoModel) -> Quarto:
    return Quarto(
        identificador=modelo.id,
        numero=modelo.numero,
        andar=modelo.andar,
        tipo=TipoQuarto(modelo.tipo),
        capacidade=modelo.capacidade,
        status=StatusQuarto(modelo.status),
        possui_banheiro=modelo.possui_banheiro,
        possui_ar_condicionado=modelo.possui_ar_condicionado,
        acessibilidade=modelo.acessibilidade,
        observacoes=modelo.observacoes,
        leitos=[leito_para_entidade(l) for l in modelo.leitos],
    )


def quarto_para_modelo(entidade: Quarto, modelo: Optional[QuartoModel] = None) -> QuartoModel:
    modelo = modelo or QuartoModel()
    modelo.numero = entidade.numero
    modelo.andar = entidade.andar
    modelo.tipo = entidade.tipo.value
    modelo.capacidade = entidade.capacidade
    modelo.status = entidade.status.value
    modelo.possui_banheiro = entidade.possui_banheiro
    modelo.possui_ar_condicionado = entidade.possui_ar_condicionado
    modelo.acessibilidade = entidade.acessibilidade
    modelo.observacoes = entidade.observacoes
    return modelo


# -------- Medicamento --------

def medicamento_para_entidade(modelo: MedicamentoModel) -> Medicamento:
    return Medicamento(
        identificador=modelo.id,
        nome_comercial=modelo.nome_comercial,
        principio_ativo=modelo.principio_ativo,
        forma_farmaceutica=modelo.forma_farmaceutica,
        concentracao=modelo.concentracao,
        fabricante=modelo.fabricante,
        necessita_receita=modelo.necessita_receita,
        controlado=modelo.controlado,
        estoque_minimo=modelo.estoque_minimo,
        observacoes=modelo.observacoes,
    )


def medicamento_para_modelo(entidade: Medicamento, modelo: Optional[MedicamentoModel] = None) -> MedicamentoModel:
    modelo = modelo or MedicamentoModel()
    modelo.nome_comercial = entidade.nome_comercial
    modelo.principio_ativo = entidade.principio_ativo
    modelo.forma_farmaceutica = entidade.forma_farmaceutica
    modelo.concentracao = entidade.concentracao
    modelo.fabricante = entidade.fabricante
    modelo.necessita_receita = entidade.necessita_receita
    modelo.controlado = entidade.controlado
    modelo.estoque_minimo = entidade.estoque_minimo
    modelo.observacoes = entidade.observacoes
    return modelo


def lote_para_entidade(modelo: LoteMedicamentoModel) -> LoteMedicamento:
    return LoteMedicamento(
        identificador=modelo.id,
        medicamento_id=modelo.medicamento_id,
        numero_lote=modelo.numero_lote,
        quantidade=modelo.quantidade,
        data_validade=modelo.data_validade,
        data_entrada=modelo.data_entrada,
        fornecedor=modelo.fornecedor,
        preco_unitario=modelo.preco_unitario,
    )


def lote_para_modelo(entidade: LoteMedicamento, modelo: Optional[LoteMedicamentoModel] = None) -> LoteMedicamentoModel:
    modelo = modelo or LoteMedicamentoModel()
    modelo.medicamento_id = entidade.medicamento_id
    modelo.numero_lote = entidade.numero_lote
    modelo.quantidade = entidade.quantidade
    modelo.data_validade = entidade.data_validade
    modelo.data_entrada = entidade.data_entrada
    modelo.fornecedor = entidade.fornecedor
    modelo.preco_unitario = entidade.preco_unitario
    return modelo


def prescricao_para_entidade(modelo: PrescricaoModel) -> Prescricao:
    return Prescricao(
        identificador=modelo.id,
        residente_id=modelo.residente_id,
        medicamento_id=modelo.medicamento_id,
        medico_id=modelo.medico_id,
        dose=modelo.dose,
        via=ViaAdministracao(modelo.via),
        frequencia_horas=modelo.frequencia_horas,
        horarios=_horarios_csv_para_lista(modelo.horarios_csv),
        data_inicio=modelo.data_inicio,
        duracao_dias=modelo.duracao_dias,
        se_necessario=modelo.se_necessario,
        observacoes=modelo.observacoes,
        suspensa=modelo.suspensa,
        data_suspensao=modelo.data_suspensao,
        motivo_suspensao=modelo.motivo_suspensao,
    )


def prescricao_para_modelo(entidade: Prescricao, modelo: Optional[PrescricaoModel] = None) -> PrescricaoModel:
    modelo = modelo or PrescricaoModel()
    modelo.residente_id = entidade.residente_id
    modelo.medicamento_id = entidade.medicamento_id
    modelo.medico_id = entidade.medico_id
    modelo.dose = entidade.dose
    modelo.via = entidade.via.value
    modelo.frequencia_horas = entidade.frequencia_horas
    modelo.horarios_csv = _horarios_lista_para_csv(entidade.horarios)
    modelo.data_inicio = entidade.data_inicio
    modelo.duracao_dias = entidade.duracao_dias
    modelo.se_necessario = entidade.se_necessario
    modelo.observacoes = entidade.observacoes
    modelo.suspensa = entidade.suspensa
    modelo.data_suspensao = entidade.data_suspensao
    modelo.motivo_suspensao = entidade.motivo_suspensao
    return modelo


def aplicacao_para_entidade(modelo: AplicacaoMedicamentoModel) -> AplicacaoMedicamento:
    return AplicacaoMedicamento(
        identificador=modelo.id,
        prescricao_id=modelo.prescricao_id,
        horario_previsto=modelo.horario_previsto,
        status=StatusAplicacao(modelo.status),
        horario_aplicado=modelo.horario_aplicado,
        funcionario_id=modelo.funcionario_id,
        observacoes=modelo.observacoes,
        motivo_recusa=modelo.motivo_recusa,
        reacao_descrita=modelo.reacao_descrita,
    )


def aplicacao_para_modelo(entidade: AplicacaoMedicamento, modelo: Optional[AplicacaoMedicamentoModel] = None) -> AplicacaoMedicamentoModel:
    modelo = modelo or AplicacaoMedicamentoModel()
    modelo.prescricao_id = entidade.prescricao_id
    modelo.horario_previsto = entidade.horario_previsto
    modelo.status = entidade.status.value
    modelo.horario_aplicado = entidade.horario_aplicado
    modelo.funcionario_id = entidade.funcionario_id
    modelo.observacoes = entidade.observacoes
    modelo.motivo_recusa = entidade.motivo_recusa
    modelo.reacao_descrita = entidade.reacao_descrita
    return modelo


# -------- Prontuário --------

def sinais_para_entidade(modelo: SinaisVitaisModel) -> SinaisVitais:
    return SinaisVitais(
        identificador=modelo.id,
        residente_id=modelo.residente_id,
        aferido_em=modelo.aferido_em,
        funcionario_id=modelo.funcionario_id,
        pressao_sistolica=modelo.pressao_sistolica,
        pressao_diastolica=modelo.pressao_diastolica,
        frequencia_cardiaca=modelo.frequencia_cardiaca,
        frequencia_respiratoria=modelo.frequencia_respiratoria,
        temperatura=modelo.temperatura,
        saturacao_oxigenio=modelo.saturacao_oxigenio,
        glicemia=modelo.glicemia,
        peso=modelo.peso,
        observacoes=modelo.observacoes,
    )


def sinais_para_modelo(e: SinaisVitais, m: Optional[SinaisVitaisModel] = None) -> SinaisVitaisModel:
    m = m or SinaisVitaisModel()
    m.residente_id = e.residente_id
    m.aferido_em = e.aferido_em
    m.funcionario_id = e.funcionario_id
    m.pressao_sistolica = e.pressao_sistolica
    m.pressao_diastolica = e.pressao_diastolica
    m.frequencia_cardiaca = e.frequencia_cardiaca
    m.frequencia_respiratoria = e.frequencia_respiratoria
    m.temperatura = e.temperatura
    m.saturacao_oxigenio = e.saturacao_oxigenio
    m.glicemia = e.glicemia
    m.peso = e.peso
    m.observacoes = e.observacoes
    return m


def evolucao_para_entidade(m: EvolucaoModel) -> Evolucao:
    return Evolucao(
        identificador=m.id,
        residente_id=m.residente_id,
        funcionario_id=m.funcionario_id,
        registrada_em=m.registrada_em,
        categoria=m.categoria,
        texto=m.texto,
    )


def evolucao_para_modelo(e: Evolucao, m: Optional[EvolucaoModel] = None) -> EvolucaoModel:
    m = m or EvolucaoModel()
    m.residente_id = e.residente_id
    m.funcionario_id = e.funcionario_id
    m.registrada_em = e.registrada_em
    m.categoria = e.categoria
    m.texto = e.texto
    return m


def alergia_para_entidade(m: AlergiaModel) -> Alergia:
    return Alergia(
        identificador=m.id,
        residente_id=m.residente_id,
        substancia=m.substancia,
        reacao=m.reacao,
        gravidade=m.gravidade,
        observacoes=m.observacoes,
    )


def alergia_para_modelo(e: Alergia, m: Optional[AlergiaModel] = None) -> AlergiaModel:
    m = m or AlergiaModel()
    m.residente_id = e.residente_id
    m.substancia = e.substancia
    m.reacao = e.reacao
    m.gravidade = e.gravidade
    m.observacoes = e.observacoes
    return m


def condicao_para_entidade(m: CondicaoCronicaModel) -> CondicaoCronica:
    return CondicaoCronica(
        identificador=m.id,
        residente_id=m.residente_id,
        descricao=m.descricao,
        cid10=m.cid10,
        data_diagnostico=m.data_diagnostico,
        observacoes=m.observacoes,
    )


def condicao_para_modelo(e: CondicaoCronica, m: Optional[CondicaoCronicaModel] = None) -> CondicaoCronicaModel:
    m = m or CondicaoCronicaModel()
    m.residente_id = e.residente_id
    m.descricao = e.descricao
    m.cid10 = e.cid10
    m.data_diagnostico = e.data_diagnostico
    m.observacoes = e.observacoes
    return m


def consulta_para_entidade(m: ConsultaModel) -> Consulta:
    return Consulta(
        identificador=m.id,
        residente_id=m.residente_id,
        tipo=TipoConsulta(m.tipo),
        data_hora=m.data_hora,
        eh_externa=m.eh_externa,
        profissional=m.profissional,
        especialidade=m.especialidade,
        local=m.local,
        motivo=m.motivo,
        observacoes=m.observacoes,
        status=StatusConsulta(m.status),
        motivo_cancelamento=m.motivo_cancelamento,
        funcionario_acompanhante_id=m.funcionario_acompanhante_id,
    )


def consulta_para_modelo(e: Consulta, m: Optional[ConsultaModel] = None) -> ConsultaModel:
    m = m or ConsultaModel()
    m.residente_id = e.residente_id
    m.tipo = e.tipo.value
    m.data_hora = e.data_hora
    m.eh_externa = e.eh_externa
    m.profissional = e.profissional
    m.especialidade = e.especialidade
    m.local = e.local
    m.motivo = e.motivo
    m.observacoes = e.observacoes
    m.status = e.status.value
    m.motivo_cancelamento = e.motivo_cancelamento
    m.funcionario_acompanhante_id = e.funcionario_acompanhante_id
    return m


# -------- Alimentação --------

def cardapio_para_entidade(m: CardapioModel) -> Cardapio:
    return Cardapio(
        identificador=m.id,
        data_referencia=m.data_referencia,
        tipo_refeicao=TipoRefeicao(m.tipo_refeicao),
        descricao=m.descricao,
        calorias_aproximadas=m.calorias_aproximadas,
        observacoes=m.observacoes,
    )


def cardapio_para_modelo(e: Cardapio, m: Optional[CardapioModel] = None) -> CardapioModel:
    m = m or CardapioModel()
    m.data_referencia = e.data_referencia
    m.tipo_refeicao = e.tipo_refeicao.value
    m.descricao = e.descricao
    m.calorias_aproximadas = e.calorias_aproximadas
    m.observacoes = e.observacoes
    return m


def dieta_para_entidade(m: DietaModel) -> Dieta:
    return Dieta(
        identificador=m.id,
        residente_id=m.residente_id,
        tipo=TipoDieta(m.tipo),
        descricao_detalhada=m.descricao_detalhada,
        prescrita_por_id=m.prescrita_por_id,
        data_inicio=m.data_inicio,
        data_termino=m.data_termino,
        ativa=m.ativa,
    )


def dieta_para_modelo(e: Dieta, m: Optional[DietaModel] = None) -> DietaModel:
    m = m or DietaModel()
    m.residente_id = e.residente_id
    m.tipo = e.tipo.value
    m.descricao_detalhada = e.descricao_detalhada
    m.prescrita_por_id = e.prescrita_por_id
    m.data_inicio = e.data_inicio
    m.data_termino = e.data_termino
    m.ativa = e.ativa
    return m


def refeicao_para_entidade(m: RefeicaoModel) -> Refeicao:
    return Refeicao(
        identificador=m.id,
        residente_id=m.residente_id,
        cardapio_id=m.cardapio_id,
        tipo_refeicao=TipoRefeicao(m.tipo_refeicao),
        servida_em=m.servida_em,
        funcionario_id=m.funcionario_id,
        aceitacao_percentual=m.aceitacao_percentual,
        observacoes=m.observacoes,
    )


def refeicao_para_modelo(e: Refeicao, m: Optional[RefeicaoModel] = None) -> RefeicaoModel:
    m = m or RefeicaoModel()
    m.residente_id = e.residente_id
    m.cardapio_id = e.cardapio_id
    m.tipo_refeicao = e.tipo_refeicao.value
    m.servida_em = e.servida_em
    m.funcionario_id = e.funcionario_id
    m.aceitacao_percentual = e.aceitacao_percentual
    m.observacoes = e.observacoes
    return m


def ingestao_para_entidade(m: IngestaoHidricaModel) -> IngestaoHidrica:
    return IngestaoHidrica(
        identificador=m.id,
        residente_id=m.residente_id,
        registrada_em=m.registrada_em,
        quantidade_ml=m.quantidade_ml,
        funcionario_id=m.funcionario_id,
    )


def ingestao_para_modelo(e: IngestaoHidrica, m: Optional[IngestaoHidricaModel] = None) -> IngestaoHidricaModel:
    m = m or IngestaoHidricaModel()
    m.residente_id = e.residente_id
    m.registrada_em = e.registrada_em
    m.quantidade_ml = e.quantidade_ml
    m.funcionario_id = e.funcionario_id
    return m


# -------- Escala / Turno --------

def turno_para_entidade(m: TurnoModel) -> Turno:
    return Turno(
        identificador=m.id,
        funcionario_id=m.funcionario_id,
        inicio=m.inicio,
        fim=m.fim,
        tipo=TipoTurno(m.tipo),
        observacoes=m.observacoes,
        confirmado=m.confirmado,
    )


def turno_para_modelo(e: Turno, m: Optional[TurnoModel] = None) -> TurnoModel:
    m = m or TurnoModel()
    m.funcionario_id = e.funcionario_id
    m.inicio = e.inicio
    m.fim = e.fim
    m.tipo = e.tipo.value
    m.observacoes = e.observacoes
    m.confirmado = e.confirmado
    return m


def escala_para_entidade(m: EscalaModel) -> Escala:
    return Escala(
        identificador=m.id,
        referencia_mes=m.referencia_mes,
        referencia_ano=m.referencia_ano,
        setor=m.setor,
        publicada=m.publicada,
        publicada_em=m.publicada_em,
        publicada_por_id=m.publicada_por_id,
        turnos=[turno_para_entidade(t) for t in m.turnos],
    )


def escala_para_modelo(e: Escala, m: Optional[EscalaModel] = None) -> EscalaModel:
    m = m or EscalaModel()
    m.referencia_mes = e.referencia_mes
    m.referencia_ano = e.referencia_ano
    m.setor = e.setor
    m.publicada = e.publicada
    m.publicada_em = e.publicada_em
    m.publicada_por_id = e.publicada_por_id
    return m


# -------- Financeiro --------

def mensalidade_para_entidade(m: MensalidadeModel) -> Mensalidade:
    return Mensalidade(
        identificador=m.id,
        residente_id=m.residente_id,
        competencia_mes=m.competencia_mes,
        competencia_ano=m.competencia_ano,
        valor=m.valor,
        data_vencimento=m.data_vencimento,
        status=StatusPagamento(m.status),
        data_pagamento=m.data_pagamento,
        valor_pago=m.valor_pago,
        forma_pagamento=FormaPagamento(m.forma_pagamento) if m.forma_pagamento else None,
        desconto=m.desconto or 0.0,
        juros_multa=m.juros_multa or 0.0,
        observacoes=m.observacoes,
    )


def mensalidade_para_modelo(e: Mensalidade, m: Optional[MensalidadeModel] = None) -> MensalidadeModel:
    m = m or MensalidadeModel()
    m.residente_id = e.residente_id
    m.competencia_mes = e.competencia_mes
    m.competencia_ano = e.competencia_ano
    m.valor = e.valor
    m.data_vencimento = e.data_vencimento
    m.status = e.status.value
    m.data_pagamento = e.data_pagamento
    m.valor_pago = e.valor_pago
    m.forma_pagamento = e.forma_pagamento.value if e.forma_pagamento else None
    m.desconto = e.desconto
    m.juros_multa = e.juros_multa
    m.observacoes = e.observacoes
    return m


def lancamento_para_entidade(m: LancamentoFinanceiroModel) -> LancamentoFinanceiro:
    return LancamentoFinanceiro(
        identificador=m.id,
        tipo=TipoLancamento(m.tipo),
        descricao=m.descricao,
        valor=m.valor,
        data_competencia=m.data_competencia,
        data_pagamento=m.data_pagamento,
        categoria=m.categoria,
        centro_custo=m.centro_custo,
        fornecedor=m.fornecedor,
        forma_pagamento=FormaPagamento(m.forma_pagamento) if m.forma_pagamento else None,
        status=StatusPagamento(m.status),
        registrado_em=m.registrado_em,
        registrado_por_id=m.registrado_por_id,
    )


def lancamento_para_modelo(e: LancamentoFinanceiro, m: Optional[LancamentoFinanceiroModel] = None) -> LancamentoFinanceiroModel:
    m = m or LancamentoFinanceiroModel()
    m.tipo = e.tipo.value
    m.descricao = e.descricao
    m.valor = e.valor
    m.data_competencia = e.data_competencia
    m.data_pagamento = e.data_pagamento
    m.categoria = e.categoria
    m.centro_custo = e.centro_custo
    m.fornecedor = e.fornecedor
    m.forma_pagamento = e.forma_pagamento.value if e.forma_pagamento else None
    m.status = e.status.value
    m.registrado_em = e.registrado_em
    m.registrado_por_id = e.registrado_por_id
    return m


# -------- Documentos --------

def modelo_doc_para_entidade(m: ModeloDocumentoModel) -> ModeloDocumento:
    return ModeloDocumento(
        identificador=m.id,
        titulo=m.titulo,
        chave=m.chave,
        conteudo_template=m.conteudo_template,
        descricao=m.descricao,
        ativo=m.ativo,
    )


def modelo_doc_para_modelo(e: ModeloDocumento, m: Optional[ModeloDocumentoModel] = None) -> ModeloDocumentoModel:
    m = m or ModeloDocumentoModel()
    m.titulo = e.titulo
    m.chave = e.chave
    m.conteudo_template = e.conteudo_template
    m.descricao = e.descricao
    m.ativo = e.ativo
    return m


def doc_assinado_para_entidade(m: DocumentoAssinadoModel) -> DocumentoAssinado:
    return DocumentoAssinado(
        identificador=m.id,
        modelo_id=m.modelo_id,
        titulo=m.titulo,
        residente_id=m.residente_id,
        funcionario_id=m.funcionario_id,
        caminho_arquivo=m.caminho_arquivo,
        hash_sha256=m.hash_sha256,
        gerado_em=m.gerado_em,
        assinado_em=m.assinado_em,
        nome_assinante=m.nome_assinante,
        documento_assinante=m.documento_assinante,
        imagem_assinatura_base64=m.imagem_assinatura_base64,
        observacoes=m.observacoes,
    )


def doc_assinado_para_modelo(e: DocumentoAssinado, m: Optional[DocumentoAssinadoModel] = None) -> DocumentoAssinadoModel:
    m = m or DocumentoAssinadoModel()
    m.modelo_id = e.modelo_id
    m.titulo = e.titulo
    m.residente_id = e.residente_id
    m.funcionario_id = e.funcionario_id
    m.caminho_arquivo = e.caminho_arquivo
    m.hash_sha256 = e.hash_sha256
    m.gerado_em = e.gerado_em
    m.assinado_em = e.assinado_em
    m.nome_assinante = e.nome_assinante
    m.documento_assinante = e.documento_assinante
    m.imagem_assinatura_base64 = e.imagem_assinatura_base64
    m.observacoes = e.observacoes
    return m


# -------- Ocorrência / Visita / Auditoria --------

def ocorrencia_para_entidade(m: OcorrenciaModel) -> Ocorrencia:
    return Ocorrencia(
        identificador=m.id,
        residente_id=m.residente_id,
        tipo=TipoOcorrencia(m.tipo),
        gravidade=GravidadeOcorrencia(m.gravidade),
        descricao=m.descricao,
        ocorreu_em=m.ocorreu_em,
        registrada_por_id=m.registrada_por_id,
        local=m.local,
        medidas_adotadas=m.medidas_adotadas,
        necessitou_hospital=m.necessitou_hospital,
        encerrada=m.encerrada,
        encerrada_em=m.encerrada_em,
    )


def ocorrencia_para_modelo(e: Ocorrencia, m: Optional[OcorrenciaModel] = None) -> OcorrenciaModel:
    m = m or OcorrenciaModel()
    m.residente_id = e.residente_id
    m.tipo = e.tipo.value
    m.gravidade = e.gravidade.value
    m.descricao = e.descricao
    m.ocorreu_em = e.ocorreu_em
    m.registrada_por_id = e.registrada_por_id
    m.local = e.local
    m.medidas_adotadas = e.medidas_adotadas
    m.necessitou_hospital = e.necessitou_hospital
    m.encerrada = e.encerrada
    m.encerrada_em = e.encerrada_em
    return m


def visita_para_entidade(m: VisitaModel) -> Visita:
    return Visita(
        identificador=m.id,
        residente_id=m.residente_id,
        nome_visitante=m.nome_visitante,
        documento_visitante=m.documento_visitante,
        parentesco_ou_relacao=m.parentesco_ou_relacao,
        entrada_em=m.entrada_em,
        saida_em=m.saida_em,
        funcionario_recebeu_id=m.funcionario_recebeu_id,
        observacoes=m.observacoes,
    )


def visita_para_modelo(e: Visita, m: Optional[VisitaModel] = None) -> VisitaModel:
    m = m or VisitaModel()
    m.residente_id = e.residente_id
    m.nome_visitante = e.nome_visitante
    m.documento_visitante = e.documento_visitante
    m.parentesco_ou_relacao = e.parentesco_ou_relacao
    m.entrada_em = e.entrada_em
    m.saida_em = e.saida_em
    m.funcionario_recebeu_id = e.funcionario_recebeu_id
    m.observacoes = e.observacoes
    return m


def auditoria_para_entidade(m: LogAuditoriaModel) -> LogAuditoria:
    return LogAuditoria(
        identificador=m.id,
        ocorrido_em=m.ocorrido_em,
        funcionario_id=m.funcionario_id,
        acao=m.acao,
        recurso=m.recurso,
        recurso_id=m.recurso_id,
        detalhes=m.detalhes,
        endereco_ip=m.endereco_ip,
        agente_usuario=m.agente_usuario,
    )


def auditoria_para_modelo(e: LogAuditoria, m: Optional[LogAuditoriaModel] = None) -> LogAuditoriaModel:
    m = m or LogAuditoriaModel()
    m.ocorrido_em = e.ocorrido_em
    m.funcionario_id = e.funcionario_id
    m.acao = e.acao
    m.recurso = e.recurso
    m.recurso_id = e.recurso_id
    m.detalhes = e.detalhes
    m.endereco_ip = e.endereco_ip
    m.agente_usuario = e.agente_usuario
    return m
