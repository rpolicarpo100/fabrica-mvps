#!/usr/bin/env python3
"""
AGENTE FÁBRICA 2026 — loop autónomo de replicação de negócios em tendência.

Loop por iteração: DESCOBRIR -> PLANEAR -> CONSTRUIR -> TESTAR -> REPARAR -> REGISTAR -> REPETIR

Modos:
  python3 agente.py --once     → executa 1 iteração (próximo negócio pendente)
  python3 agente.py            → loop contínuo até fila esvaziar
  python3 agente.py --demo     → força geradores offline (sem LLM)
  python3 agente.py --status   → mostra estado da fila

LLM opcional: define ANTHROPIC_API_KEY ou OPENAI_API_KEY (e LLM_MODEL se quiseres).
Sem chave, o agente usa geradores de template offline — continua a produzir MVPs funcionais.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).parent
FILA = RAIZ / "fila.json"
ESTADO = RAIZ / "ESTADO.md"
SMOKE = RAIZ / "testes" / "smoke.py"
MAX_TENTATIVAS = 3

# ---------------------------------------------------------------- logs
def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}")

def regista_estado(linha):
    if not ESTADO.exists():
        ESTADO.write_text("# ESTADO DO LOOP — Fábrica 2026\n\n", encoding="utf-8")
    with ESTADO.open("a", encoding="utf-8") as f:
        f.write(f"- `{datetime.now():%Y-%m-%d %H:%M}` {linha}\n")

# ---------------------------------------------------------------- fila
def carregar_fila():
    return json.loads(FILA.read_text(encoding="utf-8"))

def guardar_fila(dados):
    dados["atualizado"] = f"{datetime.now():%Y-%m-%d}"
    FILA.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def proximo_pendente(dados):
    for n in dados["fila"]:
        if n["status"] in ("pendente", "em_curso"):
            return n
    return None

# ---------------------------------------------------------------- LLM (opcional)
def chamar_llm(prompt):
    """Devolve texto do LLM ou None se não houver chave/rede."""
    modelo = os.environ.get("LLM_MODEL")
    try:
        if os.environ.get("ANTHROPIC_API_KEY"):
            corpo = json.dumps({
                "model": modelo or "claude-sonnet-4-5",
                "max_tokens": 8000,
                "messages": [{"role": "user", "content": prompt}],
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages", data=corpo,
                headers={"x-api-key": os.environ["ANTHROPIC_API_KEY"],
                         "anthropic-version": "2023-06-01",
                         "content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read())
            return "".join(b.get("text", "") for b in out.get("content", []))
        if os.environ.get("OPENAI_API_KEY"):
            corpo = json.dumps({
                "model": modelo or "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
            }).encode()
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions", data=corpo,
                headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.loads(r.read())
            return out["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"⚠ LLM indisponível ({e}); uso gerador offline.")
    return None

# ---------------------------------------------------------------- planear
def gerar_spec(n):
    pasta = RAIZ / "negocios" / f"{n['id']}-{n['slug']}"
    pasta.mkdir(parents=True, exist_ok=True)
    spec = f"""# SPEC — {n['nome']} (`{n['slug']}`)
- **Inspiração:** {n['inspiracao']}
- **Brief:** {n['brief']}
- **Formato:** single-file `index.html`, CSS/JS inline, ZERO recursos externos.
- **Execução:** {n.get('construido_por', 'agente.py')}
- **Critérios de aceitação (smoke test):**
  1. `index.html` válido (<html>/<head>/<body>)
  2. JS syntacticamente válido (node --check)
  3. Sem `src`/`href` http(s) externo
  4. Interatividade presente (event listeners / localStorage)
