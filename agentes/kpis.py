#!/usr/bin/env python3
"""📊 KIKA — Analista de Métricas da rede.
Calcula KPIs técnicos de eficiência/eficácia por negócio e gera o dashboard
público em kpis/index.html com o rate geral de cada um + média da fábrica.
Saída: kpis/index.html + agentes/estado/kpis.json | Exit 0 = sempre."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nucleo import RAIZ, agora, guardar, ler, log, negocios, nomes

AGENTE = "kika/kpis"

def kpis_negocio(html, verif):
    """Devolve 5 KPIs 0–100: qualidade, interatividade, dados, completude, monetização."""
    qualidade = 100 if verif.get("ok") else (40 if verif.get("ok") is None else 0)
    n_al = html.count("addEventListener") + html.count("onclick")
    interatividade = min(100, 40 + n_al * 15)
    tem_ls = "localStorage" in html
    tem_hist = "hist" in html.lower()
    dados = (60 if tem_ls else 0) + (40 if tem_hist else 0)
    completude = sum([
        40 if re.search(r"exemplo|sample|demo", html, re.I) else 0,   # via demo
        30 if "clipboard" in html else 0,                              # copiar
        15 if "@media" in html else 0,                                 # responsivo
        15 if re.search(r"nenhum|vazio|ainda sem", html, re.I) else 0, # empty state
    ])
    monetizacao = 100 if ("producthunt.com/posts/new" in html or "stripe.com" in html) else 0
    score = round(qualidade * .30 + interatividade * .20 + dados * .20 +
                  completude * .15 + monetizacao * .15)
    return {"qualidade": qualidade, "interatividade": interatividade, "dados": dados,
            "completude": completude, "monetizacao": monetizacao, "score": score}

def cor(n):
    return "#38d9a9" if n >= 85 else ("#f4bf75" if n >= 65 else "#ff7d92")

def barra(n, w=110):
    return (f'<span class="tbar"><span class="tfill" style="width:{n}%;'
            f'background:{cor(n)}"></span></span>')

def main():
    ver = (ler("verificacao", {}) or {}).get("por_negocio", {})
    nomes_map = nomes()
    historico = ler("kpi_historico", {}) or {}
    itens = []
    for pasta in negocios():
        slug = pasta.name
        html = (pasta / "index.html").read_text(encoding="utf-8")
        k = kpis_negocio(html, ver.get(slug, {}))
        anterior = (historico.get(slug) or {}).get("score")
        k["delta"] = (k["score"] - anterior) if anterior is not None else 0
        k["slug"] = slug
        k["nome"] = nomes_map.get(slug, slug)
        k["bytes"] = len(html.encode("utf-8"))
        historico[slug] = {"score": k["score"], "quando": agora()}
        itens.append(k)
    media = round(sum(i["score"] for i in itens) / len(itens), 1) if itens else 0
    itens.sort(key=lambda i: -i["score"])

    cards = ""
    for i in itens:
        seta = "▲" if i["delta"] > 0 else ("▼" if i["delta"] < 0 else "=")
        setac = "#38d9a9" if i["delta"] > 0 else ("#ff7d92" if i["delta"] < 0 else "#8d97ad")
        cards += f'''<a class="card" href="../negocios/{i["slug"]}/index.html">
<div class="ctop"><b>{i["nome"]}</b><span class="slug">{i["slug"]}</span>
<span class="delta" style="color:{setac}">{seta} {abs(i["delta"])}</span></div>
<div class="big" style="color:{cor(i["score"])}">{i["score"]}<small>/100</small></div>
<div class="krow"><span>qualidade</span>{barra(i["qualidade"])}<i>{i["qualidade"]}</i></div>
<div class="krow"><span>interatividade</span>{barra(i["interatividade"])}<i>{i["interatividade"]}</i></div>
<div class="krow"><span>dados</span>{barra(i["dados"])}<i>{i["dados"]}</i></div>
<div class="krow"><span>completude</span>{barra(i["completude"])}<i>{i["completude"]}</i></div>
<div class="krow"><span>monetização</span>{barra(i["monetizacao"])}<i>{i["monetizacao"]}</i></div>
</a>'''

    top3 = " · ".join(f"{i['nome']} {i['score']}" for i in itens[:3])
    flop3 = " · ".join(f"{i['nome']} {i['score']}" for i in itens[-3:])
    html_out = f'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>📊 KPIs da Fábrica 2026 — rate geral por negócio</title>
<style>
:root{{--bg:#080b12;--panel:#11182a;--line:#202c46;--txt:#e9edf6;--mut:#8d97ad;--acc:#6c8cff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:radial-gradient(1100px 600px at 85% -10%,#16203a 0%,var(--bg) 55%);color:var(--txt);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;padding:22px}}
main{{max-width:1060px;margin:0 auto}}
header{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:8px}}
h1{{font-size:1.5rem}} .mut{{color:var(--mut);font-size:.85rem}}
.hero{{display:flex;gap:18px;align-items:center;background:linear-gradient(180deg,var(--panel),#0d1424);border:1px solid var(--line);border-radius:16px;padding:20px;margin:16px 0;flex-wrap:wrap}}
.ring{{width:130px;height:130px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:conic-gradient({cor(media)} {media * 3.6}deg,#1b2740 0)}}
.ringin{{width:100px;height:100px;border-radius:50%;background:var(--panel);display:flex;flex-direction:column;align-items:center;justify-content:center}}
.ringin b{{font-size:1.9rem}} .ringin small{{color:var(--mut);font-size:.7rem}}
.resumo b{{color:var(--acc)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}}
.card{{background:linear-gradient(180deg,var(--panel),#0d1424);border:1px solid var(--line);border-radius:14px;padding:14px;text-decoration:none;color:var(--txt);display:block}}
.card:hover{{border-color:var(--acc)}}
.ctop{{display:flex;gap:8px;align-items:baseline}} .ctop b{{font-size:1rem}}
.slug{{color:var(--mut);font-size:.7rem;flex:1}} .delta{{font-size:.75rem;font-weight:700}}
.big{{font-size:2rem;font-weight:800;margin:6px 0}} .big small{{font-size:.75rem;color:var(--mut)}}
.krow{{display:flex;align-items:center;gap:8px;font-size:.68rem;color:var(--mut);margin-top:4px}}
.krow span{{width:82px}} .krow i{{width:24px;text-align:right;font-style:normal}}
.tbar{{flex:1;height:6px;background:#0a0f1c;border-radius:4px;overflow:hidden;display:block}}
.tfill{{height:100%;display:block;border-radius:4px}}
nav{{margin:14px 0}} nav a{{color:var(--acc);text-decoration:none;margin-right:16px;font-size:.85rem}}
footer{{color:var(--mut);font-size:.75rem;text-align:center;padding:26px 0 10px}}
</style></head><body><main>
<header><h1>📊 KPIs da Fábrica</h1><span class="mut">atualizado {agora()} · rede horária</span></header>
<nav><a href="../index.html">← Portal</a><a href="../rede/index.html">🕸 Rede de agentes</a><a href="../ESTADO.md">Diário de bordo</a></nav>
<div class="hero">
<div class="ring"><div class="ringin"><b>{media}</b><small>rate médio</small></div></div>
<div class="resumo">
<p><b>{len(itens)} negócios</b> monitorizados · smoke verde: <b>{sum(1 for i in itens if i['qualidade'] == 100)}/{len(itens)}</b></p>
<p>🏆 Top: {top3}</p>
<p>🔧 Foco de melhoria: {flop3}</p>
<p class="mut">Score = 30% qualidade + 20% interatividade + 20% dados + 15% completude + 15% monetização.<br>▲/▼ = variação desde o ciclo anterior.</p>
</div></div>
<div class="grid">{cards}</div>
<footer>Gerado por KIKA (analista de KPIs) · rede de agentes Fábrica 2026 · dados reais do repositório, sem telemetria externa</footer>
</main></body></html>'''
    out = RAIZ / "kpis"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html_out, encoding="utf-8")
    guardar("kpis", {"quando": agora(), "media": media, "por_negocio": {i["slug"]: i["score"] for i in itens}})
    guardar("kpi_historico", historico)
    log(AGENTE, f"KPIs calculados: média {media}/100 em {len(itens)} negócios · top {itens[0]['nome']} ({itens[0]['score']})")
    print(json.dumps({"agente": AGENTE, "media": media, "negocios": len(itens)}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
