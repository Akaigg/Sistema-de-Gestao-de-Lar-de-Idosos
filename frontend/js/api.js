/* Cliente HTTP para a API do Cuidar+. */

const CHAVE_TOKEN = "cuidarmais_token";
const CHAVE_TOKEN_REFRESH = "cuidarmais_refresh";
const CHAVE_USUARIO = "cuidarmais_usuario";

export function salvarSessao({ token_acesso, token_refresh, funcionario }) {
  localStorage.setItem(CHAVE_TOKEN, token_acesso);
  localStorage.setItem(CHAVE_TOKEN_REFRESH, token_refresh);
  localStorage.setItem(CHAVE_USUARIO, JSON.stringify(funcionario));
}

export function limparSessao() {
  localStorage.removeItem(CHAVE_TOKEN);
  localStorage.removeItem(CHAVE_TOKEN_REFRESH);
  localStorage.removeItem(CHAVE_USUARIO);
}

export function obterToken() {
  return localStorage.getItem(CHAVE_TOKEN);
}

export function obterUsuario() {
  const dados = localStorage.getItem(CHAVE_USUARIO);
  if (!dados) return null;
  try { return JSON.parse(dados); } catch { return null; }
}

export function temPapel(papel) {
  const usuario = obterUsuario();
  if (!usuario) return false;
  if (usuario.papeis.includes("administrador")) return true;
  return usuario.papeis.includes(papel);
}

async function requisicao(metodo, caminho, { corpo, parametros } = {}) {
  const url = new URL(caminho, window.location.origin);
  if (parametros) {
    Object.entries(parametros).forEach(([chave, valor]) => {
      if (valor !== undefined && valor !== null && valor !== "") {
        url.searchParams.set(chave, valor);
      }
    });
  }
  const cabecalhos = { "Content-Type": "application/json" };
  const token = obterToken();
  if (token) cabecalhos["Authorization"] = `Bearer ${token}`;

  const resposta = await fetch(url.toString(), {
    method: metodo,
    headers: cabecalhos,
    body: corpo ? JSON.stringify(corpo) : undefined,
  });

  if (resposta.status === 401) {
    limparSessao();
    if (!window.location.pathname.endsWith("login.html")) {
      window.location.href = "/login.html";
    }
    throw new Error("Sessão expirada.");
  }

  let dados = null;
  const texto = await resposta.text();
  if (texto) {
    try { dados = JSON.parse(texto); } catch { dados = texto; }
  }
  if (!resposta.ok) {
    const mensagem =
      (dados && (dados.detalhe || dados.detail)) ||
      `Erro ${resposta.status}`;
    const erro = new Error(typeof mensagem === "string" ? mensagem : "Erro na requisição");
    erro.dados = dados;
    erro.status = resposta.status;
    throw erro;
  }
  return dados;
}

export const Api = {
  get: (caminho, parametros) => requisicao("GET", caminho, { parametros }),
  post: (caminho, corpo, parametros) => requisicao("POST", caminho, { corpo, parametros }),
  put: (caminho, corpo) => requisicao("PUT", caminho, { corpo }),
  delete: (caminho) => requisicao("DELETE", caminho),
};
