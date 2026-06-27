"""Porta — Repositório de Residentes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from backend.dominio.entidades.residente import Residente, StatusResidente


class RepositorioResidentes(ABC):
    @abstractmethod
    def criar(self, residente: Residente) -> Residente: ...

    @abstractmethod
    def atualizar(self, residente: Residente) -> Residente: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Residente]: ...

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Residente]: ...

    @abstractmethod
    def listar(
        self,
        termo_busca: Optional[str] = None,
        status: Optional[StatusResidente] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[Residente]: ...

    @abstractmethod
    def contar(
        self,
        termo_busca: Optional[str] = None,
        status: Optional[StatusResidente] = None,
    ) -> int: ...

    @abstractmethod
    def listar_aniversariantes_do_mes(self, mes: int) -> list[Residente]: ...

    @abstractmethod
    def contar_ativos(self) -> int: ...
