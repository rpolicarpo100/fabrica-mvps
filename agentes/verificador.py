#!/usr/bin/env python3
"""🔍 VERA — Engenheira de Qualidade da rede.
Corre o smoke test em TODOS os negócios, de hora em hora.
Deteta regressões (o que estava verde e ficou vermelho) e regista bytes/links.
Saída: agentes/estado/verificacao.json | Exit 0 = tudo verde."""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nucleo import SMOKE, agora, guardar, ler, log, negocios

AGENTE = "vera/qualidade"

def verificar(pasta):
    r = subprocess.run([sys.executable, str(SMOKE), str(pasta)],
                       capture_output=True, text=True)
    try:
        res = json.loads(r.stdout)
    except json.JSONDecodeError:
        res = {"ok": False, "erros": ["smoke falhou", (r.stdout + r.stderr)[:400]], "avisos": []}
    html = (pasta / "index.html").read_text(encoding="utf-8")
    res["bytes"] = len(html.encode("utf-8"))
    res["links_money"] = ("producthunt.com/posts/new" in html) or ("stripe.com" in html)
    res["localstorage"] = "localStorage" in html
    return res

def main():
    anterior = ler("verificacao", {}) or {}
    prev_ok = {k for k, v in (anterior.get("por_negocio") or {}).items() if v.get("ok")}
    por, verde = {}, 0
    for pasta in negocios():
        r = verificar(pasta)
        por[pasta.name] = r
        verde += 1 if r["ok"] else 0
    total = len(por)
    agora_ok = {k for k, v in por.items() if v["ok"]}
    regressoes = sorted(prev_ok - agora_ok)
    corrigidos = sorted(agora_ok - prev_ok) if prev_ok else []
    for r in regressoes:
        log(AGENTE, f"🚨 REGRESSÃO: {r} estava verde e falhou agora")
    for k, v in por.items():
        if not v["ok"]:
            log(AGENTE, f"❌ {k}: {v['erros'][0][:120]}")
    taxa = round(100 * verde / total, 1) if total else 0.0
    guardar("verificacao", {
        "quando": agora(), "total": total, "verde": verde, "taxa": taxa,
        "taxa_anterior": anterior.get("taxa"), "regressoes": regressoes,
        "corrigidos": corrigidos, "por_negocio": por,
    })
    log(AGENTE, f"verificação completa: {verde}/{total} verdes ({taxa}%)"
                + (f" · regressões: {regressoes}" if regressoes else ""))
    print(json.dumps({"agente": AGENTE, "verde": verde, "total": total, "taxa": taxa,
                      "regressoes": regressoes}, ensure_ascii=False))
    return 0 if verde == total else 1

if __name__ == "__main__":
    sys.exit(main())
