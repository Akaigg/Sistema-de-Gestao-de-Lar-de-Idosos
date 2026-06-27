"""Entidade Residente."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class StatusResidente(str, Enum):
    ATIVO = "ativo"
    INTERNADO = "internado"
    LICENCA = "licenca"
    DESLIGADO = "desligado"
    FALECIDO = "falecido"


class GrauDependencia(str, Enum):
    """Escala simplificada de Katz/Lawton."""

    INDEPENDENTE = "independente"
    DEPENDENCIA_LEVE = "dependencia_leve"
    DEPENDENCIA_MODERADA = "dependencia_moderada"
    DEPENDENCIA_GRAVE = "dependencia_grave"
    TOTAL = "total"


@dataclass
class Residente:
    """Residente do lar."""

    nome_completo: str
    data_nascimento: date
    cpf: str
    sexo: str  # "M", "F", "O"
    data_entrada: date
    grau_dependencia: GrauDependencia = GrauDependencia.INDEPENDENTE
    status: StatusResidente = StatusResidente.ATIVO
    rg: Optional[str] = None
    cartao_sus: Optional[str] = None
    convenio: Optional[str] = None
    numero_convenio: Optional[str] = None
    religiao: Optional[str] = None
    estado_civil: Optional[str] = None
    naturalidade: Optional[str] = None
    profissao_anterior: Optional[str] = None
    observacoes: Optional[str] = None
    foto_caminho: Optional[str] = None
    consentimento_imagem: bool = False
    data_saida: Optional[date] = None
    motivo_saida: Optional[str] = None
    responsaveis_ids: list[int] = field(default_factory=list)
    identificador: Optional[int] = None

    def calcular_idade(self, hoje: Optional[date] = None) -> int:
        referencia = hoje or date.today()
        idade = referencia.year - self.data_nascimento.year
        if (referencia.month, referencia.day) < (
            self.data_nascimento.month,
            self.data_nascimento.day,
        ):
            idade -= 1
        return idade

    def esta_ativo(self) -> bool:
        return self.status == StatusResidente.ATIVO

    def desligar(self, motivo: str, quando: Optional[date] = None) -> None:
        self.status = StatusResidente.DESLIGADO
        self.data_saida = quando or date.today()
        self.motivo_saida = motivo

    def registrar_falecimento(self, quando: date, motivo: Optional[str] = None) -> None:
        self.status = StatusResidente.FALECIDO
        self.data_saida = quando
        self.motivo_saida = motivo
