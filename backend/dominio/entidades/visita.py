"""Entidade Visita (familiares ou terceiros)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Visita:
    """Visita registrada na recepção."""

    residente_id: int
    nome_visitante: str
    documento_visitante: str
    parentesco_ou_relacao: str
    entrada_em: datetime
    saida_em: Optional[datetime] = None
    funcionario_recebeu_id: Optional[int] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None

    def encerrar(self, saida: Optional[datetime] = None) -> None:
        self.saida_em = saida or datetime.utcnow()
