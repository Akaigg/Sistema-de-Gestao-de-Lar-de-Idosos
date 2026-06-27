"""Script: popula o banco com dados fictícios para demonstração.

Cria funcionários, residentes, responsáveis, quartos/leitos, catálogo de
medicamentos com lotes, prescrições e aplicações, prontuário (sinais vitais,
evoluções, alergias, condições crônicas, consultas), alimentação (cardápios,
dietas, refeições, hidratação), escalas de trabalho, financeiro (mensalidades
e lançamentos), ocorrências e visitas.

Execução:
    python -m backend.scripts.inicializar_banco        # 1º cria as tabelas/admin
    python -m backend.scripts.popular_dados_ficticios  # 2º popula os dados

Use a variável de ambiente RECRIAR=1 para apagar o banco antes de popular:
    RECRIAR=1 python -m backend.scripts.popular_dados_ficticios
"""

from __future__ import annotations

import logging
import os
import random
from datetime import date, datetime, time, timedelta

from backend.dominio.entidades.alimentacao import (
    Cardapio, Dieta, IngestaoHidrica, Refeicao, TipoDieta, TipoRefeicao,
)
from backend.dominio.entidades.documento import ModeloDocumento
from backend.dominio.entidades.escala import Escala, TipoTurno, Turno
from backend.dominio.entidades.financeiro import (
    FormaPagamento, LancamentoFinanceiro, Mensalidade, StatusPagamento, TipoLancamento,
)
from backend.dominio.entidades.funcionario import Funcionario, PapelFuncionario
from backend.dominio.entidades.medicamento import (
    AplicacaoMedicamento, LoteMedicamento, Medicamento, Prescricao,
    StatusAplicacao, ViaAdministracao,
)
from backend.dominio.entidades.ocorrencia import (
    GravidadeOcorrencia, Ocorrencia, TipoOcorrencia,
)
from backend.dominio.entidades.prontuario import (
    Alergia, CondicaoCronica, Consulta, Evolucao, SinaisVitais,
    StatusConsulta, TipoConsulta,
)
from backend.dominio.entidades.quarto import (
    Leito, Quarto, StatusLeito, StatusQuarto, TipoQuarto,
)
from backend.dominio.entidades.residente import (
    GrauDependencia, Residente, StatusResidente,
)
from backend.dominio.entidades.responsavel import Responsavel
from backend.dominio.entidades.visita import Visita
from backend.infraestrutura.banco_de_dados import SessaoLocal, criar_tabelas
from backend.infraestrutura.configuracao import configuracoes
from backend.infraestrutura.repositorios import (
    RepositorioAplicacoesSQL, RepositorioCardapiosSQL, RepositorioCondicoesCronicasSQL,
    RepositorioConsultasSQL, RepositorioDietasSQL, RepositorioEscalasSQL,
    RepositorioEvolucoesSQL, RepositorioFuncionariosSQL, RepositorioIngestaoHidricaSQL,
    RepositorioLancamentosSQL, RepositorioLotesMedicamentoSQL, RepositorioMedicamentosSQL,
    RepositorioMensalidadesSQL, RepositorioOcorrenciasSQL, RepositorioPrescricoesSQL,
    RepositorioQuartosSQL, RepositorioRefeicoesSQL, RepositorioResidentesSQL,
    RepositorioResponsaveisSQL, RepositorioSinaisVitaisSQL, RepositorioAlergiasSQL,
    RepositorioVisitasSQL, RepositorioModelosDocumentoSQL,
)
from backend.infraestrutura.seguranca import ServicoSenhaBcrypt

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("popular")

random.seed(2026)  # reprodutível
HOJE = date.today()
AGORA = datetime.now()


# --------------------------------------------------------------------------- #
# Utilitários                                                                   #
# --------------------------------------------------------------------------- #

def gerar_cpf() -> str:
    """Gera um CPF fictício com dígitos verificadores válidos (sem pontuação)."""
    n = [random.randint(0, 9) for _ in range(9)]
    for _ in range(2):
        s = sum((len(n) + 1 - i) * v for i, v in enumerate(n))
        d = (s * 10) % 11
        n.append(0 if d == 10 else d)
    return "".join(map(str, n))


def data_nasc(idade: int) -> date:
    base = HOJE.year - idade
    return date(base, random.randint(1, 12), random.randint(1, 28))


def hora_passada(dias_atras: int, hora: int, minuto: int = 0) -> datetime:
    d = HOJE - timedelta(days=dias_atras)
    return datetime(d.year, d.month, d.day, hora, minuto)


# --------------------------------------------------------------------------- #
# Dados-fonte fictícios                                                         #
# --------------------------------------------------------------------------- #

