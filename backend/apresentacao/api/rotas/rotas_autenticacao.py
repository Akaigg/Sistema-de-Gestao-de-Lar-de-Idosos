"""Rotas de autenticação."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request

from backend.aplicacao.casos_de_uso.autenticacao import (
    AutenticarFuncionario,
    TrocarSenha,
)
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_funcionarios,
    obter_servico_senha,
    obter_servico_token,
)
from backend.apresentacao.schemas.autenticacao import (
    EntradaLogin,
    EntradaTrocaSenha,
    FuncionarioResumido,
    SaidaLogin,
)
from backend.apresentacao.schemas.comuns import MensagemSimples

roteador = APIRouter(prefix="/api/auth", tags=["Autenticação"])


@roteador.post("/login", response_model=SaidaLogin)
def login(
    requisicao: Request,
    dados: EntradaLogin,
    repo_funcionarios=Depends(obter_repo_funcionarios),
    repo_auditoria=Depends(obter_repo_auditoria),
    servico_senha=Depends(obter_servico_senha),
    servico_token=Depends(obter_servico_token),
):
    caso = AutenticarFuncionario(
        repo_funcionarios, servico_senha, servico_token, repo_auditoria
    )
    resultado = caso.executar(
        dados.email,
        dados.senha,
        endereco_ip=requisicao.client.host if requisicao.client else None,
        agente_usuario=requisicao.headers.get("user-agent"),
    )
    return SaidaLogin(
        token_acesso=resultado.token_acesso,
        token_refresh=resultado.token_refresh,
        deve_trocar_senha=resultado.deve_trocar_senha,
        funcionario=FuncionarioResumido(
            identificador=resultado.funcionario.identificador,
            nome_completo=resultado.funcionario.nome_completo,
            email=resultado.funcionario.email,
            cargo=resultado.funcionario.cargo,
            papeis=[p.value for p in resultado.funcionario.papeis],
        ),
    )


@roteador.post("/trocar-senha", response_model=MensagemSimples)
def trocar_senha(
    dados: EntradaTrocaSenha,
    funcionario=Depends(obter_funcionario_logado),
    repo_funcionarios=Depends(obter_repo_funcionarios),
    repo_auditoria=Depends(obter_repo_auditoria),
    servico_senha=Depends(obter_servico_senha),
):
    caso = TrocarSenha(repo_funcionarios, servico_senha, repo_auditoria)
    caso.executar(funcionario.identificador, dados.senha_atual, dados.senha_nova)
    return MensagemSimples(mensagem="Senha alterada com sucesso.")


@roteador.get("/eu", response_model=FuncionarioResumido)
def eu(funcionario=Depends(obter_funcionario_logado)):
    return FuncionarioResumido(
        identificador=funcionario.identificador,
        nome_completo=funcionario.nome_completo,
        email=funcionario.email,
        cargo=funcionario.cargo,
        papeis=[p.value for p in funcionario.papeis],
    )
