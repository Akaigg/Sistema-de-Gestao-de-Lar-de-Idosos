"""Porta — Repositórios do prontuário."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.prontuario import (
    SinaisVitais,
    Evolucao,
    Alergia,
    CondicaoCronica,
    Consulta,
    StatusConsulta,
)


class RepositorioSinaisVitais(ABC):
    @abstractmethod
    def criar(self, sinais: SinaisVitais) -> SinaisVitais: ...

    @abstractmethod
    def listar_por_residente(
        self,
        residente_id: int,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
    ) -> list[SinaisVitais]: ...


class RepositorioEvolucoes(ABC):
    @abstractmethod
    def criar(self, evolucao: Evolucao) -> Evolucao: ...

    @abstractmethod
    def listar_por_residente(self, residente_id: int) -> list[Evolucao]: ...


class RepositorioAlergias(ABC):
    @abstractmethod
    def criar(self, alergia: Alergia) -> Alergia: ...

    @abstractmethod
    def excluir(self, identificador: int) -> None: ...

    @abstractmethod
    def listar_por_residente(self, residente_id: int) -> list[Alergia]: ...


class RepositorioCondicoesCronicas(ABC):
    @abstractmethod
    def criar(self, condicao: CondicaoCronica) -> CondicaoCronica: ...

    @abstractmethod
    def excluir(self, identificador: int) -> None: ...

    @abstractmethod
    def listar_por_residente(self, residente_id: int) -> list[CondicaoCronica]: ...


class RepositorioConsultas(ABC):
    @abstractmethod
    def criar(self, consulta: Consulta) -> Consulta: ...

    @abstractmethod
    def atualizar(self, consulta: Consulta) -> Consulta: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Consulta]: ...

    @abstractmethod
    def listar_por_periodo(
        self,
        inicio: datetime,
        fim: datetime,
        residente_id: Optional[int] = None,
        status: Optional[StatusConsulta] = None,
    ) -> list[Consulta]: ...

    @abstractmethod
    def contar_do_dia(self, dia: date) -> int: ...
