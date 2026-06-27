"""Testes unitários dos objetos de valor."""

import pytest

from backend.dominio.excecoes import DadosInvalidos
from backend.dominio.objetos_de_valor import CPF, Email, Telefone


class TesteCPF:
    def teste_cpf_valido_normaliza(self):
        cpf = CPF("111.444.777-35")
        assert cpf.numero == "11144477735"

    def teste_cpf_invalido_levanta(self):
        with pytest.raises(DadosInvalidos):
            CPF("123.456.789-00")

    def teste_cpf_repetido_invalido(self):
        with pytest.raises(DadosInvalidos):
            CPF("111.111.111-11")

    def teste_cpf_formatado(self):
        assert CPF("11144477735").formatado() == "111.444.777-35"


class TesteEmail:
    def teste_email_valido_normaliza_caixa(self):
        email = Email("USUARIO@Dominio.COM.BR")
        assert email.endereco == "usuario@dominio.com.br"

    def teste_email_invalido_levanta(self):
        with pytest.raises(DadosInvalidos):
            Email("sem-arroba.com")


class TesteTelefone:
    def teste_celular_normaliza(self):
        tel = Telefone("(11) 91234-5678")
        assert tel.numero == "11912345678"
        assert tel.formatado() == "(11) 91234-5678"

    def teste_fixo_normaliza(self):
        tel = Telefone("1132345678")
        assert tel.formatado() == "(11) 3234-5678"

    def teste_telefone_curto_invalido(self):
        with pytest.raises(DadosInvalidos):
            Telefone("12345")
