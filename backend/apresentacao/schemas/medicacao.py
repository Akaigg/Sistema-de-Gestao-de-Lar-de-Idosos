"""Schemas para medicação."""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional

from pydantic import Field

from backend.apresentacao.schemas.comuns import ModeloBase


class EntradaMedicamento(ModeloBase):
    nome_comercial: str
    principio_ativo: str
    forma_farmaceutica: str
    concentracao: str
    fabricante: Optional[str] = None
    necessita_receita: bool = True
    controlado: bool = False
    estoque_minimo: int = 10
    observacoes: Optional[str] = None


class MedicamentoSaida(ModeloBase):
    identificador: int
    nome_comercial: str
    principio_ativo: str
    forma_farmaceutica: str
    concentracao: str
    fabricante: Optional[str] = None
    necessita_receita: bool
    controlado: bool
    estoque_minimo: int


class EntradaPrescricao(ModeloBase):
    residente_id: int
    medicamento_id: int
    medico_id: int
    dose: str
    via: str
    frequencia_horas: int = Field(ge=1, le=24)
    horarios: list[str]  # ["08:00", "14:00", "20:00"]
    data_inicio: date
    duracao_dias: Optional[int] = None
    se_necessario: bool = False
    observacoes: Optional[str] = None


class PrescricaoSaida(ModeloBase):
    identificador: int
    residente_id: int
    medicamento_id: int
    medico_id: int
    dose: str
    via: str
    frequencia_horas: int
    horarios: list[str]
    data_inicio: date
    duracao_dias: Optional[int] = None
    se_necessario: bool
    suspensa: bool
    motivo_suspensao: Optional[str] = None
    observacoes: Optional[str] = None


class EntradaAplicarMedicamento(ModeloBase):
    acao: str = Field(pattern="^(aplicar|recusar|reacao)$")
    observacoes: Optional[str] = None
    motivo_recusa: Optional[str] = None
    descricao_reacao: Optional[str] = None


class AplicacaoSaida(ModeloBase):
    identificador: int
    prescricao_id: int
    horario_previsto: datetime
    status: str
    horario_aplicado: Optional[datetime] = None
    funcionario_id: Optional[int] = None
    observacoes: Optional[str] = None
    motivo_recusa: Optional[str] = None
    reacao_descrita: Optional[str] = None


class AplicacaoCalendario(ModeloBase):
    """Formato amigável para o FullCalendar."""

    id: int
    title: str
    start: datetime
    end: Optional[datetime] = None
    color: Optional[str] = None
    extendedProps: dict


class EntradaLoteMedicamento(ModeloBase):
    medicamento_id: int
    numero_lote: str
    quantidade: int = Field(ge=1)
    data_validade: date
    fornecedor: Optional[str] = None
    preco_unitario: Optional[float] = None


class LoteSaida(ModeloBase):
    identificador: int
    medicamento_id: int
    numero_lote: str
    quantidade: int
    data_validade: date
    data_entrada: date
    fornecedor: Optional[str] = None
    preco_unitario: Optional[float] = None
