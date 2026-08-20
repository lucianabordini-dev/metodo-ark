#!/usr/bin/env python3
"""Gate de encerramento da iniciativa — Método Ark.

Uso:  python3 valida_encerramento.py <nome-da-feature> [--root .]

Uma feature só está pronta quando a validação existe, o veredito é PASS,
a evidência é citável (file:line), o sensor rodou onde é obrigatório,
a lista de gaps está vazia e o conhecimento foi atualizado.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _comum import (CAMINHO_CRITICO, PLACEHOLDERS, Relatorio, acha_secao, le,
                    linhas_tabela, normaliza, secoes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feature")
    ap.add_argument("--root", default=".")
    a = ap.parse_args()

    dirf = os.path.join(a.root, ".specs", "features", a.feature)
    if not os.path.isdir(dirf):
        dirf = a.feature if os.path.isdir(a.feature) else None
    if not dirf:
        print(f"\033[31m✗\033[0m feature não encontrada: {a.feature}")
        sys.exit(1)

    pv = os.path.join(dirf, "validation.md")
    if not os.path.isfile(pv):
        print(f"\033[31m✗\033[0m sem validation.md. "
              "Feature sem validação independente não encerra — autor ≠ verificador.")
        sys.exit(1)

    texto = le(pv)
    n = normaliza(texto)
    r = Relatorio(f"encerramento ok — {a.feature}", f"encerramento de {a.feature}")
    mapa = secoes(texto)

    # veredito
    m = re.search(r"\*\*veredito\*\*\s*:?\s*([^\n]+)", n)
    if not m:
        r.erro("veredito não declarado.")
    else:
        v = m.group(1)
        if "fail" in v:
            r.erro("veredito FAIL — a feature não encerra assim.")
        elif "pass" not in v:
            r.erro(f"veredito não preenchido: '{m.group(1).strip()[:40]}'")

    # evidência citável
    if not re.search(r"[\w/\.\-]+:\d+", texto):
        r.erro("nenhuma evidência no formato file:line. "
               "Relato do agente sobre o próprio trabalho não é evidência.")

    # comandos com saída
    ev = acha_secao(mapa, "evidencia fresca", "evidencia")
    if not ev or not linhas_tabela(ev):
        r.erro("sem tabela de evidência fresca executada pelo verificador.")
    else:
        tem_numero = any(re.search(r"\d", (c[1] if len(c) > 1 else ""))
                         for c in linhas_tabela(ev))
        if not tem_numero:
            r.erro("evidência sem número. 'Gate verde' não conta; "
                   "precisa do comando e da saída.")

    # ACs
    acs = acha_secao(mapa, "criterios de aceite", "aceite")
    linhas = linhas_tabela(acs) if acs else []
    if not linhas:
        r.erro("sem tabela de ACs ancorados na spec.")
    else:
        pend = [c[0] for c in linhas
                if len(c) > 3 and not re.search(r"✅|pass|ok", normaliza(c[3]))]
        if pend:
            r.erro(f"AC sem resultado aprovado: {', '.join(pend)}. "
                   "Evidência parcial é gap nomeado, não PASS com asterisco.")

    # sensor de discriminação
    critico = any(t in n for t in CAMINHO_CRITICO)
    sensor = acha_secao(mapa, "sensor")
    mut = linhas_tabela(sensor) if sensor else []
    if critico and not mut:
        r.erro("caminho crítico sem sensor de discriminação. "
               "Teste que passa igual com o código quebrado é evidência vazia.")
    elif mut:
        vivas = [c[0] for c in mut
                 if len(c) > 3 and "killed" not in normaliza(c[3])]
        if vivas:
            r.erro(f"mutação que não matou o teste: {', '.join(vivas)}. "
                   "O assert não discrimina.")
    elif not critico:
        r.aviso("sem sensor de discriminação (permitido fora de caminho crítico).")

    # gaps
    gaps = acha_secao(mapa, "gaps")
    if gaps and gaps.strip():
        corpo = "\n".join(l for l in gaps.splitlines()
                          if l.strip() and not l.strip().startswith(">"))
        if corpo.strip() and "vazia" not in normaliza(corpo):
            r.erro("lista de gaps não está vazia.")

    # conhecimento atualizado
    conh = acha_secao(mapa, "conhecimento")
    if not conh:
        r.erro("sem checklist de conhecimento a atualizar.")
    elif "- [ ]" in conh:
        naos = [l.strip()[6:] for l in conh.splitlines() if l.strip().startswith("- [ ]")]
        r.erro("conhecimento não atualizado: " + "; ".join(naos[:4]))

    # placeholders
    achados = set()
    for pat in PLACEHOLDERS:
        achados |= set(re.findall(pat, texto, re.I))
    achados = {a for a in achados
               if not any(a != b and a.lower() in b.lower() for b in achados)}
    for achado in sorted(achados):
        if True:
            r.erro(f"placeholder no relatório de validação: {achado}")

    r.fim()


if __name__ == "__main__":
    main()
