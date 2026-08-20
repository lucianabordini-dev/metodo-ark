# O Harness
### A estrutura que transforma documentos em algo que a IA obedece
*Método Ark · v3*

---

O harness é o que separa "escrevi uma spec" de "o agente executa dentro do padrão". Ele vive no repositório, em arquivos versionados, em convenções abertas — nada de formato proprietário, nada preso a uma ferramenta.

```
projeto/
├── .agents/                    FONTE DA VERDADE — convenção aberta e portátil
│   ├── skills/
│   └── workflows/
├── .claude/skills/             espelho por symlink (só se usar Claude Code)
├── .specs/                     o método
│   ├── archive/                features encerradas
│   ├── features/               features em curso
│   │   └── <nome-da-feature>/
│   │       ├── spec.md
│   │       ├── arquitetura.md      (condicional — ver matriz de cenário)
│   │       ├── tasks.md
│   │       └── validation.md
│   ├── memory/                 o que é verdade hoje
│   │   ├── produto.md
│   │   ├── estrutura.md
│   │   ├── domain-model.md
│   │   ├── decisoes.md
│   │   ├── lessons.md
│   │   └── origem/             congelado — o histórico
│   │       ├── mvp-scope.md        (só porta Descoberta)
│   │       ├── fundacao.md
│   │       ├── prd.md
│   │       └── base-tecnica.md
│   ├── rules/                  regras do método neste projeto
│   └── templates/              modelos de spec, arquitetura, tasks, validação
├── AGENTS.md                   regras do código e do repositório (canônico)
└── CLAUDE.md                   stub que importa AGENTS.md
```

---

## `.agents/` é capacidade. `.specs/` é estado.

`.agents/` guarda o que a IA **sabe fazer** — skills e workflows, portáteis entre projetos. `.specs/` guarda o que **é verdade neste projeto** — conhecimento, regras e artefatos do método.

Uma skill viaja. Uma spec não.

### `.agents/` nasce com o projeto e é a fonte da verdade

Ela é convenção aberta: qualquer agente lê. `.claude/skills/` não é uma segunda cópia — é um **espelho por symlink**, criado apenas se você usa Claude Code, e existe por uma razão prática: skill em `.claude/skills/` pode ser invocada por comando no chat, o que muda o custo de usar o método no dia a dia.

```bash
mkdir -p .claude/skills
ln -s ../../.agents/skills/<skill> .claude/skills/<skill>
```

O symlink aponta **por skill**, não pela pasta inteira: o agente segue o link, lê o `SKILL.md` no destino, e carrega a skill uma vez só mesmo quando o mesmo alvo é alcançável por mais de um caminho. Mesma lógica vale para `~/.codex/skills/` e `.cursor/skills/`.

> ⚠️ **Armadilha em repositório compartilhado (Windows).** Symlink versionado só sobrevive ao clone com `git config core.symlinks true` e Developer Mode ligado. Sem isso, o Git materializa o link como **arquivo de texto contendo o caminho** — e o agente lê um arquivo de uma linha achando que é a skill, sem erro nenhum. Falha silenciosa, do tipo mais caro.
>
> Em repositório que outras pessoas clonam: versione `.agents/` e gere o espelho por script de setup. O symlink vira artefato local, nunca conteúdo do repositório.

**Regra derivada:** skill nova entra em `.agents/skills/`. Se o espelho existe, é ele que aponta para lá — nunca o contrário. Skill que nasce direto em `.claude/` fica invisível para todo agente que não seja o Claude Code, e o projeto perde a portabilidade sem ninguém perceber.

---

## Origem é congelada. Memory é o presente.

Esta é a regra que resolve a pergunta "atualizar ou descartar os documentos de fundação": **nem um, nem outro.**

Os documentos em `origem/` são **registro histórico**: por que este produto existe, o que se acreditava quando ele começou, quais decisões fundaram a arquitetura. Eles não são atualizados. Quando `origem/` e `memory/` divergem, isso não é inconsistência — é a biografia do produto, e é o que permite entender uma decisão estranha três anos depois.

| Congelado em `origem/` | Vive em `memory/` |
|---|---|
| `fundacao.md` + `prd.md` | `produto.md` |
| `base-tecnica.md` | `estrutura.md` |

> ⚠️ **Aviso obrigatório no topo de cada arquivo de `origem/`:**
> *"Documento histórico. Registra o que foi decidido no início do projeto e **não** reflete necessariamente o estado atual. Para o estado atual, ler `memory/produto.md` e `memory/estrutura.md`."*
>
> Sem esse aviso, a IA lê um PRD de um ano atrás como se fosse requisito vigente. É a forma mais silenciosa de um harness envenenar a própria execução.

