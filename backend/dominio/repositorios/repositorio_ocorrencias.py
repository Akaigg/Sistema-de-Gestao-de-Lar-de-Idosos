"""Porta — Repositório de Ocorrências."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from backend.dominio.entidades.ocorrencia import Ocorrencia


class RepositorioOcorrencias(ABC):
    @abstractmethod
    def criar(self, ocorrencia: Ocorrencia) -> Ocorrencia: ...

    @abstractmethod
    def atualizar(self, ocorrencia: Ocorrencia) -> Ocorrencia: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Ocorrencia]: ...

    @abstractmethod
    def listar(
        self,
        residente_id: Optional[int] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> list[Ocorrencia]: ...
