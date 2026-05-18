"""Carrega configurações via variáveis de ambiente (com defaults seguros)."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parents[3]


@dataclass
class Configuracoes:
    nome_aplicacao: str = "Cuidar+"
    versao: str = "1.0.0"
    ambiente: str = os.getenv("AMBIENTE", "desenvolvimento")

    diretorio_dados: Path = RAIZ_PROJETO / "dados"
    diretorio_uploads: Path = RAIZ_PROJETO / "backend" / "uploads"
    diretorio_assinaturas: Path = RAIZ_PROJETO / "backend" / "assinaturas"
    diretorio_frontend: Path = RAIZ_PROJETO / "frontend"

    arquivo_banco: Path = RAIZ_PROJETO / "dados" / "cuidarmais.db"
    url_banco: str = ""

    chave_secreta_jwt: str = os.getenv(
        "CHAVE_SECRETA_JWT", secrets.token_urlsafe(48)
    )
    algoritmo_jwt: str = "HS256"
    minutos_expiracao_token: int = int(os.getenv("MINUTOS_TOKEN", "30"))
    dias_expiracao_refresh: int = int(os.getenv("DIAS_REFRESH", "7"))

    cors_origens: list[str] = (
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    )

    max_tentativas_login: int = 5
    janela_bloqueio_minutos: int = 15

    fuso_horario: str = "America/Sao_Paulo"

    def __post_init__(self) -> None:
        self.diretorio_dados.mkdir(parents=True, exist_ok=True)
        self.diretorio_uploads.mkdir(parents=True, exist_ok=True)
        self.diretorio_assinaturas.mkdir(parents=True, exist_ok=True)
        if not self.url_banco:
            self.url_banco = f"sqlite:///{self.arquivo_banco}"


configuracoes = Configuracoes()
