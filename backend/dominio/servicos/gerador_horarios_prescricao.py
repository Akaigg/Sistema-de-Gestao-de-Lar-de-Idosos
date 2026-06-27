"""Serviço de domínio puro: gera aplicações esperadas a partir de uma prescrição."""

from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

from backend.dominio.entidades.medicamento import (
    AplicacaoMedicamento,
    Prescricao,
    StatusAplicacao,
)


def gerar_aplicacoes_para_dia(
    prescricoes: Iterable[Prescricao], dia: date
) -> list[AplicacaoMedicamento]:
    """Gera as AplicacaoMedicamento esperadas para um dia.

    Apenas para prescrições ativas no dia; horários `SOS` (se_necessario) são
    ignorados, pois dependem de demanda.
    """
    aplicacoes: list[AplicacaoMedicamento] = []
    for prescricao in prescricoes:
        if prescricao.se_necessario or not prescricao.esta_ativa_em(dia):
            continue
        for horario in prescricao.horarios:
            momento = datetime(
                dia.year, dia.month, dia.day, horario.hour, horario.minute
            )
            aplicacoes.append(
                AplicacaoMedicamento(
                    prescricao_id=prescricao.identificador or 0,
                    horario_previsto=momento,
                    status=StatusAplicacao.AGUARDANDO,
                )
            )
    return aplicacoes
