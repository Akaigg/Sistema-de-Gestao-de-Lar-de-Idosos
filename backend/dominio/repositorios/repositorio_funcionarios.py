"""Porta — Repositório de Funcionários."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from backend.dominio.entidades.funcionario import Funcionario


class RepositorioFuncionarios(ABC):
    """Interface para persistência de funcionários."""

    @abstractmethod
    def criar(self, funcionario: Funcionario) -> Funcionario: ...

    @abstractmethod
    def atualizar(self, funcionario: Funcionario) -> Funcionario: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[Funcionario]: ...

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Funcionario]: ...

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Funcionario]: ...

    @abstractmethod
    def listar(
        self,
        termo_busca: Optional[str] = None,
        apenas_ativos: bool = True,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[Funcionario]: ...

    @abstractmethod
    def contar(self, termo_busca: Optional[str] = None, apenas_ativos: bool = True) -> int: ...

    @abstractmethod
    def registrar_tentativa_login(
        self, email: str, sucesso: bool, endereco_ip: Optional[str] = None
    ) -> None: ...

    @abstractmethod
    def contar_tentativas_recentes(self, email: str, minutos: int = 15) -> int: ...