EQUIPE = [
    ("Dra. Helena Vasconcelos", "helena.vasconcelos", "Médica Geriatra",
     [PapelFuncionario.MEDICO], "Geriatria"),
    ("Dr. Ricardo Almeida Pinto", "ricardo.almeida", "Médico Clínico",
     [PapelFuncionario.MEDICO], "Clínica Médica"),
    ("Enf. Patrícia Nogueira", "patricia.nogueira", "Enfermeira Chefe",
     [PapelFuncionario.ENFERMEIRO], "Enfermagem"),
    ("Enf. Bruno Carvalho", "bruno.carvalho", "Enfermeiro",
     [PapelFuncionario.ENFERMEIRO], "Enfermagem"),
    ("Enf. Sandra Mendes", "sandra.mendes", "Enfermeira",
     [PapelFuncionario.ENFERMEIRO], "Enfermagem"),
    ("Lucas Ferreira", "lucas.ferreira", "Cuidador",
     [PapelFuncionario.CUIDADOR], "Cuidados"),
    ("Mariana Souza", "mariana.souza", "Cuidadora",
     [PapelFuncionario.CUIDADOR], "Cuidados"),
    ("Tiago Rodrigues", "tiago.rodrigues", "Cuidador",
     [PapelFuncionario.CUIDADOR], "Cuidados"),
    ("Camila Barbosa", "camila.barbosa", "Cuidadora",
     [PapelFuncionario.CUIDADOR], "Cuidados"),
    ("Fernanda Lima", "fernanda.lima", "Cuidadora",
     [PapelFuncionario.CUIDADOR], "Cuidados"),
    ("Dra. Juliana Castro", "juliana.castro", "Nutricionista",
     [PapelFuncionario.NUTRICIONISTA], "Nutrição"),
    ("Roberto Dias", "roberto.dias", "Analista Financeiro",
     [PapelFuncionario.FINANCEIRO], "Financeiro"),
    ("Aline Cardoso", "aline.cardoso", "Recepcionista",
     [PapelFuncionario.RECEPCAO], "Recepção"),
]

NOMES_RESIDENTES = [
    ("Antônio Carlos Pereira", "M", 84), ("Maria das Graças Silva", "F", 79),
    ("José Bonifácio Andrade", "M", 88), ("Tereza Cristina Lopes", "F", 75),
    ("Sebastião Oliveira", "M", 91), ("Conceição Aparecida Rocha", "F", 82),
    ("Manuel Joaquim Torres", "M", 86), ("Lúcia Helena Martins", "F", 77),
    ("Geraldo Magela Costa", "M", 80), ("Iracema Nunes Ferreira", "F", 93),
    ("Waldemar Schneider", "M", 85), ("Odete Ramos da Cunha", "F", 81),
    ("Benedito Alves Moraes", "M", 78), ("Carmem Lúcia Teixeira", "F", 87),
    ("Otávio Augusto Brito", "M", 83), ("Zilda Maria Fontes", "F", 90),
    ("Pedro Paulo Ribeiro", "M", 76), ("Aparecida Gomes Vieira", "F", 84),
    ("Severino do Nascimento", "M", 89), ("Dulce Regina Azevedo", "F", 79),
]

CIDADES = ["São Paulo, SP", "Curitiba, PR", "Joinville, SC", "Porto Alegre, RS",
           "Florianópolis, SC", "Campinas, SP", "Blumenau, SC", "Belo Horizonte, MG"]
RELIGIOES = ["Católica", "Evangélica", "Espírita", "Sem religião", "Luterana"]
ESTADO_CIVIL = ["Viúvo(a)", "Casado(a)", "Solteiro(a)", "Divorciado(a)"]
PROFISSOES = ["Professor(a) aposentado(a)", "Comerciante", "Costureira",
              "Agricultor", "Bancário aposentado", "Dona de casa", "Marceneiro",
              "Funcionário público", "Enfermeira aposentada", "Motorista"]
PARENTESCOS = ["Filho(a)", "Sobrinho(a)", "Neto(a)", "Cônjuge", "Irmão(ã)"]

MEDICAMENTOS = [
    ("Losartana Potássica", "Losartana", "comprimido", "50mg", "EMS", False, "Anti-hipertensivo"),
    ("AAS Protect", "Ácido acetilsalicílico", "comprimido", "100mg", "Sanofi", False, "Antiagregante plaquetário"),
    ("Glifage XR", "Metformina", "comprimido", "850mg", "Merck", True, "Antidiabético oral"),
    ("Puran T4", "Levotiroxina", "comprimido", "50mcg", "Sanofi", True, "Reposição hormonal tireoidiana"),
    ("Rivotril", "Clonazepam", "comprimido", "0,5mg", "Roche", True, "Ansiolítico (controlado)"),
    ("Sinvastatina", "Sinvastatina", "comprimido", "20mg", "Medley", False, "Redutor de colesterol"),
    ("Omeprazol", "Omeprazol", "cápsula", "20mg", "Eurofarma", False, "Protetor gástrico"),
    ("Donila", "Donepezila", "comprimido", "10mg", "Apsen", True, "Alzheimer"),
    ("Lasix", "Furosemida", "comprimido", "40mg", "Sanofi", True, "Diurético"),
    ("Tylenol", "Paracetamol", "comprimido", "750mg", "Janssen", False, "Analgésico/antitérmico"),
    ("Dipirona Sódica", "Dipirona", "solução", "500mg/ml", "Neo Química", False, "Analgésico/antitérmico"),
    ("Insulina NPH", "Insulina humana", "suspensão injetável", "100UI/ml", "Novo Nordisk", True, "Controle glicêmico"),
]
CONTROLADOS = {"Clonazepam"}