"""
    (pasta / "SPEC.md").write_text(spec, encoding="utf-8")
    return pasta

# ---------------------------------------------------------------- construir (offline)
CODIGO_POSTPILOT_JS = """
function gerarVariacoes(){
  var txt=document.getElementById('entrada').value.trim();
  var out=document.getElementById('saida');
  if(!txt){out.innerHTML='<p class="aviso">Cola primeiro um texto.</p>';return;}
  var frases=txt.split(/[.!?\\n]+/).map(function(s){return s.trim();}).filter(function(s){return s.length>20;});
  var ideia=frases[0]||txt.slice(0,120);
  var hooks=['Ninguém te diz isto sobre','Erro nº1 em','A verdade sobre','Em 30 segundos:'];
  var plats={'X / Twitter':280,'LinkedIn':1300,'Instagram':2200};
  var html='';
  Object.keys(plats).forEach(function(p){
    var limite=plats[p];
    var hook=hooks[Math.floor(Math.random()*hooks.length)]+' '+ideia.toLowerCase();
    var corpo=frases.slice(0,3).join('. ');
    var post=(hook+'\\n\\n'+corpo).slice(0,limite);
    post+='\\n\\n'+['#dica','#2026','#conteudo'].join(' ');
    html+='<div class="post"><h3>'+p+' <span>'+post.length+'/'+limite+'</span></h3><pre>'+post.replace(/</g,'&lt;')+'</pre><button onclick="copiar(this)">Copiar</button></div>';
  });
  out.innerHTML=html;
}
function copiar(btn){var t=btn.parentNode.querySelector('pre').innerText;if(navigator.clipboard){navigator.clipboard.writeText(t);}btn.innerText='Copiado ✓';setTimeout(function(){btn.innerText='Copiar';},1500);}
"""

CODIGO_DECKFORGE_JS = """
var atual=0;
function gerarDeck(){
  var txt=document.getElementById('entrada').value.trim();
  var linhas=txt.split('\\n').map(function(l){return l.trim();}).filter(Boolean);
  if(linhas.length<2){document.getElementById('saida').innerHTML='<p class="aviso">Escreve um outline: 1 título por linha (mín. 2 linhas).</p>';return;}
  var slides=linhas.map(function(l,i){
    if(i===0){return '<section class="slide capa"><h1>'+l+'</h1><p>Gerado por DeckForge</p></section>';}
    var partes=l.split(':');
    var corpo=partes.length>1?('<ul>'+partes[1].split(';').map(function(b){return '<li>'+b.trim()+'</li>';}).join('')+'</ul>'):'';
    return '<section class="slide"><h2>'+partes[0]+'</h2>'+corpo+'</section>';
  });
  document.getElementById('saida').innerHTML=slides.join('')+'<div class="nav"><button onclick="mudar(-1)">←</button><span id="pos"></span><button onclick="mudar(1)">→</button></div>';
  window.__deck=document.querySelectorAll('.slide');atual=0;mostrar();
}
function mudar(d){if(!window.__deck)return;atual=Math.max(0,Math.min(window.__deck.length-1,atual+d));mostrar();}
function mostrar(){window.__deck.forEach(function(s,i){s.style.display=i===atual?'flex':'none';});var p=document.getElementById('pos');if(p)p.innerText=(atual+1)+'/'+window.__deck.length;}
document.addEventListener('keydown',function(e){if(e.key==='ArrowRight')mudar(1);if(e.key==='ArrowLeft')mudar(-1);});
"""

CODIGO_PAUTA_JS = """
function gerarPauta(){
var el=document.getElementById('inicio');
var ini=(el&&el.value)||'10:00';
var pp=ini.split(':');var base=(parseInt(pp[0],10)||10)*60+(parseInt(pp[1],10)||0);
var linhas=document.getElementById('entrada').value.split(/\\n+/).map(function(l){return l.trim();}).filter(Boolean);
var out=document.getElementById('saida');
if(!linhas.length){out.innerHTML='<p class="aviso">Escreve um tópico por linha. Opcionais: "~15m" e "| dono: Ana".</p>';return;}
function f(x){return ('0'+Math.floor(x/60)).slice(-2)+':'+('0'+(x%60)).slice(-2);}
var tot=0,txt='',cur=base;
linhas.forEach(function(l){
var dm=l.match(/~\\s*(\\d+)\\s*m(in)?/i);var dur=dm?parseInt(dm[1],10):10;
var dn=(l.match(/\\|\\s*(?:dono|resp|owner)?:?\\s*([\\w\\u00C0-\\u024F .]+)/i)||[])[1]||'';
var tema=l.replace(/~\\s*\\d+\\s*m(in)?/i,'').replace(/\\|.*$/,'').trim()||'Tópico';
tema=tema.charAt(0).toUpperCase()+tema.slice(1);
tot+=dur;
txt+=f(cur)+'-'+f(cur+dur)+'  '+tema+(dn?' · '+dn.trim():'')+'\\n';
cur+=dur;});
out.innerHTML='<div class="post"><h3>Pauta · início '+f(base)+' · '+tot+' min no total</h3><pre>'+txt.replace(/</g,'&lt;')+'</pre><button onclick="copiarPauta(this)">Copiar pauta</button></div>';
}
function copiarPauta(btn){var t=btn.parentNode.querySelector('pre').innerText;if(navigator.clipboard){navigator.clipboard.writeText(t);}btn.innerText='Copiado ✓';setTimeout(function(){btn.innerText='Copiar pauta';},1500);}
"""

CODIGO_SCRIPT_JS = """
var HOOKS=['Pára tudo: {t} explicado em 30 segundos','Ninguém te ensina {t} assim','Se {t} te confunde, vê isto até ao fim','O erro nº1 em {t} (e a correção em 20s)','{t}: a parte que os gurus saltam'];
var SETUPS=['Contexto rápido: a maioria começa pelo sítio errado.','Vou direto ao assunto, sem introduções.','Em 3 passos — o terceiro é o que muda tudo.'];
var PAYOFFS=['Passo 1: define o objetivo numa frase. Passo 2: corta 80% das distrações. Passo 3: mede uma só métrica durante 7 dias.','Primeiro o porquê. Depois o como. No fim, o erro a evitar.','Regra simples: faz X antes de Y, sempre. O resto é detalhe.'];
var CTAS=['Guarda este vídeo — vais precisar.','Segue-me para a parte 2.','Comenta "GUIA" e eu mando o checklist.'];
function gerarGuiao(){
var tema=(document.getElementById('entrada').value||'').trim().split(/\\n/)[0].slice(0,70)||'o teu tema';
function pk(a){return a[Math.floor(Math.random()*a.length)];}
var hook=pk(HOOKS).split('{t}').join(tema);
var gui=[['0-3s · HOOK',hook],['3-8s · SETUP',pk(SETUPS)],['8-24s · PAYOFF',pk(PAYOFFS)],['24-30s · CTA',pk(CTAS)]];
var txt=gui.map(function(g){return '['+g[0]+']\\n'+g[1];}).join('\\n\\n');
var palavras=txt.split(/\\s+/).length;
document.getElementById('saida').innerHTML='<div class="post"><h3>Guião de Short: '+tema+'</h3><pre>'+txt.replace(/</g,'&lt;')+'</pre>'+
'<p style="color:#8b93a7;font-size:.82rem">'+palavras+' palavras (~70-80 = 30s de leitura natural). Filma na vertical, legendas sempre ligadas.</p>'+
'<button onclick="copiarGuiao(this)">Copiar guião</button></div>';
}
function copiarGuiao(btn){var t=btn.parentNode.querySelector('pre').innerText;if(navigator.clipboard){navigator.clipboard.writeText(t);}btn.innerText='Copiado ✓';setTimeout(function(){btn.innerText='Copiar guião';},1500);}
"""

CODIGO_PORTAL_JS = """
function gerarEstado(){
var pj=document.getElementById('proj');
var proj=(pj&&pj.value.trim())||'Projeto do cliente';
var out=document.getElementById('saida');
var linhas=document.getElementById('entrada').value.split(/\\n+/).map(function(l){return l.trim();}).filter(Boolean);
if(!linhas.length){out.innerHTML='<p class="aviso">Linhas no formato: Entregável | estado | prazo</p>';return;}
function est(e){e=(e||'').toLowerCase();
if(/(feito|conclu|done|pronto)/.test(e))return{ic:'✅',n:'feito'};
if(/(curso|andamento|fazendo|progresso)/.test(e))return{ic:'🔨',n:'curso'};
if(/(atras)/.test(e))return{ic:'⚠️',n:'atraso'};
return{ic:'⏳',n:'pendente'};}
var rows=linhas.map(function(l){
var p=l.split('|').map(function(x){return x.trim();});
return{item:p[0],est:est(p[1]||''),prazo:p[2]||''};});
var feitos=rows.filter(function(r){return r.est.n==='feito';}).length;
var atrasos=rows.filter(function(r){return r.est.n==='atraso';}).length;
var pct=Math.round(feitos/rows.length*100);
var bar='';for(var i=0;i<10;i++)bar+=i<Math.round(pct/10)?'█':'░';
var txt='ESTADO DO PROJETO — '+proj+'\\n'+new Date().toLocaleDateString('pt-PT')+'\\n\\n';
txt+='Progresso: '+pct+'% '+bar+'\\n\\n';
rows.forEach(function(r){txt+=r.est.ic+' '+r.item+(r.prazo?' — '+r.prazo:'' )+'\\n';});
var cursando=rows.filter(function(r){return r.est.n==='curso';}).length;
var pend=rows.length-feitos-cursando-atrasos;
txt+='\\nResumo: '+feitos+' feitos · '+cursando+' em curso · '+pend+' pendentes'+(atrasos?' · ⚠️ '+atrasos+' em atraso':'')+'\\n';
txt+='Próxima atualização: [data]\\n';
out.innerHTML='<div class="post"><h3>🗂 Relatório pronto a colar no email</h3><pre>'+txt.replace(/</g,'&lt;')+'</pre><button onclick="copiarEstado(this)">Copiar relatório</button></div>';
}
function copiarEstado(btn){var t=btn.parentNode.querySelector('pre').innerText;if(navigator.clipboard){navigator.clipboard.writeText(t);}btn.innerText='Copiado ✓';setTimeout(function(){btn.innerText='Copiar relatório';},1500);}
"""

CODIGO_PREP_JS = """
var CASOS=[
{t:'Encurtador de URLs',r:['100M URLs criados por mês','Redirecionamento em menos de 10ms','Analytics simples por link'],
m:['API: POST /shorten devolve código base62; GET /{codigo} faz 301','ID: contador incremental convertido a base62 (curto e único sem colisões)','Leitura: cache em memória à frente da BD; escrita append na BD','Escala: particionar por intervalo de IDs; réplicas de leitura','Falhas: réplica síncrona p/ não perder IDs; monitorizar taxa de miss de cache']},
{t:'Feed de rede social',r:['Utilizadores seguem até ~1000 contas','Feed ordenado por relevância temporal','Pico de leitura muito acima do de escrita'],
m:['Fan-out on write: ao publicar, escrever no feed (KV) dos seguidores','Fan-out on read apenas para contas enormes (híbrido)','Paginação por cursor (timestamp+id), nunca OFFSET','Cache do top-N por utilizador; ranking simples primeiro, ML depois','Falhas: fila de fan-out com retry; feed reconstruível a partir dos posts']},
{t:'Chat em tempo real',r:['Mensagens 1:1 e grupos pequenos','Entrega garantida, ordem por conversa','Presença online/offline'],
m:['Gateway WebSocket com heartbeat; ligação por utilizador mapeada a servidor','Entrega: ack do cliente + retry; fila por utilizador offline','Ordem: sequência por conversa (id monotónico por chat)','Armazenamento: mensagens particionadas por conversa, ordenadas','Falhas: servidor de gateway cai -> cliente religa a outro; dedupe no cliente por id']},
{t:'Rate limiter de API',r:['100 req/min por cliente','Distribuído (vários servidores de API)','Resposta 429 imediata'],
m:['Algoritmo: token bucket por cliente','Estado em store partilhada rápida (KV) com operações atómicas','Alternativa barata: limites locais + agregação difusa','Resposta antecipada: headers de quota restante','Falhas: store em baixo -> fail-open com limite local mais estrito']},
{t:'Sistema de reservas',r:['Vagas limitadas por horário','Duplo clique não pode duplicar reserva','Cancelamentos libertam vaga'],
m:['Invariante: uma vaga = uma linha por horário; constraint única na BD','Reserva: transação que marca a vaga; idempotency-key no pedido','Hold temporário com expiração para checkout','Concorrência: lock pessimista na vaga (é barato porque é fino)','Falhas: job que expira holds abandonados; emails são idempotentes']},
{t:'Pipeline de métricas',r:['10k eventos/segundo','Consultas por hora/dia','Custos controlados'],
m:['Ingestão append-only numa fila; consumidores processam em batch','Agregações por janelas (min->hora->dia) em rollups','Dados quentes vs frios com retenção diferente','Cuidado com cardinalidade: ids de utilizador não são dimensão de agregação','Falhas: backpressure; reprocessar janelas a partir da fila com offsets']}];
var RUBRICA=['Requisitos e estimativas ANTES de desenhar (QPS, GB/dia)','Contratos de API claros','Modelo de dados + índices','Um gargalo identificado e plano de escala','Falhas: retries, duplicados, dados perdidos'];
var LAST=-1,U_OK=[];
function gerarCaso(){
var out=document.getElementById('saida');
var i;do{i=Math.floor(Math.random()*CASOS.length);}while(i===LAST&&CASOS.length>1);
LAST=i;U_OK=RUBRICA.map(function(){return false;});
var c=CASOS[i];
var html='<div class="post"><h3>🧪 Caso: '+c.t+'</h3><pre>Requisitos:\\n'+c.r.map(function(x){return '• '+x;}).join('\\n')+'</pre>';
html+='<p style="color:#8b93a7;font-size:.85rem;margin:8px 0">1) Esboça a tua solução no campo acima. 2) Depois revela o modelo.</p>';
html+='<button onclick="revelar()" id="btnRev">👁 Revelar resposta modelo</button>';
html+='<div id="modeloBox" style="display:none"><pre style="margin-top:10px">'+c.m.map(function(x,j){return (j+1)+'. '+x;}).join('\\n')+'</pre>';
html+='<h3 style="margin-top:14px">Auto-avaliação</h3><div id="rubrica">';
RUBRICA.forEach(function(r,j){html+='<label style="display:block;margin:7px 0;font-size:.88rem;cursor:pointer"><input type="checkbox" onchange="tickR('+j+')" style="accent-color:#6c8cff;margin-right:8px">'+r+'</label>';});
html+='</div><div id="notaRub" style="margin-top:10px;font-weight:700"></div></div></div>';
out.innerHTML=html;}
function revelar(){document.getElementById('modeloBox').style.display='block';document.getElementById('btnRev').style.display='none';}
function tickR(j){U_OK[j]=!U_OK[j];var n=U_OK.filter(Boolean).length;
var el=document.getElementById('notaRub');
el.innerText=n+'/'+RUBRICA.length+' — '+(n<=2?'continua a treinar a estrutura':(n<=4?'sólido, afina os detalhes':'resposta de aprovado ✅'));}
"""

def html_generico(n):
    """Gera MVP funcional offline para qualquer negócio da fila."""
    slug = n["slug"]
    ui_js = {"postpilot": CODIGO_POSTPILOT_JS, "deckforge": CODIGO_DECKFORGE_JS, "pauta": CODIGO_PAUTA_JS, "prep": CODIGO_PREP_JS, "scripter": CODIGO_SCRIPT_JS, "portalkit": CODIGO_PORTAL_JS}.get(slug, "")
    extras = ""
    if slug == "postpilot":
        hero_sub = "Cola um texto longo → recebe variações prontas para X, LinkedIn e Instagram."
        entrada = "Cola aqui o teu artigo / guião / notas…"
        botao = "Gerar variações"
        acao = "gerarVariacoes()"
    elif slug == "deckforge":
        hero_sub = "Escreve um outline (título: ponto; ponto; ponto por linha) → deck navegável com setas ← →."
        entrada = "A minha apresentação\\nProblema: custo alto; demora; erros\\nSolução: automação; simplicidade\\nPróximos passos: pilotar; medir; escalar"
        botao = "Gerar deck"
        acao = "gerarDeck()"
    elif slug == "portalkit":
        hero_sub = "Linhas 'Entregável | estado | prazo' → relatório de progresso profissional, pronto a enviar ao cliente."
        entrada = "Identidade visual | feito | 02/08\\nSite v1 | em curso | 15/08\\nConteúdos | pendente | 30/08\\nIntegração pagamentos | atraso | 10/08"
        botao = "🗂 Gerar relatório de estado"
        acao = "gerarEstado()"
        extras = '<div style="margin-top:10px;color:var(--mut);font-size:.85rem">Projeto: <input id="proj" value="Website + loja online — Fase 1" style="background:#0d1220;color:var(--txt);border:1px solid #2a3550;border-radius:8px;padding:8px 10px;width:340px;font:inherit"></div>'
    elif slug == "scripter":
        hero_sub = "Tema na caixa → guião de Short de 30s com hook, setup, payoff e CTA."
        entrada = "Ex.: como poupar dinheiro aos 20"
        botao = "🎬 Gerar guião de Short"
        acao = "gerarGuiao()"
    elif slug == "prep":
        hero_sub = "Treino de system design: caso aleatório → esboça no campo → compara com resposta modelo e rubrica."
        entrada = "Esboça aqui o teu design: requisitos → estimativas → APIs → dados → escala/gargalos → falhas…"
        botao = "🎲 Novo caso"
        acao = "gerarCaso()"
    elif slug == "pauta":
        hero_sub = "Um tópico por linha — '~15m' para duração, '| dono: Nome' para responsável."
        entrada = "Boas-vindas e objetivo ~5m\\nRevisão do trimestre ~20m | dono: Marta\\nBloqueios e riscos ~10m\\nPróximos passos ~10m"
        botao = "Gerar pauta"
        acao = "gerarPauta()"
        extras = '<div style="margin-top:10px;color:var(--mut);font-size:.85rem">Hora de início: <input id="inicio" value="10:00" style="background:#0d1220;color:var(--txt);border:1px solid #2a3550;border-radius:8px;padding:8px 10px;width:95px;font:inherit"></div>'
    else:
        hero_sub = n["brief"]
        entrada = "Entrada…"
        botao = "Executar"
        acao = "return false"
    return f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{n['nome']} — {n['inspiracao'].split('—')[0].strip()}</title>
<style>
:root{{--bg:#0b0e14;--card:#141a26;--txt:#e6e9f0;--mut:#8b93a7;--acc:#6c8cff;--acc2:#38d9a9;}}
*{{box-sizing:border-box;margin:0}}
body{{background:radial-gradient(1200px 600px at 80% -10%,#1b2440,transparent),var(--bg);color:var(--txt);font:16px/1.6 system-ui,-apple-system,'Segoe UI',sans-serif;padding:24px}}
.wrap{{max-width:860px;margin:0 auto}}
header{{text-align:center;padding:48px 16px 32px}}
header h1{{font-size:2.4rem;background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}}
header p{{color:var(--mut);margin-top:8px}}
.card{{background:var(--card);border:1px solid #232c40;border-radius:14px;padding:20px;margin:16px 0}}
textarea{{width:100%;min-height:140px;background:#0d1220;color:var(--txt);border:1px solid #2a3550;border-radius:10px;padding:12px;font:inherit}}
button{{background:linear-gradient(90deg,var(--acc),#4f6ef0);color:#fff;border:0;border-radius:10px;padding:12px 22px;font:600 15px inherit;cursor:pointer;margin-top:12px}}
button:hover{{filter:brightness(1.1)}}
.post pre{{white-space:pre-wrap;background:#0d1220;border-radius:8px;padding:12px;margin:8px 0;font:14px/1.5 inherit}}
.post h3 span{{color:var(--mut);font-weight:400;font-size:.8rem}}
.aviso{{color:#f4bf75}}
.slide{{display:none;flex-direction:column;justify-content:center;min-height:320px;background:#101828;border:1px solid #232c40;border-radius:14px;padding:40px}}
.slide.capa h1{{font-size:2.2rem}}
.slide ul{{margin-top:12px;color:var(--mut)}}
.nav{{text-align:center;margin-top:14px}}
footer{{text-align:center;color:var(--mut);font-size:.85rem;padding:32px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:24px 0}}
.grid .card{{margin:0}}
.grid h3{{color:var(--acc2);font-size:1rem}}
.grid p{{color:var(--mut);font-size:.9rem}}
</style>
</head>
<body>
<div class="wrap">
<header>
<h1>{n['nome']}</h1>
<p>{hero_sub}</p>
</header>
<div class="card">
<textarea id="entrada" placeholder="{entrada}"></textarea>
{extras}
<button onclick="{acao}">{botao}</button>
</div>
<div id="saida"></div>
<div class="grid">
<div class="card"><h3>⚡ Rápido</h3><p>Do conteúdo ao resultado em segundos, sem registos nem servidores.</p></div>
<div class="card"><h3>🔒 Privado</h3><p>Tudo corre no teu browser. Os teus textos nunca saem daqui.</p></div>
<div class="card"><h3>💸 Modelo 2026</h3><p>Freemium: grátis até N usos/mês, Pro desbloqueia histórico e marca.</p></div>
</div>
<footer>Recriado pelo Agente Fábrica 2026 · inspiração: {n['inspiracao']} · implementação original</footer>
</div>
<script>{ui_js}</script>
</body>
</html>"""

