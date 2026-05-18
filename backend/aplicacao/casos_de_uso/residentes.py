"""Casos de uso de Residentes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.residente import (
    Residente,
    StatusResidente,
    GrauDependencia,
)
from backend.dominio.excecoes import EntidadeJaExistente, EntidadeNaoEncontrada
from backend.dominio.objetos_de_valor import CPF
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_residentes import RepositorioResidentes


@dataclass
class DadosCadastroResidente:
    nome_completo: str
    data_nascimento: date
    cpf: str
    sexo: str
    data_entrada: date
    grau_dependencia: GrauDependencia = GrauDependencia.INDEPENDENTE
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


class CadastrarResidente:
    def __init__(
        self,
        repositorio_residentes: RepositorioResidentes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_residentes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        dados: DadosCadastroResidente,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Residente:
        cpf = CPF(dados.cpf).numero
        if self._repo.buscar_por_cpf(cpf):
            raise EntidadeJaExistente("Já existe um residente com este CPF.")

        residente = Residente(
            nome_completo=dados.nome_completo.strip(),
            data_nascimento=dados.data_nascimento,
            cpf=cpf,
            sexo=dados.sexo,
            data_entrada=dados.data_entrada,
            grau_dependencia=dados.grau_dependencia,
            rg=dados.rg,
            cartao_sus=dados.cartao_sus,
            convenio=dados.convenio,
            numero_convenio=dados.numero_convenio,
            religiao=dados.religiao,
            estado_civil=dados.estado_civil,
            naturalidade=dados.naturalidade,
            profissao_anterior=dados.profissao_anterior,
            observacoes=dados.observacoes,
            consentimento_imagem=dados.consentimento_imagem,
        )
        criado = self._repo.criar(residente)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="residente",
                recurso_id=criado.identificador,
                detalhes=f"Residente {criado.nome_completo}",
            )
        )
        return criado


class AtualizarResidente:
    def __init__(
        self,
        repositorio_residentes: RepositorioResidentes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_residentes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        residente_id: int,
        atualizacoes: dict,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Residente:
        residente = self._repo.buscar_por_id(residente_id)
        if not residente:
            raise EntidadeNaoEncontrada("Residente não encontrado.")
        for chave, valor in atualizacoes.items():
            if hasattr(residente, chave) and valor is not None:
                setattr(residente, chave, valor)
        atualizado = self._repo.atualizar(residente)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="residente",
                recurso_id=residente_id,
            )
        )
        return atualizado


class ListarResidentes:
    def __init__(self, repositorio_residentes: RepositorioResidentes) -> None:
        self._repo = repositorio_residentes

    def executar(
        self,
        termo_busca: Optional[str] = None,
        status: Optional[StatusResidente] = None,
        pagina: int = 1,
        tamanho_pagina: int = 50,
    ) -> tuple[list[Residente], int]:
        itens = self._repo.listar(termo_busca, status, pagina, tamanho_pagina)
        total = self._repo.contar(termo_busca, status)
        return itens, total


class ObterResidente:
    def __init__(self, repositorio_residentes: RepositorioResidentes) -> None:
        self._repo = repositorio_residentes

    def executar(self, residente_id: int) -> Residente:
        r = self._repo.buscar_por_id(residente_id)
        if not r:
            raise EntidadeNaoEncontrada("Residente não encontrado.")
        return r


class RegistrarSaidaResidente:
    """Registra desligamento ou falecimento."""

    def __init__(
        self,
        repositorio_residentes: RepositorioResidentes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_residentes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        residente_id: int,
        motivo: str,
        falecimento: bool = False,
        data_saida: Optional[date] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Residente:
        residente = self._repo.buscar_por_id(residente_id)
        if not residente:
            raise EntidadeNaoEncontrada("Residente não encontrado.")
        if falecimento:
            residente.registrar_falecimento(data_saida or date.today(), motivo)
        else:
            residente.desligar(motivo, data_saida)
        atualizado = self._repo.atualizar(residente)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="residente",
                recurso_id=residente_id,
                detalhes=("Falecimento" if falecimento else "Desligamento") + f" — {motivo}",
            )
        )
        return atualizado
