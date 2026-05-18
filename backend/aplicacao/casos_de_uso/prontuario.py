"""Casos de uso de prontuário: sinais vitais, evoluções, alergias, consultas."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.prontuario import (
    Alergia,
    CondicaoCronica,
    Consulta,
    Evolucao,
    SinaisVitais,
    StatusConsulta,
    TipoConsulta,
)
from backend.dominio.excecoes import EntidadeNaoEncontrada, RegraDeNegocioViolada
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_prontuario import (
    RepositorioAlergias,
    RepositorioCondicoesCronicas,
    RepositorioConsultas,
    RepositorioEvolucoes,
    RepositorioSinaisVitais,
)


class RegistrarSinaisVitais:
    def __init__(
        self,
        repositorio: RepositorioSinaisVitais,
        auditoria: RepositorioAuditoria,
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        residente_id: int,
        funcionario_id: int,
        pressao_sistolica: Optional[int] = None,
        pressao_diastolica: Optional[int] = None,
        frequencia_cardiaca: Optional[int] = None,
        frequencia_respiratoria: Optional[int] = None,
        temperatura: Optional[float] = None,
        saturacao_oxigenio: Optional[int] = None,
        glicemia: Optional[int] = None,
        peso: Optional[float] = None,
        observacoes: Optional[str] = None,
        momento: Optional[datetime] = None,
    ) -> SinaisVitais:
        sinais = SinaisVitais(
            residente_id=residente_id,
            aferido_em=momento or datetime.utcnow(),
            funcionario_id=funcionario_id,
            pressao_sistolica=pressao_sistolica,
            pressao_diastolica=pressao_diastolica,
            frequencia_cardiaca=frequencia_cardiaca,
            frequencia_respiratoria=frequencia_respiratoria,
            temperatura=temperatura,
            saturacao_oxigenio=saturacao_oxigenio,
            glicemia=glicemia,
            peso=peso,
            observacoes=observacoes,
        )
        criado = self._repo.criar(sinais)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="CRIAR",
                recurso="sinais_vitais",
                recurso_id=criado.identificador,
            )
        )
        return criado


class RegistrarEvolucao:
    def __init__(
        self, repositorio: RepositorioEvolucoes, auditoria: RepositorioAuditoria
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        residente_id: int,
        funcionario_id: int,
        categoria: str,
        texto: str,
    ) -> Evolucao:
        if not texto.strip():
            raise RegraDeNegocioViolada("O texto da evolução não pode estar vazio.")
        evolucao = Evolucao(
            residente_id=residente_id,
            funcionario_id=funcionario_id,
            registrada_em=datetime.utcnow(),
            categoria=categoria,
            texto=texto.strip(),
        )
        criada = self._repo.criar(evolucao)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="CRIAR",
                recurso="evolucao",
                recurso_id=criada.identificador,
            )
        )
        return criada


class CadastrarAlergia:
    def __init__(self, repositorio: RepositorioAlergias) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        substancia: str,
        reacao: Optional[str] = None,
        gravidade: str = "leve",
        observacoes: Optional[str] = None,
    ) -> Alergia:
        alergia = Alergia(
            residente_id=residente_id,
            substancia=substancia,
            reacao=reacao,
            gravidade=gravidade,
            observacoes=observacoes,
        )
        return self._repo.criar(alergia)


class CadastrarCondicaoCronica:
    def __init__(self, repositorio: RepositorioCondicoesCronicas) -> None:
        self._repo = repositorio

    def executar(
        self,
        residente_id: int,
        descricao: str,
        cid10: Optional[str] = None,
        data_diagnostico: Optional[str] = None,
        observacoes: Optional[str] = None,
    ) -> CondicaoCronica:
        condicao = CondicaoCronica(
            residente_id=residente_id,
            descricao=descricao,
            cid10=cid10,
            data_diagnostico=data_diagnostico,
            observacoes=observacoes,
        )
        return self._repo.criar(condicao)


class AgendarConsulta:
    def __init__(
        self, repositorio: RepositorioConsultas, auditoria: RepositorioAuditoria
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        residente_id: int,
        tipo: TipoConsulta,
        data_hora: datetime,
        profissional: str,
        eh_externa: bool = False,
        especialidade: Optional[str] = None,
        local: Optional[str] = None,
        motivo: Optional[str] = None,
        observacoes: Optional[str] = None,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Consulta:
        if data_hora < datetime.utcnow() - timedelta(minutes=5):
            raise RegraDeNegocioViolada("Não é possível agendar para datas passadas.")
        consulta = Consulta(
            residente_id=residente_id,
            tipo=tipo,
            data_hora=data_hora,
            eh_externa=eh_externa,
            profissional=profissional,
            especialidade=especialidade,
            local=local,
            motivo=motivo,
            observacoes=observacoes,
        )
        criada = self._repo.criar(consulta)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="CRIAR",
                recurso="consulta",
                recurso_id=criada.identificador,
            )
        )
        return criada


class CancelarConsulta:
    def __init__(
        self, repositorio: RepositorioConsultas, auditoria: RepositorioAuditoria
    ) -> None:
        self._repo = repositorio
        self._auditoria = auditoria

    def executar(
        self,
        consulta_id: int,
        motivo: str,
        funcionario_responsavel_id: Optional[int] = None,
    ) -> Consulta:
        consulta = self._repo.buscar_por_id(consulta_id)
        if not consulta:
            raise EntidadeNaoEncontrada("Consulta não encontrada.")
        consulta.cancelar(motivo)
        atualizada = self._repo.atualizar(consulta)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_responsavel_id,
                acao="EDITAR",
                recurso="consulta",
                recurso_id=consulta_id,
                detalhes=f"Cancelada: {motivo}",
            )
        )
        return atualizada
