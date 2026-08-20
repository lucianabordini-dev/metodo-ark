# Método Ark

**Código virou commodity. Pensar, não.**
O software começa antes do prompt.

Uma **Agent Skill** que ensina o agente a construir software profissional com IA — sem terceirizar o pensamento. Padrão aberto `SKILL.md`: funciona em Claude Code, Codex CLI, Cursor, Antigravity e qualquer agente que leia o formato.

---

## O problema

Você pede uma feature. Vinte minutos depois recebe arquivos alterados, decisões implícitas, dependências novas e testes que passaram. E precisa decidir se aquilo está certo, tendo como única evidência o output cru.

Aí acontece uma de duas coisas: você confia sem ler, e a dívida aparece semanas depois; ou lê tudo, e vira gargalo humano de um processo que só existe para ser rápido.

Nenhuma das duas é decisão. As duas são desistência.

O Método Ark resolve registrando a intenção **antes** — porque só dá para julgar o depois quando existe um antes escrito.

---

## Instalação

```bash
npx metodo-ark install
```

Instala em `~/.claude/skills/`. Outros alvos:

```bash
npx metodo-ark install --agent codex      # ~/.codex/skills/
npx metodo-ark install --agent cursor     # <projeto>/.cursor/skills/
npx metodo-ark install --agent projeto    # <projeto>/.agents/skills/ — versionado, o time inteiro pega no git pull
npx metodo-ark install --agent all        # claude + codex
```

Montar o harness num projeto:

```bash
npx metodo-ark harness .    # cria .specs/, .agents/, AGENTS.md e CLAUDE.md
npx metodo-ark mirror .     # espelha .agents/skills em .claude/skills por symlink
```

<details>
<summary>Instalar na mão, sem npm</summary>

```bash
git clone https://github.com/lucianabordini-dev/metodo-ark.git /tmp/ma
cp -R /tmp/ma/skills/metodo-ark ~/.claude/skills/
```

| Agente | Destino |
|---|---|
| Claude Code · Claude Desktop | `~/.claude/skills/metodo-ark/` |
| Codex CLI | `~/.codex/skills/metodo-ark/` |
| Cursor | `<projeto>/.cursor/skills/metodo-ark/` |
| Projeto (qualquer agente) | `<projeto>/.agents/skills/metodo-ark/` |

O erro mais comum é aninhar um nível a mais. O `SKILL.md` fica em `.../skills/metodo-ark/SKILL.md`.

</details>

O espelho em `.claude/` é artefato local — não versione. Em Windows, symlink versionado só sobrevive ao clone com `core.symlinks=true` e Developer Mode; sem isso o Git materializa o link como arquivo de texto e o agente lê uma linha achando que é a skill, sem dar erro.

---

## Uso

Depois de instalada, a skill ativa sozinha quando a conversa entra no território dela. Para chamar direto:

```
usando o Método Ark, monta o harness deste projeto
usando o Método Ark, escreve a Fundação
quais regras de negócio dá pra extrair disto?
essa feature precisa de arquitetura?
valida a implementação contra a spec
```

---

## O método em uma tela

### Duas altitudes

| Altitude | Frequência | Produz |
|---|---|---|
| **Produto** | Uma vez por produto | Documentos de origem + harness |
| **Iniciativa** | Toda vez que há trabalho | Uma feature, um fix, um refactor |

### Duas portas

O que muda entre projetos não é o dono do produto — é **como se chega à dor**.

> *Consigo hoje conversar com quem vive essa dor, ou sou eu mesmo?*
> **Sim → Extração. Não → Descoberta.**

Descoberta ganha um MVP Scope, documento com poder de **matar o projeto**. Extração não — quando a dor já chegou, a decisão de construir já foi tomada.

### O ciclo

```
Iniciativa → Conversação → Spec → Arquitetura* → Tasks → Execução → Validação → Conhecimento
```

Kit mínimo por cenário: produto do zero leva os quatro artefatos, bug leva task e validação, spike não produz software nenhum.

### A regra que sustenta tudo

**Autor ≠ verificador. Evidência ou zero. E o verificador nunca conserta.**

Evidência é comando executado com a saída, assert ancorado no valor que a spec declara, e mutação no código que mata o teste. Relato do agente sobre o próprio trabalho não é evidência — é sinal.

---

## O que vem na skill

```
skills/metodo-ark/
├── SKILL.md
├── references/          tese-e-metodo · regras-de-negocio · harness
├── templates/           fundação, spec, arquitetura, tasks, validação,
│                        AGENTS.md, rules/ e memory/
└── scripts/             gates determinísticos, em Python puro
```

### Gates cobrados por código

Regra estrutural que depende do modelo lembrar não é gate. Cinco scripts, sem dependência externa:

| Script | Cobra |
|---|---|
| `valida_spec.py` | cenário declarado, seções obrigatórias, AC com outcome observável e valor concreto, zero placeholder |
| `valida_tasks.py` | domínio válido, AC vinculado, sem dependência para frente, "pronto quando" preenchido, alerta de paralelismo |
| `valida_commit.py` | Conventional Commits — também roda como git hook, sem agente |
| `valida_encerramento.py` | validação existe, veredito PASS, evidência `file:line`, sensor rodado em caminho crítico, gaps vazios, conhecimento atualizado |
| `licoes.py` | registra lições e **gradua automaticamente**: mesma lição em segunda feature distinta vira `confirmada`, candidata a virar regra |

Saída diferente de zero significa parar e corrigir — nunca seguir e anotar.

A skill cria `.specs/` no **seu** projeto — ela não traz um `.specs/` pronto, porque a estrutura é do projeto, não do método.

---

## Leitura

| Documento | Sobre |
|---|---|
| [tese-e-metodo.md](skills/metodo-ark/references/tese-e-metodo.md) | O método completo |
| [regras-de-negocio.md](skills/metodo-ark/references/regras-de-negocio.md) | Como ouvir, escrever e tipar regra de negócio |
| [harness.md](skills/metodo-ark/references/harness.md) | Por que cada pasta existe |

---

## O que este método não é

- Não é curso de prompt. Prompts são detalhe de implementação.
- Não é "aprenda a programar". A IA programa; você aprende a pensar.
- Não é vibe coding glorificado. É o antídoto do vibe coding.
- Não é teoria acadêmica. Tudo nasce de projeto real, com nome, tela e código.

## Licença

MIT — ver [LICENSE](LICENSE).