CARDAPIOS = {
    TipoRefeicao.CAFE_DA_MANHA: [
        ("Café com leite, pão integral, queijo branco e mamão", 320),
        ("Vitamina de banana, torradas e geleia sem açúcar", 300),
        ("Chá de camomila, tapioca com ovo e fruta da estação", 290),
    ],
    TipoRefeicao.LANCHE_MANHA: [
        ("Iogurte natural com aveia", 150),
        ("Suco de laranja e biscoito integral", 130),
    ],
    TipoRefeicao.ALMOCO: [
        ("Arroz, feijão, frango grelhado, legumes no vapor e salada", 620),
        ("Purê de batata, carne moída refogada, abobrinha e arroz integral", 640),
        ("Sopa de legumes com macarrão, peito de peru e gelatina diet", 540),
        ("Peixe assado, arroz, lentilha, cenoura cozida e salada de folhas", 600),
    ],
    TipoRefeicao.LANCHE_TARDE: [
        ("Café com leite e bolo de cenoura sem cobertura", 220),
        ("Chá de erva-doce e sanduíche natural", 200),
    ],
    TipoRefeicao.JANTAR: [
        ("Canja de galinha, torradas e fruta", 480),
        ("Omelete de legumes, arroz e caldo de feijão", 520),
        ("Sopa cremosa de abóbora com frango desfiado", 460),
    ],
    TipoRefeicao.CEIA: [
        ("Leite morno com biscoito maisena", 160),
        ("Chá de maçã com canela", 60),
    ],
}

EVOLUCOES_TEXTO = [
    ("enfermagem", "Residente lúcido e orientado, aceitou bem a dieta, sinais vitais estáveis. Sem queixas no plantão."),
    ("enfermagem", "Auxiliado no banho e higiene. Deambulando com apoio. Pele íntegra, hidratada."),
    ("medica", "Paciente em bom estado geral. Mantida conduta medicamentosa atual. Reavaliar pressão em 7 dias."),
    ("fisioterapia", "Realizada sessão de cinesioterapia motora. Boa adesão aos exercícios de fortalecimento de membros inferiores."),
    ("psicologia", "Atendimento de escuta ativa. Residente relatou saudade da família; orientado acolhimento e visita."),
    ("enfermagem", "Aferição de glicemia capilar dentro do esperado. Administrada medicação conforme prescrição."),
]


# --------------------------------------------------------------------------- #
# Execução                                                                      #
# --------------------------------------------------------------------------- #

def _ja_populado(sessao) -> bool:
    repo = RepositorioResidentesSQL(sessao)
    return len(repo.listar(tamanho_pagina=1)) > 0


def _garantir_admin(sessao, servico_senha) -> None:
    """Cria o administrador padrão se ainda não existir (mesma credencial do
    inicializar_banco), para que um único comando já entregue admin + equipe."""
    repo = RepositorioFuncionariosSQL(sessao)
    email_admin = "admin@cuidarmais.com.br"
    if repo.buscar_por_email(email_admin):
        logger.info("Administrador padrão já existe.")
        return
    admin = Funcionario(
        nome_completo="Administrador do Sistema",
        email=email_admin,
        senha_hash=servico_senha.gerar_hash("Admin@2026"),
        cpf="00000000191",
        cargo="Administrador(a)",
        papeis=[PapelFuncionario.ADMINISTRADOR],
        telefone=None,
        data_admissao=HOJE,
        deve_trocar_senha=True,
        ativo=True,
    )
    repo.criar(admin)
    logger.info("Administrador padrão criado.")


