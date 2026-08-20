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

  console.log();
  c.dim("Próximo passo: escrever a Fundação em .specs/memory/origem/fundacao.md");
  c.dim("Antes disso, a pergunta que classifica a porta:");
  c.dim("  consigo hoje conversar com quem vive essa dor, ou sou eu mesmo?");
  c.dim("  sim → Extração (Fundação é o 1º doc) · não → Descoberta (antes vem o MVP Scope)");
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

function ajuda() {
  console.log(`
\x1b[1mmetodo-ark\x1b[0m — construir software profissional com IA sem terceirizar o pensamento

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

Montar o harness:
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
    console.log();
    c.dim("Pronto. Peça ao agente: \"usando o Método Ark, monta o harness deste projeto\"");
    break;
  }
  case "harness": harness(resolve(o._[1] || ".")); break;
  case "mirror": espelho(resolve(o._[1] || ".")); break;
  default: ajuda(); process.exit(1);
}
