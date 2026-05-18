"""Objeto de valor Telefone."""

from __future__ import annotations

import re
from dataclasses import dataclass

from backend.dominio.excecoes import DadosInvalidos


@dataclass(frozen=True)
class Telefone:
    """Telefone brasileiro com DDD (10 ou 11 dígitos)."""

    numero: str

    def __post_init__(self) -> None:
        somente_digitos = re.sub(r"\D", "", self.numero)
        if len(somente_digitos) not in (10, 11):
            raise DadosInvalidos(f"Telefone inválido: {self.numero!r}")
        object.__setattr__(self, "numero", somente_digitos)

    def formatado(self) -> str:
        if len(self.numero) == 11:
            return f"({self.numero[:2]}) {self.numero[2:7]}-{self.numero[7:]}"
        return f"({self.numero[:2]}) {self.numero[2:6]}-{self.numero[6:]}"

    def __str__(self) -> str:
        return self.numero
