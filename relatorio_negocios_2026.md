# Relatório — Negócios novos de 2026 que estão a ter sucesso
*Compilado em 11-08-2026 a partir de Product Hunt, Forbes AI 50, CRN, Indie Hackers e estudos de indie hacking.*

## Sinais de mercado (macro)
- **Forbes AI 50 / 2026:** startups de IA levantaram $305.6B; o prémio foi para quem mostra **receita em verticais específicas** (finanças, farma, ferramentas criativas), não benchmarks de modelos. Fonte: marketscale.com (07-08-2026).
- **Agentes que executam** dominam 2026: OpenClaw ("a IA que realmente faz coisas") tornou-se o projeto de crescimento mais rápido da história do GitHub (300k+ estrelas) e gerou 50+ produtos derivados.
- **Micro-SaaS de 1 pessoa** continua a imprimir dinheiro: portefólio de Samuel Rondot a $28k/mês; fundadora solo em Lisboa atingiu $10K MRR em 47 dias com stack de IA (indieis.land).
- **Ferramentas para agentes/devs** são ~20% das novas startups: Prelint, MemoryCustodian, TryCase, Task Monki (Product Hunt, jul-2026).

## Alvos de replicação (ranqueados por viabilidade de recriar em código, offline)

### #1 — Bond-style: "To-do list que se faz sozinha" → clone: **Executare**
- Bond: #4 Product Hunt junho 2026 (665 upvotes). "The AI to-do list that does itself."
- Porquê agora: toda a gente tem to-do lists; o diferencial 2026 é o agente *executar* (rascunhos, decomposição, agendamento), não só listar.
- MVP: parsing de linguagem natural (PT), priorização automática (matriz de Eisenhower), agente que executa/decompõe/agenda tarefas localmente, plano do dia automático.
- **Status: A REPLICAR NA ITERAÇÃO 1**