def _garantir_modelos_documento(sessao) -> None:
    """Cria os modelos de documento padrão se ainda não existirem."""
    repo = RepositorioModelosDocumentoSQL(sessao)
    modelos = [
        ModeloDocumento(
            titulo="Termo de Responsabilidade",
            chave="termo_responsabilidade",
            conteudo_template=(
                "Pelo presente instrumento, eu {{nome_assinante}}, portador do documento "
                "{{documento_assinante}}, declaro estar ciente das normas internas desta "
                "instituição e assumo a responsabilidade pelas informações prestadas em "
                "relação ao(à) residente {{residente_nome}} (CPF {{residente_cpf}})."
            ),
            descricao="Termo padrão de responsabilidade do responsável legal.",
        ),
        ModeloDocumento(
            titulo="Termo de Consentimento de Uso de Imagem",
            chave="termo_imagem",
            conteudo_template=(
                "Eu, {{nome_assinante}}, documento {{documento_assinante}}, na qualidade de "
                "responsável pelo(a) residente {{residente_nome}}, autorizo, em conformidade "
                "com a LGPD, o uso da imagem do(a) referido(a) residente em registros internos."
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
    criados = 0
    for modelo in modelos:
        if not repo.buscar_por_chave(modelo.chave):
            repo.criar(modelo)
            criados += 1
    if criados:
        logger.info("%d modelos de documento criados.", criados)


def main() -> None:
    if os.getenv("RECRIAR") == "1" and configuracoes.arquivo_banco.exists():
        configuracoes.arquivo_banco.unlink()
        logger.info("Banco anterior removido (RECRIAR=1).")

    criar_tabelas()

    sessao = SessaoLocal()
    try:
        if _ja_populado(sessao):
            logger.warning(
                "O banco já possui residentes. Para repopular do zero use: "
                "RECRIAR=1 python -m backend.scripts.popular_dados_ficticios"
            )
            return

        servico_senha = ServicoSenhaBcrypt()
        senha_hash_padrao = servico_senha.gerar_hash("Cuidar@2026")

        # Garante o admin padrão também (um comando entrega admin + equipe)
        _garantir_admin(sessao, servico_senha)
        _garantir_modelos_documento(sessao)

        repo_func = RepositorioFuncionariosSQL(sessao)
        repo_res = RepositorioResidentesSQL(sessao)
        repo_resp = RepositorioResponsaveisSQL(sessao)
        repo_quarto = RepositorioQuartosSQL(sessao)
        repo_med = RepositorioMedicamentosSQL(sessao)
        repo_lote = RepositorioLotesMedicamentoSQL(sessao)
        repo_presc = RepositorioPrescricoesSQL(sessao)
        repo_aplic = RepositorioAplicacoesSQL(sessao)
        repo_sv = RepositorioSinaisVitaisSQL(sessao)
        repo_evo = RepositorioEvolucoesSQL(sessao)
        repo_alergia = RepositorioAlergiasSQL(sessao)
        repo_cond = RepositorioCondicoesCronicasSQL(sessao)
        repo_consulta = RepositorioConsultasSQL(sessao)
        repo_card = RepositorioCardapiosSQL(sessao)
        repo_dieta = RepositorioDietasSQL(sessao)
        repo_refeicao = RepositorioRefeicoesSQL(sessao)
        repo_hidr = RepositorioIngestaoHidricaSQL(sessao)
        repo_escala = RepositorioEscalasSQL(sessao)
        repo_mens = RepositorioMensalidadesSQL(sessao)
        repo_lanc = RepositorioLancamentosSQL(sessao)
        repo_ocor = RepositorioOcorrenciasSQL(sessao)
        repo_visita = RepositorioVisitasSQL(sessao)

        # ----- Funcionários -----
        funcionarios: list[Funcionario] = []
        for nome, usuario, cargo, papeis, _setor in EQUIPE:
            f = Funcionario(
                nome_completo=nome,
                email=f"{usuario}@cuidarmais.com.br",
                senha_hash=senha_hash_padrao,
                cpf=gerar_cpf(),
                cargo=cargo,
                papeis=papeis,
                telefone=f"(47) 9{random.randint(8000,9999)}-{random.randint(1000,9999)}",
                data_admissao=HOJE - timedelta(days=random.randint(120, 1500)),
                deve_trocar_senha=False,
                ativo=True,
            )
            funcionarios.append(repo_func.criar(f))
        logger.info("%d funcionários criados.", len(funcionarios))

        medicos = [f for f in funcionarios if PapelFuncionario.MEDICO in f.papeis]
        enfermeiros = [f for f in funcionarios if PapelFuncionario.ENFERMEIRO in f.papeis]
        cuidadores = [f for f in funcionarios if PapelFuncionario.CUIDADOR in f.papeis]
        nutri = next(f for f in funcionarios if PapelFuncionario.NUTRICIONISTA in f.papeis)
        recepcao = next(f for f in funcionarios if PapelFuncionario.RECEPCAO in f.papeis)
        equipe_assist = enfermeiros + cuidadores

        # ----- Medicamentos + lotes -----
        medicamentos: list[Medicamento] = []
        for nome, ativo, forma, conc, fab, controlado_recv, obs in MEDICAMENTOS:
            m = Medicamento(
                nome_comercial=nome,
                principio_ativo=ativo,
                forma_farmaceutica=forma,
                concentracao=conc,
                fabricante=fab,
                necessita_receita=ativo not in ("Ácido acetilsalicílico", "Paracetamol", "Dipirona"),
                controlado=ativo in CONTROLADOS,
                observacoes=obs,
                estoque_minimo=random.choice([10, 20, 30]),
            )
            m = repo_med.criar(m)
            medicamentos.append(m)
            for _ in range(random.randint(1, 2)):
                repo_lote.criar(LoteMedicamento(
                    medicamento_id=m.identificador,
                    numero_lote=f"L{random.randint(10000,99999)}",
                    quantidade=random.randint(40, 300),
                    data_validade=HOJE + timedelta(days=random.randint(120, 720)),
                    data_entrada=HOJE - timedelta(days=random.randint(10, 200)),
                    fornecedor=random.choice(["Distribuidora Saúde+", "Farmasul", "Panvel Distribuição"]),
                    preco_unitario=round(random.uniform(0.3, 8.5), 2),
                ))
        logger.info("%d medicamentos (com lotes) criados.", len(medicamentos))

        # ----- Quartos + leitos -----
        # 8 quartos: mistura de individuais, duplos e triplos -> 18 leitos
        plano_quartos = [
            ("101", 1, TipoQuarto.DUPLO, 2), ("102", 1, TipoQuarto.DUPLO, 2),
            ("103", 1, TipoQuarto.INDIVIDUAL, 1), ("104", 1, TipoQuarto.TRIPLO, 3),
            ("105", 1, TipoQuarto.DUPLO, 2),
            ("201", 2, TipoQuarto.DUPLO, 2), ("202", 2, TipoQuarto.DUPLO, 2),
            ("203", 2, TipoQuarto.TRIPLO, 3), ("204", 2, TipoQuarto.INDIVIDUAL, 1),
            ("205", 2, TipoQuarto.DUPLO, 2),
        ]
        # primeiro criamos os residentes (precisamos do id para ocupar leitos)
        residentes: list[Residente] = []
        for idx, (nome, sexo, idade) in enumerate(NOMES_RESIDENTES):
            graus = list(GrauDependencia)
            r = Residente(
                nome_completo=nome,
                data_nascimento=data_nasc(idade),
                cpf=gerar_cpf(),
                sexo=sexo,
                data_entrada=HOJE - timedelta(days=random.randint(30, 1400)),
                grau_dependencia=random.choice(graus),
                status=StatusResidente.ATIVO if idx < 18 else random.choice(
                    [StatusResidente.INTERNADO, StatusResidente.LICENCA]),
                rg=str(random.randint(1000000, 9999999)),
                cartao_sus="".join(str(random.randint(0, 9)) for _ in range(15)),
                convenio=random.choice([None, "Unimed", "SUS", "Bradesco Saúde"]),
                religiao=random.choice(RELIGIOES),
                estado_civil=random.choice(ESTADO_CIVIL),
                naturalidade=random.choice(CIDADES),
                profissao_anterior=random.choice(PROFISSOES),
                consentimento_imagem=random.choice([True, True, False]),
                observacoes=random.choice([
                    None, "Faz uso de óculos.", "Usa aparelho auditivo.",
                    "Cadeirante.", "Dieta pastosa por dificuldade de deglutição.",
                ]),
            )
            residentes.append(repo_res.criar(r))
        ativos = [r for r in residentes if r.status == StatusResidente.ATIVO]
        logger.info("%d residentes criados (%d ativos).", len(residentes), len(ativos))

        # responsáveis (1 a 2 por residente)
        total_resp = 0
        sobrenomes = ["dos Santos", "Pereira", "Oliveira", "Souza", "Lima", "Costa"]
        for r in residentes:
            primeiro = r.nome_completo.split()[0]
            for j in range(random.randint(1, 2)):
                resp = Responsavel(
                    nome_completo=f"{random.choice(['Ana','Carlos','Marcos','Patrícia','Júlia','Paulo'])} "
                                  f"{primeiro.split()[0]} {random.choice(sobrenomes)}",
                    cpf=gerar_cpf(),
                    parentesco=random.choice(PARENTESCOS),
                    telefone=f"(47) 9{random.randint(8000,9999)}-{random.randint(1000,9999)}",
                    email=f"familiar{r.identificador}_{j}@email.com",
                    endereco_resumido=random.choice(CIDADES),
                    eh_responsavel_legal=(j == 0),
                    eh_contato_emergencia=True,
                )
                repo_resp.criar(resp, r.identificador)
                total_resp += 1
        logger.info("%d responsáveis vinculados.", total_resp)

        # ocupar leitos com residentes ativos
        fila_ativos = list(ativos)
        for numero, andar, tipo, cap in plano_quartos:
            leitos = []
            for n in range(1, cap + 1):
                ocupante = fila_ativos.pop(0) if fila_ativos else None
                leitos.append(Leito(
                    numero=f"{numero}-{chr(64 + n)}",
                    status=StatusLeito.OCUPADO if ocupante else StatusLeito.LIVRE,
                    residente_id=ocupante.identificador if ocupante else None,
                ))
            repo_quarto.criar(Quarto(
                numero=numero, andar=andar, tipo=tipo, capacidade=cap,
                leitos=leitos, status=StatusQuarto.ATIVO,
                possui_banheiro=True,
                possui_ar_condicionado=random.choice([True, False]),
                acessibilidade=True,
            ))
        logger.info("%d quartos criados.", len(plano_quartos))

        # ----- Prontuário, prescrições, alimentação por residente ativo -----
        substancias_alergia = ["Penicilina", "Dipirona", "Frutos do mar", "Lactose",
                               "Sulfa", "Iodo", "Látex"]
        condicoes = [
            ("Hipertensão arterial sistêmica", "I10"),
            ("Diabetes mellitus tipo 2", "E11"),
            ("Doença de Alzheimer", "G30"),
            ("Osteoartrose", "M19"),
            ("Insuficiência cardíaca", "I50"),
            ("Hipotireoidismo", "E03"),
            ("Demência vascular", "F01"),
        ]
        dietas_possiveis = [
            TipoDieta.LIVRE, TipoDieta.HIPOSSODICA, TipoDieta.DIABETICA,
            TipoDieta.PASTOSA, TipoDieta.SEM_LACTOSE,
        ]
        horarios_dose = {
            1: [time(8, 0)], 2: [time(8, 0), time(20, 0)],
            3: [time(7, 0), time(13, 0), time(19, 0)],
        }

        n_presc = n_aplic = n_sv = n_evo = n_cons = 0
        for r in ativos:
            # condições crônicas (1-3)
            for desc, cid in random.sample(condicoes, random.randint(1, 3)):
                repo_cond.criar(CondicaoCronica(
                    residente_id=r.identificador, descricao=desc, cid10=cid,
                    data_diagnostico=str(HOJE.year - random.randint(2, 15)),
                ))
            # alergias (0-2)
            for subst in random.sample(substancias_alergia, random.randint(0, 2)):
                repo_alergia.criar(Alergia(
                    residente_id=r.identificador, substancia=subst,
                    reacao=random.choice(["Urticária", "Edema", "Prurido", "Náusea"]),
                    gravidade=random.choice(["leve", "moderada", "grave"]),
                ))
            # dieta
            repo_dieta.criar(Dieta(
                residente_id=r.identificador,
                tipo=random.choice(dietas_possiveis),
                descricao_detalhada="Dieta acompanhada pela nutrição.",
                prescrita_por_id=nutri.identificador,
                data_inicio=HOJE - timedelta(days=random.randint(20, 300)),
            ))
            # sinais vitais (últimos 5 dias)
            for d in range(5):
                repo_sv.criar(SinaisVitais(
                    residente_id=r.identificador,
                    aferido_em=hora_passada(d, random.choice([7, 13, 19])),
                    funcionario_id=random.choice(enfermeiros).identificador,
                    pressao_sistolica=random.randint(110, 160),
                    pressao_diastolica=random.randint(60, 95),
                    frequencia_cardiaca=random.randint(58, 92),
                    frequencia_respiratoria=random.randint(14, 20),
                    temperatura=round(random.uniform(35.8, 37.4), 1),
                    saturacao_oxigenio=random.randint(92, 99),
                    glicemia=random.randint(80, 180),
                    peso=round(random.uniform(48, 92), 1),
                ))
                n_sv += 1
            # evoluções (2-4)
            for _ in range(random.randint(2, 4)):
                cat, txt = random.choice(EVOLUCOES_TEXTO)
                repo_evo.criar(Evolucao(
                    residente_id=r.identificador,
                    funcionario_id=random.choice(equipe_assist).identificador,
                    registrada_em=hora_passada(random.randint(0, 6),
                                               random.randint(7, 21)),
                    categoria=cat, texto=txt,
                ))
                n_evo += 1
            # prescrições (1-3) + aplicações
            for med in random.sample(medicamentos, random.randint(1, 3)):
                freq = random.choice([1, 2, 3])
                presc = repo_presc.criar(Prescricao(
                    residente_id=r.identificador,
                    medicamento_id=med.identificador,
                    medico_id=random.choice(medicos).identificador,
                    dose=f"{random.choice([1, 1, 2])} {med.forma_farmaceutica}",
                    via=ViaAdministracao.ORAL,
                    frequencia_horas=24 // freq,
                    horarios=horarios_dose[freq],
                    data_inicio=HOJE - timedelta(days=random.randint(5, 120)),
                    duracao_dias=random.choice([None, 30, 60, 90]),
                    observacoes=random.choice([None, "Administrar após as refeições."]),
                ))
                n_presc += 1
                # aplicações dos últimos 2 dias + hoje
                for d in range(2, -1, -1):
                    for h in presc.horarios:
                        previsto = datetime.combine(HOJE - timedelta(days=d), h)
                        if previsto > AGORA:
                            status = StatusAplicacao.AGUARDANDO
                            aplicado = None
                            func_id = None
                        else:
                            status = random.choices(
                                [StatusAplicacao.APLICADO,
                                 StatusAplicacao.APLICADO_COM_ATRASO,
                                 StatusAplicacao.RECUSADO],
                                weights=[85, 10, 5])[0]
                            aplicado = previsto + timedelta(minutes=random.randint(-20, 50))
                            func_id = random.choice(equipe_assist).identificador
                        repo_aplic.criar(AplicacaoMedicamento(
                            prescricao_id=presc.identificador,
                            horario_previsto=previsto,
                            status=status,
                            horario_aplicado=aplicado,
                            funcionario_id=func_id,
                        ))
                        n_aplic += 1
            # hidratação (hoje)
            for h in [9, 11, 14, 16, 19]:
                repo_hidr.criar(IngestaoHidrica(
                    residente_id=r.identificador,
                    registrada_em=datetime.combine(HOJE, time(h, 0)),
                    quantidade_ml=random.choice([100, 150, 200, 250]),
                    funcionario_id=random.choice(cuidadores).identificador,
                ))
            # consultas (1-2 futuras + 1 realizada)
            for _ in range(random.randint(1, 2)):
                dias = random.randint(1, 25)
                repo_consulta.criar(Consulta(
                    residente_id=r.identificador,
                    tipo=random.choice(list(TipoConsulta)),
                    data_hora=datetime.combine(HOJE + timedelta(days=dias),
                                               time(random.randint(8, 16), random.choice([0, 30]))),
                    eh_externa=random.choice([True, False]),
                    profissional=random.choice(["Dr. Marcelo Antunes", "Dra. Beatriz Furtado",
                                                "Dr. Henrique Salles", "Dra. Renata Couto"]),
                    especialidade=random.choice(["Cardiologia", "Neurologia", "Oftalmologia",
                                                 "Geriatria", "Ortopedia"]),
                    local=random.choice(["Lar Cuidar+ — Sala 2", "Hospital Regional",
                                         "Clínica São Lucas"]),
                    motivo="Acompanhamento de rotina.",
                    status=random.choice([StatusConsulta.AGENDADA, StatusConsulta.CONFIRMADA]),
                    funcionario_acompanhante_id=random.choice(cuidadores).identificador,
                ))
                n_cons += 1
            repo_consulta.criar(Consulta(
                residente_id=r.identificador,
                tipo=TipoConsulta.CONSULTA_MEDICA,
                data_hora=datetime.combine(HOJE - timedelta(days=random.randint(5, 40)),
                                           time(10, 0)),
                eh_externa=False,
                profissional=random.choice(medicos).nome_completo,
                especialidade="Geriatria",
                local="Lar Cuidar+ — Consultório",
                motivo="Avaliação periódica.",
                status=StatusConsulta.REALIZADA,
            ))
            n_cons += 1
        logger.info("Prontuário: %d sinais vitais, %d evoluções, %d consultas.",
                    n_sv, n_evo, n_cons)
        logger.info("Medicação: %d prescrições, %d aplicações.", n_presc, n_aplic)

        # ----- Cardápios (7 dias) + refeições -----
        n_card = n_ref = 0
        cardapios_por_dia: dict = {}
        for d in range(7):
            dia = HOJE - timedelta(days=d)
            for tipo, opcoes in CARDAPIOS.items():
                desc, cal = random.choice(opcoes)
                c = repo_card.criar(Cardapio(
                    data_referencia=dia, tipo_refeicao=tipo,
                    descricao=desc, calorias_aproximadas=cal,
                ))
                cardapios_por_dia[(dia, tipo)] = c.identificador
                n_card += 1
        # refeições servidas (últimos 2 dias, refeições principais)
        for d in range(2):
            dia = HOJE - timedelta(days=d)
            for tipo, hora in [(TipoRefeicao.CAFE_DA_MANHA, 8),
                               (TipoRefeicao.ALMOCO, 12),
                               (TipoRefeicao.JANTAR, 19)]:
                for r in ativos:
                    repo_refeicao.criar(Refeicao(
                        residente_id=r.identificador,
                        cardapio_id=cardapios_por_dia.get((dia, tipo)),
                        tipo_refeicao=tipo,
                        servida_em=datetime.combine(dia, time(hora, 0)),
                        funcionario_id=random.choice(cuidadores).identificador,
                        aceitacao_percentual=random.choice([100, 100, 80, 75, 50, 90]),
                    ))
                    n_ref += 1
        logger.info("Alimentação: %d itens de cardápio, %d refeições servidas.", n_card, n_ref)

        # ----- Escalas -----
        for setor, equipe in [("Enfermagem", enfermeiros), ("Cuidadores", cuidadores)]:
            turnos = []
            for d in range(7):
                dia = HOJE + timedelta(days=d)
                for func, (hi, hf, tt) in zip(
                    random.sample(equipe, min(2, len(equipe))),
                    [(7, 19, TipoTurno.PLANTAO_12H), (19, 7, TipoTurno.PLANTAO_12H)],
                ):
                    inicio = datetime.combine(dia, time(hi, 0))
                    fim = datetime.combine(dia + (timedelta(days=1) if hf < hi else timedelta()),
                                           time(hf, 0))
                    turnos.append(Turno(
                        funcionario_id=func.identificador, inicio=inicio, fim=fim,
                        tipo=tt, confirmado=True,
                    ))
            repo_escala.criar(Escala(
                referencia_mes=HOJE.month, referencia_ano=HOJE.year,
                setor=setor, turnos=turnos, publicada=True,
                publicada_em=AGORA, publicada_por_id=enfermeiros[0].identificador,
            ))
        logger.info("2 escalas (Enfermagem e Cuidadores) publicadas.")

        # ----- Financeiro -----
        n_mens = n_lanc = 0
        for r in ativos:
            valor = random.choice([2800.0, 3200.0, 3500.0, 4100.0, 4800.0])
            for m_atras in range(3):  # 3 últimos meses
                ref = (HOJE.replace(day=1) - timedelta(days=1)).replace(day=1) if False else None
                mes = HOJE.month - m_atras
                ano = HOJE.year
                while mes <= 0:
                    mes += 12
                    ano -= 1
                venc = date(ano, mes, 10)
                pago = m_atras > 0 or random.random() > 0.4
                mens = Mensalidade(
                    residente_id=r.identificador,
                    competencia_mes=mes, competencia_ano=ano,
                    valor=valor, data_vencimento=venc,
                    status=StatusPagamento.PAGO if pago else (
                        StatusPagamento.ATRASADO if venc < HOJE else StatusPagamento.EM_ABERTO),
                    data_pagamento=venc - timedelta(days=random.randint(0, 5)) if pago else None,
                    valor_pago=valor if pago else None,
                    forma_pagamento=random.choice(list(FormaPagamento)) if pago else None,
                )
                repo_mens.criar(mens)
                n_mens += 1

        despesas = [
            ("Folha de pagamento — equipe", 48000, "Pessoal"),
            ("Compra de medicamentos", 6200, "Farmácia"),
            ("Gêneros alimentícios", 9800, "Alimentação"),
            ("Conta de energia elétrica", 3400, "Utilidades"),
            ("Conta de água", 1200, "Utilidades"),
            ("Material de higiene e limpeza", 2700, "Suprimentos"),
            ("Manutenção predial", 1800, "Manutenção"),
            ("Lavanderia terceirizada", 2200, "Serviços"),
        ]
        for desc, val, cat in despesas:
            repo_lanc.criar(LancamentoFinanceiro(
                tipo=TipoLancamento.DESPESA, descricao=desc,
                valor=float(val) * random.uniform(0.95, 1.05),
                data_competencia=HOJE.replace(day=random.randint(1, 25)),
                categoria=cat, centro_custo=cat,
                forma_pagamento=random.choice(list(FormaPagamento)),
                status=StatusPagamento.PAGO,
                registrado_por_id=funcionarios[-2].identificador,
            ))
            n_lanc += 1
        for desc, val in [("Repasse convênio Unimed", 14500), ("Doação — associação de bairro", 3000)]:
            repo_lanc.criar(LancamentoFinanceiro(
                tipo=TipoLancamento.RECEITA, descricao=desc, valor=float(val),
                data_competencia=HOJE.replace(day=random.randint(1, 25)),
                categoria="Receitas diversas", status=StatusPagamento.PAGO,
                registrado_por_id=funcionarios[-2].identificador,
            ))
            n_lanc += 1
        logger.info("Financeiro: %d mensalidades, %d lançamentos.", n_mens, n_lanc)

        # ----- Ocorrências -----
        n_ocor = 0
        for r in random.sample(ativos, min(8, len(ativos))):
            tipo = random.choice(list(TipoOcorrencia))
            grav = random.choice(list(GravidadeOcorrencia))
            repo_ocor.criar(Ocorrencia(
                residente_id=r.identificador,
                tipo=tipo, gravidade=grav,
                descricao={
                    TipoOcorrencia.QUEDA: "Queda da própria altura no quarto, sem perda de consciência.",
                    TipoOcorrencia.INTERCORRENCIA_CLINICA: "Pico hipertensivo, monitorado pela enfermagem.",
                    TipoOcorrencia.AGRESSIVIDADE: "Episódio de agitação à noite, acalmado com conversa.",
                    TipoOcorrencia.EVASAO: "Tentativa de sair da unidade, abordado pela recepção.",
                    TipoOcorrencia.REACAO_MEDICAMENTOSA: "Leve reação cutânea após medicação.",
                    TipoOcorrencia.ACIDENTE: "Pequeno corte ao manusear utensílio.",
                    TipoOcorrencia.OUTRA: "Ocorrência registrada para acompanhamento.",
                }.get(tipo, "Ocorrência registrada."),
                ocorreu_em=hora_passada(random.randint(0, 20), random.randint(0, 23)),
                registrada_por_id=random.choice(equipe_assist).identificador,
                local=random.choice(["Quarto", "Refeitório", "Pátio", "Corredor", "Banheiro"]),
                medidas_adotadas="Equipe acionada, residente avaliado e monitorado.",
                necessitou_hospital=(grav in (GravidadeOcorrencia.GRAVE, GravidadeOcorrencia.CRITICA)),
                encerrada=random.choice([True, False]),
            ))
            n_ocor += 1
        logger.info("%d ocorrências registradas.", n_ocor)

        # ----- Visitas -----
        n_vis = 0
        for _ in range(20):
            r = random.choice(ativos)
            d = random.randint(0, 10)
            entrada = hora_passada(d, random.randint(9, 16), random.choice([0, 30]))
            encerrada = d > 0 or random.random() > 0.3
            repo_visita.criar(Visita(
                residente_id=r.identificador,
                nome_visitante=f"{random.choice(['Sr.','Sra.'])} "
                               f"{random.choice(['Carlos','Marta','João','Sônia','Felipe','Beatriz'])} "
                               f"{random.choice(sobrenomes)}",
                documento_visitante=str(random.randint(10000000, 99999999)),
                parentesco_ou_relacao=random.choice(PARENTESCOS),
                entrada_em=entrada,
                saida_em=entrada + timedelta(minutes=random.randint(40, 150)) if encerrada else None,
                funcionario_recebeu_id=recepcao.identificador,
            ))
            n_vis += 1
        logger.info("%d visitas registradas.", n_vis)

        logger.info("=" * 56)
        logger.info("Banco populado com sucesso!")
        logger.info("Login de demonstração (qualquer funcionário):")
        logger.info("  E-mail: patricia.nogueira@cuidarmais.com.br")
        logger.info("  Senha:  Cuidar@2026")
        logger.info("Admin: admin@cuidarmais.com.br / Admin@2026")
        logger.info("=" * 56)
    finally:
        sessao.close()


if __name__ == "__main__":
    main()
