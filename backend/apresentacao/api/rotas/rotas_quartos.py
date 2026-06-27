"""Rotas de quartos e leitos."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from backend.aplicacao.casos_de_uso.quartos import (
    AlocarResidenteEmLeito,
    CadastrarQuarto,
    DadosCadastroQuarto,
    LiberarLeito,
    ListarQuartos,
)
from backend.dominio.entidades.quarto import TipoQuarto
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_quartos,
)
from backend.apresentacao.schemas.comuns import MensagemSimples
from backend.apresentacao.schemas.diversos import (
    EntradaAlocarLeito,
    EntradaQuarto,
    LeitoSaida,
    QuartoSaida,
)

roteador = APIRouter(prefix="/api/quartos", tags=["Quartos"])


def _para_saida(quarto) -> QuartoSaida:
    return QuartoSaida(
        identificador=quarto.identificador,
        numero=quarto.numero,
        andar=quarto.andar,
        tipo=quarto.tipo.value,
        capacidade=quarto.capacidade,
        status=quarto.status.value,
        leitos=[
            LeitoSaida(
                identificador=leito.identificador,
                numero=leito.numero,
                status=leito.status.value,
                residente_id=leito.residente_id,
            )
            for leito in quarto.leitos
        ],
        possui_banheiro=quarto.possui_banheiro,
        possui_ar_condicionado=quarto.possui_ar_condicionado,
        acessibilidade=quarto.acessibilidade,
        observacoes=quarto.observacoes,
    )


@roteador.post("", response_model=QuartoSaida)
def cadastrar(
    dados: EntradaQuarto,
    funcionario=Depends(obter_funcionario_logado),
    repo_quartos=Depends(obter_repo_quartos),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CadastrarQuarto(repo_quartos, repo_auditoria)
    quarto = caso.executar(
        DadosCadastroQuarto(
            numero=dados.numero,
            andar=dados.andar,
            tipo=TipoQuarto(dados.tipo),
            capacidade=dados.capacidade,
            leitos=dados.leitos,
            possui_banheiro=dados.possui_banheiro,
            possui_ar_condicionado=dados.possui_ar_condicionado,
            acessibilidade=dados.acessibilidade,
            observacoes=dados.observacoes,
        ),
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _para_saida(quarto)


@roteador.get("", response_model=list[QuartoSaida])
def listar(
    repo_quartos=Depends(obter_repo_quartos),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [_para_saida(q) for q in ListarQuartos(repo_quartos).executar()]


@roteador.post("/leitos/{leito_id}/alocar", response_model=LeitoSaida)
def alocar_residente_em_leito(
    leito_id: int,
    dados: EntradaAlocarLeito,
    funcionario=Depends(obter_funcionario_logado),
    repo_quartos=Depends(obter_repo_quartos),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AlocarResidenteEmLeito(repo_quartos, repo_auditoria)
    leito = caso.executar(
        leito_id, dados.residente_id, funcionario_responsavel_id=funcionario.identificador
    )
    return LeitoSaida(
        identificador=leito.identificador,
        numero=leito.numero,
        status=leito.status.value,
        residente_id=leito.residente_id,
    )


@roteador.post("/leitos/{leito_id}/liberar", response_model=LeitoSaida)
def liberar(
    leito_id: int,
    funcionario=Depends(obter_funcionario_logado),
    repo_quartos=Depends(obter_repo_quartos),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = LiberarLeito(repo_quartos, repo_auditoria)
    leito = caso.executar(leito_id, funcionario_responsavel_id=funcionario.identificador)
    return LeitoSaida(
        identificador=leito.identificador,
        numero=leito.numero,
        status=leito.status.value,
        residente_id=leito.residente_id,
    )
