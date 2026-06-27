"""Rotas de Ocorrências e Visitas."""

from __future__ import annotations

from datetime import date as Data
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.ocorrencias_e_visitas import (
    EncerrarOcorrencia,
    EncerrarVisita,
    RegistrarOcorrencia,
    RegistrarVisita,
)
from backend.dominio.entidades.ocorrencia import (
    GravidadeOcorrencia,
    TipoOcorrencia,
)
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_ocorrencias,
    obter_repo_visitas,
)
from backend.apresentacao.schemas.diversos import (
    EntradaOcorrencia,
    EntradaVisita,
    OcorrenciaSaida,
    VisitaSaida,
)

roteador = APIRouter(tags=["Ocorrências e Visitas"])


# -------- Ocorrências --------

@roteador.post("/api/ocorrencias", response_model=OcorrenciaSaida)
def registrar_ocorrencia(
    dados: EntradaOcorrencia,
    funcionario=Depends(obter_funcionario_logado),
    repo_ocorrencias=Depends(obter_repo_ocorrencias),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = RegistrarOcorrencia(repo_ocorrencias, repo_auditoria)
    o = caso.executar(
        residente_id=dados.residente_id,
        tipo=TipoOcorrencia(dados.tipo),
        gravidade=GravidadeOcorrencia(dados.gravidade),
        descricao=dados.descricao,
        funcionario_id=funcionario.identificador,
        local=dados.local,
        medidas_adotadas=dados.medidas_adotadas,
        necessitou_hospital=dados.necessitou_hospital,
    )
    return OcorrenciaSaida(
        identificador=o.identificador,
        residente_id=o.residente_id,
        tipo=o.tipo.value,
        gravidade=o.gravidade.value,
        descricao=o.descricao,
        ocorreu_em=o.ocorreu_em,
        local=o.local,
        medidas_adotadas=o.medidas_adotadas,
        necessitou_hospital=o.necessitou_hospital,
        encerrada=o.encerrada,
    )


@roteador.get("/api/ocorrencias", response_model=list[OcorrenciaSaida])
def listar_ocorrencias(
    residente_id: Optional[int] = Query(default=None),
    inicio: Optional[Data] = Query(default=None),
    fim: Optional[Data] = Query(default=None),
    repo_ocorrencias=Depends(obter_repo_ocorrencias),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        OcorrenciaSaida(
            identificador=o.identificador,
            residente_id=o.residente_id,
            tipo=o.tipo.value,
            gravidade=o.gravidade.value,
            descricao=o.descricao,
            ocorreu_em=o.ocorreu_em,
            local=o.local,
            medidas_adotadas=o.medidas_adotadas,
            necessitou_hospital=o.necessitou_hospital,
            encerrada=o.encerrada,
        )
        for o in repo_ocorrencias.listar(residente_id, inicio, fim)
    ]


@roteador.post("/api/ocorrencias/{ocorrencia_id}/encerrar", response_model=OcorrenciaSaida)
def encerrar(
    ocorrencia_id: int,
    repo_ocorrencias=Depends(obter_repo_ocorrencias),
    _funcionario=Depends(obter_funcionario_logado),
):
    o = EncerrarOcorrencia(repo_ocorrencias).executar(ocorrencia_id)
    return OcorrenciaSaida(
        identificador=o.identificador,
        residente_id=o.residente_id,
        tipo=o.tipo.value,
        gravidade=o.gravidade.value,
        descricao=o.descricao,
        ocorreu_em=o.ocorreu_em,
        local=o.local,
        medidas_adotadas=o.medidas_adotadas,
        necessitou_hospital=o.necessitou_hospital,
        encerrada=o.encerrada,
    )


# -------- Visitas --------

@roteador.post("/api/visitas", response_model=VisitaSaida)
def registrar_visita(
    dados: EntradaVisita,
    funcionario=Depends(obter_funcionario_logado),
    repo_visitas=Depends(obter_repo_visitas),
):
    v = RegistrarVisita(repo_visitas).executar(
        residente_id=dados.residente_id,
        nome_visitante=dados.nome_visitante,
        documento_visitante=dados.documento_visitante,
        parentesco_ou_relacao=dados.parentesco_ou_relacao,
        funcionario_recebeu_id=funcionario.identificador,
        observacoes=dados.observacoes,
    )
    return VisitaSaida(
        identificador=v.identificador,
        residente_id=v.residente_id,
        nome_visitante=v.nome_visitante,
        documento_visitante=v.documento_visitante,
        parentesco_ou_relacao=v.parentesco_ou_relacao,
        entrada_em=v.entrada_em,
        saida_em=v.saida_em,
    )


@roteador.post("/api/visitas/{visita_id}/encerrar", response_model=VisitaSaida)
def encerrar_visita(
    visita_id: int,
    repo_visitas=Depends(obter_repo_visitas),
    _funcionario=Depends(obter_funcionario_logado),
):
    v = EncerrarVisita(repo_visitas).executar(visita_id)
    return VisitaSaida(
        identificador=v.identificador,
        residente_id=v.residente_id,
        nome_visitante=v.nome_visitante,
        documento_visitante=v.documento_visitante,
        parentesco_ou_relacao=v.parentesco_ou_relacao,
        entrada_em=v.entrada_em,
        saida_em=v.saida_em,
    )


@roteador.get("/api/visitas", response_model=list[VisitaSaida])
def listar_visitas(
    residente_id: Optional[int] = Query(default=None),
    dia: Optional[Data] = Query(default=None),
    repo_visitas=Depends(obter_repo_visitas),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        VisitaSaida(
            identificador=v.identificador,
            residente_id=v.residente_id,
            nome_visitante=v.nome_visitante,
            documento_visitante=v.documento_visitante,
            parentesco_ou_relacao=v.parentesco_ou_relacao,
            entrada_em=v.entrada_em,
            saida_em=v.saida_em,
        )
        for v in repo_visitas.listar(residente_id, dia)
    ]
