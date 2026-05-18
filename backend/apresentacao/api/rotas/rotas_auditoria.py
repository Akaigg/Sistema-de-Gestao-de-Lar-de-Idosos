"""Rota de auditoria (somente admin)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.dominio.entidades.funcionario import PapelFuncionario
from backend.apresentacao.dependencias import (
    obter_repo_auditoria,
    requer_papeis,
)
from backend.apresentacao.schemas.diversos import LogAuditoriaSaida

roteador = APIRouter(
    prefix="/api/auditoria",
    tags=["Auditoria"],
    dependencies=[Depends(requer_papeis(PapelFuncionario.ADMINISTRADOR))],
)


@roteador.get("", response_model=list[LogAuditoriaSaida])
def listar(
    funcionario_id: Optional[int] = Query(default=None),
    recurso: Optional[str] = Query(default=None),
    inicio: Optional[datetime] = Query(default=None),
    fim: Optional[datetime] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=50, ge=1, le=200),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    itens = repo_auditoria.listar(
        funcionario_id=funcionario_id,
        recurso=recurso,
        inicio=inicio,
        fim=fim,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )
    return [
        LogAuditoriaSaida(
            identificador=i.identificador,
            ocorrido_em=i.ocorrido_em,
            funcionario_id=i.funcionario_id,
            acao=i.acao,
            recurso=i.recurso,
            recurso_id=i.recurso_id,
            detalhes=i.detalhes,
            endereco_ip=i.endereco_ip,
        )
        for i in itens
    ]
