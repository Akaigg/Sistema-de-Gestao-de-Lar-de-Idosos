"""Implementações de repositórios usando SQLAlchemy."""

from backend.infraestrutura.repositorios.repositorio_funcionarios_sql import (
    RepositorioFuncionariosSQL,
)
from backend.infraestrutura.repositorios.repositorio_residentes_sql import (
    RepositorioResidentesSQL,
)
from backend.infraestrutura.repositorios.repositorio_responsaveis_sql import (
    RepositorioResponsaveisSQL,
)
from backend.infraestrutura.repositorios.repositorio_quartos_sql import (
    RepositorioQuartosSQL,
)
from backend.infraestrutura.repositorios.repositorio_medicamentos_sql import (
    RepositorioMedicamentosSQL,
    RepositorioPrescricoesSQL,
    RepositorioAplicacoesSQL,
    RepositorioLotesMedicamentoSQL,
)
from backend.infraestrutura.repositorios.repositorio_prontuario_sql import (
    RepositorioSinaisVitaisSQL,
    RepositorioEvolucoesSQL,
    RepositorioAlergiasSQL,
    RepositorioCondicoesCronicasSQL,
    RepositorioConsultasSQL,
)
from backend.infraestrutura.repositorios.repositorio_alimentacao_sql import (
    RepositorioCardapiosSQL,
    RepositorioDietasSQL,
    RepositorioRefeicoesSQL,
    RepositorioIngestaoHidricaSQL,
)
from backend.infraestrutura.repositorios.repositorio_escalas_sql import (
    RepositorioEscalasSQL,
)
from backend.infraestrutura.repositorios.repositorio_financeiro_sql import (
    RepositorioMensalidadesSQL,
    RepositorioLancamentosSQL,
)
from backend.infraestrutura.repositorios.repositorio_documentos_sql import (
    RepositorioModelosDocumentoSQL,
    RepositorioDocumentosAssinadosSQL,
)
from backend.infraestrutura.repositorios.repositorio_ocorrencias_sql import (
    RepositorioOcorrenciasSQL,
)
from backend.infraestrutura.repositorios.repositorio_visitas_sql import (
    RepositorioVisitasSQL,
)
from backend.infraestrutura.repositorios.repositorio_auditoria_sql import (
    RepositorioAuditoriaSQL,
)

__all__ = [
    "RepositorioFuncionariosSQL",
    "RepositorioResidentesSQL",
    "RepositorioResponsaveisSQL",
    "RepositorioQuartosSQL",
    "RepositorioMedicamentosSQL",
    "RepositorioPrescricoesSQL",
    "RepositorioAplicacoesSQL",
    "RepositorioLotesMedicamentoSQL",
    "RepositorioSinaisVitaisSQL",
    "RepositorioEvolucoesSQL",
    "RepositorioAlergiasSQL",
    "RepositorioCondicoesCronicasSQL",
    "RepositorioConsultasSQL",
    "RepositorioCardapiosSQL",
    "RepositorioDietasSQL",
    "RepositorioRefeicoesSQL",
    "RepositorioIngestaoHidricaSQL",
    "RepositorioEscalasSQL",
    "RepositorioMensalidadesSQL",
    "RepositorioLancamentosSQL",
    "RepositorioModelosDocumentoSQL",
    "RepositorioDocumentosAssinadosSQL",
    "RepositorioOcorrenciasSQL",
    "RepositorioVisitasSQL",
    "RepositorioAuditoriaSQL",
]
