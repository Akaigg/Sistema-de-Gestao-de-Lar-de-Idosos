"""Porta — Repositório de Visitas."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from backend.dominio.entidades.visita import Visita


class RepositorioVisitas(ABC):
    @abstractmethod
    def criar(self, visita: Visita) -> Visita: ...

    @abstractmethod
    def atualizar(self, visita: Visita) -> Visita: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Visita]: ...

    @abstractmethod
    def listar(
        self,
        residente_id: Optional[int] = None,
        dia: Optional[date] = None,
    ) -> list[Visita]: ...
