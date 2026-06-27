"""Entidades do prontuário: sinais vitais, evoluções, alergias, consultas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


@dataclass
class SinaisVitais:
    """Aferição de sinais vitais."""

    residente_id: int
    aferido_em: datetime
    funcionario_id: int
    pressao_sistolica: Optional[int] = None
    pressao_diastolica: Optional[int] = None
    frequencia_cardiaca: Optional[int] = None
    frequencia_respiratoria: Optional[int] = None
    temperatura: Optional[float] = None
    saturacao_oxigenio: Optional[int] = None
    glicemia: Optional[int] = None
    peso: Optional[float] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None


@dataclass
class Evolucao:
    """Nota de evolução (médica ou de enfermagem)."""

    residente_id: int
    funcionario_id: int
    registrada_em: datetime
    categoria: str  # "medica", "enfermagem", "fisioterapia", "psicologia"...
    texto: str
    identificador: Optional[int] = None


@dataclass
class Alergia:
    residente_id: int
    substancia: str
    reacao: Optional[str] = None
    gravidade: str = "leve"  # leve, moderada, grave
    observacoes: Optional[str] = None
    identificador: Optional[int] = None


@dataclass
class CondicaoCronica:
    residente_id: int
    descricao: str  # ex.: "Hipertensão arterial sistêmica"
    cid10: Optional[str] = None
    data_diagnostico: Optional[str] = None
    observacoes: Optional[str] = None
    identificador: Optional[int] = None


class TipoConsulta(str, Enum):
    CONSULTA_MEDICA = "consulta_medica"
    EXAME = "exame"
    PROCEDIMENTO = "procedimento"
    FISIOTERAPIA = "fisioterapia"
    PSICOLOGIA = "psicologia"
    NUTRICAO = "nutricao"
    ODONTOLOGIA = "odontologia"
    OUTRO = "outro"


class StatusConsulta(str, Enum):
    AGENDADA = "agendada"
    CONFIRMADA = "confirmada"
    REALIZADA = "realizada"
    CANCELADA = "cancelada"
    REMARCADA = "remarcada"
    FALTOU = "faltou"


@dataclass
class Consulta:
    """Agendamento de consulta/exame/procedimento."""

    residente_id: int
    tipo: TipoConsulta
    data_hora: datetime
    eh_externa: bool
    profissional: str
    especialidade: Optional[str] = None
    local: Optional[str] = None
    motivo: Optional[str] = None
    observacoes: Optional[str] = None
    status: StatusConsulta = StatusConsulta.AGENDADA
    motivo_cancelamento: Optional[str] = None
    funcionario_acompanhante_id: Optional[int] = None
    identificador: Optional[int] = None

    def cancelar(self, motivo: str) -> None:
        self.status = StatusConsulta.CANCELADA
        self.motivo_cancelamento = motivo

    def marcar_realizada(self) -> None:
        self.status = StatusConsulta.REALIZADA
