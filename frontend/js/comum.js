/* Funções utilitárias compartilhadas. */

import { obterUsuario, limparSessao } from "./api.js";
import { icone } from "./icones.js";

// ----- Notificações -----

function obterBarra() {
  let barra = document.getElementById("barra-notificacoes");
  if (!barra) {
    barra = document.createElement("div");
    barra.id = "barra-notificacoes";
    barra.className = "barra-notificacoes";
    document.body.appendChild(barra);
  }
  return barra;
}

export function notificar(mensagem, tipo = "info", duracaoMs = 4500) {
  const barra = obterBarra();
  const elemento = document.createElement("div");
  elemento.className = `notificacao notificacao--${tipo}`;
  elemento.innerHTML = `
    <div style="flex:1">
      <strong style="display:block; font-size:0.92rem; color:var(--texto-principal)">
        ${tituloPorTipo(tipo)}
      </strong>
      <span style="color: var(--texto-secundario); font-size: 0.88rem">${escaparHTML(mensagem)}</span>
    </div>
    <button class="botao-fechar" aria-label="Fechar">&times;</button>
  `;
  barra.appendChild(elemento);
  const fechar = () => elemento.remove();
  elemento.querySelector(".botao-fechar").addEventListener("click", fechar);
  setTimeout(fechar, duracaoMs);
}

function tituloPorTipo(tipo) {
  return { sucesso: "Sucesso", perigo: "Erro", aviso: "Atenção", info: "Aviso" }[tipo] || "Aviso";
}

