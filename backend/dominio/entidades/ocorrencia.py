"""Entidade Ocorrência (queda, intercorrência, evasão, etc.)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TipoOcorrencia(str, Enum):
    QUEDA = "queda"
    INTERCORRENCIA_CLINICA = "intercorrencia_clinica"
    AGRESSIVIDADE = "agressividade"
    EVASAO = "evasao"
    REACAO_MEDICAMENTOSA = "reacao_medicamentosa"
    ACIDENTE = "acidente"
    OUTRA = "outra"


class GravidadeOcorrencia(str, Enum):
    LEVE = "leve"
    MODERADA = "moderada"
    GRAVE = "grave"
    CRITICA = "critica"


@dataclass
class Ocorrencia:
    """Registro de uma ocorrência relevante."""

    residente_id: int
    tipo: TipoOcorrencia
    gravidade: GravidadeOcorrencia
    descricao: str
    ocorreu_em: datetime
    registrada_por_id: int
    local: Optional[str] = None
    medidas_adotadas: Optional[str] = None
    necessitou_hospital: bool = False
    encerrada: bool = False
    encerrada_em: Optional[datetime] = None
    identificador: Optional[int] = None
