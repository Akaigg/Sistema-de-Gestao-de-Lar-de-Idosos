"""Rotas do Dashboard."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.aplicacao.casos_de_uso.dashboard import ObterIndicadoresDashboard
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_aplicacoes,
    obter_repo_consultas,
    obter_repo_quartos,
    obter_repo_residentes,
)
from backend.apresentacao.schemas.diversos import IndicadoresSaida

roteador = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@roteador.get("", response_model=IndicadoresSaida)
def obter(
    repo_residentes=Depends(obter_repo_residentes),
    repo_quartos=Depends(obter_repo_quartos),
    repo_aplicacoes=Depends(obter_repo_aplicacoes),
    repo_consultas=Depends(obter_repo_consultas),
    _funcionario=Depends(obter_funcionario_logado),
):
    caso = ObterIndicadoresDashboard(
        repo_residentes, repo_quartos, repo_aplicacoes, repo_consultas
    )
    ind = caso.executar()
    return IndicadoresSaida(
        total_residentes_ativos=ind.total_residentes_ativos,
        total_leitos=ind.total_leitos,
        leitos_ocupados=ind.leitos_ocupados,
        taxa_ocupacao_percentual=ind.taxa_ocupacao_percentual,
        aplicacoes_medicamento_hoje=ind.aplicacoes_medicamento_hoje,
        consultas_hoje=ind.consultas_hoje,
        total_aniversariantes_mes=ind.total_aniversariantes_mes,
    )
