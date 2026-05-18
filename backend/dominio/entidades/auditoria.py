"""Entidade LogAuditoria — registros imutáveis de ações sensíveis."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LogAuditoria:
    """Entrada da trilha de auditoria (append-only)."""

    ocorrido_em: datetime
    funcionario_id: Optional[int]
    acao: str  # "CRIAR", "EDITAR", "EXCLUIR", "LOGIN", "LOGOUT", "LOGIN_FALHOU"
    recurso: str  # "residente", "prescricao"...
    recurso_id: Optional[int] = None
    detalhes: Optional[str] = None
    endereco_ip: Optional[str] = None
    agente_usuario: Optional[str] = None
    identificador: Optional[int] = None
