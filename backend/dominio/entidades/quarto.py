"""Entidades de Quarto e Leito."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from backend.dominio.excecoes import RegraDeNegocioViolada


class TipoQuarto(str, Enum):
    INDIVIDUAL = "individual"
    DUPLO = "duplo"
    TRIPLO = "triplo"
    ENFERMARIA = "enfermaria"


class StatusQuarto(str, Enum):
    ATIVO = "ativo"
    EM_MANUTENCAO = "em_manutencao"
    DESATIVADO = "desativado"


class StatusLeito(str, Enum):
    LIVRE = "livre"
    OCUPADO = "ocupado"
    EM_HIGIENIZACAO = "em_higienizacao"
    BLOQUEADO = "bloqueado"


@dataclass
class Leito:
    """Leito dentro de um quarto."""

    numero: str
    status: StatusLeito = StatusLeito.LIVRE
    residente_id: Optional[int] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None

    def ocupar(self, residente_id: int) -> None:
        if self.status == StatusLeito.OCUPADO:
            raise RegraDeNegocioViolada("Leito já está ocupado.")
        if self.status == StatusLeito.BLOQUEADO:
            raise RegraDeNegocioViolada("Leito bloqueado para uso.")
        self.residente_id = residente_id
        self.status = StatusLeito.OCUPADO

    def liberar(self) -> None:
        self.residente_id = None
        self.status = StatusLeito.EM_HIGIENIZACAO


@dataclass
class Quarto:
    """Quarto físico do lar."""

    numero: str
    andar: int
    tipo: TipoQuarto
    capacidade: int
    leitos: list[Leito] = field(default_factory=list)
    status: StatusQuarto = StatusQuarto.ATIVO
    possui_banheiro: bool = True
    possui_ar_condicionado: bool = False
    acessibilidade: bool = True
    observacoes: Optional[str] = None
    identificador: Optional[int] = None

    def leitos_livres(self) -> list[Leito]:
        return [leito for leito in self.leitos if leito.status == StatusLeito.LIVRE]

    def esta_cheio(self) -> bool:
        return len(self.leitos_livres()) == 0

    def taxa_ocupacao(self) -> float:
        if not self.leitos:
            return 0.0
        ocupados = sum(1 for leito in self.leitos if leito.status == StatusLeito.OCUPADO)
        return ocupados / len(self.leitos)
