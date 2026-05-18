"""Entidades financeiras."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional


class TipoLancamento(str, Enum):
    RECEITA = "receita"
    DESPESA = "despesa"


class StatusPagamento(str, Enum):
    EM_ABERTO = "em_aberto"
    PAGO = "pago"
    ATRASADO = "atrasado"
    CANCELADO = "cancelado"
    PARCIAL = "parcial"


class FormaPagamento(str, Enum):
    DINHEIRO = "dinheiro"
    PIX = "pix"
    BOLETO = "boleto"
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"


@dataclass
class Mensalidade:
    """Mensalidade de um residente."""

    residente_id: int
    competencia_mes: int
    competencia_ano: int
    valor: float
    data_vencimento: date
    status: StatusPagamento = StatusPagamento.EM_ABERTO
    data_pagamento: Optional[date] = None
    valor_pago: Optional[float] = None
    forma_pagamento: Optional[FormaPagamento] = None
    desconto: float = 0.0
    juros_multa: float = 0.0
    observacoes: Optional[str] = None
    identificador: Optional[int] = None

    def total_a_pagar(self) -> float:
        return max(0.0, self.valor + self.juros_multa - self.desconto)

    def quitar(
        self,
        valor_pago: float,
        forma: FormaPagamento,
        quando: Optional[date] = None,
    ) -> None:
        self.valor_pago = valor_pago
        self.forma_pagamento = forma
        self.data_pagamento = quando or date.today()
        total = self.total_a_pagar()
        if valor_pago >= total:
            self.status = StatusPagamento.PAGO
        else:
            self.status = StatusPagamento.PARCIAL

    def esta_atrasada(self, hoje: Optional[date] = None) -> bool:
        referencia = hoje or date.today()
        return (
            self.status in (StatusPagamento.EM_ABERTO, StatusPagamento.PARCIAL)
            and self.data_vencimento < referencia
        )


@dataclass
class LancamentoFinanceiro:
    """Receita ou despesa avulsa."""

    tipo: TipoLancamento
    descricao: str
    valor: float
    data_competencia: date
    data_pagamento: Optional[date] = None
    categoria: Optional[str] = None
    centro_custo: Optional[str] = None
    fornecedor: Optional[str] = None
    forma_pagamento: Optional[FormaPagamento] = None
    status: StatusPagamento = StatusPagamento.EM_ABERTO
    registrado_em: datetime = datetime.utcnow()
    registrado_por_id: Optional[int] = None
    identificador: Optional[int] = None
