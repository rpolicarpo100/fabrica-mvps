#!/usr/bin/env python3
"""🛰 DINIS — Analista de Mercado da rede.
A cada ciclo lê fontes PÚBLICAS ao vivo (rankings do Product Hunt) à procura de
novos negócios com tração em 2026, cruza com o que a fábrica já cobre e propõe
candidatos novos. Só lê dados públicos; sem credenciais.
O SUPERVISOR aprova → fila.json · o ARTUR constrói · a VERA testa.
Saída: agentes/estado/candidatos.json | Exit 0 sempre (degradação graciosa offline)."""
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nucleo import FILA, agora, guardar, ler, log

AGENTE = "dinis/mercado"
UA = {"User-Agent": "fabrica-2026-rede-agentes/1.0 (pesquisa educativa)"}
JUNK = {"product hunt", "orangebot", "hunted.space", "top products", "today",
        "product hunt top products", "leaderboard", "best of product hunt"}

def fontes():
    d = datetime.now()
    mes = d.strftime("%B")  # nome do mês em inglês nas URLs
    return [
        ("mensal", f"https://hunted.space/top-products/monthly/{d.year}/{mes}"),
        ("diário", f"https://www.producthunt.com/leaderboard/daily/{d.year}/{d.month}/{d.day}"),
        ("snapshot", "https://orangebot.ai/product-hunt-today"),
    ]

def buscar(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "ignore")

def extrair_nomes(html):
    nomes = []
    # 1) JSON-LD com listas de produtos
    for m in re.findall(r'"name"\s*:\s*"([^"]{2,60})"', html):
        nomes.append(m.strip())
    # 2) fallback: headings simples
    if len(nomes) < 5:
        nomes += [m.strip() for m in re.findall(r"<h3[^>]*>([^<]{2,50})</h3>", html)]
    limpos, vistos = [], set()
    for n in nomes:
        n = re.sub(r"\s+", " ", n).strip(" .–—")
        chave = n.lower()
        if chave in JUNK or chave in vistos or len(n.split()) > 5 or not n:
            continue
        vistos.add(chave)
        limpos.append(n)
    return limpos

def coberto(nome, fila):
    alvo = nome.lower()
    for n in fila:
        if alvo == n["slug"] or alvo in n["nome"].lower():
            return True
        insp = n.get("inspiracao", "").lower()
        if alvo in insp or any(p in insp for p in alvo.split() if len(p) > 4):
            return True
    return False

def tema_de(nome):
    n = nome.lower()
    mapa = [("devtools", ["dev", "code", "api", "git", "lint", "repo", "merge", "cli", "agent", "terminal"]),
            ("saúde", ["health", "clinic", "doctor", "hipaa", "medic"]),
            ("creator", ["video", "short", "tiktok", "youtube", "creator", "thumb", "vlog"]),
            ("vendas/marketing", ["sales", "crm", "lead", "marketing", "seo", "ads", "email"]),
            ("finanças", ["financ", "invoice", "stripe", "payment", "crypto", "invest"]),
            ("design", ["design", "image", "logo", "figma", "canvas", "slide"])]
    for t, kws in mapa:
        if any(k in n for k in kws):
            return t
    return "produtividade"

BACKLOG = [  # validado na fase de relatório — entra quando o supervisor aprovar
    {"slug": "quadroex", "nome": "QuadroEx", "tema": "boring niches",
     "inspiracao": "Job boards verticais ($40-500K ARR)",
     "brief": "Alertas de vagas por email + destaque pago para empresas"},
    {"slug": "fideliza", "nome": "Fideliza", "tema": "analytics",
     "inspiracao": "Churn/retention analytics ($25-400K ARR)",
     "brief": "CSV de clientes → retenção por coorte, churn rate e LTV"},
    {"slug": "cumpre", "nome": "Cumpre", "tema": "regulação",
     "inspiracao": "Compliance checker vertical ($30-500K ARR)",
     "brief": "Descrição do site/serviço → checklist de conformidade RGPD"},
    {"slug": "orcamento", "nome": "Orçamento", "tema": "boring niches",
     "inspiracao": "Quoting p/ serviços ($20-200K ARR)",
     "brief": "Linhas item|horas|rate → orçamento profissional pronto a enviar"},
]

def main():
    fila = json.loads(FILA.read_text(encoding="utf-8"))["fila"]
    estado = ler("candidatos", {"vistos": [], "fontes": {}}) or {"vistos": [], "fontes": {}}
    vistos = {c["slug"] for c in estado["vistos"]}
    novos, fontes_info = [], {}
    for etiqueta, url in fontes():
        try:
            nomes = extrair_nomes(buscar(url))
        except Exception as e:
            fontes_info[etiqueta] = {"ok": False, "erro": str(e)[:120]}
            log(AGENTE, f"⚠️ fonte {etiqueta} indisponível: {str(e)[:80]}")
            continue
        achados = 0
        for nome in nomes:
            if achados >= 5:
                break
            slug = re.sub(r"[^a-z0-9]+", "", nome.lower())[:24]
            if not slug or slug in vistos or coberto(nome, fila):
                continue
            vistos.add(slug)
            estado["vistos"].append({
                "slug": slug, "nome": nome, "tema": tema_de(nome), "fonte": url,
                "descoberto_em": agora(), "estado": "proposto (aguarda supervisão)",
                "inspiracao": f"{nome} — {etiqueta} PH {datetime.now():%b %Y}",
                "brief": "Candidato descoberto ao vivo; supervisor define brief e template"})
            novos.append(nome)
            achados += 1
        fontes_info[etiqueta] = {"ok": True, "nomes_lidos": len(nomes), "novos": achados}
    # backlog validado entra como candidatos "backlog"
    existentes = {n["slug"] for n in fila}
    for b in BACKLOG:
        if b["slug"] not in vistos and b["slug"] not in existentes:
            estado["vistos"].append(dict(b, fonte="relatorio_negocios_2026.md",
                                         descoberto_em=agora(),
                                         estado="backlog validado (aguarda supervisão)"))
            vistos.add(b["slug"])
    estado["vistos"] = [c for c in estado["vistos"] if c["slug"] not in existentes]
    estado["fontes"] = fontes_info
    estado["ultima_varrimento"] = agora()
    guardar("candidatos", estado)
    temas = {}
    for c in estado["vistos"]:
        temas[c.get("tema", "?")] = temas.get(c.get("tema", "?"), 0) + 1
    log(AGENTE, f"varrimento: {len(novos)} novos ao vivo ({', '.join(novos) or '—'}) · "
                f"{len(estado['vistos'])} à espera · temas {temas}")
    print(json.dumps({"agente": AGENTE, "novos": novos,
                      "pendentes": len(estado["vistos"]), "fontes": fontes_info},
                     ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
