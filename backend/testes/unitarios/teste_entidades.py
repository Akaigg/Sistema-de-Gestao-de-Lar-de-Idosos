"""Testes unitários das principais entidades."""

from datetime import date, datetime, time, timedelta

import pytest

from backend.dominio.entidades.escala import Escala, TipoTurno, Turno
from backend.dominio.entidades.financeiro import (
    FormaPagamento,
    Mensalidade,
    StatusPagamento,
)
from backend.dominio.entidades.medicamento import (
    AplicacaoMedicamento,
    Prescricao,
    StatusAplicacao,
    ViaAdministracao,
)
from backend.dominio.entidades.quarto import Leito, StatusLeito
from backend.dominio.entidades.residente import (
    GrauDependencia,
    Residente,
    StatusResidente,
)
from backend.dominio.excecoes import RegraDeNegocioViolada


class TesteResidente:
    def teste_calcular_idade(self):
        r = Residente(
            nome_completo="Maria",
            data_nascimento=date(1942, 9, 15),
            cpf="11144477735",
            sexo="F",
            data_entrada=date(2026, 1, 1),
        )
        assert r.calcular_idade(hoje=date(2026, 5, 1)) == 83
        assert r.calcular_idade(hoje=date(2026, 9, 16)) == 84

    def teste_desligar(self):
        r = Residente(
            nome_completo="José",
            data_nascimento=date(1940, 1, 1),
            cpf="11144477735",
            sexo="M",
            data_entrada=date(2026, 1, 1),
        )
        r.desligar("Mudança de cidade", quando=date(2026, 6, 1))
        assert r.status == StatusResidente.DESLIGADO
        assert r.motivo_saida == "Mudança de cidade"


class TesteLeito:
    def teste_ocupar_livre(self):
        leito = Leito(numero="A")
        leito.ocupar(42)
        assert leito.status == StatusLeito.OCUPADO
        assert leito.residente_id == 42

    def teste_ocupar_ocupado_falha(self):
        leito = Leito(numero="A", status=StatusLeito.OCUPADO, residente_id=1)
        with pytest.raises(RegraDeNegocioViolada):
            leito.ocupar(2)


class TestePrescricao:
    def _criar(self, **kw):
        defaults = dict(
            residente_id=1,
            medicamento_id=1,
            medico_id=1,
            dose="1 cp",
            via=ViaAdministracao.ORAL,
            frequencia_horas=8,
            horarios=[time(8), time(16), time(0)],
            data_inicio=date(2026, 1, 1),
            duracao_dias=10,
        )
        defaults.update(kw)
        return Prescricao(**defaults)

    def teste_data_termino(self):
        p = self._criar(duracao_dias=10)
        assert p.data_termino() == date(2026, 1, 11)

    def teste_ativa_no_periodo(self):
        p = self._criar(duracao_dias=5)
        assert p.esta_ativa_em(date(2026, 1, 3))
        assert not p.esta_ativa_em(date(2025, 12, 31))
        assert not p.esta_ativa_em(date(2026, 1, 10))

    def teste_suspender_marca_atributos(self):
        p = self._criar()
        p.suspender("Reação adversa")
        assert p.suspensa is True
        assert p.motivo_suspensao == "Reação adversa"
        assert p.data_suspensao == date.today()


class TesteAplicacao:
    def teste_aplicacao_no_horario(self):
        previsto = datetime(2026, 1, 1, 8, 0)
        ap = AplicacaoMedicamento(prescricao_id=1, horario_previsto=previsto)
        ap.aplicar(funcionario_id=10, momento=datetime(2026, 1, 1, 8, 30))
        assert ap.status == StatusAplicacao.APLICADO

    def teste_aplicacao_com_atraso(self):
        previsto = datetime(2026, 1, 1, 8, 0)
        ap = AplicacaoMedicamento(prescricao_id=1, horario_previsto=previsto)
        ap.aplicar(funcionario_id=10, momento=datetime(2026, 1, 1, 10, 0))
        assert ap.status == StatusAplicacao.APLICADO_COM_ATRASO


class TesteEscala:
    def teste_conflito_de_turno_levanta(self):
        e = Escala(referencia_mes=1, referencia_ano=2026, setor="Cuidadores")
        t1 = Turno(funcionario_id=1, inicio=datetime(2026, 1, 1, 8),
                   fim=datetime(2026, 1, 1, 14), tipo=TipoTurno.MANHA)
        e.adicionar_turno(t1)
        t2 = Turno(funcionario_id=1, inicio=datetime(2026, 1, 1, 12),
                   fim=datetime(2026, 1, 1, 18), tipo=TipoTurno.TARDE)
        with pytest.raises(RegraDeNegocioViolada):
            e.adicionar_turno(t2)

    def teste_turnos_sem_conflito(self):
        e = Escala(referencia_mes=1, referencia_ano=2026, setor="Cuidadores")
        e.adicionar_turno(Turno(funcionario_id=1, inicio=datetime(2026, 1, 1, 8),
                                 fim=datetime(2026, 1, 1, 14), tipo=TipoTurno.MANHA))
        # Outro funcionário no mesmo horário deve ser permitido
        e.adicionar_turno(Turno(funcionario_id=2, inicio=datetime(2026, 1, 1, 8),
                                 fim=datetime(2026, 1, 1, 14), tipo=TipoTurno.MANHA))
        assert len(e.turnos) == 2


class TesteMensalidade:
    def teste_quitar_total(self):
        m = Mensalidade(residente_id=1, competencia_mes=1, competencia_ano=2026,
                        valor=2500.0, data_vencimento=date(2026, 1, 10))
        m.quitar(2500.0, FormaPagamento.PIX, date(2026, 1, 8))
        assert m.status == StatusPagamento.PAGO
        assert m.data_pagamento == date(2026, 1, 8)

    def teste_quitar_parcial(self):
        m = Mensalidade(residente_id=1, competencia_mes=1, competencia_ano=2026,
                        valor=2500.0, data_vencimento=date(2026, 1, 10))
        m.quitar(1000.0, FormaPagamento.DINHEIRO)
        assert m.status == StatusPagamento.PARCIAL

    def teste_atrasada(self):
        m = Mensalidade(residente_id=1, competencia_mes=1, competencia_ano=2026,
                        valor=2500.0, data_vencimento=date(2026, 1, 10))
        assert m.esta_atrasada(hoje=date(2026, 2, 1)) is True
        assert m.esta_atrasada(hoje=date(2026, 1, 5)) is False
