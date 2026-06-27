"""Porta — Repositório de Escalas."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from backend.dominio.entidades.escala import Escala, Turno


class RepositorioEscalas(ABC):
    @abstractmethod
    def criar(self, escala: Escala) -> Escala: ...

    @abstractmethod
    def atualizar(self, escala: Escala) -> Escala: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Escala]: ...

    @abstractmethod
    def buscar_por_mes(self, mes: int, ano: int, setor: Optional[str] = None) -> list[Escala]: ...

    @abstractmethod
    def adicionar_turno(self, escala_id: int, turno: Turno) -> Turno: ...

    @abstractmethod
    def excluir_turno(self, turno_id: int) -> None: ...

    @abstractmethod
    def listar_turnos_do_dia(self, dia: date) -> list[Turno]: ...

    @abstractmethod
    def listar_turnos_funcionario(
        self, funcionario_id: int, inicio: date, fim: date
    ) -> list[Turno]: ...
