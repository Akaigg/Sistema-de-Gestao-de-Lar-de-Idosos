"""Rotas de prontuário: sinais vitais, evoluções, alergias, condições, consultas."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.prontuario import (
    AgendarConsulta,
    CadastrarAlergia,
    CadastrarCondicaoCronica,
    CancelarConsulta,
    RegistrarEvolucao,
    RegistrarSinaisVitais,
)
from backend.dominio.entidades.prontuario import StatusConsulta, TipoConsulta
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_alergias,
    obter_repo_auditoria,
    obter_repo_condicoes,
    obter_repo_consultas,
    obter_repo_evolucoes,
    obter_repo_sinais,
)
from backend.apresentacao.schemas.diversos import (
    AlergiaSaida,
    CondicaoSaida,
    ConsultaSaida,
    EntradaAlergia,
    EntradaCancelarConsulta,
    EntradaCondicaoCronica,
    EntradaConsulta,
    EntradaEvolucao,
    EntradaSinaisVitais,
    EvolucaoSaida,
    SinaisVitaisSaida,
)

roteador = APIRouter(prefix="/api/prontuario", tags=["Prontuário"])


@roteador.post("/sinais-vitais", response_model=SinaisVitaisSaida)
def registrar_sinais(
    dados: EntradaSinaisVitais,
    funcionario=Depends(obter_funcionario_logado),
    repo_sinais=Depends(obter_repo_sinais),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = RegistrarSinaisVitais(repo_sinais, repo_auditoria)
    s = caso.executar(
        residente_id=dados.residente_id,
        funcionario_id=funcionario.identificador,
        pressao_sistolica=dados.pressao_sistolica,
        pressao_diastolica=dados.pressao_diastolica,
        frequencia_cardiaca=dados.frequencia_cardiaca,
        frequencia_respiratoria=dados.frequencia_respiratoria,
        temperatura=dados.temperatura,
        saturacao_oxigenio=dados.saturacao_oxigenio,
        glicemia=dados.glicemia,
        peso=dados.peso,
        observacoes=dados.observacoes,
    )
    return SinaisVitaisSaida(**{
        "identificador": s.identificador,
        "residente_id": s.residente_id,
        "aferido_em": s.aferido_em,
        "funcionario_id": s.funcionario_id,
        "pressao_sistolica": s.pressao_sistolica,
        "pressao_diastolica": s.pressao_diastolica,
        "frequencia_cardiaca": s.frequencia_cardiaca,
        "frequencia_respiratoria": s.frequencia_respiratoria,
        "temperatura": s.temperatura,
        "saturacao_oxigenio": s.saturacao_oxigenio,
        "glicemia": s.glicemia,
        "peso": s.peso,
        "observacoes": s.observacoes,
    })


@roteador.get("/sinais-vitais/residente/{residente_id}", response_model=list[SinaisVitaisSaida])
def listar_sinais(
    residente_id: int,
    repo_sinais=Depends(obter_repo_sinais),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        SinaisVitaisSaida(
            identificador=s.identificador,
            residente_id=s.residente_id,
            aferido_em=s.aferido_em,
            funcionario_id=s.funcionario_id,
            pressao_sistolica=s.pressao_sistolica,
            pressao_diastolica=s.pressao_diastolica,
            frequencia_cardiaca=s.frequencia_cardiaca,
            frequencia_respiratoria=s.frequencia_respiratoria,
            temperatura=s.temperatura,
            saturacao_oxigenio=s.saturacao_oxigenio,
            glicemia=s.glicemia,
            peso=s.peso,
            observacoes=s.observacoes,
        )
        for s in repo_sinais.listar_por_residente(residente_id)
    ]


@roteador.post("/evolucoes", response_model=EvolucaoSaida)
def registrar_evolucao(
    dados: EntradaEvolucao,
    funcionario=Depends(obter_funcionario_logado),
    repo_evolucoes=Depends(obter_repo_evolucoes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = RegistrarEvolucao(repo_evolucoes, repo_auditoria)
    e = caso.executar(
        residente_id=dados.residente_id,
        funcionario_id=funcionario.identificador,
        categoria=dados.categoria,
        texto=dados.texto,
    )
    return EvolucaoSaida(
        identificador=e.identificador,
        residente_id=e.residente_id,
        funcionario_id=e.funcionario_id,
        registrada_em=e.registrada_em,
        categoria=e.categoria,
        texto=e.texto,
    )


@roteador.get("/evolucoes/residente/{residente_id}", response_model=list[EvolucaoSaida])
def listar_evolucoes(
    residente_id: int,
    repo_evolucoes=Depends(obter_repo_evolucoes),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        EvolucaoSaida(
            identificador=e.identificador,
            residente_id=e.residente_id,
            funcionario_id=e.funcionario_id,
            registrada_em=e.registrada_em,
            categoria=e.categoria,
            texto=e.texto,
        )
        for e in repo_evolucoes.listar_por_residente(residente_id)
    ]


@roteador.post("/alergias", response_model=AlergiaSaida)
def cadastrar_alergia(
    dados: EntradaAlergia,
    repo_alergias=Depends(obter_repo_alergias),
    _funcionario=Depends(obter_funcionario_logado),
):
    a = CadastrarAlergia(repo_alergias).executar(
        residente_id=dados.residente_id,
        substancia=dados.substancia,
        reacao=dados.reacao,
        gravidade=dados.gravidade,
        observacoes=dados.observacoes,
    )
    return AlergiaSaida(
        identificador=a.identificador,
        residente_id=a.residente_id,
        substancia=a.substancia,
        reacao=a.reacao,
        gravidade=a.gravidade,
        observacoes=a.observacoes,
    )


@roteador.get("/alergias/residente/{residente_id}", response_model=list[AlergiaSaida])
def listar_alergias(
    residente_id: int,
    repo_alergias=Depends(obter_repo_alergias),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        AlergiaSaida(
            identificador=a.identificador,
            residente_id=a.residente_id,
            substancia=a.substancia,
            reacao=a.reacao,
            gravidade=a.gravidade,
            observacoes=a.observacoes,
        )
        for a in repo_alergias.listar_por_residente(residente_id)
    ]


@roteador.delete("/alergias/{alergia_id}")
def excluir_alergia(
    alergia_id: int,
    repo_alergias=Depends(obter_repo_alergias),
    _funcionario=Depends(obter_funcionario_logado),
):
    repo_alergias.excluir(alergia_id)
    return {"detalhe": "Alergia removida."}


@roteador.post("/condicoes", response_model=CondicaoSaida)
def cadastrar_condicao(
    dados: EntradaCondicaoCronica,
    repo_condicoes=Depends(obter_repo_condicoes),
    _funcionario=Depends(obter_funcionario_logado),
):
    c = CadastrarCondicaoCronica(repo_condicoes).executar(
        residente_id=dados.residente_id,
        descricao=dados.descricao,
        cid10=dados.cid10,
        data_diagnostico=dados.data_diagnostico,
        observacoes=dados.observacoes,
    )
    return CondicaoSaida(
        identificador=c.identificador,
        residente_id=c.residente_id,
        descricao=c.descricao,
        cid10=c.cid10,
        data_diagnostico=c.data_diagnostico,
    )


@roteador.get("/condicoes/residente/{residente_id}", response_model=list[CondicaoSaida])
def listar_condicoes(
    residente_id: int,
    repo_condicoes=Depends(obter_repo_condicoes),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        CondicaoSaida(
            identificador=c.identificador,
            residente_id=c.residente_id,
            descricao=c.descricao,
            cid10=c.cid10,
            data_diagnostico=c.data_diagnostico,
        )
        for c in repo_condicoes.listar_por_residente(residente_id)
    ]


# -------- Consultas --------

@roteador.post("/consultas", response_model=ConsultaSaida)
def agendar_consulta(
    dados: EntradaConsulta,
    funcionario=Depends(obter_funcionario_logado),
    repo_consultas=Depends(obter_repo_consultas),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AgendarConsulta(repo_consultas, repo_auditoria)
    c = caso.executar(
        residente_id=dados.residente_id,
        tipo=TipoConsulta(dados.tipo),
        data_hora=dados.data_hora,
        profissional=dados.profissional,
        eh_externa=dados.eh_externa,
        especialidade=dados.especialidade,
        local=dados.local,
        motivo=dados.motivo,
        observacoes=dados.observacoes,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return ConsultaSaida(
        identificador=c.identificador,
        residente_id=c.residente_id,
        tipo=c.tipo.value,
        data_hora=c.data_hora,
        profissional=c.profissional,
        eh_externa=c.eh_externa,
        especialidade=c.especialidade,
        local=c.local,
        motivo=c.motivo,
        observacoes=c.observacoes,
        status=c.status.value,
    )


@roteador.get("/consultas", response_model=list[ConsultaSaida])
def listar_consultas(
    inicio: Optional[datetime] = Query(default=None),
    fim: Optional[datetime] = Query(default=None),
    residente_id: Optional[int] = Query(default=None),
    repo_consultas=Depends(obter_repo_consultas),
    _funcionario=Depends(obter_funcionario_logado),
):
    if inicio is None:
        inicio = datetime.utcnow() - timedelta(days=30)
    if fim is None:
        fim = datetime.utcnow() + timedelta(days=60)
    itens = repo_consultas.listar_por_periodo(inicio, fim, residente_id)
    return [
        ConsultaSaida(
            identificador=c.identificador,
            residente_id=c.residente_id,
            tipo=c.tipo.value,
            data_hora=c.data_hora,
            profissional=c.profissional,
            eh_externa=c.eh_externa,
            especialidade=c.especialidade,
            local=c.local,
            motivo=c.motivo,
            observacoes=c.observacoes,
            status=c.status.value,
        )
        for c in itens
    ]


@roteador.post("/consultas/{consulta_id}/cancelar", response_model=ConsultaSaida)
def cancelar_consulta(
    consulta_id: int,
    dados: EntradaCancelarConsulta,
    funcionario=Depends(obter_funcionario_logado),
    repo_consultas=Depends(obter_repo_consultas),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CancelarConsulta(repo_consultas, repo_auditoria)
    c = caso.executar(consulta_id, dados.motivo, funcionario_responsavel_id=funcionario.identificador)
    return ConsultaSaida(
        identificador=c.identificador,
        residente_id=c.residente_id,
        tipo=c.tipo.value,
        data_hora=c.data_hora,
        profissional=c.profissional,
        eh_externa=c.eh_externa,
        especialidade=c.especialidade,
        local=c.local,
        motivo=c.motivo,
        observacoes=c.observacoes,
        status=c.status.value,
    )
