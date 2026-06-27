"""Implementação SQLAlchemy de RepositorioEscalas."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.escala import Escala, Turno
from backend.dominio.repositorios.repositorio_escalas import RepositorioEscalas
from backend.infraestrutura.banco_de_dados.modelos import EscalaModel, TurnoModel
from backend.infraestrutura.repositorios._conversores import (
    escala_para_entidade,
    escala_para_modelo,
    turno_para_entidade,
    turno_para_modelo,
)


class RepositorioEscalasSQL(RepositorioEscalas):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, escala: Escala) -> Escala:
        m = escala_para_modelo(escala)
        self._sessao.add(m)
        for turno in escala.turnos:
            tm = turno_para_modelo(turno)
            m.turnos.append(tm)
        self._sessao.commit()
        self._sessao.refresh(m)
        return escala_para_entidade(m)

    def atualizar(self, escala: Escala) -> Escala:
        m = self._sessao.get(EscalaModel, escala.identificador)
        if not m:
            raise ValueError("Escala não encontrada.")
        escala_para_modelo(escala, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return escala_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[Escala]:
        m = self._sessao.get(EscalaModel, identificador)
        return escala_para_entidade(m) if m else None

    def buscar_por_mes(self, mes: int, ano: int, setor: Optional[str] = None) -> list[Escala]:
        query = self._sessao.query(EscalaModel).filter(
            EscalaModel.referencia_mes == mes,
            EscalaModel.referencia_ano == ano,
        )
        if setor:
            query = query.filter(EscalaModel.setor == setor)
        return [escala_para_entidade(m) for m in query.all()]

    def adicionar_turno(self, escala_id: int, turno: Turno) -> Turno:
        m = self._sessao.get(EscalaModel, escala_id)
        if not m:
            raise ValueError("Escala não encontrada.")
        tm = turno_para_modelo(turno)
        m.turnos.append(tm)
        self._sessao.commit()
        self._sessao.refresh(tm)
        return turno_para_entidade(tm)

    def excluir_turno(self, turno_id: int) -> None:
        m = self._sessao.get(TurnoModel, turno_id)
        if m:
            self._sessao.delete(m)
            self._sessao.commit()

    def listar_turnos_do_dia(self, dia: date) -> list[Turno]:
        inicio = datetime(dia.year, dia.month, dia.day)
        fim = inicio + timedelta(days=1)
        modelos = (
            self._sessao.query(TurnoModel)
            .filter(TurnoModel.inicio < fim, TurnoModel.fim > inicio)
            .order_by(TurnoModel.inicio)
            .all()
        )
        return [turno_para_entidade(m) for m in modelos]

    def listar_turnos_funcionario(
        self, funcionario_id: int, inicio: date, fim: date
    ) -> list[Turno]:
        dt_inicio = datetime(inicio.year, inicio.month, inicio.day)
        dt_fim = datetime(fim.year, fim.month, fim.day) + timedelta(days=1)
        modelos = (
            self._sessao.query(TurnoModel)
            .filter(
                TurnoModel.funcionario_id == funcionario_id,
                TurnoModel.inicio < dt_fim,
                TurnoModel.fim > dt_inicio,
            )
            .order_by(TurnoModel.inicio)
            .all()
        )
        return [turno_para_entidade(m) for m in modelos]
