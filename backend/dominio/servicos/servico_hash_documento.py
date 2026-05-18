"""Interface — Serviço de Hash de Documento (SHA-256)."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ServicoHashDocumento(ABC):
    """Calcula hash SHA-256 de bytes ou arquivo."""

    @abstractmethod
    def calcular_hash_de_bytes(self, conteudo: bytes) -> str: ...

    @abstractmethod
    def calcular_hash_de_arquivo(self, caminho: str) -> str: ...
