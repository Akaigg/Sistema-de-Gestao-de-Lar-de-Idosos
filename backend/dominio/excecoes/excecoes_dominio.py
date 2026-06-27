"""Hierarquia de exceções da camada de domínio.

Estas exceções **não dependem** de framework HTTP — a camada de
apresentação é responsável por traduzi-las em códigos de status.
"""


class ErroDeDominio(Exception):
    """Classe base para todos os erros do domínio."""

    def __init__(self, mensagem: str = "Erro de domínio"):
        super().__init__(mensagem)
        self.mensagem = mensagem


class EntidadeNaoEncontrada(ErroDeDominio):
    """Lançada quando uma entidade não é encontrada por identificador."""


class EntidadeJaExistente(ErroDeDominio):
    """Lançada quando uma entidade que deveria ser única já existe."""


class RegraDeNegocioViolada(ErroDeDominio):
    """Lançada quando uma regra de negócio é violada."""


class DadosInvalidos(ErroDeDominio):
    """Lançada quando dados de entrada são logicamente inválidos."""


class CredenciaisInvalidas(ErroDeDominio):
    """Login/senha incorretos."""


class ContaBloqueada(ErroDeDominio):
    """Conta bloqueada por excesso de tentativas ou desativação."""


class AcessoNegado(ErroDeDominio):
    """Usuário não tem permissão para o recurso."""
