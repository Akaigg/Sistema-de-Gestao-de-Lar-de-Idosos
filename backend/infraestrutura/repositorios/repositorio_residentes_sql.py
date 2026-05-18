"""Implementação SQLAlchemy de RepositorioResidentes."""

from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import extract, or_
from sqlalchemy.orm import Session

from backend.dominio.entidades.residente import Residente, StatusResidente
from backend.dominio.repositorios.repositorio_residentes import RepositorioResidentes
from backend.infraestrutura.banco_de_dados.modelos import ResidenteModel
from backend.infraestrutura.repositorios._conversores import (
    residente_para_entidade,
    residente_para_modelo,
)


class RepositorioResidentesSQL(RepositorioResidentes):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, residente: Residente) -> Residente:
        modelo = residente_para_modelo(residente)
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return residente_para_entidade(modelo)

    def atualizar(self, residente: Residente) -> Residente:
        if residente.identificador is None:
            raise ValueError("Residente sem identificador.")
        modelo = self._sessao.get(ResidenteModel, residente.identificador)
        if not modelo:
            raise ValueError("Residente não encontrado.")
        residente_para_modelo(residente, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return residente_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Residente]:
        modelo = self._sessao.get(ResidenteModel, identificador)
        return residente_para_entidade(modelo) if modelo else None

    def buscar_por_cpf(self, cpf: str) -> Optional[Residente]:
        modelo = (
            self._sessao.query(ResidenteModel)
            .filter(ResidenteModel.cpf == cpf)
            .one_or_none()
        )
        return residente_para_entidade(modelo) if modelo else None

    def listar(
        self,
        termo_busca: Optional[str] = None,
        status: Optional[StatusResidente] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[Residente]:
        query = self._sessao.query(ResidenteModel)
        if status is not None:
            query = query.filter(ResidenteModel.status == status.value)
        if termo_busca:
            curinga = f"%{termo_busca.lower()}%"
            query = query.filter(
                or_(
                    ResidenteModel.nome_completo.ilike(curinga),
                    ResidenteModel.cpf.ilike(curinga),
                )
            )
        query = query.order_by(ResidenteModel.nome_completo)
        query = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina)
        return [residente_para_entidade(m) for m in query.all()]

    def contar(
        self,
        termo_busca: Optional[str] = None,
        status: Optional[StatusResidente] = None,
    ) -> int:
        query = self._sessao.query(ResidenteModel)
        if status is not None:
            query = query.filter(ResidenteModel.status == status.value)
        if termo_busca:
            curinga = f"%{termo_busca.lower()}%"
            query = query.filter(
                or_(
                    ResidenteModel.nome_completo.ilike(curinga),
                    ResidenteModel.cpf.ilike(curinga),
                )
            )
        return query.count()

    def listar_aniversariantes_do_mes(self, mes: int) -> list[Residente]:
        modelos = (
            self._sessao.query(ResidenteModel)
            .filter(extract("month", ResidenteModel.data_nascimento) == mes)
            .filter(ResidenteModel.status == StatusResidente.ATIVO.value)
            .order_by(extract("day", ResidenteModel.data_nascimento))
            .all()
        )
        return [residente_para_entidade(m) for m in modelos]

    def contar_ativos(self) -> int:
        return (
            self._sessao.query(ResidenteModel)
            .filter(ResidenteModel.status == StatusResidente.ATIVO.value)
            .count()
        )
