"""Entidades de alimentação: cardápio, refeição, dieta, hidratação."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class TipoRefeicao(str, Enum):
    CAFE_DA_MANHA = "cafe_da_manha"
    LANCHE_MANHA = "lanche_manha"
    ALMOCO = "almoco"
    LANCHE_TARDE = "lanche_tarde"
    JANTAR = "jantar"
    CEIA = "ceia"


class TipoDieta(str, Enum):
    LIVRE = "livre"
    HIPOSSODICA = "hipossodica"
    DIABETICA = "diabetica"
    HIPOCALORICA = "hipocalorica"
    HIPERCALORICA = "hipercalorica"
    PASTOSA = "pastosa"
    LIQUIDA = "liquida"
    ENTERAL = "enteral"
    SEM_LACTOSE = "sem_lactose"
    SEM_GLUTEN = "sem_gluten"
    OUTRA = "outra"


@dataclass
class Cardapio:
    """Cardápio diário (para todos os residentes)."""

    data_referencia: date
    tipo_refeicao: TipoRefeicao
    descricao: str
    calorias_aproximadas: Optional[int] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None


@dataclass
class Dieta:
    """Dieta individual de um residente."""

    residente_id: int
    tipo: TipoDieta
    descricao_detalhada: Optional[str] = None
    prescrita_por_id: Optional[int] = None
    data_inicio: date = field(default_factory=date.today)
    data_termino: Optional[date] = None
    ativa: bool = True
    identificador: Optional[int] = None


@dataclass
class Refeicao:
    """Registro de refeição servida e nível de aceitação."""

    residente_id: int
    cardapio_id: Optional[int]
    tipo_refeicao: TipoRefeicao
    servida_em: datetime
    funcionario_id: int
    aceitacao_percentual: int = 100  # 0..100
    observacoes: Optional[str] = None
    identificador: Optional[int] = None


@dataclass
class IngestaoHidrica:
    residente_id: int
    registrada_em: datetime
    quantidade_ml: int
    funcionario_id: int
    identificador: Optional[int] = None
