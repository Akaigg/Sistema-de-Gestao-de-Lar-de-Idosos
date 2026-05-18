"""Casos de uso de autenticação: login, troca de senha, logout."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.funcionario import Funcionario
from backend.dominio.excecoes import (
    ContaBloqueada,
    CredenciaisInvalidas,
    DadosInvalidos,
)
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_funcionarios import RepositorioFuncionarios
from backend.dominio.servicos.servico_senha import ServicoSenha
from backend.dominio.servicos.servico_token import DadosToken, ServicoToken


@dataclass
class ResultadoLogin:
    token_acesso: str
    token_refresh: str
    funcionario: Funcionario
    deve_trocar_senha: bool


class AutenticarFuncionario:
    """Caso de uso: autentica funcionário por e-mail e senha."""

    LIMITE_TENTATIVAS = 5
    JANELA_MINUTOS = 15

    def __init__(
        self,
        repositorio_funcionarios: RepositorioFuncionarios,
        servico_senha: ServicoSenha,
        servico_token: ServicoToken,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_funcionarios
        self._senha = servico_senha
        self._token = servico_token
        self._auditoria = repositorio_auditoria

    def executar(
        self, email: str, senha: str, endereco_ip: Optional[str] = None,
        agente_usuario: Optional[str] = None,
    ) -> ResultadoLogin:
        email_normalizado = email.strip().lower()

        tentativas = self._repo.contar_tentativas_recentes(
            email_normalizado, minutos=self.JANELA_MINUTOS
        )
        if tentativas >= self.LIMITE_TENTATIVAS:
            self._auditoria.registrar(
                LogAuditoria(
                    ocorrido_em=datetime.utcnow(),
                    funcionario_id=None,
                    acao="LOGIN_BLOQUEADO",
                    recurso="autenticacao",
                    detalhes=f"Excesso de tentativas para {email_normalizado}",
                    endereco_ip=endereco_ip,
                    agente_usuario=agente_usuario,
                )
            )
            raise ContaBloqueada(
                "Conta temporariamente bloqueada por excesso de tentativas. "
                f"Tente novamente em {self.JANELA_MINUTOS} minutos."
            )

        funcionario = self._repo.buscar_por_email(email_normalizado)
        if not funcionario or not funcionario.ativo:
            self._repo.registrar_tentativa_login(email_normalizado, False, endereco_ip)
            self._auditoria.registrar(
                LogAuditoria(
                    ocorrido_em=datetime.utcnow(),
                    funcionario_id=None,
                    acao="LOGIN_FALHOU",
                    recurso="autenticacao",
                    detalhes=f"Usuário inexistente/inativo: {email_normalizado}",
                    endereco_ip=endereco_ip,
                    agente_usuario=agente_usuario,
                )
            )
            raise CredenciaisInvalidas("E-mail ou senha incorretos.")

        if not self._senha.verificar(senha, funcionario.senha_hash):
            self._repo.registrar_tentativa_login(email_normalizado, False, endereco_ip)
            self._auditoria.registrar(
                LogAuditoria(
                    ocorrido_em=datetime.utcnow(),
                    funcionario_id=funcionario.identificador,
                    acao="LOGIN_FALHOU",
                    recurso="autenticacao",
                    detalhes="Senha incorreta",
                    endereco_ip=endereco_ip,
                    agente_usuario=agente_usuario,
                )
            )
            raise CredenciaisInvalidas("E-mail ou senha incorretos.")

        funcionario.registrar_acesso()
        self._repo.atualizar(funcionario)
        self._repo.registrar_tentativa_login(email_normalizado, True, endereco_ip)

        token_acesso = self._token.gerar_token_acesso(
            DadosToken(
                funcionario_id=funcionario.identificador or 0,
                email=funcionario.email,
                papeis=[p.value for p in funcionario.papeis],
            )
        )
        token_refresh = self._token.gerar_token_refresh(funcionario.identificador or 0)

        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario.identificador,
                acao="LOGIN",
                recurso="autenticacao",
                detalhes=f"Login bem-sucedido de {funcionario.email}",
                endereco_ip=endereco_ip,
                agente_usuario=agente_usuario,
            )
        )

        return ResultadoLogin(
            token_acesso=token_acesso,
            token_refresh=token_refresh,
            funcionario=funcionario,
            deve_trocar_senha=funcionario.deve_trocar_senha,
        )


class TrocarSenha:
    """Caso de uso: troca de senha do funcionário."""

    def __init__(
        self,
        repositorio_funcionarios: RepositorioFuncionarios,
        servico_senha: ServicoSenha,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_funcionarios
        self._senha = servico_senha
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        funcionario_id: int,
        senha_atual: str,
        senha_nova: str,
    ) -> None:
        funcionario = self._repo.buscar_por_id(funcionario_id)
        if not funcionario:
            raise CredenciaisInvalidas("Funcionário não encontrado.")
        if not self._senha.verificar(senha_atual, funcionario.senha_hash):
            raise CredenciaisInvalidas("Senha atual incorreta.")
        if senha_atual == senha_nova:
            raise DadosInvalidos("A nova senha deve ser diferente da atual.")
        self._senha.validar_politica(senha_nova)
        funcionario.senha_hash = self._senha.gerar_hash(senha_nova)
        funcionario.deve_trocar_senha = False
        self._repo.atualizar(funcionario)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="TROCA_SENHA",
                recurso="funcionario",
                recurso_id=funcionario_id,
            )
        )
