#!/usr/bin/env python3
"""🕸 ORQUESTRADOR — o maestro da rede de agentes da Fábrica 2026.
Corre o pipeline de hora em hora:  VERA → RUI → KIKA → DINIS
e gera o painel público da rede em rede/index.html (grafo + saúde + decisões).

Uso:
  python3 agentes/orquestrador.py --once      # 1 ciclo
  python3 agentes/orquestrador.py             # loop horário para sempre
  REDE_INTERVALO_S=600 python3 agentes/orquestrador.py   # intervalo custom (testes)

Nota de arquitetura (honesta): os agentes são programas determinísticos de
nível sénior. Com ANTHROPIC_API_KEY/OPENAI_API_KEY no ambiente, o ARTUR (agente.py)
passa a construir MVPs com LLM. A supervisão/auditoria é humana+Arena."""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nucleo import RAIZ, ESTADO, agora, guardar, ler, log

AGENTE = "orquestrador"
INTERVALO = int(os.environ.get("REDE_INTERVALO_S", "3600"))

# (id, script, critico?) — critico: se falhar, o ciclo fica vermelho
PIPELINE = [
    ("vera",   "agentes/verificador.py",  True),
    ("rui",    "agentes/revisor.py",      False),
    ("kika",   "agentes/kpis.py",         False),
    ("dinis",  "agentes/descobridor.py",  False),
]
# construtor entra SÓ se houver pendentes com template conhecido (guard anti-genérico)
CONSTRUTOR = "agente.py"

DESCRICAO = {
    "vera":  ("🔍", "VERA", "Engenheira de Qualidade", "smoke tests nos MVPs, regressões"),
    "rui":   ("📋", "RUI", "Revisor de Produto", "checklists de melhoria vivas"),
    "kika":  ("📊", "KIKA", "Analista de KPIs", "scores eficiência/eficácia + dashboard"),
    "dinis": ("🛰", "DINIS", "Analista de Mercado", "varre PH ao vivo, propõe candidatos"),
}

def correr(script):
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, str(RAIZ / script)], cwd=RAIZ,
                           capture_output=True, text=True, timeout=600)
        dt = round(time.time() - t0, 1)
        resumo = {}
        for linha in reversed(r.stdout.strip().splitlines()):
            linha = linha.strip()
            if linha.startswith("{"):
                try:
                    resumo = json.loads(linha)
                    break
                except json.JSONDecodeError:
                    continue
        return {"rc": r.returncode, "s": dt, "resumo": resumo,
                "erro": (r.stderr.strip()[-200:] if r.returncode else "")}
    except subprocess.TimeoutExpired:
        return {"rc": 9, "s": 600, "resumo": {}, "erro": "timeout 600s"}

def cor_saude(rc, resumo):
    if rc == 9:
        return "#ff7d92"
    if rc != 0 and rc != 1:  # 1 = verificação com vermelhos (parcial)
        return "#ff7d92"
    taxa = resumo.get("taxa")
    if taxa is not None and taxa < 100:
        return "#f4bf75"
    if resumo.get("regressoes"):
        return "#ff7d92"
    return "#38d9a9" if rc in (0, 1) else "#ff7d92"

def nox(cx, cy, desc, cor):
    emoji, nome, papel, func = desc
    return f'''<g>
<circle cx="{cx}" cy="{cy}" r="34" fill="#11182a" stroke="{cor}" stroke-width="2.5"/>
<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-size="20">{emoji}</text>
<text x="{cx}" y="{cy + 16}" text-anchor="middle" font-size="9" fill="#e9edf6" font-weight="700">{nome}</text>
<text x="{cx}" y="{cy + 48}" text-anchor="middle" font-size="8.5" fill="#8d97ad">{papel}</text>
<text x="{cx}" y="{cy + 60}" text-anchor="middle" font-size="7.5" fill="#5b6580">{func}</text>
</g>'''

def aresta(x1, y1, x2, y2, rotulo=""):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    lab = (f'<text x="{mx}" y="{my - 4}" text-anchor="middle" font-size="8" fill="#5b6580">{rotulo}</text>'
           if rotulo else "")
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2a3550" '
            f'stroke-width="1.5" stroke-dasharray="5,4"/>{lab}')

