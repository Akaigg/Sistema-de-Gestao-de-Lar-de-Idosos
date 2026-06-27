"""Inicialização do motor SQLAlchemy + sessão para SQLite."""

from __future__ import annotations

from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from backend.infraestrutura.configuracao import configuracoes

motor = create_engine(
    configuracoes.url_banco,
    echo=False,
    connect_args={"check_same_thread": False},
    future=True,
)


@event.listens_for(motor, "connect")
def _ativar_pragmas_sqlite(conexao_dbapi, _registro_conexao):
    """Configura PRAGMAs do SQLite: foreign keys + WAL."""
    cursor = conexao_dbapi.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("PRAGMA journal_mode = WAL")
    cursor.execute("PRAGMA synchronous = NORMAL")
    cursor.close()


SessaoLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def obter_sessao() -> Iterator[Session]:
    """Dependência FastAPI: produz uma sessão por requisição."""
    sessao = SessaoLocal()
    try:
        yield sessao
    finally:
        sessao.close()


def criar_tabelas() -> None:
    """Cria todas as tabelas (uso em desenvolvimento / inicialização)."""
    # Importa modelos para registrar no metadata
    from backend.infraestrutura.banco_de_dados import modelos  # noqa: F401

    Base.metadata.create_all(bind=motor)
