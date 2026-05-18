"""Interface — Serviço de Senha (hash, verificação, política)."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ServicoSenha(ABC):
    """Abstrai detalhes de hashing e política de senha forte."""

    @abstractmethod
    def gerar_hash(self, senha_em_texto: str) -> str: ...

    @abstractmethod
    def verificar(self, senha_em_texto: str, hash_armazenado: str) -> bool: ...

    @abstractmethod
    def validar_politica(self, senha_em_texto: str) -> None:
        """Levanta DadosInvalidos se senha violar a política mínima."""
        ...
