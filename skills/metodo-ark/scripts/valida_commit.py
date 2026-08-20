#!/usr/bin/env python3
"""Gate de commit — Método Ark. Conventional Commits, um commit atômico por task.

Uso:  python3 valida_commit.py --message "feat(checkout): adiciona stepper"
      python3 valida_commit.py --file .git/COMMIT_EDITMSG

Como guard do git (sem depender de agente):
      ln -s <skill>/scripts/valida_commit.py .git/hooks/commit-msg
"""
import argparse
import re
import sys

TIPOS = ["feat", "fix", "refactor", "perf", "docs", "test", "build", "ci", "chore", "revert"]
PADRAO = re.compile(rf"^({'|'.join(TIPOS)})(\([a-z0-9\-\.\/]+\))?(!)?: .+")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message")
    ap.add_argument("--file")
    ap.add_argument("rest", nargs="*")
    a = ap.parse_args()

    msg = a.message
    caminho = a.file or (a.rest[0] if a.rest else None)
    if not msg and caminho:
        with open(caminho, encoding="utf-8") as f:
            msg = f.read()
    if not msg:
        print("\033[31m✗\033[0m nada a validar (use --message ou --file)")
        sys.exit(1)

    linhas = [l for l in msg.splitlines() if not l.startswith("#")]
    titulo = (linhas[0] if linhas else "").strip()
    erros = []

    if not PADRAO.match(titulo):
        erros.append(f"título fora de Conventional Commits: '{titulo}'\n"
                     f"    esperado: tipo(escopo): descrição — tipos: {', '.join(TIPOS)}")
    if len(titulo) > 72:
        erros.append(f"título com {len(titulo)} caracteres (máximo 72)")
    if titulo.endswith("."):
        erros.append("título termina com ponto")

    desc = titulo.split(": ", 1)[1] if ": " in titulo else ""
    if desc[:1].isupper() and not desc[:2].isupper():
        erros.append("descrição começa com maiúscula (use minúscula)")
    if re.match(r"^\w+(ou|eu|iu|ado|ada|ando)\b", desc):
        erros.append(f"descrição não está no imperativo: '{desc[:30]}'")

    if len(linhas) > 1 and linhas[1].strip():
        erros.append("falta linha em branco entre título e corpo")

    for e in erros:
        print(f"  \033[31m✗\033[0m {e}")
    if erros:
        print("\n\033[31mcommit recusado.\033[0m Um commit atômico por task, "
              "sem agrupar e sem mudança de passagem.")
        sys.exit(1)
    print(f"\033[32m✓\033[0m commit ok — {titulo}")
    sys.exit(0)


if __name__ == "__main__":
    main()
