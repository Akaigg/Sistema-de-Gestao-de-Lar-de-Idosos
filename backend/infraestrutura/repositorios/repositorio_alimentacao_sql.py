"""Implementação SQLAlchemy dos repositórios de alimentação."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.dominio.entidades.alimentacao import (
    Cardapio,
    Dieta,
    Refeicao,
    IngestaoHidrica,
)
from backend.dominio.repositorios.repositorio_alimentacao import (
    RepositorioCardapios,
    RepositorioDietas,
    RepositorioRefeicoes,
    RepositorioIngestaoHidrica,
)
from backend.infraestrutura.banco_de_dados.modelos import (
    CardapioModel,
    DietaModel,
    RefeicaoModel,
    IngestaoHidricaModel,
)
from backend.infraestrutura.repositorios._conversores import (
    cardapio_para_entidade,
    cardapio_para_modelo,
    dieta_para_entidade,
    dieta_para_modelo,
    refeicao_para_entidade,
    refeicao_para_modelo,
    ingestao_para_entidade,
    ingestao_para_modelo,
)


class RepositorioCardapiosSQL(RepositorioCardapios):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, cardapio: Cardapio) -> Cardapio:
        m = cardapio_para_modelo(cardapio)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return cardapio_para_entidade(m)

    def listar_por_data(self, dia: date) -> list[Cardapio]:
        modelos = (
            self._sessao.query(CardapioModel)
            .filter(CardapioModel.data_referencia == dia)
            .order_by(CardapioModel.tipo_refeicao)
            .all()
        )
        return [cardapio_para_entidade(m) for m in modelos]

    def listar_por_periodo(self, inicio: date, fim: date) -> list[Cardapio]:
        modelos = (
            self._sessao.query(CardapioModel)
            .filter(
                CardapioModel.data_referencia >= inicio,
                CardapioModel.data_referencia <= fim,
            )
            .order_by(CardapioModel.data_referencia, CardapioModel.tipo_refeicao)
            .all()
        )
        return [cardapio_para_entidade(m) for m in modelos]

    def excluir(self, identificador: int) -> None:
        m = self._sessao.get(CardapioModel, identificador)
        if m:
            self._sessao.delete(m)
            self._sessao.commit()


class RepositorioDietasSQL(RepositorioDietas):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, dieta: Dieta) -> Dieta:
        m = dieta_para_modelo(dieta)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return dieta_para_entidade(m)

    def atualizar(self, dieta: Dieta) -> Dieta:
        m = self._sessao.get(DietaModel, dieta.identificador)
        if not m:
            raise ValueError("Dieta não encontrada.")
        dieta_para_modelo(dieta, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return dieta_para_entidade(m)

    def listar_por_residente(
        self, residente_id: int, apenas_ativas: bool = True
    ) -> list[Dieta]:
        query = self._sessao.query(DietaModel).filter(
            DietaModel.residente_id == residente_id
        )
        if apenas_ativas:
            query = query.filter(DietaModel.ativa.is_(True))
        modelos = query.order_by(DietaModel.data_inicio.desc()).all()
        return [dieta_para_entidade(m) for m in modelos]


class RepositorioRefeicoesSQL(RepositorioRefeicoes):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, refeicao: Refeicao) -> Refeicao:
        m = refeicao_para_modelo(refeicao)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return refeicao_para_entidade(m)

    def listar_por_residente(
        self,
        residente_id: int,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
    ) -> list[Refeicao]:
        query = self._sessao.query(RefeicaoModel).filter(
            RefeicaoModel.residente_id == residente_id
        )
        if inicio:
            query = query.filter(RefeicaoModel.servida_em >= inicio)
        if fim:
            query = query.filter(RefeicaoModel.servida_em <= fim)
        modelos = query.order_by(RefeicaoModel.servida_em.desc()).all()
        return [refeicao_para_entidade(m) for m in modelos]


class RepositorioIngestaoHidricaSQL(RepositorioIngestaoHidrica):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, registro: IngestaoHidrica) -> IngestaoHidrica:
        m = ingestao_para_modelo(registro)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return ingestao_para_entidade(m)

    def total_do_dia(self, residente_id: int, dia: date) -> int:
        inicio = datetime(dia.year, dia.month, dia.day)
        fim = inicio + timedelta(days=1)
        total = (
            self._sessao.query(func.sum(IngestaoHidricaModel.quantidade_ml))
            .filter(
                IngestaoHidricaModel.residente_id == residente_id,
                IngestaoHidricaModel.registrada_em >= inicio,
                IngestaoHidricaModel.registrada_em < fim,
            )
            .scalar()
        )
        return int(total or 0)

    def listar_do_dia(self, residente_id: int, dia: date) -> list[IngestaoHidrica]:
        inicio = datetime(dia.year, dia.month, dia.day)
        fim = inicio + timedelta(days=1)
        modelos = (
            self._sessao.query(IngestaoHidricaModel)
            .filter(
                IngestaoHidricaModel.residente_id == residente_id,
                IngestaoHidricaModel.registrada_em >= inicio,
                IngestaoHidricaModel.registrada_em < fim,
            )
            .order_by(IngestaoHidricaModel.registrada_em)
            .all()
        )
        return [ingestao_para_entidade(m) for m in modelos]
