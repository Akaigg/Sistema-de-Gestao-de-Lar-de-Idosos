"""Implementação SQLAlchemy de RepositorioOcorrencias."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.ocorrencia import Ocorrencia
from backend.dominio.repositorios.repositorio_ocorrencias import RepositorioOcorrencias
from backend.infraestrutura.banco_de_dados.modelos import OcorrenciaModel
from backend.infraestrutura.repositorios._conversores import (
    ocorrencia_para_entidade,
    ocorrencia_para_modelo,
)


class RepositorioOcorrenciasSQL(RepositorioOcorrencias):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        m = ocorrencia_para_modelo(ocorrencia)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return ocorrencia_para_entidade(m)

    def atualizar(self, ocorrencia: Ocorrencia) -> Ocorrencia:
        m = self._sessao.get(OcorrenciaModel, ocorrencia.identificador)
        if not m:
            raise ValueError("Ocorrência não encontrada.")
        ocorrencia_para_modelo(ocorrencia, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return ocorrencia_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[Ocorrencia]:
        m = self._sessao.get(OcorrenciaModel, identificador)
        return ocorrencia_para_entidade(m) if m else None

    def listar(
        self,
        residente_id: Optional[int] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
    ) -> list[Ocorrencia]:
        query = self._sessao.query(OcorrenciaModel)
        if residente_id is not None:
            query = query.filter(OcorrenciaModel.residente_id == residente_id)
        if inicio is not None:
            query = query.filter(
                OcorrenciaModel.ocorreu_em >= datetime(inicio.year, inicio.month, inicio.day)
            )
        if fim is not None:
            limite = datetime(fim.year, fim.month, fim.day) + timedelta(days=1)
            query = query.filter(OcorrenciaModel.ocorreu_em < limite)
        modelos = query.order_by(OcorrenciaModel.ocorreu_em.desc()).all()
        return [ocorrencia_para_entidade(m) for m in modelos]
