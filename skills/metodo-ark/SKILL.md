---
name: metodo-ark
description: Método Ark — construir software profissional com IA sem terceirizar o pensamento. Duas altitudes (produto e iniciativa), duas portas de entrada (Descoberta e Extração), regras de negócio tipadas como semente da arquitetura, harness do projeto em .specs/, e validação independente com evidência (autor ≠ verificador, sensor de discriminação). Use para (1) decidir se e o que construir, (2) escrever Fundação, MVP Scope, PRD, Domain Model ou Base Técnica, (3) extrair e tipar regras de negócio, (4) montar o harness do projeto num repositório, (5) escrever spec de feature, arquitetura, tasks e validação. Ativa em "Método Ark", "duas altitudes", "porta de descoberta", "porta de extração", "Fundação", "MVP Scope", "PRD", "domain model", "base técnica", "regras de negócio", "invariante", "harness do projeto", "matriz de cenário", "spec-as-source", "validação independente", "evidência". NÃO use para escrever código sem spec, nem para decisão de produto sem software envolvido.
license: MIT
metadata:
  author: Luciana Bordini
  version: 3.0.0
---

# Método Ark

> **Código virou commodity. Pensar, não.**
> **O software começa antes do prompt.**

A IA executa. Decidir, especificar e julgar continua sendo trabalho humano.

---

## Regras críticas (ler antes de agir)

**Carregando os arquivos desta skill.** As referências e templates vivem em `references/` e `templates/`, **dentro do diretório desta skill** — onde este `SKILL.md` está. Resolva os caminhos relativos ao diretório da skill, nunca à raiz do projeto, e nunca assuma um caminho fixo de instalação. Quando uma etapa mandar ler uma referência, **leia até o fim** antes de agir — nunca aja sobre leitura truncada.

**Altitude antes de tudo.** Toda tarefa é nível produto (uma vez por produto) ou nível iniciativa (toda vez que há trabalho). Aplicar artefato de produto a uma feature pequena é o que faz método virar burocracia. Escrever spec de feature sem produto definido é o que gera software sem direção.

**Criar artefato só quando a etapa produz conteúdo.** Nunca criar `arquitetura.md` vazio "para preencher depois". Arquivo vazio sinaliza que uma etapa aconteceu quando não aconteceu; ausência é o estado correto de uma etapa pulada. Isso vale para os artefatos de feature — os arquivos de `memory/` são exceção: existem desde o dia um.

**Raio de alcance.** Aprovar uma spec ou um conjunto de tasks autoriza implementação e commit **locais**. `git push`, deploy, mudança em banco de produção e qualquer operação remota, externamente visível ou destrutiva exigem autorização explícita para aquela ação específica.

**Conhecimento só se escreve depois do julgamento.** Antes disso, documento vira depósito de tentativa.

---

## Gates determinísticos — cobrados por código, não por memória

Os scripts vivem em `scripts/`, **dentro do diretório desta skill**. Resolva o diretório da skill primeiro e invoque `python3 <skill-dir>/scripts/<nome>.py`. Nunca rode `python3 scripts/...` da raiz do projeto — lá não existe essa pasta. Os dados do projeto ficam em `.specs/`, relativos à raiz do projeto (passe `--root` quando o cwd for outro).

| Quando | Comando |
|---|---|
| Antes de confirmar uma spec | `valida_spec.py <spec\|feature> [--root .]` |
| Antes de apresentar as tasks | `valida_tasks.py <tasks\|feature> [--root .]` |
| A cada commit | `valida_commit.py --message "<msg>"` |
| Antes de declarar a feature pronta | `valida_encerramento.py <feature> [--root .]` |
| Ao registrar ou promover lição | `licoes.py registrar\|listar\|promover\|render` |

**Saída diferente de zero significa PARAR e corrigir**, nunca seguir e anotar. Pule um script apenas quando não houver ferramenta de execução disponível — e então faça a mesma checagem lendo o artefato.

`valida_commit.py` funciona como guard do git, sem depender de agente nenhum:
`ln -s <skill-dir>/scripts/valida_commit.py .git/hooks/commit-msg`

`lessons.md` é **renderizado** por `licoes.py` a partir de `licoes.json`. Não editar à mão. A graduação é automática: a mesma lição registrada numa **segunda feature distinta** vira `confirmada`, e confirmada é candidata a virar regra.

---

## Orçamento de contexto

Spec-as-source falha na prática por contexto estourado, não por método errado.

**Carregar sob demanda, nunca de antemão:** as referências desta skill; `memory/decisoes.md` (ao desenhar arquitetura e ao retomar); `memory/produto.md` e `estrutura.md` (ao especificar); a spec da feature em curso; `arquitetura.md` só ao implementar a partir dela; lições **confirmadas** via `licoes.py listar --estado confirmada` — nunca as observadas.

