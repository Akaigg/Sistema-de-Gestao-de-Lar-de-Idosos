"""Casos de uso financeiros."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.financeiro import (
    FormaPagamento,
    LancamentoFinanceiro,
    Mensalidade,
    StatusPagamento,
    TipoLancamento,
)
from backend.dominio.excecoes import EntidadeNaoEncontrada, RegraDeNegocioViolada
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_financeiro import (
    RepositorioLancamentos,
    RepositorioMensalidades,
)


class CriarMensalidade:
    def __init__(
        self,
        repositorio: RepositorioMensalidades,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        residente_id: int,
        competencia_mes: int,
        competencia_ano: int,
        valor: float,
        data_vencimento: date,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Mensalidade:
        if valor <= 0:
            raise RegraDeNegocioViolada("O valor deve ser maior que zero.")
        mensalidade = Mensalidade(
            residente_id=residente_id,
            competencia_mes=competencia_mes,
            competencia_ano=competencia_ano,
            valor=valor,
            data_vencimento=data_vencimento,
        )
        criada = self._repo.criar(mensalidade)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="mensalidade",
                recurso_id=criada.identificador,
            )
        )
        return criada


class QuitarMensalidade:
    def __init__(
        self,
        repositorio: RepositorioMensalidades,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        mensalidade_id: int,
        valor_pago: float,
        forma: FormaPagamento,
        data_pagamento: Optional[date] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Mensalidade:
        mensalidade = self._repo.buscar_por_id(mensalidade_id)
        if not mensalidade:
            raise EntidadeNaoEncontrada("Mensalidade não encontrada.")
        mensalidade.quitar(valor_pago, forma, data_pagamento)
        atualizada = self._repo.atualizar(mensalidade)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="mensalidade",
                recurso_id=mensalidade_id,
                detalhes=f"Pagamento de R$ {valor_pago:.2f} por {forma.value}",
            )
        )
        return atualizada


class CriarLancamento:
    def __init__(
        self,
        repositorio: RepositorioLancamentos,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        tipo: TipoLancamento,
        descricao: str,
        valor: float,
        data_competencia: date,
        categoria: Optional[str] = None,
        centro_custo: Optional[str] = None,
        fornecedor: Optional[str] = None,
        forma_pagamento: Optional[FormaPagamento] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> LancamentoFinanceiro:
        if valor <= 0:
            raise RegraDeNegocioViolada("O valor deve ser maior que zero.")
        lancamento = LancamentoFinanceiro(
            tipo=tipo,
            descricao=descricao,
            valor=valor,
            data_competencia=data_competencia,
            categoria=categoria,
            centro_custo=centro_custo,
            fornecedor=fornecedor,
            forma_pagamento=forma_pagamento,
            registrado_em=datetime.utcnow(),
            registrado_por_id=funcionario_responsavel_id,
        )
        criado = self._repo.criar(lancamento)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="lancamento_financeiro",
                recurso_id=criado.identificador,
            )
        )
        return criado


class GerarFluxoDeCaixa:
    """Retorna totais de receitas e despesas no período + saldo."""

    def __init__(self, repositorio: RepositorioLancamentos) -> None:
        self._repo = repositorio

    def executar(self, inicio: date, fim: date) -> dict:
        receitas = self._repo.soma_por_tipo(TipoLancamento.RECEITA, inicio, fim)
        despesas = self._repo.soma_por_tipo(TipoLancamento.DESPESA, inicio, fim)
        return {
            "inicio": inicio,
            "fim": fim,
            "total_receitas": receitas,
            "total_despesas": despesas,
            "saldo": receitas - despesas,
        }
