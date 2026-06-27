"""Implementação de ServicoToken usando python-jose (JWT HS256)."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from backend.dominio.servicos.servico_token import DadosToken, ServicoToken
from backend.infraestrutura.configuracao import configuracoes


class ServicoTokenJWT(ServicoToken):
    """Emissão e verificação de tokens JWT HS256."""

    def __init__(
        self,
        chave_secreta: Optional[str] = None,
        algoritmo: Optional[str] = None,
    ) -> None:
        self._chave_secreta = chave_secreta or configuracoes.chave_secreta_jwt
        self._algoritmo = algoritmo or configuracoes.algoritmo_jwt

    def gerar_token_acesso(self, dados: DadosToken) -> str:
        agora = datetime.utcnow()
        carga = {
            "sub": str(dados.funcionario_id),
            "email": dados.email,
            "papeis": dados.papeis,
            "tipo": "acesso",
            "iat": int(agora.timestamp()),
            "exp": int(
                (agora + timedelta(minutes=configuracoes.minutos_expiracao_token)).timestamp()
            ),
            "jti": secrets.token_hex(16),
        }
        return jwt.encode(carga, self._chave_secreta, algorithm=self._algoritmo)

    def gerar_token_refresh(self, funcionario_id: int) -> str:
        agora = datetime.utcnow()
        carga = {
            "sub": str(funcionario_id),
            "tipo": "refresh",
            "iat": int(agora.timestamp()),
            "exp": int(
                (agora + timedelta(days=configuracoes.dias_expiracao_refresh)).timestamp()
            ),
            "jti": secrets.token_hex(16),
        }
        return jwt.encode(carga, self._chave_secreta, algorithm=self._algoritmo)

    def decodificar(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, self._chave_secreta, algorithms=[self._algoritmo])
        except JWTError:
            return None
