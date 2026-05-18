"""Objeto de valor Periodo (intervalo de datas/horas)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from backend.dominio.excecoes import DadosInvalidos


@dataclass(frozen=True)
class Periodo:
    """Intervalo fechado [inicio, fim]."""

    inicio: datetime
    fim: datetime

    def __post_init__(self) -> None:
        if self.fim < self.inicio:
            raise DadosInvalidos("Período inválido: fim anterior ao início.")

    def sobrepoe(self, outro: "Periodo") -> bool:
        return self.inicio <= outro.fim and outro.inicio <= self.fim

    def duracao_em_horas(self) -> float:
        return (self.fim - self.inicio).total_seconds() / 3600.0
