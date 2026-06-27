"""Entidades de Medicamento, Prescrição e Aplicação."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from enum import Enum
from typing import Optional

from backend.dominio.excecoes import DadosInvalidos, RegraDeNegocioViolada


class ViaAdministracao(str, Enum):
    ORAL = "oral"
    SUBLINGUAL = "sublingual"
    TOPICA = "topica"
    INTRAVENOSA = "intravenosa"
    INTRAMUSCULAR = "intramuscular"
    SUBCUTANEA = "subcutanea"
    INALATORIA = "inalatoria"
    OFTALMICA = "oftalmica"
    OTOLOGICA = "otologica"
    RETAL = "retal"
    OUTRA = "outra"


class StatusAplicacao(str, Enum):
    AGUARDANDO = "aguardando"
    APLICADO = "aplicado"
    APLICADO_COM_ATRASO = "aplicado_com_atraso"
    EM_ATRASO = "em_atraso"
    RECUSADO = "recusado"
    SUSPENSO = "suspenso"
    REACAO_ADVERSA = "reacao_adversa"


@dataclass
class Medicamento:
    """Catálogo de medicamentos."""

    nome_comercial: str
    principio_ativo: str
    forma_farmaceutica: str  # comprimido, xarope, ampola...
    concentracao: str  # ex.: "500mg"
    fabricante: Optional[str] = None
    necessita_receita: bool = True
    controlado: bool = False
    observacoes: Optional[str] = None
    estoque_minimo: int = 10
    identificador: Optional[int] = None


@dataclass
class LoteMedicamento:
    """Lote de um medicamento em estoque."""

    medicamento_id: int
    numero_lote: str
    quantidade: int
    data_validade: date
    data_entrada: date
    fornecedor: Optional[str] = None
    preco_unitario: Optional[float] = None
    identificador: Optional[int] = None

    def esta_vencido(self, hoje: Optional[date] = None) -> bool:
        return self.data_validade < (hoje or date.today())

    def dias_para_vencer(self, hoje: Optional[date] = None) -> int:
        return (self.data_validade - (hoje or date.today())).days


@dataclass
class Prescricao:
    """Prescrição médica para um residente."""

    residente_id: int
    medicamento_id: int
    medico_id: int
    dose: str
    via: ViaAdministracao
    frequencia_horas: int  # de quantas em quantas horas
    horarios: list[time]  # horários gerados/escolhidos no dia
    data_inicio: date
    duracao_dias: Optional[int] = None
    se_necessario: bool = False  # SOS
    observacoes: Optional[str] = None
    suspensa: bool = False
    data_suspensao: Optional[date] = None
    motivo_suspensao: Optional[str] = None
    identificador: Optional[int] = None

    def __post_init__(self) -> None:
        if self.frequencia_horas <= 0 or self.frequencia_horas > 24:
            raise DadosInvalidos("Frequência deve estar entre 1 e 24 horas.")
        if not self.horarios:
            raise DadosInvalidos("A prescrição precisa ter ao menos um horário.")

    def data_termino(self) -> Optional[date]:
        if self.duracao_dias is None:
            return None
        return self.data_inicio + timedelta(days=self.duracao_dias)

    def esta_ativa_em(self, momento: date) -> bool:
        if self.suspensa:
            return False
        if momento < self.data_inicio:
            return False
        termino = self.data_termino()
        if termino is not None and momento > termino:
            return False
        return True

    def suspender(self, motivo: str, quando: Optional[date] = None) -> None:
        if self.suspensa:
            raise RegraDeNegocioViolada("Prescrição já está suspensa.")
        self.suspensa = True
        self.motivo_suspensao = motivo
        self.data_suspensao = quando or date.today()


@dataclass
class AplicacaoMedicamento:
    """Registro de aplicação (ou não) de uma dose."""

    prescricao_id: int
    horario_previsto: datetime
    status: StatusAplicacao = StatusAplicacao.AGUARDANDO
    horario_aplicado: Optional[datetime] = None
    funcionario_id: Optional[int] = None
    observacoes: Optional[str] = None
    motivo_recusa: Optional[str] = None
    reacao_descrita: Optional[str] = None
    identificador: Optional[int] = None

    LIMITE_ATRASO_MINUTOS = 60

    def aplicar(
        self,
        funcionario_id: int,
        momento: Optional[datetime] = None,
        observacoes: Optional[str] = None,
    ) -> None:
        agora = momento or datetime.utcnow()
        diferenca = (agora - self.horario_previsto).total_seconds() / 60.0
        if abs(diferenca) <= self.LIMITE_ATRASO_MINUTOS:
            self.status = StatusAplicacao.APLICADO
        else:
            self.status = StatusAplicacao.APLICADO_COM_ATRASO
        self.horario_aplicado = agora
        self.funcionario_id = funcionario_id
        if observacoes:
            self.observacoes = observacoes

    def recusar(self, funcionario_id: int, motivo: str) -> None:
        self.status = StatusAplicacao.RECUSADO
        self.motivo_recusa = motivo
        self.funcionario_id = funcionario_id
        self.horario_aplicado = datetime.utcnow()

    def registrar_reacao(self, funcionario_id: int, descricao: str) -> None:
        self.status = StatusAplicacao.REACAO_ADVERSA
        self.reacao_descrita = descricao
        self.funcionario_id = funcionario_id
        self.horario_aplicado = datetime.utcnow()
