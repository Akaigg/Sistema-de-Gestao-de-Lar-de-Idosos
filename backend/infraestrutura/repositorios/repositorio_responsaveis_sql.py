"""Implementação SQLAlchemy de RepositorioResponsaveis."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.responsavel import Responsavel
from backend.dominio.repositorios.repositorio_responsaveis import RepositorioResponsaveis
from backend.infraestrutura.banco_de_dados.modelos import (
    ResponsavelModel,
    ResidenteResponsavelModel,
)
from backend.infraestrutura.repositorios._conversores import (
    responsavel_para_entidade,
    responsavel_para_modelo,
)


class RepositorioResponsaveisSQL(RepositorioResponsaveis):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, responsavel: Responsavel, residente_id: int) -> Responsavel:
        existente = (
            self._sessao.query(ResponsavelModel)
            .filter(ResponsavelModel.cpf == responsavel.cpf)
            .one_or_none()
        )
        if existente:
            modelo = existente
            responsavel_para_modelo(responsavel, modelo)
        else:
            modelo = responsavel_para_modelo(responsavel)
            self._sessao.add(modelo)
        self._sessao.flush()
        ja_vinculado = (
            self._sessao.query(ResidenteResponsavelModel)
            .filter(
                ResidenteResponsavelModel.responsavel_id == modelo.id,
                ResidenteResponsavelModel.residente_id == residente_id,
            )
            .one_or_none()
        )
        if not ja_vinculado:
            self._sessao.add(
                ResidenteResponsavelModel(
                    responsavel_id=modelo.id, residente_id=residente_id
                )
            )
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return responsavel_para_entidade(modelo)

    def atualizar(self, responsavel: Responsavel) -> Responsavel:
        if responsavel.identificador is None:
            raise ValueError("Responsável sem identificador.")
        modelo = self._sessao.get(ResponsavelModel, responsavel.identificador)
        if not modelo:
            raise ValueError("Responsável não encontrado.")
        responsavel_para_modelo(responsavel, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return responsavel_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Responsavel]:
        modelo = self._sessao.get(ResponsavelModel, identificador)
        return responsavel_para_entidade(modelo) if modelo else None

    def listar_por_residente(self, residente_id: int) -> list[Responsavel]:
        ids_responsaveis = [
            v.responsavel_id
            for v in self._sessao.query(ResidenteResponsavelModel)
            .filter(ResidenteResponsavelModel.residente_id == residente_id)
            .all()
        ]
        if not ids_responsaveis:
            return []
        modelos = (
            self._sessao.query(ResponsavelModel)
            .filter(ResponsavelModel.id.in_(ids_responsaveis))
            .all()
        )
        return [responsavel_para_entidade(m) for m in modelos]

    def excluir_vinculo(self, responsavel_id: int, residente_id: int) -> None:
        self._sessao.query(ResidenteResponsavelModel).filter(
            ResidenteResponsavelModel.responsavel_id == responsavel_id,
            ResidenteResponsavelModel.residente_id == residente_id,
        ).delete()
        self._sessao.commit()
