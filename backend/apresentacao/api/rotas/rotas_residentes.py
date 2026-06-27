"""Rotas de residentes e responsáveis."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.aplicacao.casos_de_uso.residentes import (
    AtualizarResidente,
    CadastrarResidente,
    DadosCadastroResidente,
    ListarResidentes,
    ObterResidente,
    RegistrarSaidaResidente,
)
from backend.dominio.entidades.residente import GrauDependencia, StatusResidente
from backend.dominio.entidades.responsavel import Responsavel
from backend.apresentacao.dependencias import (
    obter_funcionario_logado,
    obter_repo_auditoria,
    obter_repo_residentes,
    obter_repo_responsaveis,
)
from backend.apresentacao.schemas.comuns import MensagemSimples, RespostaPaginada
from backend.apresentacao.schemas.residentes import (
    EntradaAtualizacaoResidente,
    EntradaCadastroResidente,
    EntradaCadastroResponsavel,
    EntradaSaidaResidente,
    ResidenteSaida,
    ResponsavelSaida,
)

roteador = APIRouter(prefix="/api/residentes", tags=["Residentes"])


def _para_saida(residente) -> ResidenteSaida:
    return ResidenteSaida(
        identificador=residente.identificador,
        nome_completo=residente.nome_completo,
        data_nascimento=residente.data_nascimento,
        idade=residente.calcular_idade(),
        cpf=residente.cpf,
        sexo=residente.sexo,
        data_entrada=residente.data_entrada,
        grau_dependencia=residente.grau_dependencia.value,
        status=residente.status.value,
        rg=residente.rg,
        cartao_sus=residente.cartao_sus,
        convenio=residente.convenio,
        numero_convenio=residente.numero_convenio,
        religiao=residente.religiao,
        estado_civil=residente.estado_civil,
        naturalidade=residente.naturalidade,
        profissao_anterior=residente.profissao_anterior,
        observacoes=residente.observacoes,
        consentimento_imagem=residente.consentimento_imagem,
        data_saida=residente.data_saida,
        motivo_saida=residente.motivo_saida,
        foto_caminho=residente.foto_caminho,
    )


@roteador.post("", response_model=ResidenteSaida)
def cadastrar(
    dados: EntradaCadastroResidente,
    funcionario=Depends(obter_funcionario_logado),
    repo_residentes=Depends(obter_repo_residentes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = CadastrarResidente(repo_residentes, repo_auditoria)
    residente = caso.executar(
        DadosCadastroResidente(
            nome_completo=dados.nome_completo,
            data_nascimento=dados.data_nascimento,
            cpf=dados.cpf,
            sexo=dados.sexo,
            data_entrada=dados.data_entrada,
            grau_dependencia=GrauDependencia(dados.grau_dependencia),
            rg=dados.rg,
            cartao_sus=dados.cartao_sus,
            convenio=dados.convenio,
            numero_convenio=dados.numero_convenio,
            religiao=dados.religiao,
            estado_civil=dados.estado_civil,
            naturalidade=dados.naturalidade,
            profissao_anterior=dados.profissao_anterior,
            observacoes=dados.observacoes,
            consentimento_imagem=dados.consentimento_imagem,
        ),
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _para_saida(residente)


@roteador.get("", response_model=RespostaPaginada[ResidenteSaida])
def listar(
    termo_busca: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    tamanho_pagina: int = Query(default=50, ge=1, le=200),
    repo_residentes=Depends(obter_repo_residentes),
    _funcionario=Depends(obter_funcionario_logado),
):
    caso = ListarResidentes(repo_residentes)
    status_enum = StatusResidente(status) if status else None
    itens, total = caso.executar(termo_busca, status_enum, pagina, tamanho_pagina)
    return RespostaPaginada(
        itens=[_para_saida(r) for r in itens],
        total=total,
        pagina=pagina,
        tamanho_pagina=tamanho_pagina,
    )


@roteador.get("/{residente_id}", response_model=ResidenteSaida)
def obter(
    residente_id: int,
    repo_residentes=Depends(obter_repo_residentes),
    _funcionario=Depends(obter_funcionario_logado),
):
    caso = ObterResidente(repo_residentes)
    return _para_saida(caso.executar(residente_id))


@roteador.put("/{residente_id}", response_model=ResidenteSaida)
def atualizar(
    residente_id: int,
    dados: EntradaAtualizacaoResidente,
    funcionario=Depends(obter_funcionario_logado),
    repo_residentes=Depends(obter_repo_residentes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = AtualizarResidente(repo_residentes, repo_auditoria)
    atualizacoes = dados.model_dump(exclude_none=True)
    if "grau_dependencia" in atualizacoes:
        atualizacoes["grau_dependencia"] = GrauDependencia(atualizacoes["grau_dependencia"])
    residente = caso.executar(
        residente_id, atualizacoes, funcionario_responsavel_id=funcionario.identificador
    )
    return _para_saida(residente)


@roteador.post("/{residente_id}/saida", response_model=ResidenteSaida)
def registrar_saida(
    residente_id: int,
    dados: EntradaSaidaResidente,
    funcionario=Depends(obter_funcionario_logado),
    repo_residentes=Depends(obter_repo_residentes),
    repo_auditoria=Depends(obter_repo_auditoria),
):
    caso = RegistrarSaidaResidente(repo_residentes, repo_auditoria)
    residente = caso.executar(
        residente_id,
        motivo=dados.motivo,
        falecimento=dados.falecimento,
        data_saida=dados.data_saida,
        funcionario_responsavel_id=funcionario.identificador,
    )
    return _para_saida(residente)


# -------- Responsáveis --------

@roteador.post("/{residente_id}/responsaveis", response_model=ResponsavelSaida)
def adicionar_responsavel(
    residente_id: int,
    dados: EntradaCadastroResponsavel,
    repo_responsaveis=Depends(obter_repo_responsaveis),
    _funcionario=Depends(obter_funcionario_logado),
):
    responsavel = Responsavel(
        nome_completo=dados.nome_completo,
        cpf=dados.cpf,
        parentesco=dados.parentesco,
        telefone=dados.telefone,
        email=dados.email,
        endereco_resumido=dados.endereco_resumido,
        eh_responsavel_legal=dados.eh_responsavel_legal,
        eh_contato_emergencia=dados.eh_contato_emergencia,
        observacoes=dados.observacoes,
    )
    criado = repo_responsaveis.criar(responsavel, residente_id)
    return ResponsavelSaida(
        identificador=criado.identificador,
        nome_completo=criado.nome_completo,
        cpf=criado.cpf,
        parentesco=criado.parentesco,
        telefone=criado.telefone,
        email=criado.email,
        eh_responsavel_legal=criado.eh_responsavel_legal,
        eh_contato_emergencia=criado.eh_contato_emergencia,
    )


@roteador.get("/{residente_id}/responsaveis", response_model=list[ResponsavelSaida])
def listar_responsaveis(
    residente_id: int,
    repo_responsaveis=Depends(obter_repo_responsaveis),
    _funcionario=Depends(obter_funcionario_logado),
):
    itens = repo_responsaveis.listar_por_residente(residente_id)
    return [
        ResponsavelSaida(
            identificador=r.identificador,
            nome_completo=r.nome_completo,
            cpf=r.cpf,
            parentesco=r.parentesco,
            telefone=r.telefone,
            email=r.email,
            eh_responsavel_legal=r.eh_responsavel_legal,
            eh_contato_emergencia=r.eh_contato_emergencia,
        )
        for r in itens
    ]


@roteador.delete("/{residente_id}/responsaveis/{responsavel_id}", response_model=MensagemSimples)
def remover_vinculo(
    residente_id: int,
    responsavel_id: int,
    repo_responsaveis=Depends(obter_repo_responsaveis),
    _funcionario=Depends(obter_funcionario_logado),
):
    repo_responsaveis.excluir_vinculo(responsavel_id, residente_id)
    return MensagemSimples(mensagem="Vínculo removido.")
