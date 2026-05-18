"""Rotas de medicação, prescrição e aplicação."""

from __future__ import annotations

from datetime import datetime, time
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.medicacao import (
    AplicarMedicamento,
    CadastrarMedicamento,
    CadastrarPrescricaoEGerarAplicacoes,
    DadosCadastroMedicamento,
    DadosCadastroPrescricao,
    ListarAplicacoesParaCalendario,
    MarcarAplicacoesAtrasadas,
    RegistrarLoteMedicamento,
    SuspenderPrescricao,
)
from backend.dominio.entidades.medicamento import StatusAplicacao, ViaAdministracao
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_aplicacoes,
    obter_repo_auditoria,
    obter_repo_lotes,
    obter_repo_medicamentos,
    obter_repo_prescricoes,
)
from backend.apresentacao.schemas.medicacao import (
    AplicacaoCalendario,
    AplicacaoSaida,
    EntradaAplicarMedicamento,
    EntradaLoteMedicamento,
    EntradaMedicamento,
    EntradaPrescricao,
    LoteSaida,
    MedicamentoSaida,
    PrescricaoSaida,
)

roteador = APIRouter(prefix="/api/medicacao", tags=["Medicação"])


# -------- Medicamentos --------

def _med_para_saida(med) -> MedicamentoSaida:
    return MedicamentoSaida(
        identificador=med.identificador,
        nome_comercial=med.nome_comercial,
        principio_ativo=med.principio_ativo,
        forma_farmaceutica=med.forma_farmaceutica,
        concentracao=med.concentracao,
        fabricante=med.fabricante,
        necessita_receita=med.necessita_receita,
        controlado=med.controlado,
        estoque_minimo=med.estoque_minimo,
    )


