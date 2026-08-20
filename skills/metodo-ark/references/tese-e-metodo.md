# Método Ark
### Como construir software profissional com IA, sem terceirizar o pensamento
*v3 — agosto de 2026*

---

## A tese

> **O software começa muito antes do prompt.**

Código virou commodity. Qualquer pessoa gera código em segundos. O que não virou commodity — e não vai virar — é saber **o que** construir, **por que** construir e **como estruturar** para que aquilo sobreviva. A IA executa. Pensar continua sendo trabalho humano.

Três argumentos sustentam isso:

**Nada do que está surgindo é novo — o novo é o meio.** Skills, agents, harness, spec-driven development: tudo isso é engenharia e arquitetura de software reembalada. A NASA escrevia especificações formais antes de qualquer linha de código no projeto Mercury, em 1960, porque falha em órbita era catastrófica. O que mudou não é o processo; é que agora existe uma inteligência que executa a partir das nossas instruções.

**A qualidade do output é função da qualidade do input.** Se a IA traduz instruções em código, o trabalho de valor migrou: de digitar código para escrever as melhores instruções e restrições possíveis. Quem não sabe pensar a arquitetura terceiriza o cérebro para a IA — e constrói castelos de areia: protótipos rápidos, cheios de bugs, sem padrão arquitetural, impossíveis de manter.

**A porta de entrada despencou; a barra de sobrevivência subiu.** Qualquer pessoa constrói um SaaS agora. Existir deixou de ser diferencial. O que distingue produtos que duram de produtos que morrem é a profundidade do pensamento por trás.

E o gargalo se moveu de novo. Com agentes produzindo mais rápido do que se lê, o gargalo virou **compreender e julgar**. Isso não contradiz a tese — comprova. Só é possível julgar o depois quando existe um antes registrado: quem não escreveu a intenção não tem contra o quê comparar o resultado, e sobra ler diff e torcer.

---

## A pergunta que o método responde

> "Como construir software profissional — que funciona, escala e dura — usando IA como executora, sem terceirizar o pensamento?"

Serve igualmente para produto próprio, serviço para cliente e trabalho dentro de uma empresa. O contexto muda; o método não.

---

## As duas altitudes

O erro mais comum ao aplicar o método é tratar tudo como uma sequência só. Não é. São duas altitudes com frequências diferentes:

| Altitude | Frequência | Produz |
|---|---|---|
| **Nível Produto** | Uma vez por produto (e revisões raras) | Os documentos de origem + o harness |
| **Nível Iniciativa** | Toda vez que existe trabalho a fazer | Uma feature, um fix, um refactor, uma resposta |

O harness (`AGENTS.md` + `.specs/`) liga as duas: é onde o nível produto deposita conhecimento e onde o nível iniciativa vai buscá-lo.

**Regra de altitude:** antes de qualquer coisa, identificar em qual altitude a tarefa está. Aplicar artefato de produto a uma feature pequena é o erro que faz o método parecer pesado. Pular para a spec de feature sem produto definido é o erro que gera software sem direção.

---

# Altitude 1 — Nível Produto

## As duas portas de entrada

Todo software nasce de um problema. O que muda entre um projeto e outro não é o dono do produto — é **como se chega à dor**.

> **Porta Descoberta** — a dor precisa ser *encontrada e validada*, porque vive em alguém a quem não se tem acesso direto.
>
> **Porta Extração** — a dor *já está disponível*: ou foi vivida por quem constrói, ou chegou trazida por quem a vive.

**Como classificar, em uma pergunta:**

> *Eu consigo, hoje, conversar com quem vive essa dor — ou sou eu mesmo?*
> **Sim → Extração. Não → Descoberta.**

