"""Entidades de Escala de Cuidadores."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional

from backend.dominio.excecoes import RegraDeNegocioViolada
from backend.dominio.objetos_de_valor.periodo import Periodo


class TipoTurno(str, Enum):
    MANHA = "manha"
    TARDE = "tarde"
    NOITE = "noite"
    PLANTAO_12H = "plantao_12h"
    PLANTAO_24H = "plantao_24h"


@dataclass
class Turno:
    """Turno atribuído a um funcionário."""

    funcionario_id: int
    inicio: datetime
    fim: datetime
    tipo: TipoTurno
    observacoes: Optional[str] = None
    confirmado: bool = False
    identificador: Optional[int] = None

    def periodo(self) -> Periodo:
        return Periodo(inicio=self.inicio, fim=self.fim)

    def duracao_horas(self) -> float:
        return self.periodo().duracao_em_horas()


@dataclass
class Escala:
    """Escala mensal de uma equipe."""

    referencia_mes: int
    referencia_ano: int
    setor: str  # "Enfermagem", "Cuidadores Piso 1", etc.
    turnos: list[Turno] = field(default_factory=list)
    publicada: bool = False
    publicada_em: Optional[datetime] = None
    publicada_por_id: Optional[int] = None
    identificador: Optional[int] = None

    def adicionar_turno(self, novo: Turno) -> None:
        novo_periodo = novo.periodo()
        for existente in self.turnos:
            if existente.funcionario_id != novo.funcionario_id:
                continue
            if existente.periodo().sobrepoe(novo_periodo):
                raise RegraDeNegocioViolada(
                    "Conflito de horário com outro turno do mesmo funcionário."
                )
        self.turnos.append(novo)

    def total_horas_funcionario(self, funcionario_id: int) -> float:
        return sum(
            t.duracao_horas() for t in self.turnos if t.funcionario_id == funcionario_id
        )

    def publicar(self, funcionario_id: int) -> None:
        if self.publicada:
            raise RegraDeNegocioViolada("Escala já publicada.")
        self.publicada = True
        self.publicada_em = datetime.utcnow()
        self.publicada_por_id = funcionario_id