def gerar_painel(res, ciclo, duracao):
    dados = {}
    for nid, _, _ in PIPELINE:
        dados[nid] = res[nid]
    ver = ler("verificacao", {}) or {}
    rev = ler("revisoes", {}) or {}
    kpi = ler("kpis", {}) or {}
    cand = ler("candidatos", {}) or {}
    artur = ler("artur", {}) or {}
    pendentes_fila = []
    try:
        fila = json.loads((RAIZ / "fila.json").read_text(encoding="utf-8"))["fila"]
        pendentes_fila = [n for n in fila if n["status"] == "pendente"]
    except Exception:
        pass

    POS = {"vera": (170, 130), "rui": (170, 320), "kika": (690, 130), "dinis": (690, 320)}
    CX, CY = 430, 225          # orquestrador
    SX, SY = 430, 50           # supervisor
    AX, AY = 430, 400          # artur pendente???
    # arestas
    svg = aresta(SX, SY + 36, CX, CY - 36)                          # sup -> orq
    for nid, (x, y) in POS.items():
        svg += aresta(CX, CY, x, y + (0 if y < CY else -0), "1/h")
    svg += aresta(CX, CY + 36, CX, 372, "aprovação sup.")            # orq -> artur
    svg += aresta(POS["vera"][0] + 36, POS["vera"][1], CX - 36, CY, "")  # feedback loops subtis
    # nós
    svg += nox(SX, SY, ("🧭", "SUPERVISOR", "humano + Arena", "audita · direciona · aprova"), "#c9a0ff")
    resumo_orq = "ok" if all(r["rc"] in (0, 1) for r in res.values()) else "alerta"
    svg += nox(CX, CY, ("🕸", "ORQUESTRADOR", "maestro", f"ciclo #{ciclo} · {duracao}s"), "#38d9a9" if resumo_orq == "ok" else "#ff7d92")
    for nid, (x, y) in POS.items():
        svg += nox(x, y, DESCRICAO[nid], cor_saude(res[nid]["rc"], res[nid]["resumo"]))
    n_pend = len(pendentes_fila)
    cor_artur = "#f4bf75" if n_pend else "#38d9a9"
    svg += nox(CX, 400, ("🏗", "ARTUR", "Construtor (agente.py)", f"{n_pend} pendentes na fila"), cor_artur)

    def card(nid):
        emoji, nome, papel, func = DESCRICAO[nid]
        r = res[nid]
        c = cor_saude(r["rc"], r["resumo"])
        resumo_txt = json.dumps(r["resumo"], ensure_ascii=False)
        if len(resumo_txt) > 220:
            resumo_txt = resumo_txt[:220] + "…"
        return f'''<div class="card" style="border-left:4px solid {c}">
<div class="ctop">{emoji} <b>{nome}</b> <span class="mut">{papel}</span><span class="dot" style="background:{c}"></span></div>
<div class="mut" style="font-size:.78rem">{func}</div>
<div class="mono">{resumo_txt}</div>
<div class="mut" style="font-size:.7rem">exit {r["rc"]} · {r["s"]}s · {agora()}</div>
</div>'''

    logf = ESTADO / "rede.log"
    tail = ""
    if logf.exists():
        tail = "\n".join(logf.read_text(encoding="utf-8").splitlines()[-40:])
    tail = tail.replace("<", "&lt;")

    pend_html = ""
    if pendentes_fila:
        pend_html = ("<h3>⏳ À espera do ARTUR</h3><ul>" + "".join(
            f"<li><b>{n['nome']}</b> — {n.get('brief','')[:90]}</li>" for n in pendentes_fila) + "</ul>")
    cand_lista = (cand.get("vistos") or [])[-8:]
    cand_html = ""
    if cand_lista:
        cand_html = ('<h3>🛰 Candidatos à aprovação do SUPERVISOR</h3><ul>' + "".join(
            f"<li><b>{c['nome']}</b> <span class='mut'>({c.get('tema','?')})</span> — {c['estado']}</li>"
            for c in cand_lista) + "</ul>")

    html = f'''<!DOCTYPE html>
<html lang="pt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>🕸 Rede de Agentes — Fábrica 2026</title>
<style>
:root{{--bg:#080b12;--panel:#11182a;--line:#202c46;--txt:#e9edf6;--mut:#8d97ad;--acc:#6c8cff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:radial-gradient(1100px 600px at 85% -10%,#16203a 0%,var(--bg) 55%);color:var(--txt);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;padding:22px}}
main{{max-width:980px;margin:0 auto}}
header{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}}
h1{{font-size:1.5rem}} .mut{{color:var(--mut)}} .mut2{{color:#5b6580;font-size:.75rem}}
nav{{margin:12px 0}} nav a{{color:var(--acc);text-decoration:none;margin-right:16px;font-size:.85rem}}
.painel{{background:#0a0f1c;border:1px solid var(--line);border-radius:16px;padding:8px;margin:16px 0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:16px 0}}
.card{{background:linear-gradient(180deg,var(--panel),#0d1424);border:1px solid var(--line);border-radius:12px;padding:12px}}
.ctop{{display:flex;gap:8px;align-items:center}}
.dot{{width:10px;height:10px;border-radius:50%;margin-left:auto}}
.mono{{font-family:ui-monospace,monospace;font-size:.68rem;color:#9fe8c8;background:#060a12;border-radius:8px;padding:8px;margin:8px 0;word-break:break-all}}
h3{{font-size:.9rem;color:var(--mut);text-transform:uppercase;letter-spacing:1px;margin:20px 0 8px}}
ul{{margin-left:20px}} li{{font-size:.86rem;margin-bottom:4px}}
.stats{{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}}
.stat{{flex:1;min-width:130px;background:linear-gradient(180deg,var(--panel),#0d1424);border:1px solid var(--line);border-radius:12px;padding:12px;text-align:center}}
.stat b{{display:block;font-size:1.3rem;color:var(--acc)}}
.stat small{{color:var(--mut);font-size:.68rem;text-transform:uppercase;letter-spacing:.8px}}
pre.log{{background:#060a12;border:1px solid var(--line);border-radius:12px;padding:12px;font:11px/1.5 ui-monospace,monospace;color:#7fbf9a;max-height:340px;overflow:auto;white-space:pre-wrap}}
footer{{color:var(--mut);font-size:.75rem;text-align:center;padding:26px 0 10px}}
.badge{{background:#c9a0ff22;border:1px solid #c9a0ff55;color:#c9a0ff;font-size:.7rem;border-radius:999px;padding:3px 10px}}
</style></head><body><main>
<header><h1>🕸 Rede de Agentes</h1><span class="badge">auto-refresh 5 min</span></header>
<p class="mut">Fábrica 2026 — ciclo #{ciclo} terminou às {agora()} ({duracao}s) · próximo em ~{INTERVALO // 60} min</p>
<nav><a href="../index.html">← Portal (28 MVPs)</a><a href="../kpis/index.html">📊 Dashboard KPIs</a><a href="../ESTADO.md">📓 ESTADO.md</a></nav>

<div class="stats">
<div class="stat"><b style="color:{'#38d9a9' if ver.get('taxa') == 100 else '#f4bf75'}">{ver.get('verde','?')}/{ver.get('total','?')}</b><small>smoke verde</small></div>
<div class="stat"><b>{kpi.get('media','?')}</b><small>rate médio KPI</small></div>
<div class="stat"><b>{rev.get('p1_abertos','?')}</b><small>P1 por revisar</small></div>
<div class="stat"><b>{len((cand.get('vistos') or []))}</b><small>candidatos de mercado</small></div>
<div class="stat"><b>{len(pendentes_fila)}</b><small>pendentes na fila</small></div>
</div>

<h3>🗺 Grafo da rede</h3>
<div class="painel"><svg viewBox="0 0 860 470" width="100%" role="img">{svg}</svg></div>

<h3>🤖 Estado dos agentes (último ciclo)</h3>
<div class="cards">{"".join(card(n) for n, _, _ in PIPELINE)}
<div class="card" style="border-left:4px solid {cor_artur}">
<div class="ctop">🏗 <b>ARTUR</b> <span class="mut">Construtor</span><span class="dot" style="background:{cor_artur}"></span></div>
<div class="mut" style="font-size:.78rem">constrói MVPs pendentes (templates offline · LLM com key)</div>
<div class="mono">{json.dumps(artur or {"nota": "sem ciclos registados nesta sessão", "pendentes": n_pend}, ensure_ascii=False)[:220]}</div>
<div class="mut" style="font-size:.7rem">invocado sob aprovação do supervisor</div>
</div>
<div class="card" style="border-left:4px solid #c9a0ff">
<div class="ctop">🧭 <b>SUPERVISOR</b> <span class="mut">humano + Arena</span><span class="dot" style="background:#c9a0ff"></span></div>
<div class="mut" style="font-size:.78rem">audita logs, aprova candidatos, direciona rondas, adiciona agentes se necessário</div>
<div class="mono">{json.dumps({"auditoria": "ESTADO.md + rede.log", "decisoes": "candidatos→fila→build"}, ensure_ascii=False)}</div>
<div class="mut" style="font-size:.7rem">controlo em cada sessão de trabalho</div>
</div></div>

{pend_html}{cand_html}
<h3>📜 Log da rede (últimas 40)</h3>
<pre class="log">{tail or '(sem log ainda)'}</pre>
<footer>Orquestrador · loop a cada {INTERVALO // 60} min · GitHub Actions corre 1 ciclo/hora no CI · tudo determinístico e auditável</footer>
</main></body></html>'''
    out = RAIZ / "rede"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")

