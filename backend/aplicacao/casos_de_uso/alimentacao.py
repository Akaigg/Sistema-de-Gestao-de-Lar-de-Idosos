"""Casos de uso de alimentação."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.alimentacao import (
    Cardapio,
    Dieta,
    IngestaoHidrica,
    Refeicao,
    TipoDieta,
    TipoRefeicao,
)
from backend.dominio.repositorios.repositorio_alimentacao import (
    RepositorioCardapios,
    RepositorioDietas,
    RepositorioIngestaoHidrica,
    RepositorioRefeicoes,
)


class CadastrarCardapio:
    def __init__(self, repositorio: RepositorioCardapios) -> None:
        self._repo = repositorio

    def executar(
        self,
        data_referencia: date,
        tipo_refeicao: TipoRefeicao,
        descricao: str,
        calorias_aproximadas: Optional[int] = None,
        observacoes: Optional[str] = None,
    ) -> Cardapio:
        cardapio = Cardapio(
            data_referencia=data_referencia,
            tipo_refeicao=tipo_refeicao,
            descricao=descricao,
            calorias_aproximadas=calorias_aproximadas,
            observacoes=observacoes,
        )
        return self._repo.criar(cardapio)


class DefinirDietaIndividual:
    def __init__(self, repositorio: RepositorioDietas) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        tipo: TipoDieta,
        descricao_detalhada: Optional[str] = None,
        prescrita_por_id: Optional[int] = None,
        data_inicio: Optional[date] = None,
        data_termino: Optional[date] = None,
    ) -> Dieta:
        dieta = Dieta(
            residente_id=residente_id,
            tipo=tipo,
            descricao_detalhada=descricao_detalhada,
            prescrita_por_id=prescrita_por_id,
            data_inicio=data_inicio or date.today(),
            data_termino=data_termino,
        )
        return self._repo.criar(dieta)


class RegistrarRefeicaoServida:
    def __init__(self, repositorio: RepositorioRefeicoes) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        tipo_refeicao: TipoRefeicao,
        funcionario_id: int,
        cardapio_id: Optional[int] = None,
        aceitacao_percentual: int = 100,
        observacoes: Optional[str] = None,
        momento: Optional[datetime] = None,
    ) -> Refeicao:
        refeicao = Refeicao(
            residente_id=residente_id,
            cardapio_id=cardapio_id,
            tipo_refeicao=tipo_refeicao,
            servida_em=momento or datetime.utcnow(),
            funcionario_id=funcionario_id,
            aceitacao_percentual=max(0, min(100, aceitacao_percentual)),
            observacoes=observacoes,
        )
        return self._repo.criar(refeicao)


class RegistrarIngestaoHidrica:
    def __init__(self, repositorio: RepositorioIngestaoHidrica) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        quantidade_ml: int,
        funcionario_id: int,
        momento: Optional[datetime] = None,
    ) -> IngestaoHidrica:
        registro = IngestaoHidrica(
            residente_id=residente_id,
            registrada_em=momento or datetime.utcnow(),
            quantidade_ml=quantidade_ml,
            funcionario_id=funcionario_id,
        )
        return self._repo.criar(registro)
