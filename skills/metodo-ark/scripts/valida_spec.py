#!/usr/bin/env python3
"""Gate de fechamento da spec — Método Ark.

Uso:  python3 valida_spec.py <caminho-da-spec|nome-da-feature> [--root .]

Cobra o que não pode depender de memória: cenário declarado, seções obrigatórias,
ACs com outcome observável e valor concreto, IDs bem formados, zero placeholder.
"""
import argparse
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comum import (CENARIOS, PLACEHOLDERS, Relatorio, acha_secao, le,
                    linhas_tabela, normaliza, resolve, secoes)

OBRIGATORIAS = [
    (("decisoes", "decisao"), "Decisões e porquês"),
    (("o que isto toca", "toca"), "O que isto toca"),
    (("problema",), "O problema"),
    (("comportamento",), "Comportamento esperado"),
    (("fora de escopo",), "Fora de escopo"),
    (("criterios de aceite", "aceite"), "Critérios de aceite"),
    (("teste independente",), "Teste independente"),
]

VAGO = ["funciona corretamente", "funciona bem", "esta correto", "sem erros",
        "conforme esperado", "adequadamente", "corretamente"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()

    p = resolve(a.alvo, a.root, "features", "spec.md")
    if not p:
        print(f"\033[31m✗\033[0m spec não encontrada: {a.alvo}")
        sys.exit(1)

    texto = le(p)
    r = Relatorio(f"spec ok — {p}", f"spec {p}")
    mapa = secoes(texto)
    n = normaliza(texto)

    # cenário declarado e válido
    m = re.search(r"\*\*cenario\*\*\s*:?\s*([^\n|]+)", n)
    if not m:
        r.erro("cenário não declarado. Sem cenário, o kit mínimo vira o mais leve por omissão.")
    else:
        decl = m.group(1)
        if not any(c in decl for c in CENARIOS):
            r.erro(f"cenário não reconhecido: '{m.group(1).strip()}'. "
                   f"Válidos: {', '.join(CENARIOS)}")
        elif "produto do zero" in decl or "arquitetura" in decl:
            d = os.path.join(os.path.dirname(p), "arquitetura.md")
            if not os.path.isfile(d):
                r.erro("este cenário exige arquitetura.md, que não existe.")

    # seções obrigatórias
    for chaves, rotulo in OBRIGATORIAS:
        corpo = acha_secao(mapa, *chaves)
        if corpo is None:
            r.erro(f"seção ausente: {rotulo}")
        elif not corpo.strip():
            r.erro(f"seção vazia: {rotulo}")

    # critérios de aceite
    acs = acha_secao(mapa, "criterios de aceite", "aceite") or ""
    linhas = linhas_tabela(acs)
    ids = []
    if not linhas:
        r.erro("nenhum critério de aceite. Spec sem AC não é verificável.")
    for cels in linhas:
        cid = cels[0]
        if not re.fullmatch(r"[A-Z]\d+", cid):
            r.erro(f"ID de AC malformado: '{cid}' (esperado letra+número, ex. A1)")
            continue
        ids.append(cid)
        outcome = cels[1] if len(cels) > 1 else ""
        if not outcome.strip():
            r.erro(f"{cid}: outcome vazio.")
            continue
        no = normaliza(outcome)
        if any(v in no for v in VAGO):
            r.erro(f"{cid}: outcome vago ('{outcome[:40]}...'). "
                   "AC precisa de resultado observável, não de adjetivo.")
        elif not re.search(r"[\d`\"']", outcome):
            r.aviso(f"{cid}: outcome sem valor concreto. "
                    "Um AC sem número, string ou identificador é difícil de assertar.")
    if len(ids) != len(set(ids)):
        r.erro("IDs de AC repetidos.")

    # regras de negócio referenciadas
    for rn in set(re.findall(r"RN-[A-Za-z]+\d+", texto)):
        if not re.fullmatch(r"RN-[VITA]\d{2,}", rn):
            r.aviso(f"referência de regra fora do padrão: {rn} "
                    "(esperado RN-V, RN-I, RN-T ou RN-A + número)")

    # placeholders
    achados = set()
    for pat in PLACEHOLDERS:
        achados |= set(re.findall(pat, texto, re.I))
    achados = {a for a in achados
               if not any(a != b and a.lower() in b.lower() for b in achados)}
    for achado in sorted(achados):
        if True:
            r.erro(f"placeholder não preenchido: {achado}")

    r.fim()


if __name__ == "__main__":
    main()
