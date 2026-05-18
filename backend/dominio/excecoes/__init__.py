"""Exceções de domínio."""

from backend.dominio.excecoes.excecoes_dominio import (
    ErroDeDominio,
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
    CredenciaisInvalidas,
    ContaBloqueada,
    AcessoNegado,
    EntidadeJaExistente,
    DadosInvalidos,
)

__all__ = [
    "ErroDeDominio",
    "EntidadeNaoEncontrada",
    "RegraDeNegocioViolada",
    "CredenciaisInvalidas",
    "ContaBloqueada",
    "AcessoNegado",
    "EntidadeJaExistente",
    "DadosInvalidos",
]
