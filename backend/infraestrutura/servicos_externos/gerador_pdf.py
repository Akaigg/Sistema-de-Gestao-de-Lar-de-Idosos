"""Gerador de PDF para documentos e relatórios (ReportLab)."""

from __future__ import annotations

import base64
import io
from datetime import datetime
from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)


class GeradorPDF:
    """Gera PDFs de documentos a partir de modelos com placeholders simples."""

    def __init__(self, diretorio_saida: Path) -> None:
        self._diretorio = Path(diretorio_saida)
        self._diretorio.mkdir(parents=True, exist_ok=True)

    def gerar_documento(
        self,
        titulo: str,
        conteudo_texto: str,
        nome_arquivo: str,
        assinatura_base64: Optional[str] = None,
        nome_assinante: Optional[str] = None,
        documento_assinante: Optional[str] = None,
    ) -> Path:
        """Gera um PDF com título, parágrafos e (opcionalmente) bloco de assinatura."""
        caminho = self._diretorio / nome_arquivo
        documento = SimpleDocTemplate(
            str(caminho),
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title=titulo,
        )
        estilos = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(
            "TituloDoc",
            parent=estilos["Heading1"],
            alignment=1,
            fontSize=16,
            spaceAfter=18,
        )
        estilo_corpo = ParagraphStyle(
            "Corpo",
            parent=estilos["Normal"],
            fontSize=11,
            leading=16,
            alignment=4,  # justificado
        )
        elementos = []
        elementos.append(Paragraph(titulo, estilo_titulo))
        elementos.append(Spacer(1, 0.4 * cm))
        for paragrafo in conteudo_texto.split("\n\n"):
            elementos.append(Paragraph(paragrafo.replace("\n", "<br/>"), estilo_corpo))
            elementos.append(Spacer(1, 0.3 * cm))

        elementos.append(Spacer(1, 1.5 * cm))
        elementos.append(
            Paragraph(
                f"Local e data: ____________________, {datetime.now().strftime('%d/%m/%Y')}",
                estilo_corpo,
            )
        )
        elementos.append(Spacer(1, 1.5 * cm))

        if assinatura_base64:
            try:
                bytes_imagem = base64.b64decode(
                    assinatura_base64.split(",")[-1]  # remove "data:image/png;base64,"
                )
                buffer = io.BytesIO(bytes_imagem)
                imagem = Image(buffer, width=6 * cm, height=2.5 * cm)
                elementos.append(imagem)
            except Exception:
                pass

        if nome_assinante:
            elementos.append(
                Paragraph("_" * 60, estilo_corpo)
            )
            elementos.append(Paragraph(nome_assinante, estilo_corpo))
            if documento_assinante:
                elementos.append(Paragraph(f"Documento: {documento_assinante}", estilo_corpo))

        documento.build(elementos, onFirstPage=self._rodape, onLaterPages=self._rodape)
        return caminho

    @staticmethod
    def _rodape(c: canvas.Canvas, _doc):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawString(
            2 * cm, 1 * cm,
            f"Cuidar+ · Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        )
        c.drawRightString(A4[0] - 2 * cm, 1 * cm, "Página %d" % c.getPageNumber())
        c.restoreState()

    def gerar_relatorio_tabela(
        self,
        titulo: str,
        cabecalhos: list[str],
        linhas: list[list[str]],
        nome_arquivo: str,
    ) -> Path:
        """Gera um PDF tabular simples para relatórios."""
        caminho = self._diretorio / nome_arquivo
        documento = SimpleDocTemplate(str(caminho), pagesize=A4, title=titulo)
        elementos = []
        estilos = getSampleStyleSheet()
        elementos.append(Paragraph(titulo, estilos["Heading1"]))
        elementos.append(Spacer(1, 0.5 * cm))
        tabela = Table([cabecalhos, *linhas])
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.whitesmoke, colors.white]),
                ]
            )
        )
        elementos.append(tabela)
        documento.build(elementos, onFirstPage=self._rodape, onLaterPages=self._rodape)
        return caminho
