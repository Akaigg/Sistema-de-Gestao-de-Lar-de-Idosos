"""Schemas para os demais módulos (quartos, prontuário, alimentação, escalas, financeiro, etc.)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import Field

from backend.apresentacao.schemas.comuns import ModeloBase


# ------- Quartos -------

class LeitoEntrada(ModeloBase):
    numero: str
    status: str = "livre"


class EntradaQuarto(ModeloBase):
    numero: str
    andar: int = 0
    tipo: str
    capacidade: int = Field(ge=1, le=10)
    leitos: list[str] = []
    possui_banheiro: bool = True
    possui_ar_condicionado: bool = False
    acessibilidade: bool = True
    observacoes: Optional[str] = None


class LeitoSaida(ModeloBase):
    identificador: int
    numero: str
    status: str
    residente_id: Optional[int] = None


class QuartoSaida(ModeloBase):
    identificador: int
    numero: str
    andar: int
    tipo: str
    capacidade: int
    status: str
    leitos: list[LeitoSaida]
    possui_banheiro: bool
    possui_ar_condicionado: bool
    acessibilidade: bool
    observacoes: Optional[str] = None


class EntradaAlocarLeito(ModeloBase):
    residente_id: int


# ------- Prontuário -------

class EntradaSinaisVitais(ModeloBase):
    residente_id: int
    pressao_sistolica: Optional[int] = None
    pressao_diastolica: Optional[int] = None
    frequencia_cardiaca: Optional[int] = None
    frequencia_respiratoria: Optional[int] = None
    temperatura: Optional[float] = None
    saturacao_oxigenio: Optional[int] = None
    glicemia: Optional[int] = None
    peso: Optional[float] = None
    observacoes: Optional[str] = None


class SinaisVitaisSaida(ModeloBase):
    identificador: int
    residente_id: int
    aferido_em: datetime
    funcionario_id: int
    pressao_sistolica: Optional[int] = None
    pressao_diastolica: Optional[int] = None
    frequencia_cardiaca: Optional[int] = None
    frequencia_respiratoria: Optional[int] = None
    temperatura: Optional[float] = None
    saturacao_oxigenio: Optional[int] = None
    glicemia: Optional[int] = None
    peso: Optional[float] = None
    observacoes: Optional[str] = None


class EntradaEvolucao(ModeloBase):
    residente_id: int
    categoria: str = Field(min_length=2, max_length=40)
    texto: str = Field(min_length=3)


class EvolucaoSaida(ModeloBase):
    identificador: int
    residente_id: int
    funcionario_id: int
    registrada_em: datetime
    categoria: str
    texto: str


class EntradaAlergia(ModeloBase):
    residente_id: int
    substancia: str
    reacao: Optional[str] = None
    gravidade: str = "leve"
    observacoes: Optional[str] = None


class AlergiaSaida(ModeloBase):
    identificador: int
    residente_id: int
    substancia: str
    reacao: Optional[str] = None
    gravidade: str
    observacoes: Optional[str] = None


class EntradaCondicaoCronica(ModeloBase):
    residente_id: int
    descricao: str
    cid10: Optional[str] = None
    data_diagnostico: Optional[str] = None
    observacoes: Optional[str] = None


class CondicaoSaida(ModeloBase):
    identificador: int
    residente_id: int
    descricao: str
    cid10: Optional[str] = None
    data_diagnostico: Optional[str] = None


class EntradaConsulta(ModeloBase):
    residente_id: int
    tipo: str
    data_hora: datetime
    profissional: str
    eh_externa: bool = False
    especialidade: Optional[str] = None
    local: Optional[str] = None
    motivo: Optional[str] = None
    observacoes: Optional[str] = None


class ConsultaSaida(ModeloBase):
    identificador: int
    residente_id: int
    tipo: str
    data_hora: datetime
    profissional: str
    eh_externa: bool
    especialidade: Optional[str] = None
    local: Optional[str] = None
    motivo: Optional[str] = None
    observacoes: Optional[str] = None
    status: str


class EntradaCancelarConsulta(ModeloBase):
    motivo: str


# ------- Alimentação -------

class EntradaCardapio(ModeloBase):
    data_referencia: date
    tipo_refeicao: str
    descricao: str
    calorias_aproximadas: Optional[int] = None
    observacoes: Optional[str] = None


class CardapioSaida(ModeloBase):
    identificador: int
    data_referencia: date
    tipo_refeicao: str
    descricao: str
    calorias_aproximadas: Optional[int] = None
    observacoes: Optional[str] = None


class EntradaDieta(ModeloBase):
    residente_id: int
    tipo: str
    descricao_detalhada: Optional[str] = None
    data_inicio: Optional[date] = None
    data_termino: Optional[date] = None


class DietaSaida(ModeloBase):
    identificador: int
    residente_id: int
    tipo: str
    descricao_detalhada: Optional[str] = None
    data_inicio: date
    data_termino: Optional[date] = None
    ativa: bool


class EntradaRefeicaoServida(ModeloBase):
    residente_id: int
    tipo_refeicao: str
    cardapio_id: Optional[int] = None
    aceitacao_percentual: int = Field(ge=0, le=100)
    observacoes: Optional[str] = None


class RefeicaoSaida(ModeloBase):
    identificador: int
    residente_id: int
    tipo_refeicao: str
    servida_em: datetime
    aceitacao_percentual: int
    observacoes: Optional[str] = None


class EntradaIngestaoHidrica(ModeloBase):
    residente_id: int
    quantidade_ml: int = Field(ge=1, le=2000)


class IngestaoSaida(ModeloBase):
    identificador: int
    residente_id: int
    registrada_em: datetime
    quantidade_ml: int


# ------- Escalas -------

class EntradaEscala(ModeloBase):
    referencia_mes: int = Field(ge=1, le=12)
    referencia_ano: int = Field(ge=2020, le=2100)
    setor: str


class EntradaTurno(ModeloBase):
    funcionario_id: int
    inicio: datetime
    fim: datetime
    tipo: str
    observacoes: Optional[str] = None


class TurnoSaida(ModeloBase):
    identificador: int
    funcionario_id: int
    inicio: datetime
    fim: datetime
    tipo: str
    observacoes: Optional[str] = None
    confirmado: bool


class EscalaSaida(ModeloBase):
    identificador: int
    referencia_mes: int
    referencia_ano: int
    setor: str
    publicada: bool
    turnos: list[TurnoSaida]


# ------- Financeiro -------

class EntradaMensalidade(ModeloBase):
    residente_id: int
    competencia_mes: int = Field(ge=1, le=12)
    competencia_ano: int = Field(ge=2020, le=2100)
    valor: float = Field(gt=0)
    data_vencimento: date


class EntradaQuitarMensalidade(ModeloBase):
    valor_pago: float = Field(gt=0)
    forma_pagamento: str
    data_pagamento: Optional[date] = None


class MensalidadeSaida(ModeloBase):
    identificador: int
    residente_id: int
    competencia_mes: int
    competencia_ano: int
    valor: float
    data_vencimento: date
    status: str
    data_pagamento: Optional[date] = None
    valor_pago: Optional[float] = None
    forma_pagamento: Optional[str] = None


class EntradaLancamento(ModeloBase):
    tipo: str = Field(pattern="^(receita|despesa)$")
    descricao: str
    valor: float = Field(gt=0)
    data_competencia: date
    categoria: Optional[str] = None
    centro_custo: Optional[str] = None
    fornecedor: Optional[str] = None
    forma_pagamento: Optional[str] = None


class LancamentoSaida(ModeloBase):
    identificador: int
    tipo: str
    descricao: str
    valor: float
    data_competencia: date
    categoria: Optional[str] = None
    centro_custo: Optional[str] = None
    fornecedor: Optional[str] = None
    forma_pagamento: Optional[str] = None
    status: str


class FluxoCaixaSaida(ModeloBase):
    inicio: date
    fim: date
    total_receitas: float
    total_despesas: float
    saldo: float


# ------- Documentos -------

class EntradaModeloDocumento(ModeloBase):
    titulo: str
    chave: str
    conteudo_template: str
    descricao: Optional[str] = None


class ModeloDocumentoSaida(ModeloBase):
    identificador: int
    titulo: str
    chave: str
    descricao: Optional[str] = None
    ativo: bool


class EntradaGerarDocumento(ModeloBase):
    modelo_id: int
    residente_id: Optional[int] = None
    variaveis: dict = {}
    observacoes: Optional[str] = None


class EntradaAssinarDocumento(ModeloBase):
    nome_assinante: str
    documento_assinante: str
    imagem_assinatura_base64: str


class DocumentoSaida(ModeloBase):
    identificador: int
    modelo_id: int
    titulo: str
    residente_id: Optional[int] = None
    funcionario_id: int
    caminho_arquivo: str
    hash_sha256: str
    gerado_em: datetime
    assinado_em: Optional[datetime] = None
    nome_assinante: Optional[str] = None


# ------- Ocorrências / Visitas -------

class EntradaOcorrencia(ModeloBase):
    residente_id: int
    tipo: str
    gravidade: str
    descricao: str
    local: Optional[str] = None
    medidas_adotadas: Optional[str] = None
    necessitou_hospital: bool = False


class OcorrenciaSaida(ModeloBase):
    identificador: int
    residente_id: int
    tipo: str
    gravidade: str
    descricao: str
    ocorreu_em: datetime
    local: Optional[str] = None
    medidas_adotadas: Optional[str] = None
    necessitou_hospital: bool
    encerrada: bool


class EntradaVisita(ModeloBase):
    residente_id: int
    nome_visitante: str
    documento_visitante: str
    parentesco_ou_relacao: str
    observacoes: Optional[str] = None


class VisitaSaida(ModeloBase):
    identificador: int
    residente_id: int
    nome_visitante: str
    documento_visitante: str
    parentesco_ou_relacao: str
    entrada_em: datetime
    saida_em: Optional[datetime] = None


# ------- Dashboard / Auditoria -------

class IndicadoresSaida(ModeloBase):
    total_residentes_ativos: int
    total_leitos: int
    leitos_ocupados: int
    taxa_ocupacao_percentual: float
    aplicacoes_medicamento_hoje: int
    consultas_hoje: int
    total_aniversariantes_mes: int


class LogAuditoriaSaida(ModeloBase):
    identificador: int
    ocorrido_em: datetime
    funcionario_id: Optional[int] = None
    acao: str
    recurso: str
    recurso_id: Optional[int] = None
    detalhes: Optional[str] = None
    endereco_ip: Optional[str] = None
