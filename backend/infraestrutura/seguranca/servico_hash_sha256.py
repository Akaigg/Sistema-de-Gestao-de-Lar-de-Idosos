"""Implementação de ServicoHashDocumento usando SHA-256 da biblioteca padrão."""

from __future__ import annotations

import hashlib
from pathlib import Path

from backend.dominio.servicos.servico_hash_documento import ServicoHashDocumento


class ServicoHashSHA256(ServicoHashDocumento):
    def calcular_hash_de_bytes(self, conteudo: bytes) -> str:
        return hashlib.sha256(conteudo).hexdigest()

    def calcular_hash_de_arquivo(self, caminho: str) -> str:
        hasher = hashlib.sha256()
        with Path(caminho).open("rb") as arquivo:
            for bloco in iter(lambda: arquivo.read(8192), b""):
                hasher.update(bloco)
        return hasher.hexdigest()
