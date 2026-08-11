#!/usr/bin/env python3
"""Núcleo partilhado da rede de agentes da Fábrica 2026.
Todos os agentes usam estas convenções: estado JSON em agentes/estado/,
log comum em agentes/estado/rede.log."""
import json
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NEGOCIOS = RAIZ / "negocios"
ESTADO = RAIZ / "agentes" / "estado"
SMOKE = RAIZ / "testes" / "smoke.py"
FILA = RAIZ / "fila.json"

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def log(agente, msg):
    linha = f"[{agora()}] [{agente}] {msg}"
    print(linha, flush=True)
    ESTADO.mkdir(parents=True, exist_ok=True)
    logf = ESTADO / "rede.log"
    with logf.open("a", encoding="utf-8") as f:
        f.write(linha + "\n")
    try:  # rotação simples: mantém as últimas 1000 linhas
        linhas = logf.read_text(encoding="utf-8").splitlines()
        if len(linhas) > 2000:
            logf.write_text("\n".join(linhas[-1000:]) + "\n", encoding="utf-8")
    except Exception:
        pass

def guardar(nome, dados):
    ESTADO.mkdir(parents=True, exist_ok=True)
    (ESTADO / f"{nome}.json").write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def ler(nome, default=None):
    p = ESTADO / f"{nome}.json"
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default

def negocios():
    return sorted(p for p in NEGOCIOS.glob("*/") if (p / "index.html").exists())

def nomes():
    """slug-dir -> nome bonito, a partir da fila."""
    try:
        fila = json.loads(FILA.read_text(encoding="utf-8"))["fila"]
        return {f"{n['id']}-{n['slug']}": n["nome"] for n in fila}
    except Exception:
        return {}
