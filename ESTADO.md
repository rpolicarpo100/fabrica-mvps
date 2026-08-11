# ESTADO DO LOOP — Fábrica 2026

- `2026-08-11 16:11` 🔁 Loop arrancou (modo offline)
- `2026-08-11 16:11` ✅ **PostPilot** concluído (tentativa 1) — `negocios/04-postpilot/`
- `2026-08-11 16:11` ✅ **DeckForge** concluído (tentativa 1) — `negocios/05-deckforge/`
- `2026-08-11 16:11` 🏁 Fila esvaziada — fim do loop

## Sessão 2026-08-11 — log humano/assistente
- `16:05` FASE 0 — fundação: relatorio_negocios_2026.md, AGENTE.md, fila.json, testes/smoke.py, agente.py
- `16:07` ITERAÇÃO 1 — Executare (clone Bond) construído pelo assistente → smoke test ✅ à 1.ª
- `16:09` ITERAÇÃO 2 — SEOLens (clone OpenSEO) → smoke test ❌ (URL externo no HTML de exemplo) → REPARADO (href relativo) → ✅
- `16:10` ITERAÇÃO 3 — LeadForge (clone Fuzzy AI) → smoke test ✅ à 1.ª
- `16:11` ITERAÇÕES 4-5 — agente.py autónomo (modo offline) construiu PostPilot e DeckForge → ✅ à 1.ª
- `16:12` Hub/publicador criado em fabrica/index.html — 5/5 negócios funcionais. Fila esvaziada.
- PRÓXIMA RONDA: pesquisar novos alvos 2026, acrescentar à fila.json, repetir o loop.

