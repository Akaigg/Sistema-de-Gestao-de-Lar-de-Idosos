"""Rotas de alimentação: cardápios, dietas, refeições, hidratação."""

from __future__ import annotations

from datetime import date as Data

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.alimentacao import (
    CadastrarCardapio,
    DefinirDietaIndividual,
    RegistrarIngestaoHidrica,
    RegistrarRefeicaoServida,
)
from backend.dominio.entidades.alimentacao import TipoDieta, TipoRefeicao
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_cardapios,
    obter_repo_dietas,
    obter_repo_ingestao,
    obter_repo_refeicoes,
)
from backend.apresentacao.schemas.diversos import (
    CardapioSaida,
    DietaSaida,
    EntradaCardapio,
    EntradaDieta,
    EntradaIngestaoHidrica,
    EntradaRefeicaoServida,
    IngestaoSaida,
    RefeicaoSaida,
)

roteador = APIRouter(prefix="/api/alimentacao", tags=["Alimentação"])


@roteador.post("/cardapios", response_model=CardapioSaida)
def cadastrar_cardapio(
    dados: EntradaCardapio,
    repo_cardapios=Depends(obter_repo_cardapios),
    _funcionario=Depends(obter_funcionario_logado),
):
    c = CadastrarCardapio(repo_cardapios).executar(
        data_referencia=dados.data_referencia,
        tipo_refeicao=TipoRefeicao(dados.tipo_refeicao),
        descricao=dados.descricao,
        calorias_aproximadas=dados.calorias_aproximadas,
        observacoes=dados.observacoes,
    )
    return CardapioSaida(
        identificador=c.identificador,
        data_referencia=c.data_referencia,
        tipo_refeicao=c.tipo_refeicao.value,
        descricao=c.descricao,
        calorias_aproximadas=c.calorias_aproximadas,
        observacoes=c.observacoes,
    )


@roteador.get("/cardapios", response_model=list[CardapioSaida])
def listar_cardapios(
    dia: Data = Query(...),
    repo_cardapios=Depends(obter_repo_cardapios),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        CardapioSaida(
            identificador=c.identificador,
            data_referencia=c.data_referencia,
            tipo_refeicao=c.tipo_refeicao.value,
            descricao=c.descricao,
            calorias_aproximadas=c.calorias_aproximadas,
            observacoes=c.observacoes,
        )
        for c in repo_cardapios.listar_por_data(dia)
    ]


@roteador.post("/dietas", response_model=DietaSaida)
def definir_dieta(
    dados: EntradaDieta,
    funcionario=Depends(obter_funcionario_logado),
    repo_dietas=Depends(obter_repo_dietas),
):
    d = DefinirDietaIndividual(repo_dietas).executar(
        residente_id=dados.residente_id,
        tipo=TipoDieta(dados.tipo),
        descricao_detalhada=dados.descricao_detalhada,
        prescrita_por_id=funcionario.identificador,
        data_inicio=dados.data_inicio,
        data_termino=dados.data_termino,
    )
    return DietaSaida(
        identificador=d.identificador,
        residente_id=d.residente_id,
        tipo=d.tipo.value,
        descricao_detalhada=d.descricao_detalhada,
        data_inicio=d.data_inicio,
        data_termino=d.data_termino,
        ativa=d.ativa,
    )


@roteador.get("/dietas/residente/{residente_id}", response_model=list[DietaSaida])
def listar_dietas(
    residente_id: int,
    repo_dietas=Depends(obter_repo_dietas),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        DietaSaida(
            identificador=d.identificador,
            residente_id=d.residente_id,
            tipo=d.tipo.value,
            descricao_detalhada=d.descricao_detalhada,
            data_inicio=d.data_inicio,
            data_termino=d.data_termino,
            ativa=d.ativa,
        )
        for d in repo_dietas.listar_por_residente(residente_id)
    ]


@roteador.post("/refeicoes", response_model=RefeicaoSaida)
def registrar_refeicao(
    dados: EntradaRefeicaoServida,
    funcionario=Depends(obter_funcionario_logado),
    repo_refeicoes=Depends(obter_repo_refeicoes),
):
    r = RegistrarRefeicaoServida(repo_refeicoes).executar(
        residente_id=dados.residente_id,
        tipo_refeicao=TipoRefeicao(dados.tipo_refeicao),
        funcionario_id=funcionario.identificador,
        cardapio_id=dados.cardapio_id,
        aceitacao_percentual=dados.aceitacao_percentual,
        observacoes=dados.observacoes,
    )
    return RefeicaoSaida(
        identificador=r.identificador,
        residente_id=r.residente_id,
        tipo_refeicao=r.tipo_refeicao.value,
        servida_em=r.servida_em,
        aceitacao_percentual=r.aceitacao_percentual,
        observacoes=r.observacoes,
    )


@roteador.post("/hidratacao", response_model=IngestaoSaida)
def registrar_hidratacao(
    dados: EntradaIngestaoHidrica,
    funcionario=Depends(obter_funcionario_logado),
    repo_ingestao=Depends(obter_repo_ingestao),
):
    i = RegistrarIngestaoHidrica(repo_ingestao).executar(
        residente_id=dados.residente_id,
        quantidade_ml=dados.quantidade_ml,
        funcionario_id=funcionario.identificador,
    )
    return IngestaoSaida(
        identificador=i.identificador,
        residente_id=i.residente_id,
        registrada_em=i.registrada_em,
        quantidade_ml=i.quantidade_ml,
    )


@roteador.get("/hidratacao/residente/{residente_id}/total")
def total_hidratacao_do_dia(
    residente_id: int,
    dia: Data = Query(...),
    repo_ingestao=Depends(obter_repo_ingestao),
    _funcionario=Depends(obter_funcionario_logado),
):
    return {
        "residente_id": residente_id,
        "dia": dia.isoformat(),
        "total_ml": repo_ingestao.total_do_dia(residente_id, dia),
    }