**Nunca carregar ao mesmo tempo:** duas specs de features diferentes; `origem/` junto com `memory/` (um é histórico, o outro é o presente — juntos confundem o que é requisito vigente).

**Alvo:** menos de 40k tokens de contexto carregado, reservando o resto para raciocínio e saída. Passou disso, o próximo passo é fechar artefato, não abrir mais um.

---

## Delegação a sub-agentes

**Gatilho:** contar as tasks. Mais de ~8 → oferecer sub-agentes. Até ~8 → executar direto.

**Oferecer e confirmar, nunca auto-despachar.** A pessoa aceita antes de qualquer sub-agente ser criado.

**Um worker por lote de ~7 tasks, respeitando domínio.** Acumule tasks consecutivas em lotes até o orçamento; **nunca parta um domínio entre dois workers**, porque a regra de paralelismo deixa de ser verificável. Lotes rodam em sequência: um lote não começa antes de o anterior reportar tudo concluído. Cada worker implementa, roda o gate, commita por task e reporta um resumo compacto — tasks feitas, hashes, contagem de testes, desvios. **Workers não criam workers.**

**O verificador é sempre um agente novo**, nunca um dos workers. Autor ≠ verificador vale também aqui.

---

## Referências

Carregar sob demanda, nunca todas de uma vez.

| Arquivo | Quando ler |
|---|---|
| [`references/tese-e-metodo.md`](references/tese-e-metodo.md) | O método completo: tese, altitudes, portas, ciclo, matriz de cenário, validação. Ler quando a tarefa envolve decidir o que fazer, não como. |
| [`references/regras-de-negocio.md`](references/regras-de-negocio.md) | Ao extrair, ouvir, escrever ou tipar regra de negócio. Ler sempre que estiver escrevendo Fundação ou PRD. |
| [`references/harness.md`](references/harness.md) | Ao montar ou alterar o harness do projeto — `.agents/`, `.specs/` e `AGENTS.md`. |

---

## O essencial

### Duas altitudes

| Altitude | Frequência | Produz |
|---|---|---|
| **Produto** | Uma vez por produto | Documentos de origem + harness |
| **Iniciativa** | Toda vez que há trabalho | Uma feature, um fix, um refactor |

### Duas portas — a pergunta que classifica

> *Consigo hoje conversar com quem vive essa dor, ou sou eu mesmo?*
> **Sim → Extração. Não → Descoberta.**

O eixo é o **acesso à dor**, nunca o dono do produto. Produto próprio nascido de dor vivida entra por Extração — não há nada a descobrir nem validar. Descoberta ganha um **MVP Scope**, que é um documento com poder de matar o projeto; Extração não tem esse artefato, porque a decisão de construir já foi tomada.

### Documentos de origem

`MVP Scope`\* → `Fundação` → `PRD` → `Domain Model` → `Base Técnica` → harness

\* só na porta Descoberta.

**Nomes que não colidem:** "spec" é **sempre** spec de feature. O documento técnico do produto é a **Base Técnica**.

### O ciclo de uma iniciativa

```
Iniciativa → Conversação → Spec → Arquitetura* → Tasks → Execução → Validação → Conhecimento
```

Decisões e contexto são **seções da spec**, não etapas separadas. Etapa sem artefato não é executada, é lembrada.

### Matriz de cenário — o kit mínimo

| Cenário | Kit |
|---|---|
| Produto do zero · feature que toca arquitetura ou domínio | Spec + Arquitetura + Tasks + Validação |
| Feature dentro do padrão existente | Spec + Tasks + Validação |
| Refactor | Arquitetura + Tasks + Validação (asserts intocados) |
| Bug / ajuste pontual | Task + Validação |
| Spike | Pergunta + prazo + resposta escrita |

Cenário declarado no topo da spec. Não declarar é escolher o kit mais leve por omissão.

**Válvula de segurança.** Mesmo quando as tasks são puladas, a execução **começa listando os passos**. Se a listagem revelar mais de cinco passos, ou dependência entre eles, ou mais de um domínio envolvido: **pare e crie `tasks.md`** — o cenário foi classificado leve demais. A válvula existe porque o kit leve é escolhido por pressa com muito mais frequência do que por análise.

### Regras de negócio são a semente da arquitetura

| Tipo | Vira |
|---|---|
| Validação | Guards, validação de API |
| Invariante | Constraints, RLS, testes de invariância, produtor único |
| Transição de estado | Máquina de estado, ciclo de vida |
| Autorização | Policies, middleware, tiers, escopo de token |

Saem da Fundação, são numeradas no PRD. Como ouvi-las: [`references/regras-de-negocio.md`](references/regras-de-negocio.md).

