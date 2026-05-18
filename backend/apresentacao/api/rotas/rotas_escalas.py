"""Rotas de Escalas de Cuidadores."""

from __future__ import annotations

from datetime import date as Data

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.escalas import (
    AdicionarTurno,
    CriarEscala,
    ListarTurnosDoDia,
)
from backend.dominio.entidades.escala import TipoTurno
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_escalas,
)
from backend.apresentacao.schemas.diversos import (
    EntradaEscala,
    EntradaTurno,
    EscalaSaida,
    TurnoSaida,
)

roteador = APIRouter(prefix="/api/escalas", tags=["Escalas"])


def _escala_para_saida(e) -> EscalaSaida:
    return EscalaSaida(
        identificador=e.identificador,
        referencia_mes=e.referencia_mes,
        referencia_ano=e.referencia_ano,
        setor=e.setor,
        publicada=e.publicada,
        turnos=[
            TurnoSaida(
                identificador=t.identificador,
                funcionario_id=t.funcionario_id,
                inicio=t.inicio,
                fim=t.fim,
                tipo=t.tipo.value,
                observacoes=t.observacoes,
                confirmado=t.confirmado,
            )
            for t in e.turnos
        ],
    )


@roteador.post("", response_model=EscalaSaida)
def criar_escala(
    dados: EntradaEscala,
    funcionario=Depends(obter_funcionario_logado),
    repo_escalas=Depends(obter_repo_escalas),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CriarEscala(repo_escalas, repo_auditoria)
    escala = caso.executar(
        dados.referencia_mes,
        dados.referencia_ano,
        dados.setor,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _escala_para_saida(escala)


@roteador.get("", response_model=list[EscalaSaida])
def listar(
    mes: int = Query(...),
    ano: int = Query(...),
    setor: str | None = Query(default=None),
    repo_escalas=Depends(obter_repo_escalas),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [_escala_para_saida(e) for e in repo_escalas.buscar_por_mes(mes, ano, setor)]


@roteador.post("/{escala_id}/turnos", response_model=TurnoSaida)
def adicionar_turno(
    escala_id: int,
    dados: EntradaTurno,
    funcionario=Depends(obter_funcionario_logado),
    repo_escalas=Depends(obter_repo_escalas),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AdicionarTurno(repo_escalas, repo_auditoria)
    t = caso.executar(
        escala_id,
        funcionario_id=dados.funcionario_id,
        inicio=dados.inicio,
        fim=dados.fim,
        tipo=TipoTurno(dados.tipo),
        observacoes=dados.observacoes,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return TurnoSaida(
        identificador=t.identificador,
        funcionario_id=t.funcionario_id,
        inicio=t.inicio,
        fim=t.fim,
        tipo=t.tipo.value,
        observacoes=t.observacoes,
        confirmado=t.confirmado,
    )


@roteador.delete("/turnos/{turno_id}")
def excluir_turno(
    turno_id: int,
    repo_escalas=Depends(obter_repo_escalas),
    _funcionario=Depends(obter_funcionario_logado),
):
    repo_escalas.excluir_turno(turno_id)
    return {"detalhe": "Turno removido."}


@roteador.get("/turnos/dia", response_model=list[TurnoSaida])
def turnos_do_dia(
    dia: Data = Query(...),
    repo_escalas=Depends(obter_repo_escalas),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        TurnoSaida(
            identificador=t.identificador,
            funcionario_id=t.funcionario_id,
            inicio=t.inicio,
            fim=t.fim,
            tipo=t.tipo.value,
            observacoes=t.observacoes,
            confirmado=t.confirmado,
        )
        for t in ListarTurnosDoDia(repo_escalas).executar(dia)
    ]
