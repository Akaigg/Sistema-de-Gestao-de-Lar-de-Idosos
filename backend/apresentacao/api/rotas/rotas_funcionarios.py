"""Rotas de gestão de funcionários."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.funcionarios import (
    AtualizarFuncionario,
    CadastrarFuncionario,
    DadosCadastroFuncionario,
    ListarFuncionarios,
)
from backend.dominio.entidades.funcionario import PapelFuncionario
from backend.apresentacao.dependencias import (
    obter_repo_auditoria,
    obter_repo_funcionarios,
    obter_servico_senha,
    requer_papeis,
)
from backend.apresentacao.schemas.autenticacao import (
    EntradaAtualizacaoFuncionario,
    EntradaCadastroFuncionario,
    FuncionarioDetalhado,
)
from backend.apresentacao.schemas.comuns import RespostaPaginada

roteador = APIRouter(prefix="/api/funcionarios", tags=["Funcionários"])


def _para_saida(funcionario) -> FuncionarioDetalhado:
    return FuncionarioDetalhado(
        identificador=funcionario.identificador,
        nome_completo=funcionario.nome_completo,
        email=funcionario.email,
        cpf=funcionario.cpf,
        cargo=funcionario.cargo,
        papeis=[p.value for p in funcionario.papeis],
        telefone=funcionario.telefone,
        data_admissao=funcionario.data_admissao,
        data_desligamento=funcionario.data_desligamento,
        ativo=funcionario.ativo,
        ultimo_acesso=funcionario.ultimo_acesso,
    )


@roteador.post(
    "",
    response_model=FuncionarioDetalhado,
    dependencies=[Depends(requer_papeis(PapelFuncionario.ADMINISTRADOR))],
)
def cadastrar(
    dados: EntradaCadastroFuncionario,
    repo_funcionarios=Depends(obter_repo_funcionarios),
    repo_auditoria=Depends(obter_repo_auditoria),
    servico_senha=Depends(obter_servico_senha),
):
    caso = CadastrarFuncionario(repo_funcionarios, servico_senha, repo_auditoria)
    funcionario = caso.executar(
        DadosCadastroFuncionario(
            nome_completo=dados.nome_completo,
            email=dados.email,
            cpf=dados.cpf,
            cargo=dados.cargo,
            papeis=[PapelFuncionario(p) for p in dados.papeis],
            senha_inicial=dados.senha_inicial,
            telefone=dados.telefone,
            data_admissao=dados.data_admissao,
        )
    )
    return _para_saida(funcionario)


@roteador.get("", response_model=RespostaPaginada[FuncionarioDetalhado])
def listar(
    termo_busca: Optional[str] = Query(default=None),
    apenas_ativos: bool = Query(default=True),
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=50, ge=1, le=200),
    repo_funcionarios=Depends(obter_repo_funcionarios),
    _funcionario=Depends(requer_papeis(PapelFuncionario.ADMINISTRADOR)),
):
    caso = ListarFuncionarios(repo_funcionarios)
    itens, total = caso.executar(termo_busca, apenas_ativos, pagina, tamanho_pagina)
    return RespostaPaginada(
        itens=[_para_saida(f) for f in itens],
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@roteador.put(
    "/{funcionario_id}",
    response_model=FuncionarioDetalhado,
    dependencies=[Depends(requer_papeis(PapelFuncionario.ADMINISTRADOR))],
)
def atualizar(
    funcionario_id: int,
    dados: EntradaAtualizacaoFuncionario,
    repo_funcionarios=Depends(obter_repo_funcionarios),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AtualizarFuncionario(repo_funcionarios, repo_auditoria)
    funcionario = caso.executar(
        funcionario_id,
        nome_completo=dados.nome_completo,
        cargo=dados.cargo,
        telefone=dados.telefone,
        papeis=[PapelFuncionario(p) for p in dados.papeis] if dados.papeis else None,
        ativo=dados.ativo,
    )
    return _para_saida(funcionario)
