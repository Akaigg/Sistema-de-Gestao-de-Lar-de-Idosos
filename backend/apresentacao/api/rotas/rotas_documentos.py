"""Rotas de documentos: modelos, geração e assinatura digital."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from backend.aplicacao.casos_de_uso.documentos import (
    AssinarDocumento,
    CriarModeloDocumento,
    GerarDocumentoAPartirDeModelo,
)
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_gerador_pdf,
    obter_repo_auditoria,
    obter_repo_documentos_assinados,
    obter_repo_modelos_documento,
    obter_repo_residentes,
    obter_servico_hash,
)
from backend.apresentacao.schemas.diversos import (
    DocumentoSaida,
    EntradaAssinarDocumento,
    EntradaGerarDocumento,
    EntradaModeloDocumento,
    ModeloDocumentoSaida,
)

roteador = APIRouter(prefix="/api/documentos", tags=["Documentos"])


@roteador.post("/modelos", response_model=ModeloDocumentoSaida)
def criar_modelo(
    dados: EntradaModeloDocumento,
    repo_modelos=Depends(obter_repo_modelos_documento),
    _funcionario=Depends(obter_funcionario_logado),
):
    modelo = CriarModeloDocumento(repo_modelos).executar(
        titulo=dados.titulo,
        chave=dados.chave,
        conteudo_template=dados.conteudo_template,
        descricao=dados.descricao,
    )
    return ModeloDocumentoSaida(
        identificador=modelo.identificador,
        titulo=modelo.titulo,
        chave=modelo.chave,
        descricao=modelo.descricao,
        ativo=modelo.ativo,
    )


@roteador.get("/modelos", response_model=list[ModeloDocumentoSaida])
def listar_modelos(
    repo_modelos=Depends(obter_repo_modelos_documento),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [
        ModeloDocumentoSaida(
            identificador=m.identificador,
            titulo=m.titulo,
            chave=m.chave,
            descricao=m.descricao,
            ativo=m.ativo,
        )
        for m in repo_modelos.listar()
    ]


def _doc_para_saida(d) -> DocumentoSaida:
    return DocumentoSaida(
        identificador=d.identificador,
        modelo_id=d.modelo_id,
        titulo=d.titulo,
        residente_id=d.residente_id,
        funcionario_id=d.funcionario_id,
        caminho_arquivo=d.caminho_arquivo,
        hash_sha256=d.hash_sha256,
        gerado_em=d.gerado_em,
        assinado_em=d.assinado_em,
        nome_assinante=d.nome_assinante,
    )


@roteador.post("/gerar", response_model=DocumentoSaida)
def gerar(
    dados: EntradaGerarDocumento,
    funcionario=Depends(obter_funcionario_logado),
    repo_modelos=Depends(obter_repo_modelos_documento),
    repo_documentos=Depends(obter_repo_documentos_assinados),
    repo_residentes=Depends(obter_repo_residentes),
    repo_auditoria=Depends(obter_repo_auditoria),
    gerador_pdf=Depends(obter_gerador_pdf),
    servico_hash=Depends(obter_servico_hash),
):
    caso = GerarDocumentoAPartirDeModelo(
        repo_modelos,
        repo_documentos,
        repo_residentes,
        repo_auditoria,
        gerador_pdf,
        servico_hash,
    )
    documento = caso.executar(
        modelo_id=dados.modelo_id,
        funcionario_id=funcionario.identificador,
        residente_id=dados.residente_id,
        variaveis=dados.variaveis,
        observacoes=dados.observacoes,
    )
    return _doc_para_saida(documento)


@roteador.post("/{documento_id}/assinar", response_model=DocumentoSaida)
def assinar(
    documento_id: int,
    dados: EntradaAssinarDocumento,
    funcionario=Depends(obter_funcionario_logado),
    repo_modelos=Depends(obter_repo_modelos_documento),
    repo_documentos=Depends(obter_repo_documentos_assinados),
    repo_residentes=Depends(obter_repo_residentes),
    repo_auditoria=Depends(obter_repo_auditoria),
    gerador_pdf=Depends(obter_gerador_pdf),
    servico_hash=Depends(obter_servico_hash),
):
    caso = AssinarDocumento(
        repo_documentos,
        repo_modelos,
        repo_residentes,
        repo_auditoria,
        gerador_pdf,
        servico_hash,
    )
    documento = caso.executar(
        documento_id=documento_id,
        funcionario_id=funcionario.identificador,
        nome_assinante=dados.nome_assinante,
        documento_assinante=dados.documento_assinante,
        imagem_assinatura_base64=dados.imagem_assinatura_base64,
    )
    return _doc_para_saida(documento)


@roteador.get("", response_model=list[DocumentoSaida])
def listar(
    repo_documentos=Depends(obter_repo_documentos_assinados),
    _funcionario=Depends(obter_funcionario_logado),
):
    return [_doc_para_saida(d) for d in repo_documentos.listar()]


@roteador.get("/{documento_id}/baixar")
def baixar(
    documento_id: int,
    repo_documentos=Depends(obter_repo_documentos_assinados),
    _funcionario=Depends(obter_funcionario_logado),
):
    documento = repo_documentos.buscar_por_id(documento_id)
    if not documento or not Path(documento.caminho_arquivo).exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Arquivo não encontrado.")
    return FileResponse(
        documento.caminho_arquivo,
        media_type="application/pdf",
        filename=Path(documento.caminho_arquivo).name,
    )