### Validação — a regra que sustenta tudo

**Autor ≠ verificador. Evidência ou zero. E o verificador nunca conserta.**

Hierarquia: comando executado pelo verificador com a saída > assert ancorado em `file:line` no valor que a spec declara > sensor de discriminação (mutação que mata o teste) > verificação documental > confirmação visual.

Nunca conta: relato do agente sobre o próprio trabalho; "gate verde" sem comando e número; cobertura agregada; evidência herdada sem o diff que prova runtime idêntico.

**Sensor de discriminação** é obrigatório em caminho crítico (pagamento, auth, dado sensível, migration, contenção, invariante declarada), recomendado no AC central de feature normal, dispensado em copy e estilo.

---

## O harness do projeto — a estrutura que esta skill cria

> **"Harness do projeto" — e por que a qualificação importa.** No vocabulário do mercado, *harness* é a infraestrutura em volta do modelo que o transforma em agente: execução de ferramentas, memória, estado, loops de feedback. Nesse sentido, **o harness é o Claude Code, o Codex, o Cursor** — a própria documentação do Claude Code se descreve assim.
>
> O que o Método Ark monta é outra camada, e por isso ela sempre leva sobrenome: **harness do projeto** (ou *harness Ark*). É a estrutura dentro do repositório que faz aquele harness genérico se comportar de um jeito específico aqui:
>
> - **o que a IA sabe fazer** (`.agents/skills/`)
> - **o que é verdade neste projeto** (`.specs/memory/`)
> - **o que ela precisa provar** (`.specs/rules/`, os gates, a validação)
>
> Nunca diga "o harness" sozinho: quem é técnico vai entender a ferramenta, não a estrutura.

Ele vive no projeto de quem usa a skill, não aqui.

```
.agents/skills/            skills do projeto (fonte da verdade, portátil)
.specs/
├── features/<nome>/       iniciativa em curso
│   ├── spec.md
│   ├── arquitetura.md         (só quando a matriz exige)
│   ├── tasks.md
│   └── validation.md
├── archive/               iniciativas encerradas
├── memory/                o que é verdade hoje
│   ├── produto.md  estrutura.md  domain-model.md  decisoes.md  lessons.md
│   └── origem/            CONGELADO — fundação, PRD, base técnica, MVP Scope
├── rules/                 regras do método neste projeto
└── templates/             modelos dos artefatos
AGENTS.md                  regras do código (canônico)
CLAUDE.md                  stub que importa AGENTS.md
```

**Origem é congelada; memory é o presente.** Documento em `origem/` não se atualiza e carrega aviso de que não reflete o estado atual. Divergência entre os dois é a biografia do produto, não um bug.

**Cada regra mora num lugar só.** Regra de código em `AGENTS.md`; regra de método em `.specs/rules/`.

### Montando o harness do projeto

Copiar de `templates/` desta skill para o projeto:

| De (nesta skill) | Para (no projeto) |
|---|---|
| `templates/memory/*.md` | `.specs/memory/` |
| `templates/memory/origem-README.md` | `.specs/memory/origem/README.md` |
| `templates/rules/*.md` | `.specs/rules/` |
| `templates/*-modelo.md` | `.specs/templates/` |
| `templates/AGENTS-modelo.md` | `AGENTS.md` (raiz) |

`.claude/skills/` é **espelho por symlink** de `.agents/skills/`, criado só se a pessoa usa Claude Code — artefato local, nunca versionado. Detalhes e a armadilha de symlink em Windows: [`references/harness.md`](references/harness.md).

---

## Templates

`templates/fundacao-modelo.md` · `spec-modelo.md` · `arquitetura-modelo.md` · `tasks-modelo.md` · `validacao-modelo.md` · `AGENTS-modelo.md` · `rules/` · `memory/`

---

## Regras de decisão

1. **Porta pelo acesso à dor, nunca pelo dono do produto.**
2. **Kit pela matriz de cenário.** Não pedir quatro artefatos para um bug, nem aceitar produto do zero sem arquitetura.
3. **Tasks por domínio** (`banco` · `back-end` · `front-end` · `regra de negócio` · `arquitetura` · `infra`). Paralelo só entre domínios diferentes; um commit atômico por task.
4. **Validação não é opcional**, e o verificador não conserta: nomeia o gap, um implementador fecha, ele re-verifica.
5. **Origem é histórico, memory é presente.**
6. **Lição repetida vira regra.** Segunda ocorrência em feature distinta promove a lição para `.specs/rules/` ou `AGENTS.md`.
7. **Regime único: spec-as-source.** A especificação é a fonte; o código é subproduto. Não há modo reduzido.
8. **Se o pedido é implementação e não existe spec nem regra que a sustente, a resposta certa é subir uma altitude** — não gerar mais rápido.
