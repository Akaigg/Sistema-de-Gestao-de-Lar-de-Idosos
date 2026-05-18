"""Entidades de domínio."""

from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.dominio.entidades.residente import Residente, StatusResidente, GrauDependencia
from backend.dominio.entidades.responsavel import Responsavel
from backend.dominio.entidades.quarto import Quarto, TipoQuarto, StatusQuarto, Leito, StatusLeito
from backend.dominio.entidades.medicamento import (
    Medicamento,
    Prescricao,
    AplicacaoMedicamento,
    StatusAplicacao,
    ViaAdministracao,
    LoteMedicamento,
)
from backend.dominio.entidades.prontuario import (
    SinaisVitais,
    Evolucao,
    Alergia,
    CondicaoCronica,
    Consulta,
    StatusConsulta,
    TipoConsulta,
)
from backend.dominio.entidades.alimentacao import (
    Cardapio,
    Refeicao,
    TipoRefeicao,
    Dieta,
    TipoDieta,
    IngestaoHidrica,
)
from backend.dominio.entidades.escala import Escala, Turno, TipoTurno
from backend.dominio.entidades.financeiro import (
    Mensalidade,
    LancamentoFinanceiro,
    TipoLancamento,
    StatusPagamento,
    FormaPagamento,
)
from backend.dominio.entidades.documento import DocumentoAssinado, ModeloDocumento
from backend.dominio.entidades.ocorrencia import Ocorrencia, TipoOcorrencia, GravidadeOcorrencia
from backend.dominio.entidades.visita import Visita
from backend.dominio.entidades.auditoria import LogAuditoria

__all__ = [
    "Funcionario",
    "PapelFuncionario",
    "Residente",
    "StatusResidente",
    "GrauDependencia",
    "Responsavel",
    "Quarto",
    "TipoQuarto",
    "StatusQuarto",
    "Leito",
    "StatusLeito",
    "Medicamento",
    "Prescricao",
    "AplicacaoMedicamento",
    "StatusAplicacao",
    "ViaAdministracao",
    "LoteMedicamento",
    "SinaisVitais",
    "Evolucao",
    "Alergia",
    "CondicaoCronica",
    "Consulta",
    "StatusConsulta",
    "TipoConsulta",
    "Cardapio",
    "Refeicao",
    "TipoRefeicao",
    "Dieta",
    "TipoDieta",
    "IngestaoHidrica",
    "Escala",
    "Turno",
    "TipoTurno",
    "Mensalidade",
    "LancamentoFinanceiro",
    "TipoLancamento",
    "StatusPagamento",
    "FormaPagamento",
    "DocumentoAssinado",
    "ModeloDocumento",
    "Ocorrencia",
    "TipoOcorrencia",
    "GravidadeOcorrencia",
    "Visita",
    "LogAuditoria",
]
