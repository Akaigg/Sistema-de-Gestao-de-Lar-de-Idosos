"""Modelos ORM SQLAlchemy (tabelas do banco)."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from backend.infraestrutura.banco_de_dados.sessao import Base


# ----------- Funcionários e papéis -----------

class FuncionarioModel(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    senha_hash = Column(String(200), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True, index=True)
    cargo = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)
    data_admissao = Column(Date, nullable=True)
    data_desligamento = Column(Date, nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    deve_trocar_senha = Column(Boolean, default=True, nullable=False)
    ultimo_acesso = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    papeis = relationship("PapelFuncionarioModel", back_populates="funcionario",
                          cascade="all, delete-orphan")


class PapelFuncionarioModel(Base):
    __tablename__ = "funcionarios_papeis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    papel = Column(String(50), nullable=False)

    funcionario = relationship("FuncionarioModel", back_populates="papeis")

    __table_args__ = (
        UniqueConstraint("funcionario_id", "papel", name="uq_funcionario_papel"),
    )


class TentativaLoginModel(Base):
    __tablename__ = "tentativas_login"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(200), nullable=False, index=True)
    ocorreu_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    sucesso = Column(Boolean, default=False, nullable=False)
    endereco_ip = Column(String(45), nullable=True)


class TokenRevogadoModel(Base):
    __tablename__ = "tokens_revogados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String(64), nullable=False, unique=True, index=True)
    revogado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


# ----------- Residentes e responsáveis -----------

class ResidenteModel(Base):
    __tablename__ = "residentes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(200), nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    cpf = Column(String(11), nullable=False, unique=True, index=True)
    sexo = Column(String(1), nullable=False)
    data_entrada = Column(Date, nullable=False)
    grau_dependencia = Column(String(40), nullable=False, default="independente")
    status = Column(String(20), nullable=False, default="ativo", index=True)
    rg = Column(String(20), nullable=True)
    cartao_sus = Column(String(20), nullable=True)
    convenio = Column(String(100), nullable=True)
    numero_convenio = Column(String(50), nullable=True)
    religiao = Column(String(100), nullable=True)
    estado_civil = Column(String(20), nullable=True)
    naturalidade = Column(String(100), nullable=True)
    profissao_anterior = Column(String(100), nullable=True)
    observacoes = Column(Text, nullable=True)
    foto_caminho = Column(String(255), nullable=True)
    consentimento_imagem = Column(Boolean, default=False, nullable=False)
    data_saida = Column(Date, nullable=True)
    motivo_saida = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ResponsavelModel(Base):
    __tablename__ = "responsaveis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_completo = Column(String(200), nullable=False)
    cpf = Column(String(11), nullable=False, index=True)
    parentesco = Column(String(50), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(200), nullable=True)
    endereco_resumido = Column(String(255), nullable=True)
    eh_responsavel_legal = Column(Boolean, default=False)
    eh_contato_emergencia = Column(Boolean, default=True)
    observacoes = Column(Text, nullable=True)


class ResidenteResponsavelModel(Base):
    __tablename__ = "residentes_responsaveis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False)
    responsavel_id = Column(Integer, ForeignKey("responsaveis.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("residente_id", "responsavel_id", name="uq_res_resp"),
    )


# ----------- Quartos e leitos -----------

class QuartoModel(Base):
    __tablename__ = "quartos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(String(20), nullable=False, unique=True)
    andar = Column(Integer, nullable=False, default=0)
    tipo = Column(String(20), nullable=False)
    capacidade = Column(Integer, nullable=False, default=1)
    status = Column(String(20), nullable=False, default="ativo")
    possui_banheiro = Column(Boolean, default=True)
    possui_ar_condicionado = Column(Boolean, default=False)
    acessibilidade = Column(Boolean, default=True)
    observacoes = Column(Text, nullable=True)

    leitos = relationship("LeitoModel", back_populates="quarto",
                          cascade="all, delete-orphan")


class LeitoModel(Base):
    __tablename__ = "leitos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quarto_id = Column(Integer, ForeignKey("quartos.id"), nullable=False)
    numero = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="livre")
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=True)
    observacoes = Column(Text, nullable=True)

    quarto = relationship("QuartoModel", back_populates="leitos")


class AlocacaoLeitoModel(Base):
    __tablename__ = "alocacoes_leito"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False)
    leito_id = Column(Integer, ForeignKey("leitos.id"), nullable=False)
    data_inicio = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    motivo = Column(String(255), nullable=True)


# ----------- Medicação -----------

class MedicamentoModel(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_comercial = Column(String(150), nullable=False, index=True)
    principio_ativo = Column(String(150), nullable=False, index=True)
    forma_farmaceutica = Column(String(50), nullable=False)
    concentracao = Column(String(50), nullable=False)
    fabricante = Column(String(100), nullable=True)
    necessita_receita = Column(Boolean, default=True)
    controlado = Column(Boolean, default=False)
    estoque_minimo = Column(Integer, default=10)
    observacoes = Column(Text, nullable=True)


class LoteMedicamentoModel(Base):
    __tablename__ = "lotes_medicamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)
    numero_lote = Column(String(50), nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_validade = Column(Date, nullable=False, index=True)
    data_entrada = Column(Date, default=datetime.utcnow, nullable=False)
    fornecedor = Column(String(150), nullable=True)
    preco_unitario = Column(Float, nullable=True)


class PrescricaoModel(Base):
    __tablename__ = "prescricoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    dose = Column(String(100), nullable=False)
    via = Column(String(30), nullable=False)
    frequencia_horas = Column(Integer, nullable=False)
    horarios_csv = Column(String(255), nullable=False)  # "08:00,14:00,20:00"
    data_inicio = Column(Date, nullable=False)
    duracao_dias = Column(Integer, nullable=True)
    se_necessario = Column(Boolean, default=False)
    suspensa = Column(Boolean, default=False)
    data_suspensao = Column(Date, nullable=True)
    motivo_suspensao = Column(String(255), nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False)


class AplicacaoMedicamentoModel(Base):
    __tablename__ = "aplicacoes_medicamento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prescricao_id = Column(Integer, ForeignKey("prescricoes.id"), nullable=False, index=True)
    horario_previsto = Column(DateTime, nullable=False, index=True)
    horario_aplicado = Column(DateTime, nullable=True)
    status = Column(String(30), nullable=False, default="aguardando", index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    observacoes = Column(Text, nullable=True)
    motivo_recusa = Column(String(255), nullable=True)
    reacao_descrita = Column(Text, nullable=True)


# ----------- Prontuário -----------

class SinaisVitaisModel(Base):
    __tablename__ = "sinais_vitais"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    aferido_em = Column(DateTime, nullable=False, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    pressao_sistolica = Column(Integer, nullable=True)
    pressao_diastolica = Column(Integer, nullable=True)
    frequencia_cardiaca = Column(Integer, nullable=True)
    frequencia_respiratoria = Column(Integer, nullable=True)
    temperatura = Column(Float, nullable=True)
    saturacao_oxigenio = Column(Integer, nullable=True)
    glicemia = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    observacoes = Column(Text, nullable=True)


class EvolucaoModel(Base):
    __tablename__ = "evolucoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    registrada_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    categoria = Column(String(40), nullable=False)
    texto = Column(Text, nullable=False)


class AlergiaModel(Base):
    __tablename__ = "alergias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    substancia = Column(String(150), nullable=False)
    reacao = Column(String(255), nullable=True)
    gravidade = Column(String(20), default="leve")
    observacoes = Column(Text, nullable=True)


class CondicaoCronicaModel(Base):
    __tablename__ = "condicoes_cronicas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    descricao = Column(String(255), nullable=False)
    cid10 = Column(String(10), nullable=True)
    data_diagnostico = Column(String(20), nullable=True)
    observacoes = Column(Text, nullable=True)


class ConsultaModel(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    tipo = Column(String(40), nullable=False)
    data_hora = Column(DateTime, nullable=False, index=True)
    eh_externa = Column(Boolean, default=False)
    profissional = Column(String(150), nullable=False)
    especialidade = Column(String(100), nullable=True)
    local = Column(String(200), nullable=True)
    motivo = Column(String(255), nullable=True)
    observacoes = Column(Text, nullable=True)
    status = Column(String(20), default="agendada", index=True)
    motivo_cancelamento = Column(String(255), nullable=True)
    funcionario_acompanhante_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)


# ----------- Alimentação -----------

class CardapioModel(Base):
    __tablename__ = "cardapios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_referencia = Column(Date, nullable=False, index=True)
    tipo_refeicao = Column(String(30), nullable=False)
    descricao = Column(Text, nullable=False)
    calorias_aproximadas = Column(Integer, nullable=True)
    observacoes = Column(Text, nullable=True)


class DietaModel(Base):
    __tablename__ = "dietas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    tipo = Column(String(30), nullable=False)
    descricao_detalhada = Column(Text, nullable=True)
    prescrita_por_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    data_inicio = Column(Date, nullable=False)
    data_termino = Column(Date, nullable=True)
    ativa = Column(Boolean, default=True, index=True)


class RefeicaoModel(Base):
    __tablename__ = "refeicoes_servidas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    cardapio_id = Column(Integer, ForeignKey("cardapios.id"), nullable=True)
    tipo_refeicao = Column(String(30), nullable=False)
    servida_em = Column(DateTime, nullable=False, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    aceitacao_percentual = Column(Integer, default=100)
    observacoes = Column(Text, nullable=True)


class IngestaoHidricaModel(Base):
    __tablename__ = "ingestao_hidrica"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    registrada_em = Column(DateTime, nullable=False, index=True)
    quantidade_ml = Column(Integer, nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)


# ----------- Escalas -----------

class EscalaModel(Base):
    __tablename__ = "escalas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referencia_mes = Column(Integer, nullable=False)
    referencia_ano = Column(Integer, nullable=False)
    setor = Column(String(100), nullable=False)
    publicada = Column(Boolean, default=False)
    publicada_em = Column(DateTime, nullable=True)
    publicada_por_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)

    turnos = relationship("TurnoModel", back_populates="escala", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("referencia_mes", "referencia_ano", "setor", name="uq_escala_mes_ano_setor"),
    )


class TurnoModel(Base):
    __tablename__ = "turnos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    escala_id = Column(Integer, ForeignKey("escalas.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False, index=True)
    inicio = Column(DateTime, nullable=False, index=True)
    fim = Column(DateTime, nullable=False)
    tipo = Column(String(20), nullable=False)
    observacoes = Column(String(255), nullable=True)
    confirmado = Column(Boolean, default=False)

    escala = relationship("EscalaModel", back_populates="turnos")


# ----------- Financeiro -----------

class MensalidadeModel(Base):
    __tablename__ = "mensalidades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    competencia_mes = Column(Integer, nullable=False)
    competencia_ano = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    data_vencimento = Column(Date, nullable=False, index=True)
    status = Column(String(20), default="em_aberto", index=True)
    data_pagamento = Column(Date, nullable=True)
    valor_pago = Column(Float, nullable=True)
    forma_pagamento = Column(String(30), nullable=True)
    desconto = Column(Float, default=0.0)
    juros_multa = Column(Float, default=0.0)
    observacoes = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("residente_id", "competencia_mes", "competencia_ano",
                         name="uq_mensalidade_residente_competencia"),
    )


class LancamentoFinanceiroModel(Base):
    __tablename__ = "lancamentos_financeiros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(10), nullable=False, index=True)  # receita/despesa
    descricao = Column(String(255), nullable=False)
    valor = Column(Float, nullable=False)
    data_competencia = Column(Date, nullable=False, index=True)
    data_pagamento = Column(Date, nullable=True)
    categoria = Column(String(100), nullable=True)
    centro_custo = Column(String(100), nullable=True)
    fornecedor = Column(String(150), nullable=True)
    forma_pagamento = Column(String(30), nullable=True)
    status = Column(String(20), default="em_aberto")
    registrado_em = Column(DateTime, default=datetime.utcnow)
    registrado_por_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)


# ----------- Documentos -----------

class ModeloDocumentoModel(Base):
    __tablename__ = "modelos_documento"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    chave = Column(String(100), nullable=False, unique=True, index=True)
    conteudo_template = Column(Text, nullable=False)
    descricao = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True)


class DocumentoAssinadoModel(Base):
    __tablename__ = "documentos_assinados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelo_id = Column(Integer, ForeignKey("modelos_documento.id"), nullable=False)
    titulo = Column(String(200), nullable=False)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    caminho_arquivo = Column(String(255), nullable=False)
    hash_sha256 = Column(String(64), nullable=False, index=True)
    gerado_em = Column(DateTime, default=datetime.utcnow, nullable=False)
    assinado_em = Column(DateTime, nullable=True)
    nome_assinante = Column(String(200), nullable=True)
    documento_assinante = Column(String(50), nullable=True)
    imagem_assinatura_base64 = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)


# ----------- Operacional -----------

class OcorrenciaModel(Base):
    __tablename__ = "ocorrencias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    tipo = Column(String(40), nullable=False)
    gravidade = Column(String(20), nullable=False)
    descricao = Column(Text, nullable=False)
    ocorreu_em = Column(DateTime, nullable=False, index=True)
    registrada_por_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    local = Column(String(150), nullable=True)
    medidas_adotadas = Column(Text, nullable=True)
    necessitou_hospital = Column(Boolean, default=False)
    encerrada = Column(Boolean, default=False)
    encerrada_em = Column(DateTime, nullable=True)


class VisitaModel(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    residente_id = Column(Integer, ForeignKey("residentes.id"), nullable=False, index=True)
    nome_visitante = Column(String(200), nullable=False)
    documento_visitante = Column(String(50), nullable=False)
    parentesco_ou_relacao = Column(String(50), nullable=False)
    entrada_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    saida_em = Column(DateTime, nullable=True)
    funcionario_recebeu_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True)
    observacoes = Column(Text, nullable=True)


class LogAuditoriaModel(Base):
    __tablename__ = "log_auditoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ocorrido_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=True, index=True)
    acao = Column(String(40), nullable=False, index=True)
    recurso = Column(String(50), nullable=False, index=True)
    recurso_id = Column(Integer, nullable=True)
    detalhes = Column(Text, nullable=True)
    endereco_ip = Column(String(45), nullable=True)
    agente_usuario = Column(String(255), nullable=True)


Index("ix_aplicacoes_status_horario", AplicacaoMedicamentoModel.status,
      AplicacaoMedicamentoModel.horario_previsto)
