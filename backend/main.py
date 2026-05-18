"""Ponto de entrada da aplicação FastAPI — Cuidar+."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from backend.apresentacao.api.rotas import (
    rotas_alimentacao,
    rotas_auditoria,
    rotas_autenticacao,
    rotas_dashboard,
    rotas_documentos,
    rotas_escalas,
    rotas_financeiro,
    rotas_funcionarios,
    rotas_medicacao,
    rotas_ocorrencias_visitas,
    rotas_prontuario,
    rotas_quartos,
    rotas_residentes,
)
from backend.apresentacao.middlewares import registrar_tratadores_de_erro
from backend.infraestrutura.banco_de_dados import criar_tabelas
from backend.infraestrutura.configuracao import configuracoes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("cuidarmais")


def criar_aplicacao() -> FastAPI:
    """Fábrica do FastAPI."""
    aplicacao = FastAPI(
        title=configuracoes.nome_aplicacao,
        version=configuracoes.versao,
        description=(
            "Sistema interno de gestão de Lar de Idosos. "
            "Acesso restrito a funcionários autorizados."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    aplicacao.add_middleware(
        CORSMiddleware,
        allow_origins=list(configuracoes.cors_origens),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    registrar_tratadores_de_erro(aplicacao)

    # API
    aplicacao.include_router(rotas_autenticacao.roteador)
    aplicacao.include_router(rotas_funcionarios.roteador)
    aplicacao.include_router(rotas_residentes.roteador)
    aplicacao.include_router(rotas_quartos.roteador)
    aplicacao.include_router(rotas_medicacao.roteador)
    aplicacao.include_router(rotas_prontuario.roteador)
    aplicacao.include_router(rotas_alimentacao.roteador)
    aplicacao.include_router(rotas_escalas.roteador)
    aplicacao.include_router(rotas_financeiro.roteador)
    aplicacao.include_router(rotas_documentos.roteador)
    aplicacao.include_router(rotas_ocorrencias_visitas.roteador)
    aplicacao.include_router(rotas_dashboard.roteador)
    aplicacao.include_router(rotas_auditoria.roteador)

    @aplicacao.get("/saude", tags=["Sistema"])
    def saude():
        return {
            "status": "ok",
            "aplicacao": configuracoes.nome_aplicacao,
            "versao": configuracoes.versao,
        }

    # Frontend estático (registrado por último para não engolir rotas da API)
    diretorio_frontend = configuracoes.diretorio_frontend
    if diretorio_frontend.exists():
        aplicacao.mount(
            "/estatico",
            StaticFiles(directory=str(diretorio_frontend), html=False),
            name="estatico",
        )

        @aplicacao.get("/", include_in_schema=False)
        def raiz():
            indice = diretorio_frontend / "index.html"
            if indice.exists():
                return FileResponse(str(indice))
            return RedirectResponse(url="/api/docs")

        @aplicacao.get("/paginas/{nome_arquivo}", include_in_schema=False)
        def servir_pagina(nome_arquivo: str):
            destino = diretorio_frontend / "paginas" / nome_arquivo
            if destino.exists() and destino.is_file():
                return FileResponse(str(destino))
            return FileResponse(str(diretorio_frontend / "index.html"))

        @aplicacao.get("/{nome_arquivo}", include_in_schema=False)
        def servir_arquivo_raiz(nome_arquivo: str):
            """Serve arquivos da raiz do frontend (login.html, favicon, etc.)."""
            destino = diretorio_frontend / nome_arquivo
            if destino.exists() and destino.is_file():
                return FileResponse(str(destino))
            indice = diretorio_frontend / "index.html"
            if indice.exists():
                return FileResponse(str(indice))
            return RedirectResponse(url="/api/docs")

    @aplicacao.on_event("startup")
    def _inicializar():
        logger.info("Iniciando %s v%s...", configuracoes.nome_aplicacao, configuracoes.versao)
        criar_tabelas()
        logger.info("Banco de dados pronto em %s", configuracoes.arquivo_banco)

    return aplicacao


app = criar_aplicacao()
