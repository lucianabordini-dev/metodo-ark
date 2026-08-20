#!/usr/bin/env node
/**
 * metodo-ark — instalador da skill e do harness.
 * Node puro, zero dependências.
 */
import { cpSync, existsSync, mkdirSync, readdirSync, symlinkSync, rmSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PKG = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SKILL = join(PKG, "skills", "metodo-ark");

const c = {
  ok: (m) => console.log(`\x1b[32m✓\x1b[0m ${m}`),
  skip: (m) => console.log(`\x1b[33m—\x1b[0m ${m}`),
  err: (m) => console.error(`\x1b[31m✗\x1b[0m ${m}`),
  dim: (m) => console.log(`\x1b[2m${m}\x1b[0m`),
};

const GLOBAIS = {
  claude: { dir: () => join(homedir(), ".claude", "skills"), nome: "Claude Code / Desktop" },
  codex: { dir: () => join(homedir(), ".codex", "skills"), nome: "Codex CLI" },
  cursor: { dir: () => join(homedir(), ".cursor", "skills"), nome: "Cursor" },
};

function args(argv) {
  const o = { _: [], agente: null, force: false, projeto: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--agent" || a === "-a") o.agente = argv[++i];
    else if (a === "--project" || a === "--projeto" || a === "-p") o.projeto = true;
    else if (a === "--force" || a === "-f") o.force = true;
    else if (a === "--help" || a === "-h") o.help = true;
    else if (!a.startsWith("-")) o._.push(a);
  }
  return o;
}

function copiar(base, nome, force) {
  const dest = join(base, "metodo-ark");
  if (existsSync(dest) && !force) {
    c.skip(`${nome} já tem metodo-ark — use --force para atualizar`);
    return false;
  }
  mkdirSync(base, { recursive: true });
  if (force && existsSync(dest)) rmSync(dest, { recursive: true, force: true });
  cpSync(SKILL, dest, { recursive: true });
  c.ok(`${nome} → ${dest}`);
  return true;
}

function instalarGlobal(chaves, force) {
  for (const k of chaves) {
    const alvo = GLOBAIS[k];
    if (!alvo) {
      c.err(`agente desconhecido: ${k} — use ${Object.keys(GLOBAIS).join(", ")}`);
      process.exit(1);
    }
    copiar(alvo.dir(), alvo.nome, force);
  }
}

function instalarProjeto(raiz, force) {
  copiar(join(raiz, ".agents", "skills"), "Projeto (.agents/skills — versionado)", force);
  espelho(raiz, true);
}

function harness(raiz) {
  const t = join(SKILL, "templates");
  const specs = join(raiz, ".specs");
  if (existsSync(specs)) {
    c.err(`${specs} já existe — abortei para não misturar com o que já está lá`);
    process.exit(1);
  }
  for (const d of ["archive", "features", "memory/origem", "rules", "templates"]) {
    mkdirSync(join(specs, d), { recursive: true });
  }
  mkdirSync(join(raiz, ".agents", "skills"), { recursive: true });

  for (const f of readdirSync(join(t, "memory"))) {
    const alvo = f === "origem-README.md"
      ? join(specs, "memory", "origem", "README.md")
      : join(specs, "memory", f);
    cpSync(join(t, "memory", f), alvo);
  }
  cpSync(join(t, "rules"), join(specs, "rules"), { recursive: true });
  for (const f of readdirSync(t).filter((f) => f.endsWith("-modelo.md") && f !== "AGENTS-modelo.md")) {
    cpSync(join(t, f), join(specs, "templates", f));
  }
  c.ok(`harness montado em ${specs}`);

  const agents = join(raiz, "AGENTS.md");
  if (existsSync(agents)) c.skip("AGENTS.md já existe — mantive o seu");
  else { cpSync(join(t, "AGENTS-modelo.md"), agents); c.ok("AGENTS.md criado (esqueleto)"); }

  const claude = join(raiz, "CLAUDE.md");
  if (existsSync(claude)) c.skip("CLAUDE.md já existe — mantive o seu");
  else { cpSync(join(t, "CLAUDE-stub.md"), claude); c.ok("CLAUDE.md criado como stub"); }

}

function espelho(raiz, quieto = false) {
  const src = join(raiz, ".agents", "skills");
  if (!existsSync(src)) { c.err(`não achei ${src} — rode 'harness' primeiro`); process.exit(1); }
  const destBase = join(raiz, ".claude", "skills");
  mkdirSync(destBase, { recursive: true });
  let n = 0;
  for (const nome of readdirSync(src)) {
    const link = join(destBase, nome);
    if (existsSync(link)) { c.skip(`${nome} já está no espelho`); continue; }
    symlinkSync(join(relative(destBase, src), nome), link, "junction");
    c.ok(`.claude/skills/${nome} → .agents/skills/${nome}`);
    n++;
  }
  if (!n) c.skip("nada a espelhar");
  if (quieto) return;
  console.log();
  c.dim("O espelho é artefato local — não versione. Adicione .claude/ ao .gitignore.");
  c.dim("Em Windows, symlink versionado só sobrevive ao clone com core.symlinks=true");
  c.dim("e Developer Mode; sem isso o Git materializa o link como arquivo de texto");
  c.dim("e o agente lê uma linha achando que é a skill, sem dar erro.");
}

function proximo(modo, projeto = false) {
  const b = (m) => `\x1b[1m${m}\x1b[0m`;
  console.log();
  if (modo === "global") {
    c.dim("A skill está instalada e ativa sozinha quando a conversa entra no assunto.");
    console.log();
    console.log("  Para preparar um projeto, entre na pasta dele e rode:");
    console.log(`    ${b("npx metodo-ark harness .")}`);
    console.log();
    c.dim('  Ou peça ao seu agente: "usando o Método Ark, prepara este projeto"');
    return;
  }
  if (modo === "projeto") {
    c.dim("A skill agora vive dentro do repositório — quem clonar recebe junto.");
    console.log();
    console.log("  Falta preparar a estrutura do método:");
    console.log(`    ${b("npx metodo-ark harness .")}`);
    return;
  }
  // modo === "harness" ou "init"
  console.log(b("O harness do projeto está montado"));
  c.dim("— a estrutura no repositório que dirige a execução da IA.");
  console.log();
  console.log("  .agents/     o que a IA sabe fazer aqui (skills e workflows)");
  console.log("  .specs/      o que é verdade neste projeto, e o que ela precisa provar");
  console.log("  AGENTS.md    as regras do seu código — hoje um esqueleto, você preenche com o tempo");
  console.log();
  console.log(`${b("Comece assim")} — abra seu agente de código e peça, com estas palavras:`);
  console.log();
  console.log(`  ${b('"usando o Método Ark, quero começar um produto novo"')}`);
  console.log();
  c.dim("Ele conduz a partir daí: faz as perguntas, e escreve com você o primeiro");
  c.dim("documento do projeto. Você não precisa conhecer o método antes — só responder.");
  console.log();
  c.dim("Já tem um projeto em andamento? Peça no lugar:");
  c.dim('  "usando o Método Ark, extrai o que já existe neste código"');
  if (projeto) {
    console.log();
    c.dim("A skill está versionada em .agents/skills/ — quem clonar o repo recebe junto.");
    c.dim("Acrescente .claude/ ao .gitignore: o espelho é local e não se commita.");
  }
}


function ajuda() {
  console.log(`
\x1b[1mmetodo-ark\x1b[0m — construir software profissional com IA sem terceirizar o pensamento

  npx metodo-ark init    [caminho]      instala a skill E monta o harness
  npx metodo-ark install [--agent <nome>] [--project] [--force]
  npx metodo-ark harness [caminho]      monta .specs/ e .agents/ no projeto
  npx metodo-ark mirror  [caminho]      espelha .agents/skills em .claude/skills

Instalação global (padrão) — vale em todos os seus projetos:
  ~/.claude/skills/    Claude Code e Claude Desktop
  ~/.codex/skills/     Codex CLI
  ~/.cursor/skills/    Cursor

  npx metodo-ark install                  os três de uma vez
  npx metodo-ark install --agent codex    só um deles
  npx metodo-ark install --force          atualiza para a versão nova

Instalação por projeto — versionada, o time inteiro pega no git pull:
  npx metodo-ark install --project        .agents/skills/ + espelho .claude/skills

Do zero, num projeto novo — um comando só:
  npx metodo-ark init .              instala global + monta o harness
  npx metodo-ark init . --project    instala versionado no repo + monta o harness

Montar só o harness (skill já instalada):
  npx metodo-ark harness .
`);
}

const o = args(process.argv.slice(2));
const cmd = o._[0] || "install";

if (o.help) { ajuda(); process.exit(0); }

switch (cmd) {
  case "install": {
    if (o.projeto) {
      instalarProjeto(resolve(o._[1] || "."), o.force);
    } else {
      instalarGlobal(o.agente ? [o.agente] : Object.keys(GLOBAIS), o.force);
    }
    proximo(o.projeto ? "projeto" : "global");
    break;
  }
  case "init": {
    const raiz = resolve(o._[1] || ".");
    if (o.projeto) {
      copiar(join(raiz, ".agents", "skills"), "Projeto (.agents/skills — versionado)", o.force);
      espelho(raiz, true);
    } else {
      instalarGlobal(Object.keys(GLOBAIS), o.force);
    }
    console.log();
    harness(raiz);
    proximo("init", o.projeto);
    break;
  }
  case "harness": harness(resolve(o._[1] || ".")); proximo("harness"); break;
  case "mirror": espelho(resolve(o._[1] || ".")); break;
  default: ajuda(); process.exit(1);
}
