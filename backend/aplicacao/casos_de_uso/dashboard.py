"""Caso de uso para o painel inicial (dashboard)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from backend.dominio.repositorios.repositorio_medicamentos import RepositorioAplicacoes
from backend.dominio.repositorios.repositorio_prontuario import RepositorioConsultas
from backend.dominio.repositorios.repositorio_quartos import RepositorioQuartos
from backend.dominio.repositorios.repositorio_residentes import RepositorioResidentes


@dataclass
class IndicadoresDashboard:
    total_residentes_ativos: int
    total_leitos: int
    leitos_ocupados: int
    taxa_ocupacao_percentual: float
    aplicacoes_medicamento_hoje: int
    consultas_hoje: int
    total_aniversariantes_mes: int


class ObterIndicadoresDashboard:
    def __init__(
        self,
        repositorio_residentes: RepositorioResidentes,
        repositorio_quartos: RepositorioQuartos,
        repositorio_aplicacoes: RepositorioAplicacoes,
        repositorio_consultas: RepositorioConsultas,
    ) -> None:
        self._residentes = repositorio_residentes
        self._quartos = repositorio_quartos
        self._aplicacoes = repositorio_aplicacoes
        self._consultas = repositorio_consultas

    def executar(self, hoje: date | None = None) -> IndicadoresDashboard:
        hoje = hoje or date.today()
        total_residentes = self._residentes.contar_ativos()
        total_leitos = self._quartos.contar_leitos_totais()
        ocupados = self._quartos.contar_leitos_ocupados()
        taxa = (ocupados / total_leitos * 100.0) if total_leitos else 0.0
        return IndicadoresDashboard(
            total_residentes_ativos=total_residentes,
            total_leitos=total_leitos,
            leitos_ocupados=ocupados,
            taxa_ocupacao_percentual=round(taxa, 1),
            aplicacoes_medicamento_hoje=self._aplicacoes.contar_do_dia(hoje),
            consultas_hoje=self._consultas.contar_do_dia(hoje),
            total_aniversariantes_mes=len(
                self._residentes.listar_aniversariantes_do_mes(hoje.month)
            ),
        )
