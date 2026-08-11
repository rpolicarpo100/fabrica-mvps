#!/usr/bin/env python3
"""Smoke test de MVPs da fábrica.
Uso: python3 testes/smoke.py <pasta_do_mvp>
Verifica: ficheiros, JS válido (node --check se disponível), sem recursos
externos que bloqueiam o preview offline, requisitos mínimos do SPEC."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

def extrair_scripts(html: str):
    return re.findall(r"<script>(.*?)</script>", html, re.S)

def testar(pasta: Path) -> dict:
    erros, avisos = [], []
    idx = pasta / "index.html"
    spec = pasta / "SPEC.md"
    if not idx.exists():
        return {"ok": False, "erros": ["index.html em falta"], "avisos": []}
    if not spec.exists():
        avisos.append("SPEC.md em falta")
    html = idx.read_text(encoding="utf-8")

    # 1) Recursos externos (bloqueiam preview sandboxed)
    externos = re.findall(r'(?:src|href)\s*=\s*"(https?://[^"]+)"', html)
    if externos:
        erros.append(f"recursos externos bloqueiam o preview: {externos[:3]}")

    # 2) JS válido
    scripts = extrair_scripts(html)
    if not scripts:
        avisos.append("sem <script> — app possivelmente estática")
    node = shutil.which("node")
    js_total = 0
    for i, js in enumerate(scripts):
        if not js.strip():
            continue
        js_total += 1
        if node:
            tmp = pasta / f".__smoke_{i}.js"
            tmp.write_text(js, encoding="utf-8")
            r = subprocess.run([node, "--check", str(tmp)], capture_output=True, text=True)
            tmp.unlink(missing_ok=True)
            if r.returncode != 0:
                erros.append(f"JS inválido no script #{i}: {r.stderr.strip()[:300]}")
        else:
            for abre, fecha in (("{", "}"), ("(", ")"), ("[", "]")):
                if js.count(abre) != js.count(fecha):
                    erros.append(f"JS script #{i}: '{abre}{fecha}' desequilibrado")

    # 3) HTML básico
    for tag in ("<html", "<head", "<body"):
        if tag not in html.lower():
            erros.append(f"estrutura HTML: falta {tag}")

    # 4) LocalStorage ou interatividade
    if js_total and "localStorage" not in html and "addEventListener" not in html:
        avisos.append("sem localStorage nem event listeners — interatividade duvidosa")

    return {"ok": not erros, "erros": erros, "avisos": avisos}

if __name__ == "__main__":
    alvo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    res = testar(alvo)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0 if res["ok"] else 1)
