"""Implementação de ServicoSenha usando bcrypt diretamente."""

from __future__ import annotations

import re

import bcrypt

from backend.dominio.excecoes import DadosInvalidos
from backend.dominio.servicos.servico_senha import ServicoSenha


class ServicoSenhaBcrypt(ServicoSenha):
    """Hash e verificação de senha com bcrypt (custo 12).

    Bcrypt limita a 72 bytes; este wrapper trunca silenciosamente o restante,
    que é o comportamento padrão do bcrypt e suficiente para senhas humanas.
    """

    CUSTO = 12

    @staticmethod
    def _para_bytes(senha: str) -> bytes:
        return senha.encode("utf-8")[:72]

    def gerar_hash(self, senha_em_texto: str) -> str:
        salt = bcrypt.gensalt(rounds=self.CUSTO)
        return bcrypt.hashpw(self._para_bytes(senha_em_texto), salt).decode("utf-8")

    def verificar(self, senha_em_texto: str, hash_armazenado: str) -> bool:
        try:
            return bcrypt.checkpw(
                self._para_bytes(senha_em_texto),
                hash_armazenado.encode("utf-8"),
            )
        except (ValueError, TypeError):
            return False

    def validar_politica(self, senha_em_texto: str) -> None:
        """Política: mínimo 8 caracteres com maiúscula, minúscula, número e símbolo."""
        if len(senha_em_texto) < 8:
            raise DadosInvalidos("A senha deve ter no mínimo 8 caracteres.")
        if not re.search(r"[A-Z]", senha_em_texto):
            raise DadosInvalidos("A senha deve conter ao menos uma letra maiúscula.")
        if not re.search(r"[a-z]", senha_em_texto):
            raise DadosInvalidos("A senha deve conter ao menos uma letra minúscula.")
        if not re.search(r"\d", senha_em_texto):
            raise DadosInvalidos("A senha deve conter ao menos um número.")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", senha_em_texto):
            raise DadosInvalidos("A senha deve conter ao menos um caractere especial.")
