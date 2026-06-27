"""Dependências de autenticação e autorização (RBAC)."""

from __future__ import annotations

from typing import Iterable, Optional

from fastapi import Depends, Header, HTTPException, status

from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.infraestrutura.repositorios import RepositorioFuncionariosSQL
from backend.infraestrutura.seguranca import ServicoTokenJWT

from backend.apresentacao.dependencias.injecoes import (
    obter_repo_funcionarios,
    obter_servico_token,
)


def _extrair_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return authorization.split(" ", 1)[1].strip()


def obter_funcionario_logado(
    authorization: Optional[str] = Header(default=None),
    servico_token: ServicoTokenJWT = Depends(obter_servico_token),
    repositorio_funcionarios: RepositorioFuncionariosSQL = Depends(obter_repo_funcionarios),
) -> Funcionario:
    token = _extrair_token(authorization)
    carga = servico_token.decodificar(token)
    if not carga or carga.get("tipo") != "acesso":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        funcionario_id = int(carga["sub"])
    except (KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token corrompido.")
    funcionario = repositorio_funcionarios.buscar_por_id(funcionario_id)
    if not funcionario or not funcionario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conta inativa ou inexistente.",
        )
    return funcionario


def requer_papeis(*papeis_permitidos: PapelFuncionario):
    """Dependência que valida se o funcionário possui ao menos um dos papéis."""

    def _verificar(
        funcionario: Funcionario = Depends(obter_funcionario_logado),
    ) -> Funcionario:
        if PapelFuncionario.ADMINISTRADOR in funcionario.papeis:
            return funcionario  # admin tem acesso a tudo
        if not any(p in funcionario.papeis for p in papeis_permitidos):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para esta operação.",
            )
        return funcionario

    return _verificar
