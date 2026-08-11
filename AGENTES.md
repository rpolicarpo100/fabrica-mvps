# 🕸 Rede de Agentes — Fábrica 2026

Seis papéis especializados em **loop horário**, coordenados pelo orquestrador e
supervisionados pelo dono do projeto + Arena.

## Os agentes

| Agente | Papel | Entrada → Saída |
|--------|-------|-----------------|
| 🔍 **VERA** | Engenheira de Qualidade | `negocios/*/index.html` → smoke test, bytes, regressões → `estado/verificacao.json` |
| 📋 **RUI** | Revisor de Produto | HTML de cada MVP → checklist viva de melhorias → `melhorias/*.md` + `estado/revisoes.json` |
| 📊 **KIKA** | Analista de KPIs | verificação + heurísticas de UX → score 0-100 → `kpis/index.html` + `estado/kpis.json` |
| 🛰 **DINIS** | Analista de Mercado | Product Hunt ao vivo (mensal + snapshot) → candidatos novos → `estado/candidatos.json` |
| 🏗 **ARTUR** | Construtor (`agente.py`) | `fila.json` pendentes **com template** → MVP novo → validado pela VERA no mesmo ciclo |
| 🧭 **SUPERVISOR** | humano + Arena | audita logs, aprova candidatos→fila, decide rondas, adiciona agentes |

## Fluxo de dados (grafo)

```
SUPERVISOR ──audita/direciona──▶ ORQUESTRADOR ──timer 1/h──▶ VERA ─┐
                    │                                            ▼
                    │            RUI ◀── HTML dos MVPs       （re-testo）
                    ▼                                            │
              (cada hora)      KIKA ◀── verificacao.json ◀───────┘
                    │            DINIS ──▶ candidatos.json
                    ▼                  supervisor aprova ▼
                 ARTUR ◀── fila.json (só slugs com template)
                    │
                    ▼
              MVP novo ──▶ VERA re-testa no mesmo ciclo
```

## Garantias de segurança da rede

1. **Guard anti-genérico**: o ARTUR em modo offline só constrói slugs presentes em
   `TEMPLATES_OFFLINE` (bug da ronda 6/7 — nunca mais sobrescreve trabalho manual).
2. **VERA crítica**: se a VERA falhar de forma crítica (não regressão), o ciclo aborta.
3. **Regressões = alerta**: o que estava verde e fica vermelho gera 🚨 no log e
   marca o nó a amarelo/vermelho no grafo.
4. **Tudo commitável**: estado em JSON + log rotativo em `agentes/estado/` —
   auditoria completa por `git log` e `ESTADO.md`.
5. **Sem segredos em ficheiros**: chaves LLM só por variáveis de ambiente.

## Bottão de pânico / expansão

- Parar o loop local: `pkill -f orquestrador.py` (ou parar o processo no Arena)
- Parar o CI: apagar/desativar `.github/workflows/rede.yml`
- Novo agente: criar `agentes/<nome>.py` a escrever em `estado/<nome>.json`,
  registá-lo no `PIPELINE` do `orquestrador.py` e no grafo (`POS`/`DESCRICAO`).

## Onde ver

- 🕸 Painel da rede: `rede/index.html` (auto-refresh 5 min)
- 📊 Dashboard de KPIs: `kpis/index.html`
- 📋 Checklists: `melhorias/NN-slug.md` por negócio
- 📜 Log: `agentes/estado/rede.log`
