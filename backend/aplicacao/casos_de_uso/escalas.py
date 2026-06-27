"""Casos de uso de Escalas de Cuidadores."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.escala import Escala, TipoTurno, Turno
from backend.dominio.excecoes import EntidadeNaoEncontrada, RegraDeNegocioViolada
from backend.dominio.objetos_de_valor.periodo import Periodo
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_escalas import RepositorioEscalas


class CriarEscala:
    def __init__(
        self, repositorio: RepositorioEscalas, auditoria: RepositorioAuditoria
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        mes: int,
        ano: int,
        setor: str,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Escala:
        escala = Escala(referencia_mes=mes, referencia_ano=ano, setor=setor)
        criada = self._repo.criar(escala)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="escala",
                recurso_id=criada.identificador,
            )
        )
        return criada


class AdicionarTurno:
    def __init__(
        self, repositorio: RepositorioEscalas, auditoria: RepositorioAuditoria
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        escala_id: int,
        funcionario_id: int,
        inicio: datetime,
        fim: datetime,
        tipo: TipoTurno,
        observacoes: Optional[str] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Turno:
        escala = self._repo.buscar_por_id(escala_id)
        if not escala:
            raise EntidadeNaoEncontrada("Escala não encontrada.")

        # Valida conflito contra todos os turnos do funcionário no período do mês
        novo_periodo = Periodo(inicio, fim)
        turnos_existentes = self._repo.listar_turnos_funcionario(
            funcionario_id, inicio.date(), fim.date()
        )
        for existente in turnos_existentes:
            if existente.periodo().sobrepoe(novo_periodo):
                raise RegraDeNegocioViolada(
                    "Conflito: o funcionário já possui turno sobreposto."
                )
        turno = Turno(
            funcionario_id=funcionario_id,
            inicio=inicio,
            fim=fim,
            tipo=tipo,
            observacoes=observacoes,
        )
        criado = self._repo.adicionar_turno(escala_id, turno)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="turno",
                recurso_id=criado.identificador,
            )
        )
        return criado


class ListarTurnosDoDia:
    def __init__(self, repositorio: RepositorioEscalas) -> None:
        self._repo = repositorio

    def executar(self, dia: date) -> list[Turno]:
        return self._repo.listar_turnos_do_dia(dia)