| | Descoberta | Extração |
|---|---|---|
| **De onde vem** | Hipótese sobre um público que não é você e que você ainda não ouviu | Dor vivida por você, ou trazida por empresa/cliente |
| **Risco principal** | Construir o que ninguém quer | Resolver o problema errado por não ter entendido as regras |
| **O trabalho da etapa 0** | Ouvir, benchmarkear, testar hipótese de fit | Entrevistar (ou se entrevistar) e traduzir realidade em regra |
| **Artefato exclusivo** | **MVP Scope** | — |
| **Pode matar o projeto?** | Sim, e essa é a função | Não. A decisão de construir já foi tomada |

**Descoberta não é sobre ser produto de mercado; é sobre não ter acesso à dor.** Um app pessoal que um dia vai ao mercado entra por Extração — quando a dor é sua, não há nada a descobrir nem a validar, porque você tem acesso total ao usuário. Classificar isso como Descoberta obriga a fazer pesquisa de mercado para provar uma dor que você já vive. Trabalho cerimonial é o que faz método virar burocracia.

O inverso também vale: um produto pode nascer de dor vivida em primeira pessoa e ainda assim entrar por Descoberta, se o público a quem ele se destina não é você. É o caso clássico de "resolvi meu problema e assumi que os outros têm o mesmo" — e o comportamento de compra desse público é exatamente a hipótese que pode matar o projeto.

**O resíduo que a Extração não cobre.** Produto próprio que um dia vai ao mercado precisa, em algum momento, de recorte competitivo e diferencial. **Isso não é uma porta**: é uma seção da Fundação, preenchida apenas quando o produto for vendido. A porta continua limpa e a validação não some.

---

## Os documentos de origem

| # | Documento | Quando existe | Responde |
|---|---|---|---|
| 0 | **MVP Scope** | Só na porta Descoberta | Vale construir? Existe fit? O que pode matar isso? |
| 1 | **Fundação** | Sempre | O que é, para quem, por quê, o que está dentro e fora, quais são as regras |
| 2 | **PRD** | Sempre | As regras formalizadas, numeradas e tipadas; o produto em requisito |
| 3 | **Domain Model** | Sempre | Entidades, estados, relações — como o mundo do problema funciona |
| 4 | **Base Técnica** | Sempre | Stack, arquitetura macro, banco, segurança, contratos de API |

**MVP Scope e Fundação não são o mesmo documento com nomes diferentes.**

O MVP Scope é **um documento que pode matar o projeto**. Tem panorama competitivo, hipótese de fit testável, riscos de negócio e as perguntas que precisam de resposta antes de qualquer linha de código. Ele morre com a decisão — e se a decisão for "não", fica no repositório como registro de um não fundamentado, que vale tanto quanto um sim.

A Fundação **não pode matar nada**, porque quando ela é escrita a decisão de construir já foi tomada. Ela responde *o que é isso* e estabelece as regras. Na porta Descoberta, nasce depois do MVP Scope e herda dele o que sobreviveu; na porta Extração, é o primeiro documento do projeto.

**As regras de negócio saem da Fundação.** É lá que são extraídas e enunciadas pela primeira vez, em linguagem de negócio. O PRD as formaliza e numera; o Domain Model transforma as de estado em máquina de estado; a Base Técnica transforma as demais em guard, constraint e policy.

📘 **Como caçar, escrever e tipar uma regra: [`regras-de-negocio.md`](./regras-de-negocio.md).** É o pilar menos óbvio e mais valioso do método.

📘 **Como montar o harness: [`harness.md`](./harness.md).**

---

# Altitude 2 — Nível Iniciativa

Toda vez que existe trabalho a fazer, o trabalho passa por este ciclo:

```
Iniciativa → Conversação → Spec → Arquitetura* → Tasks → Execução → Validação → Conhecimento
                                  (*condicional)
```

**Decisões e contexto são seções da própria Spec, não etapas separadas.** Etapa sem artefato próprio não é executada, é lembrada — e o que não vira arquivo some entre sessões. A spec abre com *o que foi decidido e por quê* e *o que isto toca* (arquivos, módulos, invariantes vigentes). O porquê fica ancorado no mesmo documento que a execução lê, e a camada de intenção fica separada da descritiva.

## A matriz de cenário