@roteador.post("/medicamentos", response_model=MedicamentoSaida)
def cadastrar_medicamento(
    dados: EntradaMedicamento,
    funcionario=Depends(obter_funcionario_logado),
    repo_medicamentos=Depends(obter_repo_medicamentos),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CadastrarMedicamento(repo_medicamentos, repo_auditoria)
    med = caso.executar(
        DadosCadastroMedicamento(**dados.model_dump()),
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _med_para_saida(med)


@roteador.get("/medicamentos", response_model=list[MedicamentoSaida])
def listar_medicamentos(
    termo_busca: Optional[str] = Query(default=None),
    repo_medicamentos=Depends(obter_repo_medicamentos),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [_med_para_saida(m) for m in repo_medicamentos.listar(termo_busca)]


# -------- Lotes --------

@roteador.post("/lotes", response_model=LoteSaida)
def registrar_lote(
    dados: EntradaLoteMedicamento,
    funcionario=Depends(obter_funcionario_logado),
    repo_lotes=Depends(obter_repo_lotes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = RegistrarLoteMedicamento(repo_lotes, repo_auditoria)
    lote = caso.executar(
        medicamento_id=dados.medicamento_id,
        numero_lote=dados.numero_lote,
        quantidade=dados.quantidade,
        data_validade=dados.data_validade,
        fornecedor=dados.fornecedor,
        preco_unitario=dados.preco_unitario,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return LoteSaida(
        identificador=lote.identificador,
        medicamento_id=lote.medicamento_id,
        numero_lote=lote.numero_lote,
        quantidade=lote.quantidade,
        data_validade=lote.data_validade,
        data_entrada=lote.data_entrada,
        fornecedor=lote.fornecedor,
        preco_unitario=lote.preco_unitario,
    )


@roteador.get("/lotes/proximos-vencimento", response_model=list[LoteSaida])
def listar_proximos_vencimento(
    dias: int = Query(default=30, ge=1, le=365),
    repo_lotes=Depends(obter_repo_lotes),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        LoteSaida(
            identificador=l.identificador,
            medicamento_id=l.medicamento_id,
            numero_lote=l.numero_lote,
            quantidade=l.quantidade,
            data_validade=l.data_validade,
            data_entrada=l.data_entrada,
            fornecedor=l.fornecedor,
            preco_unitario=l.preco_unitario,
        )
        for l in repo_lotes.listar_proximos_vencimento(dias)
    ]


# -------- Prescrições --------

def _presc_para_saida(p) -> PrescricaoSaida:
    return PrescricaoSaida(
        identificador=p.identificador,
        residente_id=p.residente_id,
        medicamento_id=p.medicamento_id,
        medico_id=p.medico_id,
        dose=p.dose,
        via=p.via.value,
        frequencia_horas=p.frequencia_horas,
        horarios=[f"{h.hour:02d}:{h.minute:02d}" for h in p.horarios],
        data_inicio=p.data_inicio,
        duracao_dias=p.duracao_dias,
        se_necessario=p.se_necessario,
        suspensa=p.suspensa,
        motivo_suspensao=p.motivo_suspensao,
        observacoes=p.observacoes,
    )


@roteador.post("/prescricoes", response_model=PrescricaoSaida)
def cadastrar_prescricao(
    dados: EntradaPrescricao,
    funcionario=Depends(obter_funcionario_logado),
    repo_prescricoes=Depends(obter_repo_prescricoes),
    repo_aplicacoes=Depends(obter_repo_aplicacoes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    horarios_obj: list[time] = []
    for h in dados.horarios:
        hora, minuto = h.split(":")
        horarios_obj.append(time(int(hora), int(minuto)))
    caso = CadastrarPrescricaoEGerarAplicacoes(repo_prescricoes, repo_aplicacoes, repo_auditoria)
    p = caso.executar(
        DadosCadastroPrescricao(
            residente_id=dados.residente_id,
            medicamento_id=dados.medicamento_id,
            medico_id=dados.medico_id,
            dose=dados.dose,
            via=ViaAdministracao(dados.via),
            frequencia_horas=dados.frequencia_horas,
            horarios=horarios_obj,
            data_inicio=dados.data_inicio,
            duracao_dias=dados.duracao_dias,
            se_necessario=dados.se_necessario,
            observacoes=dados.observacoes,
        ),
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _presc_para_saida(p)


@roteador.get("/prescricoes/residente/{residente_id}", response_model=list[PrescricaoSaida])
def listar_prescricoes(
    residente_id: int,
    apenas_ativas: bool = Query(default=True),
    repo_prescricoes=Depends(obter_repo_prescricoes),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        _presc_para_saida(p)
        for p in repo_prescricoes.listar_por_residente(residente_id, apenas_ativas)
    ]


@roteador.post("/prescricoes/{prescricao_id}/suspender", response_model=PrescricaoSaida)
def suspender(
    prescricao_id: int,
    motivo: str,
    funcionario=Depends(obter_funcionario_logado),
    repo_prescricoes=Depends(obter_repo_prescricoes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = SuspenderPrescricao(repo_prescricoes, repo_auditoria)
    p = caso.executar(prescricao_id, motivo, funcionario_responsavel_id=funcionario.identificador)
    return _presc_para_saida(p)


# -------- Aplicações --------

_CORES_POR_STATUS = {
    StatusAplicacao.AGUARDANDO: "#94a3b8",
    StatusAplicacao.APLICADO: "#16a34a",
    StatusAplicacao.APLICADO_COM_ATRASO: "#f59e0b",
    StatusAplicacao.EM_ATRASO: "#dc2626",
    StatusAplicacao.RECUSADO: "#475569",
    StatusAplicacao.SUSPENSO: "#0f172a",
    StatusAplicacao.REACAO_ADVERSA: "#7c3aed",
}


@roteador.get("/aplicacoes", response_model=list[AplicacaoCalendario])
def listar_aplicacoes_calendario(
    inicio: datetime = Query(...),
    fim: datetime = Query(...),
    residente_id: Optional[int] = Query(default=None),
    repo_aplicacoes=Depends(obter_repo_aplicacoes),
    repo_prescricoes=Depends(obter_repo_prescricoes),
    repo_medicamentos=Depends(obter_repo_medicamentos),
    _funcionario=Depends(obter_funcionario_logado),
):
    caso = ListarAplicacoesParaCalendario(repo_aplicacoes)
    aplicacoes = caso.executar(inicio, fim, residente_id)

    eventos: list[AplicacaoCalendario] = []
    cache_prescricoes: dict[int, str] = {}
    for aplicacao in aplicacoes:
        descricao = cache_prescricoes.get(aplicacao.prescricao_id)
        if descricao is None:
            p = repo_prescricoes.buscar_por_id(aplicacao.prescricao_id)
            if p:
                med = repo_medicamentos.buscar_por_id(p.medicamento_id)
                descricao = f"{med.nome_comercial if med else 'Medicamento'} — {p.dose}"
            else:
                descricao = "Medicamento"
            cache_prescricoes[aplicacao.prescricao_id] = descricao
        eventos.append(
            AplicacaoCalendario(
                id=aplicacao.identificador or 0,
                title=descricao,
                start=aplicacao.horario_previsto,
                color=_CORES_POR_STATUS.get(aplicacao.status, "#94a3b8"),
                extendedProps={
                    "status": aplicacao.status.value,
                    "horario_aplicado": (
                        aplicacao.horario_aplicado.isoformat()
                        if aplicacao.horario_aplicado else None
                    ),
                    "prescricao_id": aplicacao.prescricao_id,
                    "observacoes": aplicacao.observacoes,
                },
            )
        )
    return eventos


@roteador.post("/aplicacoes/{aplicacao_id}/registrar", response_model=AplicacaoSaida)
def registrar_aplicacao(
    aplicacao_id: int,
    dados: EntradaAplicarMedicamento,
    funcionario=Depends(obter_funcionario_logado),
    repo_aplicacoes=Depends(obter_repo_aplicacoes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AplicarMedicamento(repo_aplicacoes, repo_auditoria)
    aplicacao = caso.executar(
        aplicacao_id,
        funcionario_id=funcionario.identificador,
        acao=dados.acao,
        observacoes=dados.observacoes,
        motivo_recusa=dados.motivo_recusa,
        descricao_reacao=dados.descricao_reacao,
    )
    return AplicacaoSaida(
        identificador=aplicacao.identificador,
        prescricao_id=aplicacao.prescricao_id,
        horario_previsto=aplicacao.horario_previsto,
        status=aplicacao.status.value,
        horario_aplicado=aplicacao.horario_aplicado,
        funcionario_id=aplicacao.funcionario_id,
        observacoes=aplicacao.observacoes,
        motivo_recusa=aplicacao.motivo_recusa,
        reacao_descrita=aplicacao.reacao_descrita,
    )


@roteador.post("/aplicacoes/marcar-atrasadas")
def marcar_atrasadas(
    repo_aplicacoes=Depends(obter_repo_aplicacoes),
    _funcionario=Depends(obter_funcionario_logado),
):
    caso = MarcarAplicacoesAtrasadas(repo_aplicacoes)
    quantidade = caso.executar()
    return {"marcadas": quantidade}
