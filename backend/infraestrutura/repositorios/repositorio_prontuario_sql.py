"""Implementação SQLAlchemy dos repositórios de prontuário."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.prontuario import (
    SinaisVitais,
    Evolucao,
    Alergia,
    CondicaoCronica,
    Consulta,
    StatusConsulta,
)
from backend.dominio.repositorios.repositorio_prontuario import (
    RepositorioSinaisVitais,
    RepositorioEvolucoes,
    RepositorioAlergias,
    RepositorioCondicoesCronicas,
    RepositorioConsultas,
)
from backend.infraestrutura.banco_de_dados.modelos import (
    SinaisVitaisModel,
    EvolucaoModel,
    AlergiaModel,
    CondicaoCronicaModel,
    ConsultaModel,
)
from backend.infraestrutura.repositorios._conversores import (
    sinais_para_entidade,
    sinais_para_modelo,
    evolucao_para_entidade,
    evolucao_para_modelo,
    alergia_para_entidade,
    alergia_para_modelo,
    condicao_para_entidade,
    condicao_para_modelo,
    consulta_para_entidade,
    consulta_para_modelo,
)


class RepositorioSinaisVitaisSQL(RepositorioSinaisVitais):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, sinais: SinaisVitais) -> SinaisVitais:
        m = sinais_para_modelo(sinais)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return sinais_para_entidade(m)

    def listar_por_residente(
        self,
        residente_id: int,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
    ) -> list[SinaisVitais]:
        query = self._sessao.query(SinaisVitaisModel).filter(
            SinaisVitaisModel.residente_id == residente_id
        )
        if inicio:
            query = query.filter(SinaisVitaisModel.aferido_em >= inicio)
        if fim:
            query = query.filter(SinaisVitaisModel.aferido_em <= fim)
        modelos = query.order_by(SinaisVitaisModel.aferido_em.desc()).all()
        return [sinais_para_entidade(m) for m in modelos]


class RepositorioEvolucoesSQL(RepositorioEvolucoes):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, evolucao: Evolucao) -> Evolucao:
        m = evolucao_para_modelo(evolucao)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return evolucao_para_entidade(m)

    def listar_por_residente(self, residente_id: int) -> list[Evolucao]:
        modelos = (
            self._sessao.query(EvolucaoModel)
            .filter(EvolucaoModel.residente_id == residente_id)
            .order_by(EvolucaoModel.registrada_em.desc())
            .all()
        )
        return [evolucao_para_entidade(m) for m in modelos]


class RepositorioAlergiasSQL(RepositorioAlergias):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, alergia: Alergia) -> Alergia:
        m = alergia_para_modelo(alergia)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return alergia_para_entidade(m)

    def excluir(self, identificador: int) -> None:
        m = self._sessao.get(AlergiaModel, identificador)
        if m:
            self._sessao.delete(m)
            self._sessao.commit()

    def listar_por_residente(self, residente_id: int) -> list[Alergia]:
        modelos = (
            self._sessao.query(AlergiaModel)
            .filter(AlergiaModel.residente_id == residente_id)
            .order_by(AlergiaModel.substancia)
            .all()
        )
        return [alergia_para_entidade(m) for m in modelos]


class RepositorioCondicoesCronicasSQL(RepositorioCondicoesCronicas):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, condicao: CondicaoCronica) -> CondicaoCronica:
        m = condicao_para_modelo(condicao)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return condicao_para_entidade(m)

    def excluir(self, identificador: int) -> None:
        m = self._sessao.get(CondicaoCronicaModel, identificador)
        if m:
            self._sessao.delete(m)
            self._sessao.commit()

    def listar_por_residente(self, residente_id: int) -> list[CondicaoCronica]:
        modelos = (
            self._sessao.query(CondicaoCronicaModel)
            .filter(CondicaoCronicaModel.residente_id == residente_id)
            .order_by(CondicaoCronicaModel.descricao)
            .all()
        )
        return [condicao_para_entidade(m) for m in modelos]


class RepositorioConsultasSQL(RepositorioConsultas):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, consulta: Consulta) -> Consulta:
        m = consulta_para_modelo(consulta)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return consulta_para_entidade(m)

    def atualizar(self, consulta: Consulta) -> Consulta:
        m = self._sessao.get(ConsultaModel, consulta.identificador)
        if not m:
            raise ValueError("Consulta não encontrada.")
        consulta_para_modelo(consulta, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return consulta_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[Consulta]:
        m = self._sessao.get(ConsultaModel, identificador)
        return consulta_para_entidade(m) if m else None

    def listar_por_periodo(
        self,
        inicio: datetime,
        fim: datetime,
        residente_id: Optional[int] = None,
        status: Optional[StatusConsulta] = None,
    ) -> list[Consulta]:
        query = self._sessao.query(ConsultaModel).filter(
            ConsultaModel.data_hora >= inicio,
            ConsultaModel.data_hora <= fim,
        )
        if residente_id is not None:
            query = query.filter(ConsultaModel.residente_id == residente_id)
        if status is not None:
            query = query.filter(ConsultaModel.status == status.value)
        modelos = query.order_by(ConsultaModel.data_hora).all()
        return [consulta_para_entidade(m) for m in modelos]

    def contar_do_dia(self, dia: date) -> int:
        inicio = datetime(dia.year, dia.month, dia.day)
        fim = inicio + timedelta(days=1)
        return (
            self._sessao.query(ConsultaModel)
            .filter(
                ConsultaModel.data_hora >= inicio,
                ConsultaModel.data_hora < fim,
                ConsultaModel.status.in_(["agendada", "confirmada"]),
            )
            .count()
        )