**O Domain Model é a exceção e fica em `memory/`.** Nasce junto com os documentos de origem, mas é o único doc de produto que muda toda semana: entidade nova, estado novo, relação nova. Congelá-lo seria congelar o mapa do território enquanto o território anda.

---

## Os arquivos de memória

| Arquivo | O que é | Origem | Erro que previne |
|---|---|---|---|
| **`produto.md`** | O produto em linguagem natural: visão, problema que resolve, capacidades, para quem, fluxos, por que existe | Fundação + PRD, mantidos vivos | IA que implementa feature sem entender o produto |
| **`estrutura.md`** | A estrutura-alvo do repositório: módulos, responsabilidades, onde cada coisa mora | Base Técnica, mantida viva | Arquivo criado no lugar errado; padrão que se dissolve |
| **`domain-model.md`** | Entidades, estados, relações, invariantes do domínio | Documentos de origem, vivo | Software que não reflete a realidade do negócio |
| **`decisoes.md`** | Decisões arquiteturais numeradas: data, decisão, razão, trade-off, escopo. Inclui o checklist de produção | Julgamento humano | Decisão revogada em silêncio; a próxima pessoa copiando o padrão antigo |
| **`lessons.md`** | O que aprendemos com o que deu errado | Falha de validação, divergência recorrente | Repetir o mesmo erro em feature diferente |

**Por que `decisoes.md` é um arquivo separado.** Decisão não é lição (lição vem de erro) nem produto (produto é o quê, não o porquê). Quando uma invariante que sustentava um programa inteiro é revogada por decisão de produto, isso não cabe em nenhum dos outros dois — e precisa estar escrito, com data e razão, ou a próxima pessoa reimplanta o comportamento antigo achando que está seguindo o padrão.

---

## `lessons.md` e a graduação de lição para regra

Lições são gravadas **por gatilho automático**, ao fim de cada execução e de cada validação — nunca por disciplina de quem lembra de escrever. Um script no repositório faz o append; o que o dispara é hook do agente, não vontade humana.

O que uma lição registra: data, contexto (feature, task), o que aconteceu, o que se aprendeu e o estado (`observada` ou `confirmada`).

**A regra que impede o arquivo de virar lixão:**

> Lição que se repete numa **segunda feature distinta** é promovida: vira regra em `.specs/rules/` (se for processo) ou em `AGENTS.md` (se for código), e sai de `lessons.md` como referência.

Sem graduação, `lessons.md` cresce para sempre, ninguém lê, e o conhecimento fica arquivado em vez de aplicado. Com graduação, o arquivo mede a maturidade do projeto: lição promovida é aprendizado que virou estrutura.

---

## Onde cada regra mora — sem sobreposição

Duas fontes de regra é como uma delas fica desatualizada em silêncio.

| Local | Governa | Exemplos |
|---|---|---|
| **`AGENTS.md`** (canônico) | Código e repositório | Arquitetura em uma frase, regras transversais não-negociáveis, gates, invariantes, branch e commits |
| **`.specs/rules/`** | O método neste projeto | Como executar uma spec, o que a matriz de cenário exige, nomenclatura de feature, formato de evidência, o que o verificador não pode fazer |
| **`CLAUDE.md`** | Nada | Stub que importa `AGENTS.md` |

**Regra dura: cada regra mora num lugar só.** Se um espelho for necessário para uma ferramenta que não lê nenhum dos dois, ele declara no topo que é espelho, aponta o canônico, e o mesmo commit atualiza os dois.

---

## Ordem de montagem

1. `.agents/skills/` e `.specs/` (as pastas vazias, versionadas com `.gitkeep`)
2. `AGENTS.md` com a arquitetura em uma frase — mesmo que seja só isso no dia um
3. `CLAUDE.md` como stub de uma linha
4. Os documentos de origem em `.specs/memory/origem/`, com o aviso de histórico no topo
5. `produto.md` e `estrutura.md` derivados deles
6. `domain-model.md`
7. `decisoes.md` e `lessons.md` vazios, com o cabeçalho de formato
8. `rules/` e `templates/` copiados do scaffold e ajustados ao projeto
9. O espelho `.claude/skills/` por symlink, se aplicável — local, não versionado

A partir daí, toda iniciativa entra por `features/` e sai por `archive/`.
