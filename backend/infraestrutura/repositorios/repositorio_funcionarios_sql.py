"""Implementação SQLAlchemy de RepositorioFuncionarios."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.dominio.entidades.funcionario import Funcionario
from backend.dominio.repositorios.repositorio_funcionarios import RepositorioFuncionarios
from backend.infraestrutura.banco_de_dados.modelos import (
    FuncionarioModel,
    PapelFuncionarioModel,
    TentativaLoginModel,
)
from backend.infraestrutura.repositorios._conversores import (
    funcionario_para_entidade,
    funcionario_para_modelo,
)


class RepositorioFuncionariosSQL(RepositorioFuncionarios):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, funcionario: Funcionario) -> Funcionario:
        modelo = funcionario_para_modelo(funcionario)
        for papel in funcionario.papeis:
            modelo.papeis.append(PapelFuncionarioModel(papel=papel.value))
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return funcionario_para_entidade(modelo)

    def atualizar(self, funcionario: Funcionario) -> Funcionario:
        if funcionario.identificador is None:
            raise ValueError("Funcionário sem identificador para atualização.")
        modelo = self._sessao.get(FuncionarioModel, funcionario.identificador)
        if not modelo:
            raise ValueError("Funcionário não encontrado.")
        funcionario_para_modelo(funcionario, modelo)
        # Sincroniza papéis
        papeis_existentes = {p.papel for p in modelo.papeis}
        papeis_desejados = {p.value for p in funcionario.papeis}
        for p in list(modelo.papeis):
            if p.papel not in papeis_desejados:
                self._sessao.delete(p)
        for novo in papeis_desejados - papeis_existentes:
            modelo.papeis.append(PapelFuncionarioModel(papel=novo))
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return funcionario_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Funcionario]:
        modelo = self._sessao.get(FuncionarioModel, identificador)
        return funcionario_para_entidade(modelo) if modelo else None

    def buscar_por_email(self, email: str) -> Optional[Funcionario]:
        modelo = (
            self._sessao.query(FuncionarioModel)
            .filter(FuncionarioModel.email == email.lower())
            .one_or_none()
        )
        return funcionario_para_entidade(modelo) if modelo else None

    def buscar_por_cpf(self, cpf: str) -> Optional[Funcionario]:
        modelo = (
            self._sessao.query(FuncionarioModel)
            .filter(FuncionarioModel.cpf == cpf)
            .one_or_none()
        )
        return funcionario_para_entidade(modelo) if modelo else None

    def listar(
        self,
        termo_busca: Optional[str] = None,
        apenas_ativos: bool = True,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> list[Funcionario]:
        query = self._sessao.query(FuncionarioModel)
        if apenas_ativos:
            query = query.filter(FuncionarioModel.ativo.is_(True))
        if termo_busca:
            curinga = f"%{termo_busca.lower()}%"
            query = query.filter(
                or_(
                    FuncionarioModel.nome_completo.ilike(curinga),
                    FuncionarioModel.email.ilike(curinga),
                    FuncionarioModel.cpf.ilike(curinga),
                )
            )
        query = query.order_by(FuncionarioModel.nome_completo)
        query = query.offset((pagina - 1) * tamanho_pagina).limit(tamanho_pagina)
        return [funcionario_para_entidade(m) for m in query.all()]

    def contar(self, termo_busca: Optional[str] = None, apenas_ativos: bool = True) -> int:
        query = self._sessao.query(FuncionarioModel)
        if apenas_ativos:
            query = query.filter(FuncionarioModel.ativo.is_(True))
        if termo_busca:
            curinga = f"%{termo_busca.lower()}%"
            query = query.filter(
                or_(
                    FuncionarioModel.nome_completo.ilike(curinga),
                    FuncionarioModel.email.ilike(curinga),
                    FuncionarioModel.cpf.ilike(curinga),
                )
            )
        return query.count()

    def registrar_tentativa_login(
        self, email: str, sucesso: bool, endereco_ip: Optional[str] = None
    ) -> None:
        tentativa = TentativaLoginModel(
            email=email.lower(),
            sucesso=sucesso,
            endereco_ip=endereco_ip,
            ocorreu_em=datetime.utcnow(),
        )
        self._sessao.add(tentativa)
        self._sessao.commit()

    def contar_tentativas_recentes(self, email: str, minutos: int = 15) -> int:
        limite = datetime.utcnow() - timedelta(minutes=minutos)
        return (
            self._sessao.query(TentativaLoginModel)
            .filter(
                TentativaLoginModel.email == email.lower(),
                TentativaLoginModel.sucesso.is_(False),
                TentativaLoginModel.ocorreu_em >= limite,
            )
            .count()
        )