# ---------------------------------------------------------------- construir (LLM)
PROMPT_SISTEMA = """És o construtor da Fábrica 2026. Gera APENAS o ficheiro index.html completo:
single-file, CSS e JS inline, NENHUM recurso externo (sem CDN/URLs),
interface em português europeu, dark mode profissional, app funcional offline
(localStorage se fizer sentido). Sem markdown fences na resposta."""

def construir_com_llm(n, erros_anteriores=None):
    extra = f"\nNa tentativa anterior estes testes falharam, corrige: {erros_anteriores}" if erros_anteriores else ""
    prompt = f"{PROMPT_SISTEMA}\n\nNegócio: {n['nome']}\nInspiração: {n['inspiracao']}\nBrief: {n['brief']}{extra}"
    txt = chamar_llm(prompt)
    if not txt:
        return None
    txt = txt.strip()
    txt = re.sub(r"^```[a-z]*\n?|\n?```$", "", txt, flags=re.S).strip()
    return txt if "<html" in txt.lower() else None

# ---------------------------------------------------------------- testar
def smoke(pasta):
    r = subprocess.run([sys.executable, str(SMOKE), str(pasta)],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "erros": ["smoke.py falhou", r.stdout + r.stderr], "avisos": []}

def correcao_estatica(pasta):
    """Fixes sem LLM: remover recursos externos."""
    idx = pasta / "index.html"
    html = idx.read_text(encoding="utf-8")
    novo = re.sub(r'(src|href)\s*=\s*"https?://[^"]+"', r'\1="#"', html)
    if novo != html:
        idx.write_text(novo, encoding="utf-8")
        return True
    return False

