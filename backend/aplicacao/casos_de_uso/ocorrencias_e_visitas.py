"""Casos de uso de Ocorrências e Visitas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.ocorrencia import (
    GravidadeOcorrencia,
    Ocorrencia,
    TipoOcorrencia,
)
from backend.dominio.entidades.visita import Visita
from backend.dominio.excecoes import EntidadeNaoEncontrada
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_ocorrencias import RepositorioOcorrencias
from backend.dominio.repositorios.repositorio_visitas import RepositorioVisitas


class RegistrarOcorrencia:
    def __init__(
        self,
        repositorio: RepositorioOcorrencias,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        residente_id: int,
        tipo: TipoOcorrencia,
        gravidade: GravidadeOcorrencia,
        descricao: str,
        funcionario_id: int,
        local: Optional[str] = None,
        medidas_adotadas: Optional[str] = None,
        necessitou_hospital: bool = False,
        momento: Optional[datetime] = None,
    ) -> Ocorrencia:
        ocorrencia = Ocorrencia(
            residente_id=residente_id,
            tipo=tipo,
            gravidade=gravidade,
            descricao=descricao,
            ocorreu_em=momento or datetime.utcnow(),
            registrada_por_id=funcionario_id,
            local=local,
            medidas_adotadas=medidas_adotadas,
            necessitou_hospital=necessitou_hospital,
        )
        criada = self._repo.criar(ocorrencia)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="CRIAR",
                recurso="ocorrencia",
                recurso_id=criada.identificador,
            )
        )
        return criada


class EncerrarOcorrencia:
    def __init__(self, repositorio: RepositorioOcorrencias) -> None:
        self._repo = repositorio

    def executar(self, ocorrencia_id: int) -> Ocorrencia:
        ocorrencia = self._repo.buscar_por_id(ocorrencia_id)
        if not ocorrencia:
            raise EntidadeNaoEncontrada("Ocorrência não encontrada.")
        ocorrencia.encerrada = True
        ocorrencia.encerrada_em = datetime.utcnow()
        return self._repo.atualizar(ocorrencia)


class RegistrarVisita:
    def __init__(self, repositorio: RepositorioVisitas) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        nome_visitante: str,
        documento_visitante: str,
        parentesco_ou_relacao: str,
        funcionario_recebeu_id: Optional[int] = None,
        observacoes: Optional[str] = None,
    ) -> Visita:
        visita = Visita(
            residente_id=residente_id,
            nome_visitante=nome_visitante,
            documento_visitante=documento_visitante,
            parentesco_ou_relacao=parentesco_ou_relacao,
            entrada_em=datetime.utcnow(),
            funcionario_recebeu_id=funcionario_recebeu_id,
            observacoes=observacoes,
        )
        return self._repo.criar(visita)


class EncerrarVisita:
    def __init__(self, repositorio: RepositorioVisitas) -> None:
        self._repo = repositorio

    def executar(self, visita_id: int) -> Visita:
        visita = self._repo.buscar_por_id(visita_id)
        if not visita:
            raise EntidadeNaoEncontrada("Visita não encontrada.")
        visita.encerrar()
        return self._repo.atualizar(visita)
