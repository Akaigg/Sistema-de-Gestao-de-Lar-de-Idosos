"""Porta — Repositórios de alimentação."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.alimentacao import (
    Cardapio,
    Dieta,
    Refeicao,
    IngestaoHidrica,
)


class RepositorioCardapios(ABC):
    @abstractmethod
    def criar(self, cardapio: Cardapio) -> Cardapio: ...

    @abstractmethod
    def listar_por_data(self, dia: date) -> list[Cardapio]: ...

    @abstractmethod
    def listar_por_periodo(self, inicio: date, fim: date) -> list[Cardapio]: ...

    @abstractmethod
    def excluir(self, identificador: int) -> None: ...


class RepositorioDietas(ABC):
    @abstractmethod
    def criar(self, dieta: Dieta) -> Dieta: ...

    @abstractmethod
    def atualizar(self, dieta: Dieta) -> Dieta: ...

    @abstractmethod
    def listar_por_residente(
        self, residente_id: int, apenas_ativas: bool = True
    ) -> list[Dieta]: ...


class RepositorioRefeicoes(ABC):
    @abstractmethod
    def criar(self, refeicao: Refeicao) -> Refeicao: ...

    @abstractmethod
    def listar_por_residente(
        self,
        residente_id: int,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
    ) -> list[Refeicao]: ...


class RepositorioIngestaoHidrica(ABC):
    @abstractmethod
    def criar(self, registro: IngestaoHidrica) -> IngestaoHidrica: ...

    @abstractmethod
    def total_do_dia(self, residente_id: int, dia: date) -> int: ...

    @abstractmethod
    def listar_do_dia(self, residente_id: int, dia: date) -> list[IngestaoHidrica]: ...
