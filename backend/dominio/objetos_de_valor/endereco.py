"""Objeto de valor Endereço."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Endereco:
    """Endereço residencial."""

    logradouro: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str
    complemento: Optional[str] = None

    def linha_unica(self) -> str:
        partes = [
            f"{self.logradouro}, {self.numero}",
            self.complemento or None,
            self.bairro,
            f"{self.cidade}-{self.estado}",
            self.cep,
        ]
        return " · ".join([p for p in partes if p])
