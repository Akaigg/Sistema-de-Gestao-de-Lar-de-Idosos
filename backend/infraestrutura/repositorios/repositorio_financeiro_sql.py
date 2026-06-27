"""Implementação SQLAlchemy dos repositórios financeiros."""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.dominio.entidades.financeiro import (
    Mensalidade,
    LancamentoFinanceiro,
    StatusPagamento,
    TipoLancamento,
)
from backend.dominio.repositorios.repositorio_financeiro import (
    RepositorioMensalidades,
    RepositorioLancamentos,
)
from backend.infraestrutura.banco_de_dados.modelos import (
    MensalidadeModel,
    LancamentoFinanceiroModel,
)
from backend.infraestrutura.repositorios._conversores import (
    mensalidade_para_entidade,
    mensalidade_para_modelo,
    lancamento_para_entidade,
    lancamento_para_modelo,
)


class RepositorioMensalidadesSQL(RepositorioMensalidades):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, mensalidade: Mensalidade) -> Mensalidade:
        m = mensalidade_para_modelo(mensalidade)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return mensalidade_para_entidade(m)

    def atualizar(self, mensalidade: Mensalidade) -> Mensalidade:
        m = self._sessao.get(MensalidadeModel, mensalidade.identificador)
        if not m:
            raise ValueError("Mensalidade não encontrada.")
        mensalidade_para_modelo(mensalidade, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return mensalidade_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[Mensalidade]:
        m = self._sessao.get(MensalidadeModel, identificador)
        return mensalidade_para_entidade(m) if m else None

    def listar(
        self,
        residente_id: Optional[int] = None,
        status: Optional[StatusPagamento] = None,
        mes: Optional[int] = None,
        ano: Optional[int] = None,
    ) -> list[Mensalidade]:
        query = self._sessao.query(MensalidadeModel)
        if residente_id is not None:
            query = query.filter(MensalidadeModel.residente_id == residente_id)
        if status is not None:
            query = query.filter(MensalidadeModel.status == status.value)
        if mes is not None:
            query = query.filter(MensalidadeModel.competencia_mes == mes)
        if ano is not None:
            query = query.filter(MensalidadeModel.competencia_ano == ano)
        modelos = query.order_by(MensalidadeModel.data_vencimento.desc()).all()
        return [mensalidade_para_entidade(m) for m in modelos]

    def listar_atrasadas(self, hoje: date) -> list[Mensalidade]:
        modelos = (
            self._sessao.query(MensalidadeModel)
            .filter(
                MensalidadeModel.status.in_(["em_aberto", "parcial"]),
                MensalidadeModel.data_vencimento < hoje,
            )
            .order_by(MensalidadeModel.data_vencimento)
            .all()
        )
        return [mensalidade_para_entidade(m) for m in modelos]


class RepositorioLancamentosSQL(RepositorioLancamentos):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro:
        m = lancamento_para_modelo(lancamento)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return lancamento_para_entidade(m)

    def atualizar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro:
        m = self._sessao.get(LancamentoFinanceiroModel, lancamento.identificador)
        if not m:
            raise ValueError("Lançamento não encontrado.")
        lancamento_para_modelo(lancamento, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return lancamento_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[LancamentoFinanceiro]:
        m = self._sessao.get(LancamentoFinanceiroModel, identificador)
        return lancamento_para_entidade(m) if m else None

    def listar(
        self,
        tipo: Optional[TipoLancamento] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> list[LancamentoFinanceiro]:
        query = self._sessao.query(LancamentoFinanceiroModel)
        if tipo is not None:
            query = query.filter(LancamentoFinanceiroModel.tipo == tipo.value)
        if inicio is not None:
            query = query.filter(LancamentoFinanceiroModel.data_competencia >= inicio)
        if fim is not None:
            query = query.filter(LancamentoFinanceiroModel.data_competencia <= fim)
        modelos = query.order_by(LancamentoFinanceiroModel.data_competencia.desc()).all()
        return [lancamento_para_entidade(m) for m in modelos]

    def soma_por_tipo(
        self,
        tipo: TipoLancamento,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> float:
        query = self._sessao.query(func.sum(LancamentoFinanceiroModel.valor)).filter(
            LancamentoFinanceiroModel.tipo == tipo.value
        )
        if inicio is not None:
            query = query.filter(LancamentoFinanceiroModel.data_competencia >= inicio)
        if fim is not None:
            query = query.filter(LancamentoFinanceiroModel.data_competencia <= fim)
        total = query.scalar()
        return float(total or 0.0)