"Arquitetura é opcional" sem critério vira "arquitetura é opcional sempre". O kit mínimo é declarado pelo tipo de iniciativa:

| Cenário | Kit obrigatório |
|---|---|
| **Produto do zero** | Spec + Arquitetura + Tasks + Validação |
| **Feature que toca arquitetura ou domínio** | Spec + Arquitetura + Tasks + Validação |
| **Feature dentro do padrão existente** | Spec + Tasks + Validação |
| **Refactor** | Arquitetura + Tasks + Validação (asserts intocados) |
| **Bug / ajuste pontual** | Task + Validação |
| **Spike** | Pergunta + prazo + resposta escrita → decisão ou lição |

**Refactor** muda a estrutura interna sem mudar comportamento. Não leva spec porque não há comportamento novo a especificar; leva arquitetura porque o refactor *é* a mudança de arquitetura. E tem critério de validação próprio: **a suíte existente passa sem nenhum assert alterado.** Assert editado durante refactor é o refactor se autoaprovando.

**Spike** é investigação com tempo-caixa para responder uma pergunta técnica antes de decidir. Não produz software: produz uma resposta escrita, que vira decisão registrada ou lição. Código de spike é descartável por definição — se sobreviver, virou feature e volta ao topo da matriz.


**Válvula de segurança.** Mesmo quando as tasks são puladas, a execução **começa listando os passos**. Se a listagem revelar mais de cinco passos, ou dependência entre eles, ou mais de um domínio envolvido: **pare e crie `tasks.md`** — o cenário foi classificado leve demais. A válvula existe porque o kit leve é escolhido por pressa com muito mais frequência do que por análise.

**Gates cobrados por código, não por memória.** Regra estrutural que depende do modelo lembrar não é gate. O método envia validadores determinísticos que rodam antes da revisão humana: fechamento da spec, granularidade e dependências das tasks, formato de commit, e o gate de encerramento (validação existe, veredito PASS, evidência citável, sensor rodado onde é obrigatório, gaps vazios, conhecimento atualizado). Saída diferente de zero significa parar e corrigir.

**Raio de alcance.** Aprovar uma spec ou um conjunto de tasks autoriza implementação e commit **locais**. `git push`, deploy, mudança em banco de produção e qualquer operação remota, externamente visível ou destrutiva exigem autorização explícita para aquela ação.

### Orçamento de contexto

Spec-as-source falha na prática por contexto estourado, não por método errado. Carregar sob demanda: decisões ao desenhar arquitetura, produto e estrutura ao especificar, arquitetura só ao implementar a partir dela, lições **confirmadas** apenas. Nunca carregar duas specs ao mesmo tempo, nem `origem/` junto com `memory/` — um é histórico, o outro é o presente, e juntos confundem o que é requisito vigente. Alvo: menos de 40k tokens carregados. Passou disso, o próximo passo é fechar artefato, não abrir mais um.

### Delegação a sub-agentes

Mais de ~8 tasks → oferecer sub-agentes; até ~8 → executar direto. **Oferecer e confirmar, nunca auto-despachar.** Um worker por lote de ~7 tasks, **sem partir um domínio entre dois workers** — se partir, a regra de paralelismo deixa de ser verificável. Lotes em sequência: um não começa antes de o anterior reportar tudo concluído. Workers não criam workers, e o verificador é sempre um agente novo — autor ≠ verificador vale aqui também.

## Tasks e execução por domínio

Tasks são separadas por domínio, e a execução respeita a separação. Domínios canônicos:

`banco` · `back-end` · `front-end` · `regra de negócio` · `arquitetura` · `infra`

**Regra de paralelismo:** paralelo só entre domínios diferentes. Duas tasks do mesmo domínio rodam em sequência, salvo quando comprovadamente não tocam os mesmos arquivos. Um commit atômico por task, sem agrupar e sem mudança "de passagem".

## Validação: autor ≠ verificador, evidência ou zero

A validação é feita por um **sub-agente independente**. Quem escreveu não valida — não por desconfiança, mas porque quem escreveu já provou para si mesmo que está certo, e é exatamente isso que o passo precisa testar.

