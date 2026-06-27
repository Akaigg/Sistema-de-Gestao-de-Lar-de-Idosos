"""Porta — Repositórios de Medicamento, Prescrição, Aplicação e Lotes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.medicamento import (
    Medicamento,
    Prescricao,
    AplicacaoMedicamento,
    LoteMedicamento,
)


class RepositorioMedicamentos(ABC):
    @abstractmethod
    def criar(self, medicamento: Medicamento) -> Medicamento: ...

    @abstractmethod
    def atualizar(self, medicamento: Medicamento) -> Medicamento: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Medicamento]: ...

    @abstractmethod
    def listar(self, termo_busca: Optional[str] = None) -> list[Medicamento]: ...


class RepositorioPrescricoes(ABC):
    @abstractmethod
    def criar(self, prescricao: Prescricao) -> Prescricao: ...

    @abstractmethod
    def atualizar(self, prescricao: Prescricao) -> Prescricao: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Prescricao]: ...

    @abstractmethod
    def listar_por_residente(
        self, residente_id: int, apenas_ativas: bool = True
    ) -> list[Prescricao]: ...

    @abstractmethod
    def listar_ativas_no_periodo(
        self, inicio: date, fim: date
    ) -> list[Prescricao]: ...


class RepositorioAplicacoes(ABC):
    @abstractmethod
    def criar(self, aplicacao: AplicacaoMedicamento) -> AplicacaoMedicamento: ...

    @abstractmethod
    def atualizar(self, aplicacao: AplicacaoMedicamento) -> AplicacaoMedicamento: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[AplicacaoMedicamento]: ...

    @abstractmethod
    def listar_por_periodo(
        self,
        inicio: datetime,
        fim: datetime,
        residente_id: Optional[int] = None,
    ) -> list[AplicacaoMedicamento]: ...

    @abstractmethod
    def listar_em_atraso(self, momento_referencia: datetime) -> list[AplicacaoMedicamento]: ...

    @abstractmethod
    def contar_do_dia(self, dia: date) -> int: ...


class RepositorioLotesMedicamento(ABC):
    @abstractmethod
    def criar(self, lote: LoteMedicamento) -> LoteMedicamento: ...

    @abstractmethod
    def atualizar(self, lote: LoteMedicamento) -> LoteMedicamento: ...

    @abstractmethod
    def listar_por_medicamento(self, medicamento_id: int) -> list[LoteMedicamento]: ...

    @abstractmethod
    def listar_proximos_vencimento(self, dias: int = 30) -> list[LoteMedicamento]: ...

    @abstractmethod
    def quantidade_total(self, medicamento_id: int) -> int: ...
