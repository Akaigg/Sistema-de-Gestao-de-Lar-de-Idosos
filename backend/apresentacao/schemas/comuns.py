"""Schemas comuns."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ModeloBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class RespostaPaginada(ModeloBase, Generic[T]):
    itens: list[T]
    total: int
    pagina: int
    tamanho_pagina: int


class MensagemSimples(ModeloBase):
    mensagem: str
