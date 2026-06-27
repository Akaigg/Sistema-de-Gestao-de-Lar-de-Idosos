"""Casos de uso de gestão de funcionários."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.dominio.excecoes import EntidadeJaExistente, EntidadeNaoEncontrada
from backend.dominio.objetos_de_valor import CPF, Email, Telefone
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_funcionarios import RepositorioFuncionarios
from backend.dominio.servicos.servico_senha import ServicoSenha


@dataclass
class DadosCadastroFuncionario:
    nome_completo: str
    email: str
    cpf: str
    cargo: str
    papeis: list[PapelFuncionario]
    senha_inicial: str
    telefone: Optional[str] = None
    data_admissao: Optional[date] = None


class CadastrarFuncionario:
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
        self, dados: DadosCadastroFuncionario, funcionario_responsavel_id: Optional[int] = None
    ) -> Funcionario:
        email = Email(dados.email).endereco
        cpf = CPF(dados.cpf).numero
        if dados.telefone:
            Telefone(dados.telefone)

        if self._repo.buscar_por_email(email):
            raise EntidadeJaExistente("Já existe um funcionário com este e-mail.")
        if self._repo.buscar_por_cpf(cpf):
            raise EntidadeJaExistente("Já existe um funcionário com este CPF.")

        self._senha.validar_politica(dados.senha_inicial)

        funcionario = Funcionario(
            nome_completo=dados.nome_completo.strip(),
            email=email,
            senha_hash=self._senha.gerar_hash(dados.senha_inicial),
            cpf=cpf,
            cargo=dados.cargo,
            papeis=dados.papeis,
            telefone=dados.telefone,
            data_admissao=dados.data_admissao or date.today(),
            deve_trocar_senha=True,
        )
        criado = self._repo.criar(funcionario)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="funcionario",
                recurso_id=criado.identificador,
                detalhes=f"Funcionário {criado.nome_completo}",
            )
        )
        return criado


class AtualizarFuncionario:
    def __init__(
        self,
        repositorio_funcionarios: RepositorioFuncionarios,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_funcionarios
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        funcionario_id: int,
        nome_completo: Optional[str] = None,
        cargo: Optional[str] = None,
        telefone: Optional[str] = None,
        papeis: Optional[list[PapelFuncionario]] = None,
        ativo: Optional[bool] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Funcionario:
        funcionario = self._repo.buscar_por_id(funcionario_id)
        if not funcionario:
            raise EntidadeNaoEncontrada("Funcionário não encontrado.")
        if nome_completo is not None:
            funcionario.nome_completo = nome_completo.strip()
        if cargo is not None:
            funcionario.cargo = cargo
        if telefone is not None:
            Telefone(telefone)
            funcionario.telefone = telefone
        if papeis is not None:
            funcionario.papeis = papeis
        if ativo is not None:
            funcionario.ativo = ativo
            if not ativo and not funcionario.data_desligamento:
                funcionario.data_desligamento = date.today()
        atualizado = self._repo.atualizar(funcionario)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="funcionario",
                recurso_id=funcionario_id,
            )
        )
        return atualizado


class ListarFuncionarios:
    def __init__(self, repositorio_funcionarios: RepositorioFuncionarios) -> None:
        self._repo = repositorio_funcionarios

    def executar(
        self,
        termo_busca: Optional[str] = None,
        apenas_ativos: bool = True,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> tuple[list[Funcionario], int]:
        itens = self._repo.listar(termo_busca, apenas_ativos, pagina, tamanho_pagina)
        total = self._repo.contar(termo_busca, apenas_ativos)
        return itens, total
