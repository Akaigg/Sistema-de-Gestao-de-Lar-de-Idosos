"""Interfaces (portas) de repositório.

Estas interfaces são implementadas pela camada de infraestrutura.
"""

from backend.dominio.repositorios.repositorio_funcionarios import RepositorioFuncionarios
from backend.dominio.repositorios.repositorio_residentes import RepositorioResidentes
from backend.dominio.repositorios.repositorio_responsaveis import RepositorioResponsaveis
from backend.dominio.repositorios.repositorio_quartos import RepositorioQuartos
from backend.dominio.repositorios.repositorio_medicamentos import (
    RepositorioMedicamentos,
    RepositorioPrescricoes,
    RepositorioAplicacoes,
    RepositorioLotesMedicamento,
)
from backend.dominio.repositorios.repositorio_prontuario import (
    RepositorioSinaisVitais,
    RepositorioEvolucoes,
    RepositorioAlergias,
    RepositorioCondicoesCronicas,
    RepositorioConsultas,
)
from backend.dominio.repositorios.repositorio_alimentacao import (
    RepositorioCardapios,
    RepositorioDietas,
    RepositorioRefeicoes,
    RepositorioIngestaoHidrica,
)
from backend.dominio.repositorios.repositorio_escalas import RepositorioEscalas
from backend.dominio.repositorios.repositorio_financeiro import (
    RepositorioMensalidades,
    RepositorioLancamentos,
)
from backend.dominio.repositorios.repositorio_documentos import (
    RepositorioModelosDocumento,
    RepositorioDocumentosAssinados,
)
from backend.dominio.repositorios.repositorio_ocorrencias import RepositorioOcorrencias
from backend.dominio.repositorios.repositorio_visitas import RepositorioVisitas
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria

__all__ = [
    "RepositorioFuncionarios",
    "RepositorioResidentes",
    "RepositorioResponsaveis",
    "RepositorioQuartos",
    "RepositorioMedicamentos",
    "RepositorioPrescricoes",
    "RepositorioAplicacoes",
    "RepositorioLotesMedicamento",
    "RepositorioSinaisVitais",
    "RepositorioEvolucoes",
    "RepositorioAlergias",
    "RepositorioCondicoesCronicas",
    "RepositorioConsultas",
    "RepositorioCardapios",
    "RepositorioDietas",
    "RepositorioRefeicoes",
    "RepositorioIngestaoHidrica",
    "RepositorioEscalas",
    "RepositorioMensalidades",
    "RepositorioLancamentos",
    "RepositorioModelosDocumento",
    "RepositorioDocumentosAssinados",
    "RepositorioOcorrencias",
    "RepositorioVisitas",
    "RepositorioAuditoria",
]
