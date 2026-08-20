#!/usr/bin/env python3
"""Lições do projeto — Método Ark.

Estado canônico em .specs/memory/licoes.json (dono: máquina).
Render em .specs/memory/lessons.md (não editar à mão).

  registrar  --contexto <feature/task> --o-que <o que aconteceu>
             --licao <o que aprendemos> [--regra <enunciado candidato>]
  listar     [--estado observada|confirmada|promovida]
  promover   L-007 --para .specs/rules/como-executar.md
  render

Graduação: lição registrada de novo numa SEGUNDA feature distinta vira `confirmada`
automaticamente. Confirmada é candidata a virar regra — e sair daqui.
"""
import argparse
import json
import os
import re
import sys
from datetime import date

REL_JSON = os.path.join(".specs", "memory", "licoes.json")
REL_MD = os.path.join(".specs", "memory", "lessons.md")


def caminhos(raiz):
    return os.path.join(raiz, REL_JSON), os.path.join(raiz, REL_MD)


def carrega(pj):
    if not os.path.isfile(pj):
        return {"versao": 1, "licoes": []}
    with open(pj, encoding="utf-8") as f:
        return json.load(f)


def salva(pj, d):
    os.makedirs(os.path.dirname(pj), exist_ok=True)
    with open(pj, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def chave(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()


def feature_de(ctx):
    return (ctx or "").split("/")[0].strip().lower()


def render(d, pm):
    L = ["# Lições",
         "",
         "> Arquivo **renderizado** por `licoes.py`. Não editar à mão — o estado canônico",
         "> é `licoes.json`.",
         "",
         "> **Graduação:** lição que se repete numa segunda feature distinta vira",
         "> `confirmada`. Confirmada vira regra em `.specs/rules/` (processo) ou em",
         "> `AGENTS.md` (código), e sai daqui como referência.",
         ""]
    for est, titulo in [("confirmada", "Confirmadas — candidatas a virar regra"),
                        ("observada", "Observadas — uma ocorrência"),
                        ("promovida", "Promovidas — já viraram regra")]:
        itens = [l for l in d["licoes"] if l["estado"] == est]
        if not itens:
            continue
        L += [f"## {titulo}", ""]
        L += ["| # | Ocorrências | Contexto | O que aconteceu | O que aprendemos | Destino |",
              "|---|---|---|---|---|---|"]
        for l in itens:
            L.append(f"| {l['id']} | {len(l['ocorrencias'])} | "
                     f"{', '.join(sorted(set(l['ocorrencias'])))} | {l['o_que']} | "
                     f"{l['licao']} | {l.get('destino') or '—'} |")
        L.append("")
    os.makedirs(os.path.dirname(pm), exist_ok=True)
    with open(pm, "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["registrar", "listar", "promover", "render"])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--root", default=".")
    ap.add_argument("--contexto")
    ap.add_argument("--o-que", dest="o_que")
    ap.add_argument("--licao")
    ap.add_argument("--regra")
    ap.add_argument("--para")
    ap.add_argument("--estado")
    a = ap.parse_args()

    pj, pm = caminhos(a.root)
    d = carrega(pj)

    if a.cmd == "registrar":
        if not (a.contexto and a.o_que and a.licao):
            print("faltam --contexto, --o-que e --licao")
            sys.exit(1)
        k = chave(a.licao)
        feat = feature_de(a.contexto)
        for l in d["licoes"]:
            if chave(l["licao"]) == k:
                l["ocorrencias"].append(a.contexto)
                feats = {feature_de(o) for o in l["ocorrencias"]}
                if len(feats) >= 2 and l["estado"] == "observada":
                    l["estado"] = "confirmada"
                    print(f"\033[33m↑\033[0m {l['id']} promovida a CONFIRMADA "
                          f"(2ª feature distinta). Candidata a virar regra.")
                else:
                    print(f"\033[32m✓\033[0m {l['id']} — ocorrência registrada")
                salva(pj, d)
                render(d, pm)
                return
        novo = {
            "id": f"L-{len(d['licoes']) + 1:03d}",
            "data": date.today().isoformat(),
            "ocorrencias": [a.contexto],
            "o_que": a.o_que,
            "licao": a.licao,
            "regra_candidata": a.regra,
            "estado": "observada",
            "destino": None,
        }
        d["licoes"].append(novo)
        salva(pj, d)
        render(d, pm)
        print(f"\033[32m✓\033[0m {novo['id']} registrada (observada)")

    elif a.cmd == "listar":
        itens = [l for l in d["licoes"] if not a.estado or l["estado"] == a.estado]
        if not itens:
            print("nenhuma lição.")
            return
        for l in itens:
            print(f"{l['id']} [{l['estado']}] ({len(l['ocorrencias'])}x) {l['licao']}")

    elif a.cmd == "promover":
        if not (a.id and a.para):
            print("uso: promover L-007 --para .specs/rules/como-executar.md")
            sys.exit(1)
        for l in d["licoes"]:
            if l["id"] == a.id:
                if l["estado"] == "observada":
                    print(f"\033[31m✗\033[0m {a.id} ainda é observada. "
                          "Promova só na segunda ocorrência — uma vez é acaso.")
                    sys.exit(1)
                l["estado"] = "promovida"
                l["destino"] = a.para
                salva(pj, d)
                render(d, pm)
                print(f"\033[32m✓\033[0m {a.id} promovida → {a.para}. "
                      "Escreva a regra lá agora.")
                return
        print(f"\033[31m✗\033[0m {a.id} não existe.")
        sys.exit(1)

    elif a.cmd == "render":
        render(d, pm)
        print(f"\033[32m✓\033[0m {pm}")


if __name__ == "__main__":
    main()
