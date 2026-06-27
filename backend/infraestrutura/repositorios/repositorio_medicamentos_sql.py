"""Implementação SQLAlchemy de repositórios de medicação."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.dominio.entidades.medicamento import (
    Medicamento,
    Prescricao,
    AplicacaoMedicamento,
    LoteMedicamento,
    StatusAplicacao,
)
from backend.dominio.repositorios.repositorio_medicamentos import (
    RepositorioMedicamentos,
    RepositorioPrescricoes,
    RepositorioAplicacoes,
    RepositorioLotesMedicamento,
)
from backend.infraestrutura.banco_de_dados.modelos import (
    MedicamentoModel,
    PrescricaoModel,
    AplicacaoMedicamentoModel,
    LoteMedicamentoModel,
)
from backend.infraestrutura.repositorios._conversores import (
    medicamento_para_entidade,
    medicamento_para_modelo,
    prescricao_para_entidade,
    prescricao_para_modelo,
    aplicacao_para_entidade,
    aplicacao_para_modelo,
    lote_para_entidade,
    lote_para_modelo,
)


class RepositorioMedicamentosSQL(RepositorioMedicamentos):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, medicamento: Medicamento) -> Medicamento:
        modelo = medicamento_para_modelo(medicamento)
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return medicamento_para_entidade(modelo)

    def atualizar(self, medicamento: Medicamento) -> Medicamento:
        modelo = self._sessao.get(MedicamentoModel, medicamento.identificador)
        if not modelo:
            raise ValueError("Medicamento não encontrado.")
        medicamento_para_modelo(medicamento, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return medicamento_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Medicamento]:
        modelo = self._sessao.get(MedicamentoModel, identificador)
        return medicamento_para_entidade(modelo) if modelo else None

    def listar(self, termo_busca: Optional[str] = None) -> list[Medicamento]:
        query = self._sessao.query(MedicamentoModel)
        if termo_busca:
            curinga = f"%{termo_busca.lower()}%"
            query = query.filter(
                or_(
                    MedicamentoModel.nome_comercial.ilike(curinga),
                    MedicamentoModel.principio_ativo.ilike(curinga),
                )
            )
        query = query.order_by(MedicamentoModel.nome_comercial)
        return [medicamento_para_entidade(m) for m in query.all()]


class RepositorioPrescricoesSQL(RepositorioPrescricoes):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, prescricao: Prescricao) -> Prescricao:
        modelo = prescricao_para_modelo(prescricao)
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return prescricao_para_entidade(modelo)

    def atualizar(self, prescricao: Prescricao) -> Prescricao:
        modelo = self._sessao.get(PrescricaoModel, prescricao.identificador)
        if not modelo:
            raise ValueError("Prescrição não encontrada.")
        prescricao_para_modelo(prescricao, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return prescricao_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[Prescricao]:
        modelo = self._sessao.get(PrescricaoModel, identificador)
        return prescricao_para_entidade(modelo) if modelo else None

    def listar_por_residente(
        self, residente_id: int, apenas_ativas: bool = True
    ) -> list[Prescricao]:
        query = self._sessao.query(PrescricaoModel).filter(
            PrescricaoModel.residente_id == residente_id
        )
        if apenas_ativas:
            query = query.filter(PrescricaoModel.suspensa.is_(False))
        return [prescricao_para_entidade(m) for m in query.order_by(PrescricaoModel.data_inicio.desc()).all()]

    def listar_ativas_no_periodo(self, inicio: date, fim: date) -> list[Prescricao]:
        modelos = (
            self._sessao.query(PrescricaoModel)
            .filter(
                PrescricaoModel.suspensa.is_(False),
                PrescricaoModel.data_inicio <= fim,
            )
            .all()
        )
        # Filtragem fina (duração) feita em memória, pois SQLite não tem date_add nativo
        ativas: list[Prescricao] = []
        for modelo in modelos:
            entidade = prescricao_para_entidade(modelo)
            if entidade.duracao_dias is None:
                ativas.append(entidade)
                continue
            termino = entidade.data_termino()
            if termino is None or termino >= inicio:
                ativas.append(entidade)
        return ativas


class RepositorioAplicacoesSQL(RepositorioAplicacoes):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, aplicacao: AplicacaoMedicamento) -> AplicacaoMedicamento:
        modelo = aplicacao_para_modelo(aplicacao)
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return aplicacao_para_entidade(modelo)

    def atualizar(self, aplicacao: AplicacaoMedicamento) -> AplicacaoMedicamento:
        modelo = self._sessao.get(AplicacaoMedicamentoModel, aplicacao.identificador)
        if not modelo:
            raise ValueError("Aplicação não encontrada.")
        aplicacao_para_modelo(aplicacao, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return aplicacao_para_entidade(modelo)

    def buscar_por_id(self, identificador: int) -> Optional[AplicacaoMedicamento]:
        modelo = self._sessao.get(AplicacaoMedicamentoModel, identificador)
        return aplicacao_para_entidade(modelo) if modelo else None

    def listar_por_periodo(
        self,
        inicio: datetime,
        fim: datetime,
        residente_id: Optional[int] = None,
    ) -> list[AplicacaoMedicamento]:
        query = self._sessao.query(AplicacaoMedicamentoModel).filter(
            AplicacaoMedicamentoModel.horario_previsto >= inicio,
            AplicacaoMedicamentoModel.horario_previsto <= fim,
        )
        if residente_id is not None:
            query = query.join(
                PrescricaoModel,
                PrescricaoModel.id == AplicacaoMedicamentoModel.prescricao_id,
            ).filter(PrescricaoModel.residente_id == residente_id)
        modelos = query.order_by(AplicacaoMedicamentoModel.horario_previsto).all()
        return [aplicacao_para_entidade(m) for m in modelos]

    def listar_em_atraso(self, momento_referencia: datetime) -> list[AplicacaoMedicamento]:
        limite = momento_referencia - timedelta(minutes=AplicacaoMedicamento.LIMITE_ATRASO_MINUTOS)
        modelos = (
            self._sessao.query(AplicacaoMedicamentoModel)
            .filter(
                AplicacaoMedicamentoModel.status == StatusAplicacao.AGUARDANDO.value,
                AplicacaoMedicamentoModel.horario_previsto < limite,
            )
            .all()
        )
        return [aplicacao_para_entidade(m) for m in modelos]

    def contar_do_dia(self, dia: date) -> int:
        inicio = datetime(dia.year, dia.month, dia.day)
        fim = inicio + timedelta(days=1)
        return (
            self._sessao.query(AplicacaoMedicamentoModel)
            .filter(
                AplicacaoMedicamentoModel.horario_previsto >= inicio,
                AplicacaoMedicamentoModel.horario_previsto < fim,
            )
            .count()
        )


class RepositorioLotesMedicamentoSQL(RepositorioLotesMedicamento):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, lote: LoteMedicamento) -> LoteMedicamento:
        modelo = lote_para_modelo(lote)
        self._sessao.add(modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return lote_para_entidade(modelo)

    def atualizar(self, lote: LoteMedicamento) -> LoteMedicamento:
        modelo = self._sessao.get(LoteMedicamentoModel, lote.identificador)
        if not modelo:
            raise ValueError("Lote não encontrado.")
        lote_para_modelo(lote, modelo)
        self._sessao.commit()
        self._sessao.refresh(modelo)
        return lote_para_entidade(modelo)

    def listar_por_medicamento(self, medicamento_id: int) -> list[LoteMedicamento]:
        modelos = (
            self._sessao.query(LoteMedicamentoModel)
            .filter(LoteMedicamentoModel.medicamento_id == medicamento_id)
            .order_by(LoteMedicamentoModel.data_validade)
            .all()
        )
        return [lote_para_entidade(m) for m in modelos]

    def listar_proximos_vencimento(self, dias: int = 30) -> list[LoteMedicamento]:
        limite = date.today() + timedelta(days=dias)
        modelos = (
            self._sessao.query(LoteMedicamentoModel)
            .filter(LoteMedicamentoModel.data_validade <= limite)
            .order_by(LoteMedicamentoModel.data_validade)
            .all()
        )
        return [lote_para_entidade(m) for m in modelos]

    def quantidade_total(self, medicamento_id: int) -> int:
        total = (
            self._sessao.query(LoteMedicamentoModel)
            .filter(LoteMedicamentoModel.medicamento_id == medicamento_id)
            .with_entities(LoteMedicamentoModel.quantidade)
            .all()
        )
        return sum(q[0] for q in total) if total else 0
