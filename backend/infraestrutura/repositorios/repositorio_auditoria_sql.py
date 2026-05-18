"""Implementação SQLAlchemy de RepositorioAuditoria."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.infraestrutura.banco_de_dados.modelos import LogAuditoriaModel
from backend.infraestrutura.repositorios._conversores import (
    auditoria_para_entidade,
    auditoria_para_modelo,
)


class RepositorioAuditoriaSQL(RepositorioAuditoria):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def registrar(self, log: LogAuditoria) -> LogAuditoria:
        m = auditoria_para_modelo(log)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return auditoria_para_entidade(m)

    def listar(
        self,
        funcionario_id: Optional[int] = None,
        recurso: Optional[str] = None,
        inicio: Optional[datetime] = None,
        fim: Optional[datetime] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[LogAuditoria]:
        query = self._sessao.query(LogAuditoriaModel)
        if funcionario_id is not None:
            query = query.filter(LogAuditoriaModel.funcionario_id == funcionario_id)
        if recurso:
            query = query.filter(LogAuditoriaModel.recurso == recurso)
        if inicio:
            query = query.filter(LogAuditoriaModel.ocorrido_em >= inicio)
        if fim:
            query = query.filter(LogAuditoriaModel.ocorrido_em <= fim)
        query = query.order_by(LogAuditoriaModel.ocorrido_em.desc())
        query = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina)
        return [auditoria_para_entidade(m) for m in query.all()]
