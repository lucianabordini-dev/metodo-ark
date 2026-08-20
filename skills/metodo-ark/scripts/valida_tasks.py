#!/usr/bin/env python3
"""Gate das tasks — Método Ark.

Uso:  python3 valida_tasks.py <caminho-tasks|nome-da-feature> [--root .]

Cobra: domínio válido por task, AC vinculado, sem dependência para frente,
"pronto quando" preenchido, e alerta de paralelismo no mesmo domínio.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comum import DOMINIOS, Relatorio, le, linhas_tabela, normaliza, resolve


def num(t):
    m = re.fullmatch(r"[Tt](\d+)", t.strip())
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()

    p = resolve(a.alvo, a.root, "features", "tasks.md")
    if not p:
        print(f"\033[31m✗\033[0m tasks.md não encontrado: {a.alvo}")
        sys.exit(1)

    texto = le(p)
    r = Relatorio(f"tasks ok — {p}", f"tasks {p}")

    linhas = linhas_tabela(texto)
    if not linhas:
        print("\033[31m✗\033[0m nenhuma task na tabela.")
        sys.exit(1)

    vistos, dominio_de, deps_de = [], {}, {}
    for cels in linhas:
        if len(cels) < 5:
            r.erro(f"linha incompleta: {' | '.join(cels)[:60]}")
            continue
        tid, dom, titulo, dep, ac = cels[0], cels[1], cels[2], cels[3], cels[4]
        n = num(tid)
        if n is None:
            r.erro(f"ID de task malformado: '{tid}' (esperado T1, T2, ...)")
            continue
        if n in vistos:
            r.erro(f"{tid} duplicada.")
        vistos.append(n)

        nd = normaliza(dom)
        if nd not in DOMINIOS:
            r.erro(f"{tid}: domínio inválido '{dom}'. Válidos: {', '.join(sorted(DOMINIOS))}")
        dominio_de[n] = nd

        if not titulo.strip():
            r.erro(f"{tid}: sem título.")
        if not ac.strip() or ac.strip() in ("-", "—"):
            r.erro(f"{tid}: nenhum AC vinculado. Task que não atende AC não deveria existir.")

        alvos = [num(x) for x in re.split(r"[,\s]+", dep) if num(x) is not None]
        deps_de[n] = alvos
        for al in alvos:
            if al >= n:
                r.erro(f"{tid}: depende de T{al}, que vem depois. Dependência para frente.")
            if al not in vistos and al > 0:
                r.erro(f"{tid}: depende de T{al}, que não existe na tabela.")

    # granularidade: cada task precisa de "pronto quando"
    for n in vistos:
        bloco = re.search(rf"###\s*T{n}\b(.*?)(?=\n###|\Z)", texto, re.S)
        if not bloco:
            r.aviso(f"T{n}: sem detalhe abaixo da tabela.")
        elif "pronto quando" not in normaliza(bloco.group(1)):
            r.erro(f"T{n}: sem 'Pronto quando'. Sem o comando que prova, a task não tem gate.")

    # paralelismo no mesmo domínio sem dependência declarada
    for i, n1 in enumerate(vistos):
        for n2 in vistos[i + 1:]:
            if dominio_de.get(n1) and dominio_de.get(n1) == dominio_de.get(n2):
                if n1 not in deps_de.get(n2, []):
                    r.aviso(f"T{n1} e T{n2} são do mesmo domínio ({dominio_de[n1]}) "
                            "e não têm dependência entre si — rode em sequência, "
                            "salvo se comprovadamente não tocam os mesmos arquivos.")
                break

    r.fim()


if __name__ == "__main__":
    main()
