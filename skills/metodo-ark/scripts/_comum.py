"""Utilidades compartilhadas pelos gates do Método Ark."""
import os
import re
import sys

CENARIOS = {
    "produto do zero": {"spec", "arquitetura", "tasks", "validacao"},
    "feature com arquitetura": {"spec", "arquitetura", "tasks", "validacao"},
    "feature no padrao": {"spec", "tasks", "validacao"},
    "refactor": {"arquitetura", "tasks", "validacao"},
    "bug": {"tasks", "validacao"},
    "spike": set(),
}

DOMINIOS = {"banco", "back-end", "front-end", "regra de negocio", "arquitetura", "infra"}

CAMINHO_CRITICO = [
    "pagamento", "cobranca", "cartao", "auth", "autenticacao", "autorizacao",
    "permissao", "migration", "migracao", "dado sensivel", "credencial",
    "segredo", "contencao", "bloqueio", "invariante",
]

PLACEHOLDERS = [r"\{[a-z\-]+\}", r"\bTODO\b", r"\bTBD\b", r"XXX", r"preencher"]


def normaliza(t):
    """Minúsculas sem acento, para comparar rótulo escrito de qualquer jeito."""
    t = t.lower()
    for a, b in [("á", "a"), ("à", "a"), ("â", "a"), ("ã", "a"), ("é", "e"),
                 ("ê", "e"), ("í", "i"), ("ó", "o"), ("ô", "o"), ("õ", "o"),
                 ("ú", "u"), ("ç", "c")]:
        t = t.replace(a, b)
    return t


def resolve(caminho, raiz, sub, arquivo):
    """Aceita caminho completo OU só o nome da feature."""
    if os.path.isfile(caminho):
        return caminho
    p = os.path.join(raiz, ".specs", sub, caminho, arquivo)
    if os.path.isfile(p):
        return p
    return None


def le(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def secoes(texto):
    """Mapa {titulo normalizado: corpo} a partir dos headings markdown."""
    out, atual, buf = {}, None, []
    for linha in texto.splitlines():
        m = re.match(r"^#{1,4}\s+(.*)$", linha)
        if m:
            if atual is not None:
                out[atual] = "\n".join(buf)
            atual = normaliza(re.sub(r"^\d+\.\s*", "", m.group(1)).strip())
            buf = []
        else:
            buf.append(linha)
    if atual is not None:
        out[atual] = "\n".join(buf)
    return out


def acha_secao(mapa, *chaves):
    for k, v in mapa.items():
        if any(c in k for c in chaves):
            return v
    return None


def linhas_tabela(corpo):
    """Linhas de dados de uma tabela markdown (sem cabeçalho nem separador)."""
    out = []
    for l in (corpo or "").splitlines():
        l = l.strip()
        if not l.startswith("|") or set(l) <= set("|-: "):
            continue
        cels = [c.strip() for c in l.strip("|").split("|")]
        out.append(cels)
    return out[1:] if out else []


class Relatorio:
    def __init__(self, titulo, alvo=None):
        self.titulo = titulo
        self.alvo = alvo or titulo
        self.erros = []
        self.avisos = []

    def erro(self, msg):
        self.erros.append(msg)

    def aviso(self, msg):
        self.avisos.append(msg)

    def fim(self):
        for a in self.avisos:
            print(f"  \033[33m!\033[0m {a}")
        for e in self.erros:
            print(f"  \033[31m✗\033[0m {e}")
        if self.erros:
            print(f"\n\033[31m{self.alvo}: {len(self.erros)} bloqueio(s).\033[0m "
                  "Corrija antes de seguir.")
            sys.exit(1)
        print(f"\033[32m✓\033[0m {self.titulo}" +
              (f" — {len(self.avisos)} aviso(s)" if self.avisos else ""))
        sys.exit(0)