def pendentes_com_template():
    try:
        fila = json.loads((RAIZ / "fila.json").read_text(encoding="utf-8"))["fila"]
    except Exception:
        return []
    try:
        fonte = (RAIZ / CONSTRUTOR).read_text(encoding="utf-8")
        m = re.search(r"TEMPLATES_OFFLINE\s*=\s*\{([^}]*)\}", fonte)
        conhecidos = set(re.findall(r'"([^"]+)"', m.group(1))) if m else set()
    except Exception:
        conhecidos = set()
    return [n for n in fila
            if n["status"] == "pendente" and n.get("template") in conhecidos]

def ciclo(n):
    t0 = time.time()
    log(AGENTE, f"═══ ciclo #{n} ═══")
    res = {}
    for nid, script, _ in PIPELINE:
        log(AGENTE, f"▶ {nid}…")
        res[nid] = correr(script)
        if nid == "vera" and res[nid]["rc"] not in (0, 1):
            log(AGENTE, "🛑 VERA falhou de forma crítica — ciclo abortado antes dos restantes")
            break
    # ARTUR: constrói no máximo 1 pendente-com-template por ciclo, depois re-testa com VERA
    pendentes = pendentes_com_template()
    if pendentes:
        alvo = pendentes[0]
        log(AGENTE, f"▶ artur → construir {alvo['nome']} ({alvo['slug']})…")
        r = subprocess.run([sys.executable, str(RAIZ / CONSTRUTOR), "--once", "--demo"],
                           cwd=RAIZ, capture_output=True, text=True, timeout=600)
        ok = "FUNCIONAL" in r.stdout
        guardar("artur", {"quando": agora(), "alvo": alvo["slug"], "ok": ok,
                          "saida": r.stdout.strip().splitlines()[-1:]})
        if ok:
            log(AGENTE, f"🏗 {alvo['nome']} construído — VERA re-testa…")
            res["vera"] = correr("agentes/verificador.py")
            r2 = correr("agentes/revisor.py"); res["rui"] = r2
            res["kika"] = correr("agentes/kpis.py")
        else:
            log(AGENTE, f"⚠️ ARTUR não conseguiu {alvo['nome']}; fica para o supervisor")
            guardar("artur", {"quando": agora(), "alvo": alvo["slug"], "ok": False,
                              "saida": (r.stdout + r.stderr).strip().splitlines()[-2:]})
    duracao = round(time.time() - t0, 1)
    guardar("rede", {"quando": agora(), "ciclo": n, "duracao_s": duracao,
                     "agentes": res})
    gerar_painel(res, n, duracao)
    falhas = [k for k, r in res.items() if r["rc"] not in (0, 1)]
    log(AGENTE, f"ciclo #{n} terminado em {duracao}s · {'OK ✅' if not falhas else 'falhas: ' + ','.join(falhas)}")
    return 0 if not falhas else 1

def main():
    once = "--once" in sys.argv
    n = (ler("rede", {}) or {}).get("ciclo", 0)
    if once:
        return ciclo(n + 1)
    log(AGENTE, f"loop iniciado — ciclo a cada {INTERVALO}s (Ctrl+C para parar)")
    while True:
        n += 1
        ciclo(n)
        log(AGENTE, f"💤 a dormir {INTERVALO}s até ao próximo ciclo…")
        time.sleep(INTERVALO)

if __name__ == "__main__":
    sys.exit(main())
