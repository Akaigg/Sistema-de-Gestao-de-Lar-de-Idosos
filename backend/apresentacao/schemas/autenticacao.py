"""Schemas para autenticação e funcionários."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import EmailStr, Field

from backend.apresentacao.schemas.comuns import ModeloBase


class EntradaLogin(ModeloBase):
    email: EmailStr
    senha: str = Field(min_length=1, max_length=200)


class SaidaLogin(ModeloBase):
    token_acesso: str
    token_refresh: str
    tipo_token: str = "Bearer"
    deve_trocar_senha: bool
    funcionario: "FuncionarioResumido"


class FuncionarioResumido(ModeloBase):
    identificador: Optional[int] = None
    nome_completo: str
    email: str
    cargo: str
    papeis: list[str]


class EntradaTrocaSenha(ModeloBase):
    senha_atual: str = Field(min_length=1, max_length=200)
    senha_nova: str = Field(min_length=8, max_length=200)


class EntradaCadastroFuncionario(ModeloBase):
    nome_completo: str = Field(min_length=3, max_length=200)
    email: EmailStr
    cpf: str
    cargo: str
    papeis: list[str]
    senha_inicial: str = Field(min_length=8, max_length=200)
    telefone: Optional[str] = None
    data_admissao: Optional[date] = None


class EntradaAtualizacaoFuncionario(ModeloBase):
    nome_completo: Optional[str] = None
    cargo: Optional[str] = None
    telefone: Optional[str] = None
    papeis: Optional[list[str]] = None
    ativo: Optional[bool] = None


class FuncionarioDetalhado(ModeloBase):
    identificador: int
    nome_completo: str
    email: str
    cpf: str
    cargo: str
    papeis: list[str]
    telefone: Optional[str] = None
    data_admissao: Optional[date] = None
    data_desligamento: Optional[date] = None
    ativo: bool
    ultimo_acesso: Optional[datetime] = None


SaidaLogin.model_rebuild()
