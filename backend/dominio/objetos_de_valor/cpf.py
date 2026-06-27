"""Objeto de valor CPF — valida e normaliza CPF brasileiro."""

from __future__ import annotations

import re
from dataclasses import dataclass

from backend.dominio.excecoes import DadosInvalidos


@dataclass(frozen=True)
class CPF:
    """Representa um CPF válido (somente dígitos, 11 caracteres)."""

    numero: str

    def __post_init__(self) -> None:
        somente_digitos = re.sub(r"\D", "", self.numero)
        if not self._eh_valido(somente_digitos):
            raise DadosInvalidos(f"CPF inválido: {self.numero!r}")
        object.__setattr__(self, "numero", somente_digitos)

    @staticmethod
    def _eh_valido(cpf: str) -> bool:
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        for posicao_verificador in (9, 10):
            soma = sum(
                int(cpf[indice]) * (posicao_verificador + 1 - indice)
                for indice in range(posicao_verificador)
            )
            digito = (soma * 10) % 11 % 10
            if digito != int(cpf[posicao_verificador]):
                return False
        return True

    def formatado(self) -> str:
        return f"{self.numero[:3]}.{self.numero[3:6]}.{self.numero[6:9]}-{self.numero[9:]}"

    def __str__(self) -> str:
        return self.numero