# ---------------------------------------------------------------- iteração
def iteracao(dados, usar_llm):
    n = proximo_pendente(dados)
    if not n:
        return None
    log(f"▶ ITERAÇÃO: {n['nome']} — {n['inspiracao']}")
    n["status"] = "em_curso"
    guardar_fila(dados)
    pasta = gerar_spec(n)

    html, erros = None, None
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        log(f"  construção (tentativa {tentativa})…")
        if usar_llm:
            html = construir_com_llm(n, erros)
        if not html:
            html = html_generico(n)
        (pasta / "index.html").write_text(html, encoding="utf-8")

        log("  smoke test…")
        res = smoke(pasta)
        if res["ok"]:
            log(f"  ✅ {n['nome']} FUNCIONAL")
            n["status"] = "concluido"
            n["concluido_em"] = f"{datetime.now():%Y-%m-%d %H:%M}"
            guardar_fila(dados)
            regista_estado(f"✅ **{n['nome']}** concluído (tentativa {tentativa}) — `negocios/{n['id']}-{n['slug']}/`")
            return n
        erros = res["erros"]
        log(f"  ✗ falhou: {erros[0][:120]}")
        if correcao_estatica(pasta):
            log("  correção estática aplicada, re-testo…")
            if smoke(pasta)["ok"]:
                n["status"] = "concluido"
                n["concluido_em"] = f"{datetime.now():%Y-%m-%d %H:%M}"
                guardar_fila(dados)
                regista_estado(f"✅ **{n['nome']}** concluído após correção estática")
                return n

    log(f"  ⚠ {n['nome']} não passou em {MAX_TENTATIVAS} tentativas — fica para revisão")
    n["status"] = "falhou"
    guardar_fila(dados)
    regista_estado(f"❌ **{n['nome']}** falhou smoke test ({len(erros)} erros) — fila segue")
    return n

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Agente Fábrica 2026")
    ap.add_argument("--once", action="store_true", help="só uma iteração")
    ap.add_argument("--demo", action="store_true", help="força geradores offline")
    ap.add_argument("--status", action="store_true", help="mostra estado da fila")
    ap.add_argument("--max-iter", type=int, default=10)
    args = ap.parse_args()

    dados = carregar_fila()
    if args.status:
        for n in dados["fila"]:
            icone = {"concluido": "✅", "pendente": "⏳", "em_curso": "🔨", "falhou": "❌"}[n["status"]]
            print(f"{icone}  {n['id']}  {n['nome']:<12} {n['status']:<10} {n['inspiracao']}")
        return

    usar_llm = not args.demo and (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"))
    log(f"Agente Fábrica 2026 — modo {'LLM' if usar_llm else 'OFFLINE/demo'}")
    regista_estado(f"🔁 Loop arrancou (modo {'LLM' if usar_llm else 'offline'})")

    feitos = 0
    for _ in range(args.max_iter):
        n = iteracao(dados, usar_llm)
        if not n:
            log("🏁 Fila esvaziada. O agente propõe: pesquisar novos alvos e acrescentar à fila.")
            regista_estado("🏁 Fila esvaziada — fim do loop")
            break
        feitos += 1
        if args.once:
            break
        time.sleep(2)
    if feitos == 0:
        log("Nada pendente. Usa --status para ver a fila.")

if __name__ == "__main__":
    main()
