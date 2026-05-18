"""Implementação SQLAlchemy de RepositorioVisitas."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.visita import Visita
from backend.dominio.repositorios.repositorio_visitas import RepositorioVisitas
from backend.infraestrutura.banco_de_dados.modelos import VisitaModel
from backend.infraestrutura.repositorios._conversores import (
    visita_para_entidade,
    visita_para_modelo,
)


class RepositorioVisitasSQL(RepositorioVisitas):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, visita: Visita) -> Visita:
        m = visita_para_modelo(visita)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return visita_para_entidade(m)

    def atualizar(self, visita: Visita) -> Visita:
        m = self._sessao.get(VisitaModel, visita.identificador)
        if not m:
            raise ValueError("Visita não encontrada.")
        visita_para_modelo(visita, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return visita_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[Visita]:
        m = self._sessao.get(VisitaModel, identificador)
        return visita_para_entidade(m) if m else None

    def listar(
        self,
        residente_id: Optional[int] = None,
        dia: Optional[date] = None,
    ) -> list[Visita]:
        query = self._sessao.query(VisitaModel)
        if residente_id is not None:
            query = query.filter(VisitaModel.residente_id == residente_id)
        if dia is not None:
            inicio = datetime(dia.year, dia.month, dia.day)
            fim = inicio + timedelta(days=1)
            query = query.filter(
                VisitaModel.entrada_em >= inicio, VisitaModel.entrada_em < fim
            )
        modelos = query.order_by(VisitaModel.entrada_em.desc()).all()
        return [visita_para_entidade(m) for m in modelos]
