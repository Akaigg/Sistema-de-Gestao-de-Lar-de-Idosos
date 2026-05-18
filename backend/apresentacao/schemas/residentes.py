"""Schemas para residentes."""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import Field

from backend.apresentacao.schemas.comuns import ModeloBase


class EntradaCadastroResidente(ModeloBase):
    nome_completo: str = Field(min_length=3, max_length=200)
    data_nascimento: date
    cpf: str
    sexo: str = Field(pattern="^[MFO]$")
    data_entrada: date
    grau_dependencia: str = "independente"
    rg: Optional[str] = None
    cartao_sus: Optional[str] = None
    convenio: Optional[str] = None
    numero_convenio: Optional[str] = None
    religiao: Optional[str] = None
    estado_civil: Optional[str] = None
    naturalidade: Optional[str] = None
    profissao_anterior: Optional[str] = None
    observacoes: Optional[str] = None
    consentimento_imagem: bool = False


class EntradaAtualizacaoResidente(ModeloBase):
    nome_completo: Optional[str] = None
    sexo: Optional[str] = None
    grau_dependencia: Optional[str] = None
    rg: Optional[str] = None
    cartao_sus: Optional[str] = None
    convenio: Optional[str] = None
    numero_convenio: Optional[str] = None
    religiao: Optional[str] = None
    estado_civil: Optional[str] = None
    naturalidade: Optional[str] = None
    profissao_anterior: Optional[str] = None
    observacoes: Optional[str] = None
    consentimento_imagem: Optional[bool] = None


class EntradaSaidaResidente(ModeloBase):
    motivo: str
    falecimento: bool = False
    data_saida: Optional[date] = None


class ResidenteSaida(ModeloBase):
    identificador: int
    nome_completo: str
    data_nascimento: date
    idade: int
    cpf: str
    sexo: str
    data_entrada: date
    grau_dependencia: str
    status: str
    rg: Optional[str] = None
    cartao_sus: Optional[str] = None
    convenio: Optional[str] = None
    numero_convenio: Optional[str] = None
    religiao: Optional[str] = None
    estado_civil: Optional[str] = None
    naturalidade: Optional[str] = None
    profissao_anterior: Optional[str] = None
    observacoes: Optional[str] = None
    consentimento_imagem: bool
    data_saida: Optional[date] = None
    motivo_saida: Optional[str] = None
    foto_caminho: Optional[str] = None


class EntradaCadastroResponsavel(ModeloBase):
    nome_completo: str
    cpf: str
    parentesco: str
    telefone: str
    email: Optional[str] = None
    endereco_resumido: Optional[str] = None
    eh_responsavel_legal: bool = False
    eh_contato_emergencia: bool = True
    observacoes: Optional[str] = None


class ResponsavelSaida(ModeloBase):
    identificador: int
    nome_completo: str
    cpf: str
    parentesco: str
    telefone: str
    email: Optional[str] = None
    eh_responsavel_legal: bool
    eh_contato_emergencia: bool
