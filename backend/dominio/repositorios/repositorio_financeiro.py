"""Porta — Repositórios financeiros."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from backend.dominio.entidades.financeiro import (
    Mensalidade,
    LancamentoFinanceiro,
    StatusPagamento,
    TipoLancamento,
)


class RepositorioMensalidades(ABC):
    @abstractmethod
    def criar(self, mensalidade: Mensalidade) -> Mensalidade: ...

    @abstractmethod
    def atualizar(self, mensalidade: Mensalidade) -> Mensalidade: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Mensalidade]: ...

    @abstractmethod
    def listar(
        self,
        residente_id: Optional[int] = None,
        status: Optional[StatusPagamento] = None,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
    ) -> list[Mensalidade]: ...

    @abstractmethod
    def listar_atrasadas(self, hoje: date) -> list[Mensalidade]: ...


class RepositorioLancamentos(ABC):
    @abstractmethod
    def criar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro: ...

    @abstractmethod
    def atualizar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[LancamentoFinanceiro]: ...

    @abstractmethod
    def listar(
        self,
        tipo: Optional[TipoLancamento] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> list[LancamentoFinanceiro]: ...

    @abstractmethod
    def soma_por_tipo(
        self,
        tipo: TipoLancamento,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> float: ...