## Ronda 2 (2026-08-11 tarde)
- 🔍 DESCOBERTA: novos alvos validados (Fundraisly #1 mensal PH jun-2026; Paradigm e Migma AI PH jul-2026)
- ITERAÇÃO 6 — DeckScore (pitch → score investidor) construído → smoke ✅ à 1.ª
- ITERAÇÃO 7 — Rumo (trajetos de aprendizagem) construído → bug de sintaxe detetado em revisão de código (função obsoleta) → REPARADO → smoke ✅
- ITERAÇÃO 8 — Reporta (CSV → relatório) construído → smoke ✅ à 1.ª
- Hub atualizado: 8/8 MVPs funcionais. Fila novamente esvaziada.
- `2026-08-11 16:42` 🔁 Loop arrancou (modo offline)
- `2026-08-11 16:42` ✅ **Pauta** concluído (tentativa 1) — `negocios/12-pauta/`

## Ronda 3 (2026-08-11 noite)
- 🔍 DESCOBERTA: pool validado jun-jul + frescos de ago-2026 (agentic workspaces, voz local-first)
- ITERAÇÃO 9 — Timbre (Goldfish) construído → smoke ✅ à 1.ª
- ITERAÇÃO 10 — Tração (Elentaria) construído → smoke ⚠️ (sem persistência) → melhorado (localStorage das respostas) → ✅
- ITERAÇÃO 11 — ProvaFogo (Replay QA) construído → smoke ❌ (URL externo no HTML de exemplo) → REPARADO → ✅
- ITERAÇÃO 12 — Pauta construída pelo agente.py (template novo CODIGO_PAUTA_JS) → smoke ✅ à 1.ª
- NOTA DE PROCESSO: pipeline marcou 11 como concluído antes da re-verificação; corrigido na sequência e registado aqui.
- 12/12 MVPs funcionais. Fila esvaziada. Próxima ronda: novos alvos ou nicho dirigido pelo utilizador.
- `2026-08-11 17:03` 🔁 Loop arrancou (modo offline)
- `2026-08-11 17:03` ✅ **Prep** concluído (tentativa 1) — `negocios/16-prep/`

## Ronda 4 (2026-08-11 noite tardia, modo offline por escolha do utilizador)
- 🔍 DESCOBERTA: AdAnt AI (#1 PH ago-2026), DocsAlot (#1 dia jul-2026), Impause, LeetDesign
- ITERAÇÃO 13 — Freio (anti-impulso) → bug barra de progresso detetado em revisão → REPARADO → smoke ✅
- ITERAÇÃO 14 — DuoDocs (docs humano+llms.txt) → smoke ✅ à 1.ª
- ITERAÇÃO 15 — Anuncia (copy por frameworks) → smoke ✅ à 1.ª
- ITERAÇÃO 16 — Prep (system design) construído pelo agente.py (template CODIGO_PREP_JS novo) → smoke ✅
- Utilizador optou por seguir sem API key; modo LLM fica disponível (rede sandbox→APIs confirmada: 401 = alcançável).
- 16/16 MVPs funcionais.
- `2026-08-11 17:27` 🔁 Loop arrancou (modo offline)
- `2026-08-11 17:27` ✅ **Scripter** concluído (tentativa 1) — `negocios/20-scripter/`

## Ronda 5 (2026-08-11) — nicho dirigido pelo utilizador: X / YouTube / Instagram
- 🔍 Validação: packaging YouTube quente (OverseerOS, Pikzels, ThumbnailTest); link-in-bio resiste (cap IG = oportunidade, YourSitee top PH ago); clips repurposing (AutoShorts/PassiveShorts)
- ITERAÇÃO 17 — Gancho (grader CTR títulos/hooks) → smoke ✅ à 1.ª
- ITERAÇÃO 18 — Clica (bio builder + export bio.html standalone) → smoke ✅ à 1.ª
- ITERAÇÃO 19 — ClipRadar (longo → plano de clips) → smoke ✅ à 1.ª
- ITERAÇÃO 20 — Scripter (guião Short 30s) pelo agente.py (template CODIGO_SCRIPT_JS) → smoke ✅
- 20/20 MVPs funcionais · agente autónomo tem 5 templates ativos
- `2026-08-11 17:58` 🔁 Loop arrancou (modo offline)
- `2026-08-11 17:58` ✅ **ProvaSocial** concluído (tentativa 1) — `negocios/21-provasocial/`
- `2026-08-11 18:01` 🔁 Loop arrancou (modo offline)
- `2026-08-11 18:01` ✅ **PortalKit** concluído (tentativa 1) — `negocios/24-portalkit/`

## Ronda 6 (2026-08-11) — "boring niches" com teto validado
- 🔍 Prova social verificada como categoria paga em 2026 (Senja $29/mês; Famewall, Trustmary, VouchPost)
- ITERAÇÃO 21 — ProvaSocial (wall of love exportável) → smoke ✅ à 1.ª (1.ª construção)
- ITERAÇÃO 22 — Marca (página de marcações exportável, mailto) → smoke ✅ à 1.ª
- ITERAÇÃO 23 — Recupera (dunning ROI + 4 emails) → smoke ❌ (array emails mal fechado: ']]' vs ']}]') → REPARADO → ✅
- ⚠ INCIDENTE: a falha do #23 interrompeu a cadeia && → agente correu no alvo pendente errado (#21) e pisou o ficheiro com um template genérico. Detetado na verificação global. #21 restaurado, cadeia refeita com validação por ficheiros temporários, agente re-executado no alvo certo (#24).
- ITERAÇÃO 24 — PortalKit (relatório de estado) pelo agente.py → smoke ✅
- Lição aplicada: o passo de registo na fila ficou condicionado a smoke ok (guard explícito), e a verificação global a N MVPs faz parte de cada ronda.
- 24/24 MVPs funcionais.

## 2026-08-11 — Preparação para deploy no GitHub
- Repositório git inicializado (branch main, commit inicial).
- Adicionados: README.md, LICENSE (MIT), .gitignore, DEPLOY.md e workflow GitHub Pages (.github/workflows/pages.yml).
- Pendente: push (aguarda autenticação do utilizador — token nunca será gravado em ficheiros).
- Deploy efetuado: rpolicarpo100/fabrica-mvps (público) + GitHub Pages → https://rpolicarpo100.github.io/fabrica-mvps/
- Validação pós-deploy: portal HTTP 200 + MVPs a responder (workflow GitHub Pages: success).
- Hosting: adicionado render.yaml (Blueprint, static site, auto-deploy do GitHub) — alternativa grátis ao domínio .pt.
- `2026-08-11 19:49` 🔁 Loop arrancou (modo offline)
- `2026-08-11 19:49` ✅ **Deriva** concluído (tentativa 1) — `negocios/25-deriva/`
- `2026-08-11 19:52` 🔁 Loop arrancou (modo offline)
- `2026-08-11 19:52` ✅ **Medidor** concluído (tentativa 1) — `negocios/28-medidor/`

## 🏁 Ronda 7 — "Economia dos agentes de IA" (2026-08-11, noite)

### Entregue
- 4 iterações: **25-Deriva**, **26-Emprega**, **27-Escriba** (assistente) + **28-Medidor** (agente.py, novo template `medidor`)
- Pedido do utilizador implementado: **todos os 28 MVPs têm agora links de monetização** (🎯 inspiração/PH · 💰 Stripe Payment Links · 🚀 lançar no Product Hunt)
- `smoke.py` refinado: `src=` bloqueado sempre; `href=` externo permitido em `<a>` (era excessivamente estrito)
- Gate global: **28/28 verde** (re-verificado após todas as alterações)

### Incidentes do processo (transparência total)
1. **Agente sobrescreveu o 25-Deriva manual** — `agente.py` apanhava o primeiro pendente, mesmo sem template (`template: null` → gerador genérico pior). Detetado, ficheiro restaurado, causa corrigida: `proximo_pendente(dados, usar_llm)` agora **só escolhe slugs com template conhecido** em modo offline (lista `TEMPLATES_OFFLINE`).
2. **Links injetados dentro de `<script>` em 6 MVPs** (02, 08, 11, 18, 21, 22) — a injeção retroativa usou o primeiro `</body>` possível; nesses ficheiros o JS declara `'</scr'+'ipt>'`/`</body>` em strings de stdout? (não: o bloco foi colado antes do `</script>` por ordem de append simples). Detetado pelo gate global (6 ❌), bloco movido para antes do `</body>` real, validado por smoke individual + global. Lição registada: sempre gate global depois de edições em massa.

### Gate final
28/28 verde · 28/28 com links de monetização · ronda 7 completa.

## 🕸 Rede de Agentes autónoma (2026-08-11, noite) — pedido do utilizador

### Construído
- `agentes/nucleo.py` — convenções partilhadas (estado JSON, log rotativo, paths)
- `agentes/verificador.py` — **VERA** 🔍: smoke nos 28 + regressões + bytes
- `agentes/revisor.py` — **RUI** 📋: checklists vivas em `melhorias/*.md` (10 regras P1-P3)
- `agentes/kpis.py` — **KIKA** 📊: 5 KPIs ponderados/negócio → `kpis/index.html` (rate geral + ▲▼)
- `agentes/descobridor.py` — **DINIS** 🛰: lê PH ao vivo (hunted.space + orangebot) → candidatos
- `agentes/orquestrador.py` — maestro: ciclo horário VERA→RUI→KIKA→DINIS→(ARTUR se pendente c/ template), grafo SVG em `rede/index.html`
- `.github/workflows/rede.yml` — **cron horário no CI** (grátis, repo público) com auto-commit dos relatórios
- Hub atualizado: 2 cartões novos (Rede + KPIs) · `AGENTES.md` documenta a rede

### Primeiros ciclos reais (medidos)
- Ciclo #1 e #2: 2.7s/2.5s, OK ✅ · VERA 28/28 · RUI 0 P1 abertos · KIKA média 84.2 · DINIS 10 candidatos novos ao vivo + 4 do backlog (PH diário devolveu 403 → degradou com gracia)

### Nota honesta de arquitetura
Os agentes são programas determinísticos (checks de nível sénior codificados), NÃO LLMs com acesso extraordinário. "Acesso a repos públicos" = leitura de páginas públicas (DINIS). Upgrade a LLM: chave por env var ativa o modo generativo do ARTUR. Supervisão humana+Arena: auditoria de logs, aprovação de candidatos, direção de rondas. Loop 24/7 real = GitHub Actions cron; loop local no sandbox = instância viva de demonstração.