**Regra dura: o verificador nunca conserta.** Encontrou gap, o gap é nomeado e um implementador fecha; o verificador re-verifica depois. Verificador que conserta virou autor, e a independência morre naquele instante.

### A hierarquia de evidência

Do que mais vale ao que menos vale:

1. **Comando executado pelo próprio verificador, com a saída.** `33 passed (2.1m)` — não "os testes passam". Rodado por ele, não relatado pelo autor.
2. **Assert ancorado em `file:line` observando o outcome definido na spec.** O valor assertado é o valor que a spec declara — não "o teste de quantidade passa".
3. **Sensor de discriminação.** Quebrar o código de propósito, uma mutação por vez, e o teste tem que morrer. É o que separa evidência de teatro: **teste que passa igual com o código quebrado é evidência vazia**, e não existe outra forma de descobrir isso.
4. **Verificação documental** para mudança docs-only, com `git show --stat` provando zero runtime.
5. **Confirmação visual**, apenas quando o outcome não é observável por assert — e declarada como tal, nunca contada como prova.

**O que nunca conta como evidência:** relato do agente sobre o próprio trabalho ("implementei conforme a spec"); "gate verde" sem nome de comando e número; cobertura como percentual agregado; evidência herdada sem o diff que prova que o runtime não mudou.

### Profundidade do sensor

O sensor de discriminação é caro. É graduado por risco, não aplicado uniformemente:

| Nível | Quando | Sensor |
|---|---|---|
| **Crítico** | Pagamento, autenticação, autorização, dado sensível, migration, contenção/bloqueio, qualquer invariante declarada | **Obrigatório** — uma mutação por AC discriminante |
| **Padrão** | Feature normal de produto | Recomendado — ao menos uma mutação no AC central |
| **Baixo** | Copy, estilo, documentação | Dispensado |

### Duas regras de honestidade

- **Evidência parcial é gap nomeado, não PASS com asterisco.** Um AC provado por composição, ou sem assert direto, entra como observação escrita — nunca como aprovado silencioso.
- **Divergência de precisão se registra, não se apaga.** Se o teste provou a mesma propriedade com valores diferentes dos do exemplo da spec, isso fica anotado. É o que impede a próxima pessoa de ler "26/26" como "26 asserts perfeitos".

## Atualizar conhecimento — o ritual de encerramento

O ciclo só fecha quando o conhecimento reflete o que foi decidido. **Conhecimento só se escreve depois do julgamento**: antes disso, documento vira depósito de tentativa.

O encerramento de uma iniciativa faz, nesta ordem:

1. Atualiza `produto.md` e `estrutura.md`, se algo mudou.
2. Atualiza `domain-model.md`, se entrou entidade, estado ou relação.
3. Registra em `decisoes.md` toda decisão arquitetural do caminho, com razão e trade-off — e todo item que só vale no deploy.
4. Grava em `lessons.md` o que se aprendeu; promove a regra o que for segunda ocorrência.
5. Move a pasta da feature de `features/` para `archive/`.

Item de produção nunca se reporta em conversa: quem fecha uma feature não está fazendo deploy, e o que é dito em chat se perde entre sessões.

---

## O método é spec-as-source

O Método Ark opera em um regime só: **a especificação é a fonte, o código é subproduto.** O humano quase não toca código; ele decide, especifica, julga e valida.

Existem regimes mais fracos no mercado — spec descartável por feature, spec versionada mas sem autoridade. São degraus de chegada de quem está migrando. **Não são modos de operação do método.** Um método que aceita a própria versão diluída não consegue exigir nada.

## O que o método NÃO é

- Não é curso de prompt. Prompts são detalhe de implementação.
- Não é "aprenda a programar". A IA programa; você aprende a pensar.
- Não é vibe coding glorificado. É o antídoto do vibe coding.
- Não é teoria acadêmica de arquitetura. Tudo nasce de projetos reais, com nome, tela e código.
