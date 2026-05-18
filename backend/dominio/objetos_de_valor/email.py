"""Objeto de valor Email."""

from __future__ import annotations

import re
from dataclasses import dataclass

from backend.dominio.excecoes import DadosInvalidos

_PADRAO_EMAIL = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


@dataclass(frozen=True)
class Email:
    """Endereço de e-mail validado por regex simples."""

    endereco: str

    def __post_init__(self) -> None:
        endereco_normalizado = self.endereco.strip().lower()
        if not _PADRAO_EMAIL.match(endereco_normalizado):
            raise DadosInvalidos(f"E-mail inválido: {self.endereco!r}")
        object.__setattr__(self, "endereco", endereco_normalizado)

    def __str__(self) -> str:
        return self.endereco
