"""Rotas financeiras."""

from __future__ import annotations

from datetime import date as Data
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.financeiro import (
    CriarLancamento,
    CriarMensalidade,
    GerarFluxoDeCaixa,
    QuitarMensalidade,
)
from backend.dominio.entidades.financeiro import (
    FormaPagamento,
    StatusPagamento,
    TipoLancamento,
)
from backend.dominio.entidades.funcionario import PapelFuncionario
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_lancamentos,
    obter_repo_mensalidades,
    requer_papeis,
)
from backend.apresentacao.schemas.diversos import (
    EntradaLancamento,
    EntradaMensalidade,
    EntradaQuitarMensalidade,
    FluxoCaixaSaida,
    LancamentoSaida,
    MensalidadeSaida,
)

roteador = APIRouter(prefix="/api/financeiro", tags=["Financeiro"])


def _mens_para_saida(m) -> MensalidadeSaida:
    return MensalidadeSaida(
        identificador=m.identificador,
        residente_id=m.residente_id,
        competencia_mes=m.competencia_mes,
        competencia_ano=m.competencia_ano,
        valor=m.valor,
        data_vencimento=m.data_vencimento,
        status=m.status.value,
        data_pagamento=m.data_pagamento,
        valor_pago=m.valor_pago,
        forma_pagamento=m.forma_pagamento.value if m.forma_pagamento else None,
    )


def _lanc_para_saida(l) -> LancamentoSaida:
    return LancamentoSaida(
        identificador=l.identificador,
        tipo=l.tipo.value,
        descricao=l.descricao,
        valor=l.valor,
        data_competencia=l.data_competencia,
        categoria=l.categoria,
        centro_custo=l.centro_custo,
        fornecedor=l.fornecedor,
        forma_pagamento=l.forma_pagamento.value if l.forma_pagamento else None,
        status=l.status.value,
    )


@roteador.post(
    "/mensalidades",
    response_model=MensalidadeSaida,
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def criar_mensalidade(
    dados: EntradaMensalidade,
    funcionario=Depends(obter_funcionario_logado),
    repo_mens=Depends(obter_repo_mensalidades),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CriarMensalidade(repo_mens, repo_auditoria)
    m = caso.executar(
        residente_id=dados.residente_id,
        competencia_mes=dados.competencia_mes,
        competencia_ano=dados.competencia_ano,
        valor=dados.valor,
        data_vencimento=dados.data_vencimento,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _mens_para_saida(m)


@roteador.get(
    "/mensalidades",
    response_model=list[MensalidadeSaida],
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def listar_mensalidades(
    residente_id: Optional[int] = Query(default=None),
    status: Optional[str] = Query(default=None),
    mes: Optional[int] = Query(default=None),
    ano: Optional[int] = Query(default=None),
    repo_mens=Depends(obter_repo_mensalidades),
):
    status_enum = StatusPagamento(status) if status else None
    itens = repo_mens.listar(residente_id, status_enum, mes, ano)
    return [_mens_para_saida(m) for m in itens]


@roteador.post(
    "/mensalidades/{mensalidade_id}/quitar",
    response_model=MensalidadeSaida,
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def quitar_mensalidade(
    mensalidade_id: int,
    dados: EntradaQuitarMensalidade,
    funcionario=Depends(obter_funcionario_logado),
    repo_mens=Depends(obter_repo_mensalidades),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = QuitarMensalidade(repo_mens, repo_auditoria)
    m = caso.executar(
        mensalidade_id=mensalidade_id,
        valor_pago=dados.valor_pago,
        forma=FormaPagamento(dados.forma_pagamento),
        data_pagamento=dados.data_pagamento,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _mens_para_saida(m)


@roteador.post(
    "/lancamentos",
    response_model=LancamentoSaida,
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def criar_lancamento(
    dados: EntradaLancamento,
    funcionario=Depends(obter_funcionario_logado),
    repo_lanc=Depends(obter_repo_lancamentos),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CriarLancamento(repo_lanc, repo_auditoria)
    l = caso.executar(
        tipo=TipoLancamento(dados.tipo),
        descricao=dados.descricao,
        valor=dados.valor,
        data_competencia=dados.data_competencia,
        categoria=dados.categoria,
        centro_custo=dados.centro_custo,
        fornecedor=dados.fornecedor,
        forma_pagamento=FormaPagamento(dados.forma_pagamento) if dados.forma_pagamento else None,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _lanc_para_saida(l)


@roteador.get(
    "/lancamentos",
    response_model=list[LancamentoSaida],
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def listar_lancamentos(
    tipo: Optional[str] = Query(default=None),
    inicio: Optional[Data] = Query(default=None),
    fim: Optional[Data] = Query(default=None),
    repo_lanc=Depends(obter_repo_lancamentos),
):
    tipo_enum = TipoLancamento(tipo) if tipo else None
    itens = repo_lanc.listar(tipo_enum, inicio, fim)
    return [_lanc_para_saida(l) for l in itens]


@roteador.get(
    "/fluxo-caixa",
    response_model=FluxoCaixaSaida,
    dependencies=[Depends(requer_papeis(PapelFuncionario.FINANCEIRO))],
)
def fluxo_de_caixa(
    inicio: Data = Query(...),
    fim: Data = Query(...),
    repo_lanc=Depends(obter_repo_lancamentos),
):
    resultado = GerarFluxoDeCaixa(repo_lanc).executar(inicio, fim)
    return FluxoCaixaSaida(**resultado)
