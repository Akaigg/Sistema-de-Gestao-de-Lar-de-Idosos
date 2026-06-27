"""Fábricas de dependências (DI container manual do FastAPI)."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.infraestrutura.banco_de_dados import obter_sessao
from backend.infraestrutura.configuracao import configuracoes
from backend.infraestrutura.repositorios import (
    RepositorioFuncionariosSQL,
    RepositorioResidentesSQL,
    RepositorioResponsaveisSQL,
    RepositorioQuartosSQL,
    RepositorioMedicamentosSQL,
    RepositorioPrescricoesSQL,
    RepositorioAplicacoesSQL,
    RepositorioLotesMedicamentoSQL,
    RepositorioSinaisVitaisSQL,
    RepositorioEvolucoesSQL,
    RepositorioAlergiasSQL,
    RepositorioCondicoesCronicasSQL,
    RepositorioConsultasSQL,
    RepositorioCardapiosSQL,
    RepositorioDietasSQL,
    RepositorioRefeicoesSQL,
    RepositorioIngestaoHidricaSQL,
    RepositorioEscalasSQL,
    RepositorioMensalidadesSQL,
    RepositorioLancamentosSQL,
    RepositorioModelosDocumentoSQL,
    RepositorioDocumentosAssinadosSQL,
    RepositorioOcorrenciasSQL,
    RepositorioVisitasSQL,
    RepositorioAuditoriaSQL,
)
from backend.infraestrutura.seguranca import (
    ServicoHashSHA256,
    ServicoSenhaBcrypt,
    ServicoTokenJWT,
)
from backend.infraestrutura.servicos_externos import GeradorPDF


# Serviços singleton

@lru_cache(maxsize=1)
def obter_servico_senha() -> ServicoSenhaBcrypt:
    return ServicoSenhaBcrypt()


@lru_cache(maxsize=1)
def obter_servico_token() -> ServicoTokenJWT:
    return ServicoTokenJWT()


@lru_cache(maxsize=1)
def obter_servico_hash() -> ServicoHashSHA256:
    return ServicoHashSHA256()


@lru_cache(maxsize=1)
def obter_gerador_pdf() -> GeradorPDF:
    return GeradorPDF(configuracoes.diretorio_assinaturas)


# Repositórios (escopo: requisição)

def obter_repo_funcionarios(sessao: Session = Depends(obter_sessao)) -> RepositorioFuncionariosSQL:
    return RepositorioFuncionariosSQL(sessao)


def obter_repo_residentes(sessao: Session = Depends(obter_sessao)) -> RepositorioResidentesSQL:
    return RepositorioResidentesSQL(sessao)


def obter_repo_responsaveis(sessao: Session = Depends(obter_sessao)) -> RepositorioResponsaveisSQL:
    return RepositorioResponsaveisSQL(sessao)


def obter_repo_quartos(sessao: Session = Depends(obter_sessao)) -> RepositorioQuartosSQL:
    return RepositorioQuartosSQL(sessao)


def obter_repo_medicamentos(sessao: Session = Depends(obter_sessao)) -> RepositorioMedicamentosSQL:
    return RepositorioMedicamentosSQL(sessao)


def obter_repo_prescricoes(sessao: Session = Depends(obter_sessao)) -> RepositorioPrescricoesSQL:
    return RepositorioPrescricoesSQL(sessao)


def obter_repo_aplicacoes(sessao: Session = Depends(obter_sessao)) -> RepositorioAplicacoesSQL:
    return RepositorioAplicacoesSQL(sessao)


def obter_repo_lotes(sessao: Session = Depends(obter_sessao)) -> RepositorioLotesMedicamentoSQL:
    return RepositorioLotesMedicamentoSQL(sessao)


def obter_repo_sinais(sessao: Session = Depends(obter_sessao)) -> RepositorioSinaisVitaisSQL:
    return RepositorioSinaisVitaisSQL(sessao)


def obter_repo_evolucoes(sessao: Session = Depends(obter_sessao)) -> RepositorioEvolucoesSQL:
    return RepositorioEvolucoesSQL(sessao)


def obter_repo_alergias(sessao: Session = Depends(obter_sessao)) -> RepositorioAlergiasSQL:
    return RepositorioAlergiasSQL(sessao)


def obter_repo_condicoes(sessao: Session = Depends(obter_sessao)) -> RepositorioCondicoesCronicasSQL:
    return RepositorioCondicoesCronicasSQL(sessao)


def obter_repo_consultas(sessao: Session = Depends(obter_sessao)) -> RepositorioConsultasSQL:
    return RepositorioConsultasSQL(sessao)


def obter_repo_cardapios(sessao: Session = Depends(obter_sessao)) -> RepositorioCardapiosSQL:
    return RepositorioCardapiosSQL(sessao)


def obter_repo_dietas(sessao: Session = Depends(obter_sessao)) -> RepositorioDietasSQL:
    return RepositorioDietasSQL(sessao)


def obter_repo_refeicoes(sessao: Session = Depends(obter_sessao)) -> RepositorioRefeicoesSQL:
    return RepositorioRefeicoesSQL(sessao)


def obter_repo_ingestao(sessao: Session = Depends(obter_sessao)) -> RepositorioIngestaoHidricaSQL:
    return RepositorioIngestaoHidricaSQL(sessao)


def obter_repo_escalas(sessao: Session = Depends(obter_sessao)) -> RepositorioEscalasSQL:
    return RepositorioEscalasSQL(sessao)


def obter_repo_mensalidades(sessao: Session = Depends(obter_sessao)) -> RepositorioMensalidadesSQL:
    return RepositorioMensalidadesSQL(sessao)


def obter_repo_lancamentos(sessao: Session = Depends(obter_sessao)) -> RepositorioLancamentosSQL:
    return RepositorioLancamentosSQL(sessao)


def obter_repo_modelos_documento(sessao: Session = Depends(obter_sessao)) -> RepositorioModelosDocumentoSQL:
    return RepositorioModelosDocumentoSQL(sessao)


def obter_repo_documentos_assinados(sessao: Session = Depends(obter_sessao)) -> RepositorioDocumentosAssinadosSQL:
    return RepositorioDocumentosAssinadosSQL(sessao)


def obter_repo_ocorrencias(sessao: Session = Depends(obter_sessao)) -> RepositorioOcorrenciasSQL:
    return RepositorioOcorrenciasSQL(sessao)


def obter_repo_visitas(sessao: Session = Depends(obter_sessao)) -> RepositorioVisitasSQL:
    return RepositorioVisitasSQL(sessao)


def obter_repo_auditoria(sessao: Session = Depends(obter_sessao)) -> RepositorioAuditoriaSQL:
    return RepositorioAuditoriaSQL(sessao)
