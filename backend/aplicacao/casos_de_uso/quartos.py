"""Casos de uso para quartos e leitos."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.quarto import (
    Quarto,
    Leito,
    TipoQuarto,
    StatusLeito,
)
from backend.dominio.excecoes import (
    EntidadeJaExistente,
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
)
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_quartos import RepositorioQuartos


@dataclass
class DadosCadastroQuarto:
    numero: str
    andar: int
    tipo: TipoQuarto
    capacidade: int
    leitos: list[str] = field(default_factory=list)
    possui_banheiro: bool = True
    possui_ar_condicionado: bool = False
    acessibilidade: bool = True
    observacoes: Optional[str] = None


class CadastrarQuarto:
    def __init__(
        self,
        repositorio_quartos: RepositorioQuartos,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_quartos
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        dados: DadosCadastroQuarto,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Quarto:
        if len(dados.leitos) > dados.capacidade:
            raise RegraDeNegocioViolada(
                "Número de leitos não pode exceder a capacidade do quarto."
            )
        leitos = [Leito(numero=numero) for numero in dados.leitos]
        quarto = Quarto(
            numero=dados.numero,
            andar=dados.andar,
            tipo=dados.tipo,
            capacidade=dados.capacidade,
            leitos=leitos,
            possui_banheiro=dados.possui_banheiro,
            possui_ar_condicionado=dados.possui_ar_condicionado,
            acessibilidade=dados.acessibilidade,
            observacoes=dados.observacoes,
        )
        criado = self._repo.criar(quarto)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="quarto",
                recurso_id=criado.identificador,
                detalhes=f"Quarto {dados.numero}",
            )
        )
        return criado


class AlocarResidenteEmLeito:
    def __init__(
        self,
        repositorio_quartos: RepositorioQuartos,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_quartos
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        leito_id: int,
        residente_id: int,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Leito:
        leito = self._repo.buscar_leito(leito_id)
        if not leito:
            raise EntidadeNaoEncontrada("Leito não encontrado.")

        # Libera leito atual do residente, se houver
        leito_anterior = self._repo.buscar_leito_por_residente(residente_id)
        if leito_anterior and leito_anterior.identificador != leito_id:
            leito_anterior.liberar()
            self._repo.atualizar_leito(leito_anterior)

        leito.ocupar(residente_id)
        atualizado = self._repo.atualizar_leito(leito)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="leito",
                recurso_id=leito_id,
                detalhes=f"Residente {residente_id} alocado",
            )
        )
        return atualizado


class LiberarLeito:
    def __init__(
        self,
        repositorio_quartos: RepositorioQuartos,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_quartos
        self._auditoria = repositorio_auditoria

    def executar(
        self, leito_id: int, funcionario_responsavel_id: Optional[int] = None
    ) -> Leito:
        leito = self._repo.buscar_leito(leito_id)
        if not leito:
            raise EntidadeNaoEncontrada("Leito não encontrado.")
        leito.liberar()
        atualizado = self._repo.atualizar_leito(leito)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="leito",
                recurso_id=leito_id,
                detalhes="Leito liberado",
            )
        )
        return atualizado


class ListarQuartos:
    def __init__(self, repositorio_quartos: RepositorioQuartos) -> None:
        self._repo = repositorio_quartos

    def executar(self) -> list[Quarto]:
        return self._repo.listar()
