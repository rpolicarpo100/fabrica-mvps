#!/usr/bin/env python3
"""📋 RUI — Revisor de Produto da rede.
Revisa cada negócio com heurísticas sénior e mantém uma checklist de melhorias
viva em melhorias/NN-slug.md (✅ auto-marcado quando a melhoria entra).
Saída: melhorias/*.md + agentes/estado/revisoes.json | Exit 0 = sempre (é consultivo)."""
import re
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nucleo import RAIZ, agora, guardar, ler, log, negocios, nomes

AGENTE = "rui/revisão"

# (id, prioridade, melhoria recomendada, teste)
REGRAS = [
    ("smoke",    "P1", "Passa no smoke test sem erros",                lambda h, v: bool(v.get("ok"))),
    ("titulo",   "P1", "Tem <title> e meta viewport",                  lambda h, v: "<title>" in h and "viewport" in h),
    ("money",    "P1", "Links de monetização (Stripe + Product Hunt)", lambda h, v: "producthunt.com/posts/new" in h or "stripe.com" in h),
    ("storage",  "P2", "Persistência local (localStorage)",            lambda h, v: "localStorage" in h),
    ("exemplo",  "P2", "Botão de demonstração com dados de exemplo",   lambda h, v: bool(re.search(r"exemplo|sample|demo", h, re.I))),
    ("copiar",   "P2", "Copiar resultado p/ clipboard",                lambda h, v: "clipboard" in h),
    ("historico","P3", "Histórico de utilizações guardado",            lambda h, v: "hist" in h.lower()),
    ("responsivo","P3","Refinar responsividade (@media)",              lambda h, v: "@media" in h),
    ("vazio",    "P3", "Empty state amigável (\"ainda sem…\")",        lambda h, v: bool(re.search(r"nenhum|vazio|ainda sem|sem ", h, re.I))),
    ("atalhos",  "P3", "Atalhos de teclado (keydown)",                 lambda h, v: "keydown" in h),
]

def main():
    ver = (ler("verificacao", {}) or {}).get("por_negocio", {})
    nomes_map = nomes()
    pasta_melhorias = RAIZ / "melhorias"
    pasta_melhorias.mkdir(exist_ok=True)
    revisoes = {}
    p1_totais = 0
    for pasta in negocios():
        slug = pasta.name
        html = (pasta / "index.html").read_text(encoding="utf-8")
        v = ver.get(slug, {"ok": True})
        linhas, feitos, abertos_p1 = [], 0, []
        for rid, prio, desc, fn in REGRAS:
            try:
                ok = bool(fn(html, v))
            except Exception:
                ok = False
            feitos += 1 if ok else 0
            if not ok and prio == "P1":
                abertos_p1.append(desc)
            linhas.append(f"| {'✅' if ok else '⬜'} | {prio} | {desc} |")
        (pasta_melhorias / f"{slug}.md").write_text(
            f"# 📋 Checklist de melhorias — {nomes_map.get(slug, slug)} (`{slug}`)\n\n"
            f"_Revisão automática por **Rui** · {agora()} · reavaliado a cada ciclo da rede_\n\n"
            "Legenda: ✅ feito · ⬜ por fazer · P1 crítico · P2 importante · P3 polish\n\n"
            "| Estado | Prior. | Melhoria |\n|---|---|---|\n" + "\n".join(linhas) + "\n\n"
            f"**{feitos}/{len(REGRAS)} concluído** — os ⬜ são as próximas melhorias por prioridade. "
            f"Score global no [dashboard de KPIs](../kpis/).\n",
            encoding="utf-8")
        revisoes[slug] = {"feitos": feitos, "total": len(REGRAS),
                          "abertos": len(REGRAS) - feitos, "abertos_p1": abertos_p1}
        p1_totais += len(abertos_p1)
    guardar("revisoes", {"quando": agora(), "por_negocio": revisoes, "p1_abertos": p1_totais})
    piores = sorted(revisoes.items(), key=lambda kv: kv[1]["abertos"], reverse=True)[:3]
    log(AGENTE, f"revisão feita: {len(revisoes)} checklists · {p1_totais} P1 abertos · "
                f"mais trabalho: {', '.join(s for s, _ in piores)}")
    print(json.dumps({"agente": AGENTE, "checklists": len(revisoes), "p1_abertos": p1_totais},
                     ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
