"""Configuração de banco de dados (SQLAlchemy + SQLite)."""

from backend.infraestrutura.banco_de_dados.sessao import (
    Base,
    SessaoLocal,
    motor,
    obter_sessao,
    criar_tabelas,
)

__all__ = ["Base", "SessaoLocal", "motor", "obter_sessao", "criar_tabelas"]
