"""Entidades de documentos e assinatura digital."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ModeloDocumento:
    """Modelo (template) de documento gerável pelo sistema."""

    titulo: str
    chave: str  # ex.: "termo_responsabilidade"
    conteudo_template: str  # texto com placeholders {{residente_nome}}
    descricao: Optional[str] = None
    ativo: bool = True
    identificador: Optional[int] = None


@dataclass
class DocumentoAssinado:
    """Documento gerado e assinado no sistema."""

    modelo_id: int
    titulo: str
    residente_id: Optional[int]
    funcionario_id: int
    caminho_arquivo: str
    hash_sha256: str
    gerado_em: datetime
    assinado_em: Optional[datetime] = None
    nome_assinante: Optional[str] = None
    documento_assinante: Optional[str] = None
    imagem_assinatura_base64: Optional[str] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None

    def esta_assinado(self) -> bool:
        return self.assinado_em is not None
