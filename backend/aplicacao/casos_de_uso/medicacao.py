"""Casos de uso de medicação: cadastro, prescrição, aplicação."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.medicamento import (
    AplicacaoMedicamento,
    Medicamento,
    Prescricao,
    StatusAplicacao,
    ViaAdministracao,
    LoteMedicamento,
)
from backend.dominio.excecoes import (
    EntidadeNaoEncontrada,
    RegraDeNegocioViolada,
)
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_medicamentos import (
    RepositorioAplicacoes,
    RepositorioLotesMedicamento,
    RepositorioMedicamentos,
    RepositorioPrescricoes,
)
from backend.dominio.servicos.gerador_horarios_prescricao import (
    gerar_aplicacoes_para_dia,
)


@dataclass
class DadosCadastroMedicamento:
    nome_comercial: str
    principio_ativo: str
    forma_farmaceutica: str
    concentracao: str
    fabricante: Optional[str] = None
    necessita_receita: bool = True
    controlado: bool = False
    estoque_minimo: int = 10
    observacoes: Optional[str] = None


class CadastrarMedicamento:
    def __init__(
        self,
        repositorio: RepositorioMedicamentos,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        dados: DadosCadastroMedicamento,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Medicamento:
        medicamento = Medicamento(
            nome_comercial=dados.nome_comercial.strip(),
            principio_ativo=dados.principio_ativo.strip(),
            forma_farmaceutica=dados.forma_farmaceutica,
            concentracao=dados.concentracao,
            fabricante=dados.fabricante,
            necessita_receita=dados.necessita_receita,
            controlado=dados.controlado,
            estoque_minimo=dados.estoque_minimo,
            observacoes=dados.observacoes,
        )
        criado = self._repo.criar(medicamento)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="medicamento",
                recurso_id=criado.identificador,
            )
        )
        return criado


@dataclass
class DadosCadastroPrescricao:
    residente_id: int
    medicamento_id: int
    medico_id: int
    dose: str
    via: ViaAdministracao
    frequencia_horas: int
    horarios: list[time]
    data_inicio: date
    duracao_dias: Optional[int] = None
    se_necessario: bool = False
    observacoes: Optional[str] = None


class CadastrarPrescricaoEGerarAplicacoes:
    """Cria uma prescrição e já gera as aplicações para o período."""

    def __init__(
        self,
        repositorio_prescricoes: RepositorioPrescricoes,
        repositorio_aplicacoes: RepositorioAplicacoes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._prescricoes = repositorio_prescricoes
        self._aplicacoes = repositorio_aplicacoes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        dados: DadosCadastroPrescricao,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Prescricao:
        prescricao = Prescricao(
            residente_id=dados.residente_id,
            medicamento_id=dados.medicamento_id,
            medico_id=dados.medico_id,
            dose=dados.dose,
            via=dados.via,
            frequencia_horas=dados.frequencia_horas,
            horarios=dados.horarios,
            data_inicio=dados.data_inicio,
            duracao_dias=dados.duracao_dias,
            se_necessario=dados.se_necessario,
            observacoes=dados.observacoes,
        )
        criada = self._prescricoes.criar(prescricao)
        if not criada.se_necessario:
            duracao = criada.duracao_dias or 30
            for delta in range(duracao):
                dia = criada.data_inicio + timedelta(days=delta)
                for aplicacao in gerar_aplicacoes_para_dia([criada], dia):
                    self._aplicacoes.criar(aplicacao)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="prescricao",
                recurso_id=criada.identificador,
            )
        )
        return criada


class SuspenderPrescricao:
    def __init__(
        self,
        repositorio_prescricoes: RepositorioPrescricoes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_prescricoes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        prescricao_id: int,
        motivo: str,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Prescricao:
        prescricao = self._repo.buscar_por_id(prescricao_id)
        if not prescricao:
            raise EntidadeNaoEncontrada("Prescrição não encontrada.")
        prescricao.suspender(motivo)
        atualizada = self._repo.atualizar(prescricao)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="prescricao",
                recurso_id=prescricao_id,
                detalhes=f"Suspensa: {motivo}",
            )
        )
        return atualizada


class AplicarMedicamento:
    """Marca aplicação como aplicada/recusada/reação adversa."""

    def __init__(
        self,
        repositorio_aplicacoes: RepositorioAplicacoes,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_aplicacoes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        aplicacao_id: int,
        funcionario_id: int,
        acao: str,
        observacoes: Optional[str] = None,
        motivo_recusa: Optional[str] = None,
        descricao_reacao: Optional[str] = None,
    ) -> AplicacaoMedicamento:
        aplicacao = self._repo.buscar_por_id(aplicacao_id)
        if not aplicacao:
            raise EntidadeNaoEncontrada("Aplicação não encontrada.")
        if acao == "aplicar":
            aplicacao.aplicar(funcionario_id, observacoes=observacoes)
        elif acao == "recusar":
            if not motivo_recusa:
                raise RegraDeNegocioViolada("Informe o motivo da recusa.")
            aplicacao.recusar(funcionario_id, motivo_recusa)
        elif acao == "reacao":
            if not descricao_reacao:
                raise RegraDeNegocioViolada("Descreva a reação observada.")
            aplicacao.registrar_reacao(funcionario_id, descricao_reacao)
        else:
            raise RegraDeNegocioViolada(f"Ação desconhecida: {acao}")

        atualizada = self._repo.atualizar(aplicacao)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="APLICAR_MEDICAMENTO",
                recurso="aplicacao_medicamento",
                recurso_id=aplicacao_id,
                detalhes=f"Ação: {acao}",
            )
        )
        return atualizada


class ListarAplicacoesParaCalendario:
    """Retorna aplicações de um período para alimentar o calendário do frontend."""

    def __init__(self, repositorio_aplicacoes: RepositorioAplicacoes) -> None:
        self._repo = repositorio_aplicacoes

    def executar(
        self,
        inicio: datetime,
        fim: datetime,
        residente_id: Optional[int] = None,
    ) -> list[AplicacaoMedicamento]:
        return self._repo.listar_por_periodo(inicio, fim, residente_id)


class MarcarAplicacoesAtrasadas:
    """Atualiza para EM_ATRASO toda aplicação aguardando passada há mais que o limite."""

    def __init__(self, repositorio_aplicacoes: RepositorioAplicacoes) -> None:
        self._repo = repositorio_aplicacoes

    def executar(self, momento_referencia: Optional[datetime] = None) -> int:
        agora = momento_referencia or datetime.utcnow()
        atrasadas = self._repo.listar_em_atraso(agora)
        for aplicacao in atrasadas:
            aplicacao.status = StatusAplicacao.EM_ATRASO
            self._repo.atualizar(aplicacao)
        return len(atrasadas)


class RegistrarLoteMedicamento:
    def __init__(
        self,
        repositorio_lotes: RepositorioLotesMedicamento,
        repositorio_auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio_lotes
        self._auditoria = repositorio_auditoria

    def executar(
        self,
        medicamento_id: int,
        numero_lote: str,
        quantidade: int,
        data_validade: date,
        fornecedor: Optional[str] = None,
        preco_unitario: Optional[float] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> LoteMedicamento:
        lote = LoteMedicamento(
            medicamento_id=medicamento_id,
            numero_lote=numero_lote,
            quantidade=quantidade,
            data_validade=data_validade,
            data_entrada=date.today(),
            fornecedor=fornecedor,
            preco_unitario=preco_unitario,
        )
        criado = self._repo.criar(lote)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="lote_medicamento",
                recurso_id=criado.identificador,
            )
        )
        return criado
