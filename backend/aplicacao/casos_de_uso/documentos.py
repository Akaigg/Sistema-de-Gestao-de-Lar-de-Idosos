"""Casos de uso para geração e assinatura digital de documentos."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from backend.dominio.entidades.auditoria import LogAuditoria
from backend.dominio.entidades.documento import DocumentoAssinado, ModeloDocumento
from backend.dominio.excecoes import EntidadeNaoEncontrada, RegraDeNegocioViolada
from backend.dominio.repositorios.repositorio_auditoria import RepositorioAuditoria
from backend.dominio.repositorios.repositorio_documentos import (
    RepositorioDocumentosAssinados,
    RepositorioModelosDocumento,
)
from backend.dominio.repositorios.repositorio_residentes import RepositorioResidentes
from backend.dominio.servicos.servico_hash_documento import ServicoHashDocumento
from backend.infraestrutura.servicos_externos.gerador_pdf import GeradorPDF


_PADRAO_PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")


def aplicar_placeholders(template: str, variaveis: dict) -> str:
    def _substituir(correspondencia: re.Match) -> str:
        chave = correspondencia.group(1)
        return str(variaveis.get(chave, f"[{chave} não informado]"))

    return _PADRAO_PLACEHOLDER.sub(_substituir, template)


class GerarDocumentoAPartirDeModelo:
    """Gera um PDF baseado em um modelo e em variáveis fornecidas."""

    def __init__(
        self,
        repositorio_modelos: RepositorioModelosDocumento,
        repositorio_documentos: RepositorioDocumentosAssinados,
        repositorio_residentes: RepositorioResidentes,
        repositorio_auditoria: RepositorioAuditoria,
        gerador_pdf: GeradorPDF,
        servico_hash: ServicoHashDocumento,
    ) -> None:
        self._modelos = repositorio_modelos
        self._documentos = repositorio_documentos
        self._residentes = repositorio_residentes
        self._auditoria = repositorio_auditoria
        self._gerador = gerador_pdf
        self._hash = servico_hash

    def executar(
        self,
        modelo_id: int,
        funcionario_id: int,
        residente_id: Optional[int] = None,
        variaveis: Optional[dict] = None,
        observacoes: Optional[str] = None,
    ) -> DocumentoAssinado:
        modelo = self._modelos.buscar_por_id(modelo_id)
        if not modelo:
            raise EntidadeNaoEncontrada("Modelo de documento não encontrado.")
        if not modelo.ativo:
            raise RegraDeNegocioViolada("Modelo desativado.")

        variaveis = dict(variaveis or {})
        if residente_id is not None:
            residente = self._residentes.buscar_por_id(residente_id)
            if residente:
                variaveis.setdefault("residente_nome", residente.nome_completo)
                variaveis.setdefault("residente_cpf", residente.cpf)
        variaveis.setdefault("data_atual", datetime.now().strftime("%d/%m/%Y"))

        conteudo = aplicar_placeholders(modelo.conteudo_template, variaveis)
        nome_arquivo = (
            f"{modelo.chave}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{funcionario_id}.pdf"
        )
        caminho = self._gerador.gerar_documento(
            titulo=modelo.titulo,
            conteudo_texto=conteudo,
            nome_arquivo=nome_arquivo,
        )
        hash_calculado = self._hash.calcular_hash_de_arquivo(str(caminho))

        documento = DocumentoAssinado(
            modelo_id=modelo_id,
            titulo=modelo.titulo,
            residente_id=residente_id,
            funcionario_id=funcionario_id,
            caminho_arquivo=str(caminho),
            hash_sha256=hash_calculado,
            gerado_em=datetime.utcnow(),
            observacoes=observacoes,
        )
        criado = self._documentos.criar(documento)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="CRIAR",
                recurso="documento",
                recurso_id=criado.identificador,
                detalhes=f"Documento {modelo.chave}",
            )
        )
        return criado


class AssinarDocumento:
    """Anexa imagem de assinatura ao documento, regenera PDF e atualiza hash."""

    def __init__(
        self,
        repositorio_documentos: RepositorioDocumentosAssinados,
        repositorio_modelos: RepositorioModelosDocumento,
        repositorio_residentes: RepositorioResidentes,
        repositorio_auditoria: RepositorioAuditoria,
        gerador_pdf: GeradorPDF,
        servico_hash: ServicoHashDocumento,
    ) -> None:
        self._documentos = repositorio_documentos
        self._modelos = repositorio_modelos
        self._residentes = repositorio_residentes
        self._auditoria = repositorio_auditoria
        self._gerador = gerador_pdf
        self._hash = servico_hash

    def executar(
        self,
        documento_id: int,
        funcionario_id: int,
        nome_assinante: str,
        documento_assinante: str,
        imagem_assinatura_base64: str,
    ) -> DocumentoAssinado:
        documento = self._documentos.buscar_por_id(documento_id)
        if not documento:
            raise EntidadeNaoEncontrada("Documento não encontrado.")
        if documento.esta_assinado():
            raise RegraDeNegocioViolada("Documento já está assinado.")

        modelo = self._modelos.buscar_por_id(documento.modelo_id)
        if not modelo:
            raise EntidadeNaoEncontrada("Modelo associado não encontrado.")

        variaveis = {
            "data_atual": datetime.now().strftime("%d/%m/%Y"),
            "nome_assinante": nome_assinante,
            "documento_assinante": documento_assinante,
        }
        if documento.residente_id is not None:
            residente = self._residentes.buscar_por_id(documento.residente_id)
            if residente:
                variaveis["residente_nome"] = residente.nome_completo
                variaveis["residente_cpf"] = residente.cpf

        conteudo = aplicar_placeholders(modelo.conteudo_template, variaveis)
        novo_arquivo = Path(documento.caminho_arquivo).name.replace(
            ".pdf", "_assinado.pdf"
        )
        caminho = self._gerador.gerar_documento(
            titulo=modelo.titulo,
            conteudo_texto=conteudo,
            nome_arquivo=novo_arquivo,
            assinatura_base64=imagem_assinatura_base64,
            nome_assinante=nome_assinante,
            documento_assinante=documento_assinante,
        )
        novo_hash = self._hash.calcular_hash_de_arquivo(str(caminho))

        documento.caminho_arquivo = str(caminho)
        documento.hash_sha256 = novo_hash
        documento.assinado_em = datetime.utcnow()
        documento.nome_assinante = nome_assinante
        documento.documento_assinante = documento_assinante
        documento.imagem_assinatura_base64 = imagem_assinatura_base64
        atualizado = self._documentos.atualizar(documento)
        self._auditoria.registrar(
            LogAuditoria(
                ocorrido_em=datetime.utcnow(),
                funcionario_id=funcionario_id,
                acao="ASSINAR",
                recurso="documento",
                recurso_id=documento_id,
                detalhes=f"Assinado por {nome_assinante}",
            )
        )
        return atualizado


class CriarModeloDocumento:
    def __init__(self, repositorio: RepositorioModelosDocumento) -> None:
        self._repo = repositorio

    def executar(
        self,
        titulo: str,
        chave: str,
        conteudo_template: str,
        descricao: Optional[str] = None,
    ) -> ModeloDocumento:
        modelo = ModeloDocumento(
            titulo=titulo,
            chave=chave,
            conteudo_template=conteudo_template,
            descricao=descricao,
        )
        return self._repo.criar(modelo)
