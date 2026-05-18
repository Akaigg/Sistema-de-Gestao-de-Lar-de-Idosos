"""Implementação SQLAlchemy de RepositorioQuartos."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.quarto import Quarto, Leito, StatusLeito
from backend.dominio.repositorios.repositorio_quartos import RepositorioQuartos
from backend.infraestrutura.banco_de_dados.modelos import QuartoModel, LeitoModel
from backend.infraestrutura.repositorios._conversores import (
    quarto_para_entidade,
    quarto_para_modelo,
    leito_para_entidade,
)


class RepositorioQuartosSQL(RepositorioQuartos):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, quarto: Quarto) -> Quarto:
        modelo = quarto_para_modelo(quarto)
        for leito in quarto.leitos:
            modelo.leitos.append(
                LeitoModel(
                    numero=leito.numero,
                    status=leito.status.value,
                    residente_id=leito.residente_id,
                    observacoes=leito.observacoes,
                )
            )
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return quarto_para_entidade(modelo)

    def atualizar(self, quarto: Quarto) -> Quarto:
        modelo = self._sessao.get(QuartoModel, quarto.identificador)
        if not modelo:
            raise ValueError("Quarto não encontrado.")
        quarto_para_modelo(quarto, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return quarto_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Quarto]:
        modelo = self._sessao.get(QuartoModel, identificador)
        return quarto_para_entidade(modelo) if modelo else None

    def listar(self) -> list[Quarto]:
        modelos = self._sessao.query(QuartoModel).order_by(QuartoModel.numero).all()
        return [quarto_para_entidade(m) for m in modelos]

    def buscar_leito(self, leito_id: int) -> Optional[Leito]:
        modelo = self._sessao.get(LeitoModel, leito_id)
        return leito_para_entidade(modelo) if modelo else None

    def atualizar_leito(self, leito: Leito) -> Leito:
        modelo = self._sessao.get(LeitoModel, leito.identificador)
        if not modelo:
            raise ValueError("Leito não encontrado.")
        modelo.numero = leito.numero
        modelo.status = leito.status.value
        modelo.residente_id = leito.residente_id
        modelo.observacoes = leito.observacoes
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return leito_para_entidade(modelo)

    def listar_leitos_do_quarto(self, quarto_id: int) -> list[Leito]:
        modelos = (
            self._sessao.query(LeitoModel)
            .filter(LeitoModel.quarto_id == quarto_id)
            .order_by(LeitoModel.numero)
            .all()
        )
        return [leito_para_entidade(m) for m in modelos]

    def buscar_leito_por_residente(self, residente_id: int) -> Optional[Leito]:
        modelo = (
            self._sessao.query(LeitoModel)
            .filter(LeitoModel.residente_id == residente_id)
            .one_or_none()
        )
        return leito_para_entidade(modelo) if modelo else None

    def contar_leitos_ocupados(self) -> int:
        return (
            self._sessao.query(LeitoModel)
            .filter(LeitoModel.status == StatusLeito.OCUPADO.value)
            .count()
        )

    def contar_leitos_totais(self) -> int:
        return self._sessao.query(LeitoModel).count()
