# AGENTE FÁBRICA 2026 — Manual do loop autónomo

## O que é
Um agente que, em loop contínuo:
1. **DESCOBRE** — lê `relatorio_negocios_2026.md` / `fila.json` (negócios de 2026 validados)
2. **PLANEIA** — gera `SPEC.md` por negócio (alvo, features, critérios de aceitação)
3. **CONSTRÓI** — gera os ficheiros do MVP (single-file HTML/JS, sem dependências externas → funciona em qualquer lado)
4. **TESTA** — corre `testes/smoke.py` (ficheiros existem, JS válido, sem recursos externos, requisitos presentes)
5. **REPARA** — se o teste falhar, reintroduz os erros no gerador e tenta de novo (máx. N tentativas)
6. **REGISTA** — atualiza `fila.json` (status) e `ESTADO.md` (log do loop)
7. **REPETE** — passa ao próximo negócio da fila. Quando a fila esvazia, propõe novos alvos.

## Dois modos de execução
| Modo | Como | Requer |
|---|---|---|
| **Eu (assistente Arena) executo o loop** | Peço iteração a iteração nesta conversa | Nada |
| **Script autónomo** | `python3 agente.py` | Python 3.9+; opcional `ANTHROPIC_API_KEY` ou `OPENAI_API_KEY` para geração por LLM; sem chave usa geradores de template offline (`--demo`) |

## Comandos
```bash
python3 agente.py --once          # uma iteração (próximo negócio pendente)
python3 agente.py                 # loop contínuo até a fila esvaziar
python3 agente.py --demo          # força modo offline (sem LLM)
python3 agente.py --status        # estado atual da fila
python3 testes/smoke.py negocios/01-executare   # testar um MVP manualmente
```

## Regras do agente
- Todo o MVP é **self-contained** (CSS/JS inline, zero CDN) → preview funciona offline.
- Cada iteração só fecha com **smoke test verde**.
- Nunca copiar marca/código/conteúdo alheio; recriar funcionalidade com implementação original.
- Log honesto: o que foi feito por mim vs. pelo script, e o que falta.
