"""Porta — Repositório de Auditoria."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria


class RepositorioAuditoria(ABC):
    @abstractmethod
    def registrar(self, log: LogAuditoria) -> LogAuditoria: ...

    @abstractmethod
    def listar(
        self,
        funcionario_id: Optional[int] = None,
        recurso: Optional[str] = None,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[LogAuditoria]: ...
