"""Registra tratadores globais de erro do FastAPI."""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from backend.dominio.excecoes import (
    AcessoNegado,
    ContaBloqueada,
    CredenciaisInvalidas,
    DadosInvalidos,
    EntidadeJaExistente,
    EntidadeNaoEncontrada,
    ErroDeDominio,
    RegraDeNegocioViolada,
)

logger = logging.getLogger("cuidarmais")


def registrar_tratadores_de_erro(app: FastAPI) -> None:
    """Registra os tratadores no app FastAPI."""

    @app.exception_handler(EntidadeNaoEncontrada)
    async def _nao_encontrada(_req: Request, exc: EntidadeNaoEncontrada):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(EntidadeJaExistente)
    async def _ja_existe(_req: Request, exc: EntidadeJaExistente):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(CredenciaisInvalidas)
    async def _credenciais(_req: Request, exc: CredenciaisInvalidas):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(ContaBloqueada)
    async def _bloqueada(_req: Request, exc: ContaBloqueada):
        return JSONResponse(
            status_code=status.HTTP_423_LOCKED,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(AcessoNegado)
    async def _acesso(_req: Request, exc: AcessoNegado):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(DadosInvalidos)
    async def _invalidos(_req: Request, exc: DadosInvalidos):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(RegraDeNegocioViolada)
    async def _regra(_req: Request, exc: RegraDeNegocioViolada):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detalhe": exc.mensagem},
        )

    @app.exception_handler(ErroDeDominio)
    async def _generico(_req: Request, exc: ErroDeDominio):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detalhe": exc.mensagem},
        )
