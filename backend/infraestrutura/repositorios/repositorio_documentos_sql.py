"""Implementação SQLAlchemy dos repositórios de documentos."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from backend.dominio.entidades.documento import ModeloDocumento, DocumentoAssinado
from backend.dominio.repositorios.repositorio_documentos import (
    RepositorioModelosDocumento,
    RepositorioDocumentosAssinados,
)
from backend.infraestrutura.banco_de_dados.modelos import (
    ModeloDocumentoModel,
    DocumentoAssinadoModel,
)
from backend.infraestrutura.repositorios._conversores import (
    modelo_doc_para_entidade,
    modelo_doc_para_modelo,
    doc_assinado_para_entidade,
    doc_assinado_para_modelo,
)


class RepositorioModelosDocumentoSQL(RepositorioModelosDocumento):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, modelo: ModeloDocumento) -> ModeloDocumento:
        m = modelo_doc_para_modelo(modelo)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return modelo_doc_para_entidade(m)

    def atualizar(self, modelo: ModeloDocumento) -> ModeloDocumento:
        m = self._sessao.get(ModeloDocumentoModel, modelo.identificador)
        if not m:
            raise ValueError("Modelo de documento não encontrado.")
        modelo_doc_para_modelo(modelo, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return modelo_doc_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[ModeloDocumento]:
        m = self._sessao.get(ModeloDocumentoModel, identificador)
        return modelo_doc_para_entidade(m) if m else None

    def buscar_por_chave(self, chave: str) -> Optional[ModeloDocumento]:
        m = (
            self._sessao.query(ModeloDocumentoModel)
            .filter(ModeloDocumentoModel.chave == chave)
            .one_or_none()
        )
        return modelo_doc_para_entidade(m) if m else None

    def listar(self) -> list[ModeloDocumento]:
        modelos = (
            self._sessao.query(ModeloDocumentoModel)
            .order_by(ModeloDocumentoModel.titulo)
            .all()
        )
        return [modelo_doc_para_entidade(m) for m in modelos]


class RepositorioDocumentosAssinadosSQL(RepositorioDocumentosAssinados):
    def __init__(self, sessao: Session) -> None:
        self._sessao = sessao

    def criar(self, documento: DocumentoAssinado) -> DocumentoAssinado:
        m = doc_assinado_para_modelo(documento)
        self._sessao.add(m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return doc_assinado_para_entidade(m)

    def atualizar(self, documento: DocumentoAssinado) -> DocumentoAssinado:
        m = self._sessao.get(DocumentoAssinadoModel, documento.identificador)
        if not m:
            raise ValueError("Documento não encontrado.")
        doc_assinado_para_modelo(documento, m)
        self._sessao.commit()
        self._sessao.refresh(m)
        return doc_assinado_para_entidade(m)

    def buscar_por_id(self, identificador: int) -> Optional[DocumentoAssinado]:
        m = self._sessao.get(DocumentoAssinadoModel, identificador)
        return doc_assinado_para_entidade(m) if m else None

    def listar_por_residente(self, residente_id: int) -> list[DocumentoAssinado]:
        modelos = (
            self._sessao.query(DocumentoAssinadoModel)
            .filter(DocumentoAssinadoModel.residente_id == residente_id)
            .order_by(DocumentoAssinadoModel.gerado_em.desc())
            .all()
        )
        return [doc_assinado_para_entidade(m) for m in modelos]

    def listar(self) -> list[DocumentoAssinado]:
        modelos = (
            self._sessao.query(DocumentoAssinadoModel)
            .order_by(DocumentoAssinadoModel.gerado_em.desc())
            .all()
        )
        return [doc_assinado_para_entidade(m) for m in modelos]
