"""Porta — Repositório de Quartos e Leitos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from backend.dominio.entidades.quarto import Quarto, Leito


class RepositorioQuartos(ABC):
    @abstractmethod
    def criar(self, quarto: Quarto) -> Quarto: ...

    @abstractmethod
    def atualizar(self, quarto: Quarto) -> Quarto: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Quarto]: ...

    @abstractmethod
    def listar(self) -> list[Quarto]: ...

    @abstractmethod
    def buscar_leito(self, leito_id: int) -> Optional[Leito]: ...

    @abstractmethod
    def atualizar_leito(self, leito: Leito) -> Leito: ...

    @abstractmethod
    def listar_leitos_do_quarto(self, quarto_id: int) -> list[Leito]: ...

    @abstractmethod
    def buscar_leito_por_residente(self, residente_id: int) -> Optional[Leito]: ...

    @abstractmethod
    def contar_leitos_ocupados(self) -> int: ...

    @abstractmethod
    def contar_leitos_totais(self) -> int: ...
