"""Porta — Repositório de Responsáveis."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from backend.dominio.entidades.responsavel import Responsavel


class RepositorioResponsaveis(ABC):
    @abstractmethod
    def criar(self, responsavel: Responsavel, residente_id: int) -> Responsavel: ...

    @abstractmethod
    def atualizar(self, responsavel: Responsavel) -> Responsavel: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Responsavel]: ...

    @abstractmethod
    def listar_por_residente(self, residente_id: int) -> list[Responsavel]: ...

    @abstractmethod
    def excluir_vinculo(self, responsavel_id: int, residente_id: int) -> None: ...
