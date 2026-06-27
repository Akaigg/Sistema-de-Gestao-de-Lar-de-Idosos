"""Entidade Responsável (familiar ou responsável legal)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Responsavel:
    """Responsável legal ou familiar de um residente."""

    nome_completo: str
    cpf: str
    parentesco: str
    telefone: str
    email: Optional[str] = None
    endereco_resumido: Optional[str] = None
    eh_responsavel_legal: bool = False
    eh_contato_emergencia: bool = True
    observacoes: Optional[str] = None
    identificador: Optional[int] = None