export function escaparHTML(texto) {
  if (texto === null || texto === undefined) return "";
  return String(texto)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// ----- Datas / formatos -----

export function formatarData(valor) {
  if (!valor) return "—";
  const d = typeof valor === "string" ? new Date(valor) : valor;
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString("pt-BR");
}

export function formatarDataHora(valor) {
  if (!valor) return "—";
  const d = typeof valor === "string" ? new Date(valor) : valor;
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

export function formatarMoeda(valor) {
  if (valor === null || valor === undefined) return "—";
  return Number(valor).toLocaleString("pt-BR", {
    style: "currency", currency: "BRL",
  });
}

export function formatarCPF(cpf) {
  if (!cpf || cpf.length !== 11) return cpf || "—";
  return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9)}`;
}

// ----- Tema -----

export function alternarTema() {
  const atual = document.documentElement.dataset.tema || "claro";
  const novo = atual === "claro" ? "escuro" : "claro";
  document.documentElement.dataset.tema = novo;
  localStorage.setItem("cuidarmais_tema", novo);
}

export function aplicarTemaSalvo() {
  const salvo = localStorage.getItem("cuidarmais_tema") || "claro";
  document.documentElement.dataset.tema = salvo;
}

// ----- Logout -----

export function sair() {
  limparSessao();
  window.location.href = "/login.html";
}

// ----- Cabeçalho do app (topo + barra lateral) -----

const ITENS_MENU = [
  { rotulo: "Painel", icone: "painel", url: "/paginas/dashboard.html", id: "dashboard", grupo: "Visão geral" },
  { rotulo: "Residentes", icone: "residentes", url: "/paginas/residentes.html", id: "residentes", grupo: "Cuidado" },
  { rotulo: "Medicação", icone: "medicacao", url: "/paginas/medicacao.html", id: "medicacao", grupo: "Cuidado" },
  { rotulo: "Consultas", icone: "consultas", url: "/paginas/consultas.html", id: "consultas", grupo: "Cuidado" },
  { rotulo: "Alimentação", icone: "alimentacao", url: "/paginas/alimentacao.html", id: "alimentacao", grupo: "Cuidado" },
  { rotulo: "Ocorrências", icone: "ocorrencias", url: "/paginas/ocorrencias.html", id: "ocorrencias", grupo: "Cuidado" },
  { rotulo: "Quartos", icone: "quartos", url: "/paginas/quartos.html", id: "quartos", grupo: "Operação" },
  { rotulo: "Escalas", icone: "escalas", url: "/paginas/escalas.html", id: "escalas", grupo: "Operação" },
  { rotulo: "Funcionários", icone: "funcionarios", url: "/paginas/funcionarios.html", id: "funcionarios", grupo: "Operação" },
  { rotulo: "Visitas", icone: "visitas", url: "/paginas/visitas.html", id: "visitas", grupo: "Operação" },
  { rotulo: "Financeiro", icone: "financeiro", url: "/paginas/financeiro.html", id: "financeiro", grupo: "Administração" },
  { rotulo: "Documentos", icone: "documentos", url: "/paginas/documentos.html", id: "documentos", grupo: "Administração" },
  { rotulo: "Auditoria", icone: "auditoria", url: "/paginas/auditoria.html", id: "auditoria", grupo: "Administração", apenas_admin: true },
];

export function montarLayout({ idPaginaAtiva, titulo, subtitulo } = {}) {
  const usuario = obterUsuario();
  if (!usuario) {
    window.location.href = "/login.html";
    return;
  }
  document.body.classList.add("tem-layout");

  const ehAdmin = usuario.papeis.includes("administrador");
  const itensVisiveis = ITENS_MENU.filter(item => !item.apenas_admin || ehAdmin);

  // Agrupa os itens do menu por seção (catálogo)
  const grupos = [];
  for (const item of itensVisiveis) {
    let g = grupos.find(x => x.nome === item.grupo);
    if (!g) { g = { nome: item.grupo, itens: [] }; grupos.push(g); }
    g.itens.push(item);
  }

  const htmlMenu = grupos.map(grupo => `
    <div class="menu__grupo">
      <h6>${escaparHTML(grupo.nome)}</h6>
      ${grupo.itens.map((item, i) => `
        <a href="${item.url}"
           class="menu__item ${item.id === idPaginaAtiva ? "menu__item--ativo" : ""}"
           style="--ordem:${i}">
          <span class="menu__item-icone" aria-hidden="true">${icone(item.icone, 19)}</span>
          <span>${item.rotulo}</span>
        </a>
      `).join("")}
    </div>
  `).join("");

  const elementoLayout = document.createElement("div");
  elementoLayout.className = "layout-aplicativo";
  elementoLayout.innerHTML = `
    <div class="cortina" id="cortina-menu" hidden></div>
    <aside class="barra-lateral" id="catalogo" aria-label="Catálogo de páginas">
      <div class="barra-lateral__logo">
        <div class="marca">${icone("coracao", 22)}</div>
        <div>
          <h1>Cuidar+</h1>
          <small>Lar de Idosos</small>
        </div>
        <button class="botao-fechar barra-lateral__fechar" id="btn-fechar-menu"
                aria-label="Fechar catálogo">${icone("fechar", 18)}</button>
      </div>
      <nav class="menu" aria-label="Menu principal">
        ${htmlMenu}
      </nav>
      <div class="barra-lateral__rodape">
        <button id="btn-tema" class="botao botao--fantasma" style="width:100%; justify-content:flex-start">
          <span aria-hidden="true">${icone("tema", 18)}</span> Alternar tema
        </button>
        <button id="btn-sair" class="botao botao--fantasma" style="width:100%; justify-content:flex-start">
          <span aria-hidden="true">${icone("sair", 18)}</span> Sair do sistema
        </button>
      </div>
    </aside>
    <main class="conteudo-principal">
      <header class="topo">
        <div class="topo__esquerda">
          <button class="botao botao--icone botao--fantasma" id="btn-abrir-menu"
                  aria-label="Abrir catálogo de páginas" aria-expanded="false"
                  aria-controls="catalogo">${icone("menu", 20)}</button>
          <div class="topo__titulo">
            <h2>${escaparHTML(titulo || "Cuidar+")}</h2>
            <p>${escaparHTML(subtitulo || "")}</p>
          </div>
        </div>
        <div class="topo__acoes">
          <div class="busca">
            <span aria-hidden="true">${icone("busca", 18)}</span>
            <input id="busca-global" placeholder="Buscar..." aria-label="Buscar" />
          </div>
          <div class="usuario-topo" role="button" tabindex="0" id="menu-usuario" title="Sair do sistema">
            <div class="avatar">${(usuario.nome_completo || "?").charAt(0)}</div>
            <div class="info">
              <span class="nome">${escaparHTML(usuario.nome_completo)}</span>
              <span class="papel">${escaparHTML(usuario.cargo)}</span>
            </div>
          </div>
        </div>
      </header>
      <section class="area-conteudo" id="area-conteudo"></section>
    </main>
  `;
  const areaExistente = document.getElementById("raiz") || document.body;
  areaExistente.appendChild(elementoLayout);

  // ----- Catálogo abre/fecha (drawer) -----
  const cortina = document.getElementById("cortina-menu");
  const botaoAbrir = document.getElementById("btn-abrir-menu");

  const abrirMenu = () => {
    elementoLayout.classList.add("menu-aberto");
    cortina.hidden = false;
    botaoAbrir.setAttribute("aria-expanded", "true");
  };
  const fecharMenu = () => {
    elementoLayout.classList.remove("menu-aberto");
    cortina.hidden = true;
    botaoAbrir.setAttribute("aria-expanded", "false");
  };

  botaoAbrir.addEventListener("click", abrirMenu);
  document.getElementById("btn-fechar-menu").addEventListener("click", fecharMenu);
  cortina.addEventListener("click", fecharMenu);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") fecharMenu(); });

  // ----- Ações -----
  document.getElementById("btn-tema").addEventListener("click", alternarTema);
  const aoSair = () => { if (confirm("Deseja sair do sistema?")) sair(); };
  document.getElementById("btn-sair").addEventListener("click", aoSair);
  document.getElementById("menu-usuario").addEventListener("click", aoSair);

  return document.getElementById("area-conteudo");
}

// ----- Confirmação -----

export function confirmar(mensagem) {
  return new Promise(resolver => {
    const fundo = document.createElement("div");
    fundo.className = "fundo-modal";
    fundo.innerHTML = `
      <div class="modal">
        <div class="modal__cabecalho">
          <h3>Confirmação</h3>
          <button class="botao-fechar" data-acao="cancelar">&times;</button>
        </div>
        <div class="modal__corpo"><p>${escaparHTML(mensagem)}</p></div>
        <div class="modal__rodape">
          <button class="botao botao--secundario" data-acao="cancelar">Cancelar</button>
          <button class="botao botao--perigo" data-acao="confirmar">Confirmar</button>
        </div>
      </div>
    `;
    document.body.appendChild(fundo);
    fundo.addEventListener("click", (e) => {
      const acao = e.target.dataset.acao;
      if (acao === "confirmar") { resolver(true); fundo.remove(); }
      else if (acao === "cancelar" || e.target === fundo) { resolver(false); fundo.remove(); }
    });
  });
}

// ----- Modal genérico -----

export function abrirModal({ titulo, conteudoHtml, larguraGrande = false, aoConfirmar, textoConfirmar = "Salvar" }) {
  return new Promise(resolver => {
    const fundo = document.createElement("div");
    fundo.className = "fundo-modal";
    fundo.innerHTML = `
      <div class="modal ${larguraGrande ? "modal--grande" : ""}">
        <div class="modal__cabecalho">
          <h3>${escaparHTML(titulo)}</h3>
          <button class="botao-fechar" data-acao="cancelar">&times;</button>
        </div>
        <div class="modal__corpo">${conteudoHtml}</div>
        <div class="modal__rodape">
          <button class="botao botao--secundario" data-acao="cancelar">Cancelar</button>
          <button class="botao" data-acao="confirmar">${escaparHTML(textoConfirmar)}</button>
        </div>
      </div>
    `;
    document.body.appendChild(fundo);
    const fechar = () => { resolver(null); fundo.remove(); };
    fundo.addEventListener("click", async (e) => {
      const acao = e.target.dataset.acao;
      if (acao === "cancelar" || e.target === fundo) { fechar(); }
      else if (acao === "confirmar") {
        const resultado = aoConfirmar ? await aoConfirmar(fundo) : null;
        if (resultado !== false) { resolver(resultado); fundo.remove(); }
      }
    });
  });
}

aplicarTemaSalvo();
