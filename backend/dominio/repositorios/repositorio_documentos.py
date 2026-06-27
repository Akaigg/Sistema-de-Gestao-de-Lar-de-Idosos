"""Porta — Repositórios de Documentos e Modelos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from backend.dominio.entidades.documento import ModeloDocumento, DocumentoAssinado


class RepositorioModelosDocumento(ABC):
    @abstractmethod
    def criar(self, modelo: ModeloDocumento) -> ModeloDocumento: ...

    @abstractmethod
    def atualizar(self, modelo: ModeloDocumento) -> ModeloDocumento: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[ModeloDocumento]: ...

    @abstractmethod
    def buscar_por_chave(self, chave: str) -> Optional[ModeloDocumento]: ...

    @abstractmethod
    def listar(self) -> list[ModeloDocumento]: ...


class RepositorioDocumentosAssinados(ABC):
    @abstractmethod
    def criar(self, documento: DocumentoAssinado) -> DocumentoAssinado: ...

    @abstractmethod
    def atualizar(self, documento: DocumentoAssinado) -> DocumentoAssinado: ...

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> Optional[DocumentoAssinado]: ...

    @abstractmethod
    def listar_por_residente(self, residente_id: int) -> list[DocumentoAssinado]: ...

    @abstractmethod
    def listar(self) -> list[DocumentoAssinado]: ...
