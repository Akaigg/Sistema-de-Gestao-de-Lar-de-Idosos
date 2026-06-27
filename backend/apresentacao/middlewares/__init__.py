"""Middlewares e tratadores de erro."""

from backend.apresentacao.middlewares.tratamento_erros import (
    registrar_tratadores_de_erro,
)

__all__ = ["registrar_tratadores_de_erro"]
