"""Interface — Serviço de Token (JWT) usado para autenticação."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class DadosToken:
    """Carga útil mínima de um token de acesso."""

    funcionario_id: int
    email: str
    papeis: list[str]


class ServicoToken(ABC):
    @abstractmethod
    def gerar_token_acesso(self, dados: DadosToken) -> str: ...

    @abstractmethod
    def gerar_token_refresh(self, funcionario_id: int) -> str: ...

    @abstractmethod
    def decodificar(self, token: str) -> Optional[dict]: ...
