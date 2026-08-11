# SPEC — Executare (`01-executare`)
- **Inspiração:** Bond (PH #4 jun-2026) — "A to-do list que se faz sozinha"
- **Formato:** single-file `index.html`, zero recursos externos, PT-PT
- **Features do MVP:**
  1. Parser de linguagem natural PT: datas (hoje/amanhã/dias da semana/dia N), horas (às 10h, 15:30, de manhã/tarde/noite), prioridade (!alta/urgente), tags (#), esforço (~30m)
  2. Priorização automática com score urgency×importância + vista Eisenhower
  3. Agente executor: rascunhos de email, decomposição de tarefas grandes, guiões de chamada, briefs de pesquisa; fallback = agenda bloco de foco
  4. Modo autónomo (executa a fila sozinho a cada N segundos)
  5. Plano do dia automático (blocos 09–13h / 14–18h)
  6. Persistência localStorage + registo de ações do agente + stats
- **Critérios de aceitação:** smoke.py verde.
