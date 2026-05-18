"""Objetos de valor (Value Objects) do domínio."""

from backend.dominio.objetos_de_valor.cpf import CPF
from backend.dominio.objetos_de_valor.email import Email
from backend.dominio.objetos_de_valor.endereco import Endereco
from backend.dominio.objetos_de_valor.telefone import Telefone
from backend.dominio.objetos_de_valor.periodo import Periodo

__all__ = ["CPF", "Email", "Endereco", "Telefone", "Periodo"]
