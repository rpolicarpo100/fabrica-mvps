# 🏭 Fábrica de MVPs 2026

Agente autónomo que identifica modelos de negócio digitais em crescimento em 2026 e recria **MVPs funcionais** — em loop, até passarem nos testes de fumo.

- ✅ **24 MVPs funcionais** construídos em 6 rondas
- 🧪 Gate de qualidade: `testes/smoke.py` — 24/24 verde
- 🤖 Orquestrador: `agente.py` (modo template offline + modo LLM via variável de ambiente)
- 🌐 Portal/hub: `index.html` (publicado via GitHub Pages)

---

## 🌐 Demo online

Quando publicado no GitHub Pages: `https://TEU-UTILIZADOR.github.io/fabrica-mvps/`

Todos os MVPs são ficheiros HTML únicos, 100% offline (zero recursos externos), em PT-PT e com modo escuro.

---

## 📂 Estrutura

```
agente.py                   # Loop autónomo: descobrir → construir → testar → reparar
fila.json                   # Fila e estado dos negócios (24 concluídos)
ESTADO.md                   # Diário de bordo: bugs, reparações e decisões
relatorio_negocios_2026.md  # Pesquisa de mercado validada por ronda
testes/smoke.py             # Testes de fumo (gate de qualidade)
negocios/NN-slug/           # SPEC.md + index.html de cada MVP
index.html                  # Portal com todos os MVPs
```

---

## ▶️ Como correr

Pré-requisito: **Python 3.9+** (apenas biblioteca standard — sem instalações).

```bash
# Ver o estado da fila
python3 agente.py --status

# Executar 1 iteração do loop (modo template, offline)
python3 agente.py --once --demo

# Testar um MVP individual
python3 testes/smoke.py negocios/01-executare

# Abrir o portal localmente
python3 -m http.server 8080
# → http://localhost:8080
```

### Modo LLM (opcional)

A chave é passada **apenas** via variável de ambiente, nunca gravada em ficheiros:

```bash
ANTHROPIC_API_KEY=sk-ant-... python3 agente.py --once
# ou
OPENAI_API_KEY=sk-proj-... python3 agente.py --once
```

---

## 🧩 Os 24 MVPs

| Ronda | Pasta | MVP | Modelo de referência |
|------:|-------|-----|----------------------|
| 1 | `negocios/01-executare` | Executare | Bond (agentes de IA) |
| 1 | `negocios/02-seolens` | SEOLens | OpenSEO |
| 1 | `negocios/03-leadforge` | LeadForge | Fuzzy AI |
| 1 | `negocios/04-postpilot` | PostPilot | StoryShort (~20k$/mês) |
| 1 | `negocios/05-deckforge` | DeckForge | Gamma |
| 2 | `negocios/06-deckscore` | DeckScore | VC Boom / Fundraisly |
| 2 | `negocios/07-rumo` | Rumo | Paradigm |
| 2 | `negocios/08-reporta` | Reporta | Migma AI |
| 3 | `negocios/09-timbre` | Timbre | Goldfish |
| 3 | `negocios/10-tracao` | Tração | Elentaria |
| 3 | `negocios/11-provafogo` | ProvaFogo | Replay QA |
| 3 | `negocios/12-pauta` | Pauta | Mina Meeting |
| 4 | `negocios/13-freio` | Freio | Impause |
| 4 | `negocios/14-duodocs` | DuoDocs | DocsAlot |
| 4 | `negocios/15-anuncia` | Anuncia | AdAnt AI |
| 4 | `negocios/16-prep` | Prep | LeetDesign |
| 5 | `negocios/17-gancho` | Gancho | Pikzels (25k$ MRR) |
| 5 | `negocios/18-clica` | Clica | YourSitee |
| 5 | `negocios/19-clipradar` | ClipRadar | AutoShorts |
| 5 | `negocios/20-scripter` | Scripter | Creator AI |
| 6 | `negocios/21-provasocial` | ProvaSocial | Senja (83k$ MRR) |
| 6 | `negocios/22-marca` | Marca | Agendamento vertical (nichos) |
| 6 | `negocios/23-recupera` | Recupera | Churnkey (dunning) |
| 6 | `negocios/24-portalkit` | PortalKit | Portais de cliente verticais |

Rondas com 🤖 incluem MVPs construídos pelo próprio `agente.py` (04, 05, 12, 16, 20, 24).

---

## ⚠️ Nota ética

Reimplementações **originais** de modelos de negócio públicos, para fins educativos e de produto próprio. Não é copiada marca, código ou conteúdo de terceiros.

---

## 📄 Licença

MIT — vê [LICENSE](LICENSE).
