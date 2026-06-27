"""Entidade Funcionario — usuário do sistema."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class PapelFuncionario(str, Enum):
    """Papéis (roles) atribuíveis a um funcionário."""

    ADMINISTRADOR = "administrador"
    MEDICO = "medico"
    ENFERMEIRO = "enfermeiro"
    CUIDADOR = "cuidador"
    NUTRICIONISTA = "nutricionista"
    FINANCEIRO = "financeiro"
    RECEPCAO = "recepcao"


@dataclass
class Funcionario:
    """Funcionário (usuário do sistema)."""

    nome_completo: str
    email: str
    senha_hash: str
    cpf: str
    cargo: str
    papeis: list[PapelFuncionario] = field(default_factory=list)
    telefone: Optional[str] = None
    data_admissao: Optional[date] = None
    data_desligamento: Optional[date] = None
    ativo: bool = True
    deve_trocar_senha: bool = True
    ultimo_acesso: Optional[datetime] = None
    identificador: Optional[int] = None

    def possui_papel(self, papel: PapelFuncionario) -> bool:
        return papel in self.papeis

    def possui_algum_papel(self, papeis: list[PapelFuncionario]) -> bool:
        return any(p in self.papeis for p in papeis)

    def desligar(self, data_desligamento: Optional[date] = None) -> None:
        """Desliga o funcionário; mantém histórico mas impede login."""
        self.ativo = False
        self.data_desligamento = data_desligamento or date.today()

    def registrar_acesso(self, momento: Optional[datetime] = None) -> None:
        self.ultimo_acesso = momento or datetime.utcnow()
