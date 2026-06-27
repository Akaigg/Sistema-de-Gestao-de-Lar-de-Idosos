"""Script: cria o banco e o usuário administrador padrão.

Execução:
    python -m backend.scripts.inicializar_banco
"""

from __future__ import annotations

import logging
from datetime import date

from backend.dominio.entidades.documento import ModeloDocumento
from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.infraestrutura.banco_de_dados import criar_tabelas, SessaoLocal
from backend.infraestrutura.repositorios import (
    RepositorioFuncionariosSQL,
    RepositorioModelosDocumentoSQL,
)
from backend.infraestrutura.seguranca import ServicoSenhaBcrypt

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("inicializar")

EMAIL_ADMIN = "admin@cuidarmais.com.br"
SENHA_ADMIN = "Admin@2026"


def _criar_admin_se_necessario() -> None:
    sessao = SessaoLocal()
    try:
        repo = RepositorioFuncionariosSQL(sessao)
        if repo.buscar_por_email(EMAIL_ADMIN):
            logger.info("Administrador padrão já existe — nada a fazer.")
            return
        servico_senha = ServicoSenhaBcrypt()
        funcionario = Funcionario(
            nome_completo="Administrador do Sistema",
            email=EMAIL_ADMIN,
            senha_hash=servico_senha.gerar_hash(SENHA_ADMIN),
            cpf="00000000191",  # CPF "fictício" mas válido nos dígitos
            cargo="Administrador(a)",
            papeis=[PapelFuncionario.ADMINISTRADOR],
            telefone=None,
            data_admissao=date.today(),
            deve_trocar_senha=True,
            ativo=True,
        )
        repo.criar(funcionario)
        logger.info(
            "Administrador criado.\n  E-mail: %s\n  Senha:  %s (troque no primeiro acesso)",
            EMAIL_ADMIN, SENHA_ADMIN,
        )
    finally:
        sessao.close()


def _criar_modelos_padrao_se_necessario() -> None:
    sessao = SessaoLocal()
    try:
        repo = RepositorioModelosDocumentoSQL(sessao)
        modelos_padrao = [
            ModeloDocumento(
                titulo="Termo de Responsabilidade",
                chave="termo_responsabilidade",
                conteudo_template=(
                    "Pelo presente instrumento, eu {{nome_assinante}}, portador do documento "
                    "{{documento_assinante}}, declaro estar ciente das normas internas desta instituição "
                    "e assumo a responsabilidade pelas informações prestadas em relação ao(à) residente "
                    "{{residente_nome}} (CPF {{residente_cpf}}).\n\n"
                    "Comprometo-me a comunicar a instituição de quaisquer alterações relevantes referentes "
                    "ao(à) residente, bem como autorizo os cuidados de rotina prestados pela equipe técnica."
                ),
                descricao="Termo padrão de responsabilidade do responsável legal.",
            ),
            ModeloDocumento(
                titulo="Termo de Consentimento de Uso de Imagem",
                chave="termo_imagem",
                conteudo_template=(
                    "Eu, {{nome_assinante}}, documento {{documento_assinante}}, na qualidade de responsável "
                    "pelo(a) residente {{residente_nome}}, autorizo, em conformidade com a LGPD, o uso da imagem "
                    "do(a) referido(a) residente em registros internos, materiais comemorativos e atividades "
                    "promovidas pela instituição, vedada a comercialização e a divulgação em redes sociais sem "
                    "autorização específica."
                ),
                descricao="Termo de uso de imagem (LGPD).",
            ),
            ModeloDocumento(
                titulo="Declaração de Permanência",
                chave="declaracao_permanencia",
                conteudo_template=(
                    "Declaramos, para os devidos fins, que o(a) residente {{residente_nome}}, "
                    "CPF {{residente_cpf}}, encontra-se em regime de permanência nesta instituição, "
                    "sob nossos cuidados, na presente data ({{data_atual}})."
                ),
                descricao="Declaração simples de permanência.",
            ),
        ]
        for modelo in modelos_padrao:
            if not repo.buscar_por_chave(modelo.chave):
                repo.criar(modelo)
                logger.info("Modelo de documento '%s' criado.", modelo.chave)
    finally:
        sessao.close()


def main() -> None:
    logger.info("Criando tabelas do banco de dados...")
    criar_tabelas()
    logger.info("Tabelas criadas/verificadas com sucesso.")
    _criar_admin_se_necessario()
    _criar_modelos_padrao_se_necessario()
    logger.info("Inicialização concluída.")


if __name__ == "__main__":
    main()