### #2 — OpenSEO-style: auditoria SEO/GEO open-source → clone: **SEOLens**
- OpenSEO: #3 Product Hunt julho 2026 (783 upvotes) — "alternativa open-source ao Ahrefs".
- Tendência extra: GEO (Generative Engine Optimization) — otimizar para motores de IA recomendarem a marca (ver Scribble Network, #47 jul-2026).
- MVP: colar HTML → auditoria de title/meta/headings/alt/OG/JSON-LD + score GEO com recomendações.
- **Status: A REPLICAR NA ITERAÇÃO 2**

### #3 — Fuzzy AI-style: aquecimento de prospects → clone: **LeadForge**
- Fuzzy AI: #7 Product Hunt julho 2026 — "we warm your prospects before reaching out". Ver também Fundraisly (#1 junho) e Katalyst (agente que trabalha o pipeline Salesforce).
- MVP: importar CSV de leads → scoring heurístico (cargo, domínio de email, sinais) → gerador de primeira mensagem personalizada por tier → pipeline simples.
- **Status: A REPLICAR NA ITERAÇÃO 3**

### #4 — StoryShort/AutoShorts-style: repurposing de conteúdo → clone: **PostPilot**
- StoryShort.ai ~$20k/mês; AutoShorts.ai citado como caso indie. Repurpose.io cobra $349/ano.
- MVP (via agente autónomo, template): gerador de variações de uma peça de conteúdo para X/LinkedIn/Instagram com hooks por plataforma.
- **Status: PENDENTE (iteração autónoma)**

### #5 — Gamma-style: apresentações por IA → clone: **DeckForge**
- Gamma: $2.1B valuation, $100M ARR com 50 funcionários (Forbes 2026).
- MVP (template): outline → slides em HTML.
- **Status: PENDENTE (iteração autónoma)**

## Nota ética/legal
Replicamos **modelos de negócio e funcionalidade** (ideias não são protegidas por direitos de autor). Nunca copiamos marca, design integral, código ou conteúdo de terceiros. Os clones são produtos originais inspirados em tendências validadas.

---

## Ronda 2 (11-08-2026, tarde) — novos alvos descobertos

### #6 — Fundraisly/VC Boom-style: avaliação de pitch decks → clone: **DeckScore**
- Fundraisly: #1 do mês no Product Hunt (jun-2026, 1027 upvotes) — "AI fundraising agent". VC Boom: "Score your deck, meet investors who fit".
- MVP: colar texto do pitch → análise por framework de 10 secções (problema, solução, mercado, tração, modelo, concorrência, vantagem, equipa, finanças, pedido), deteção de números/métricas, medidor de "buzzwords", veredito de investor-readiness + relatório MD.

### #7 — Paradigm-style: trajetos de aprendizagem adaptativos → clone: **Rumo**
- Paradigm: PH jul-2026 — "Turn any goal into a personalized, adaptive learning path". MentorJi/LeetDesign confirmam tendência edtech-IA.
- MVP: objetivo + nível + horas/semana → plano por fases com marcos, duração ajustada, checklist com progresso em localStorage, "sessão de hoje".

### #8 — Migma AI-style: analista de dados instantâneo → clone: **Reporta**
- Migma AI: PH jul-2026 — "Ask your AI Analyst and get back a ready-to-share report".
- MVP: colar CSV → auto-detetar tipos de colunas → KPIs, médias/medianas, gráficos SVG (barras por categoria, evolução temporal), insights automáticos em PT, exportar MD/dashboard HTML.

---

## Ronda 3 (11-08-2026, noite) — descoberta com dados de agosto 2026

Dados frescos PH (semana 1–5 ago-2026): agentic dev-workspaces, voz local-first (yapyap), multiplayer coding (mpai), governança de agentes. Cruzados com o pool validado de jun/jul ficam 4 novos clones:

### #9 — Goldfish-style → clone: **Timbre**
- Goldfish: PH #2 jun-2026 — "conhece o teu trabalho e responde como tu".
- MVP: cola amostras da tua escrita → perfil estilométrico (formalidade, ritmo, emojis, saudação/despedida habituais) → gera resposta no teu tom a partir de pontos.

### #10 — Elentaria-style → clone: **Tração**
- Elentaria: PH top-10 jun-2026 — "O teu GTM: do diagnóstico à execução".
- MVP: questionário (fase, tipo, ticket, ciclo, canais, recursos, gargalo) → motor de regras → top-3 canais com justificação + avisos + plano 30 dias + KPI norte.

### #11 — Replay QA-style → clone: **ProvaFogo**
- Replay QA: PH jul-2026 — "diz-te o que está partido antes dos utilizadores".
- MVP: colar HTML → auditoria QA/a11y (links internos quebrados, ids duplicados, labels, alt, noopener, CLS hints) com severidades e score de risco.

### #12 — Mina Meeting Assistant-style + trend voz local-first (ago-2026) → clone: **Pauta**
- MVP: tópicos "~15m | dono" → pauta cronometrada pronta a copiar. Construído pelo agente.py (template novo).

---

## Ronda 4 (11-08-2026, noite tardia) — modo offline, dados de meados de agosto

### #13 — Impause-style → clone: **Freio**
- Impause: lista "Best SaaS Tools 2026" (justhunt) — app anti-compras por impulso com psicologia comportamental.
- MVP: regista intenção de compra → período de arrefecimento com countdown → "horas de trabalho" e custo/uso → decisão consciente → total poupado + taxa de desistência.

### #14 — DocsAlot-style → clone: **DuoDocs**
- DocsAlot: PH #1 do dia 05-07-2026 (134↑)— "documentação que serve humanos e sistemas de IA".
- MVP: notas do produto → duas saídas: doc para humanos (estrutura README) + llms.txt para agentes/LLMs (tendência 2026).

### #15 — AdAnt AI-style → clone: **Anuncia**
- AdAnt AI: #1 do "Best of August 2026" PH (1.3k followers) — "Claude para social ads virais".
- MVP: produto+público+dor+CTA → variações de copy por framework (AIDA, PAS, Hook-Prova-Oferta) com limites por plataforma e botão copiar.

### #16 — LeetDesign-style → clone: **Prep** (via agente.py, template novo)
- LeetDesign: entrevistas de system design com entrevistador IA.
- MVP: banco de casos de system design PT + espaço de esboço + resposta modelo + rubrica de auto-avaliação.

---

## Ronda 5 (11-08-2026) — nicho dirigido: ferramentas para X / YouTube / Instagram

Validação: packaging para YouTube é categoria quente de 2026 (OverseerOS, Pikzels, ThumbnailTest, IntoThumbnail — overseeros.com); link-in-bio continua relevante (Metricool 08-2026: cap de 10 links/mês no IG mantém a necessidade; YourSitee #3 PH ago); repurposing de clips (AutoShorts $, PassiveShorts PH ago).

### #17 — Pikzels/ThumbnailTest-style → clone: **Gancho**
Grader de títulos/hooks (YouTube/X/IG): heurísticas CTR (números, poder, curiosidade, comprimento ideal por plataforma), avisos anti-clickbait vazio, gerador de variantes.

### #18 — YourSitee-style → clone: **Clica**
Builder de link-in-bio: dados + links → preview + exporta página single-file pronta a alojar em qualquer lado.

### #19 — AutoShorts/PassiveShorts-style → clone: **ClipRadar**
Momentos de longo formato → conceitos de clips (hook, duração pelo ritmo de leitura, corte, caption com hashtags por nicho) para Shorts/Reels/TikTok.

### #20 — Creator AI-style → clone: **Scripter** (via agente.py, template novo)
Tema → guião de Short de 30s (hook 0-3s / setup / payoff / CTA) com orçamento de palavras.

---

## Ronda 6 (11-08-2026) — "boring niches" com teto de receita validado (flowjam/wisernotify 2026)

### #21 — Senja-class → clone: **ProvaSocial** 🧱
Senja $29/mês, $83K MRR em 2 pessoas; categoria 2026 cheia de alternativas pagas (Famewall, Trustmary, VouchPost).
MVP: linhas "Nome | Cargo | ⭐ | texto" → moderação automática (dedupe, clamp, flags) → Wall of Love exportável (wall.html).

### #22 — Scheduling por nicho → clone: **Marca** 📅
Salões/clínicas/consultores: $35K–$450K ARR.
MVP: serviços com duração/preço + disponibilidade semanal → calculadora de capacidade/receita potencial + página de marcação exportável (CTA mailto).

### #23 — Dunning/payment recovery → clone: **Recupera** 💸
Classe Churnkey: $20K–$360K ARR. Benchmark recuperação 40–70%.
MVP: calculadora de receita recuperável (MRR, churn, taxa falha) + sequência de 4 emails PT (dia 0/2/5/7) prontos a copiar.

### #24 — Client portal p/ agências → clone: **PortalKit** 🗂 (via agente.py)
$30K–$400K ARR. MVP: entregáveis+estado+prazo → relatório de progresso com barra e resumo, pronto a colar no email do cliente.

---

## 🔍 Ronda 7 — "Economia dos Agentes de IA + Verticais Aborrecidas" (2026-08-11)

Fontes: Product Hunt Leaderboard diário (29/07/2026), PH mensal julho/2026 (hunted.space), Superframeworks (receitas verificadas de micro-SaaS 2026), BigIdeasDB (8.699 startups).

### Sinais fortes do mercado
- **Prelint** — 🥇 #1 Product of the Day 29/07/2026: "prevent product drift in AI-written code". Nova categoria inteira: QA da *intenção* em código gerado por IA.
- **RemoteOK** — $2.5M+ ARR (Pieter Levels, solo): job boards de nicho continuam a ser das máquinas de dinheiro mais "aborrecidas" e fiáveis. Teto reportado no flowjam: $40-500K ARR.
- **ClinicFrame** — Top 5 PH: "Granola para saúde, HIPAA-compliant". Confirma a tese: meeting intelligence **vertical** (regulada) vale muito mais que a genérica.
- **AgentQuartz** — trending devtools: medidor de consumo/custo de agentes IA. "A conta de luz dos agentes" — com Claude/Codex omnipresentes, observabilidade de custos explodiu.

### Os 4 escolhidos
| ID | Slug | Nome | Modelo | Validacao |
|----|------|------|--------|-----------|
| 25 | deriva | Deriva | Spec→ texto; checklist contra drift | PH #1 do dia (Prelint) |
| 26 | emprega | Emprega | Job board vertical (IA em PT) | RemoteOK $2.5M ARR |
| 27 | escriba | Escriba | Notas clínicas SOAP locais | ClinicFrame top-5 PH |
| 28 | medidor | Medidor | Custos de agentes IA (tokens→€) | AgentQuartz trending |

Nota ética: como sempre — reimplementações originais do *modelo*, zero marca/código/conteúdo alheio. Dados de demonstração fictícios.
