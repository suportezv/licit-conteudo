#!/usr/bin/env python3
"""Biblioteca comum das pecas do formato "Por Dentro da Granja" (HyperFrames).

Cada peca tem um gera.py que:
  1. define SEG (narracao por segmento, chaves "01".."NN");
  2. cria Peca(SEG, ...), marca cues (cap/sfx/ev/cam), HUD (hud_set/val/delta/dot), cartoes extras (card)
     e os dados genericos do diorama (diorama(...));
  3. chama p.write(), que escreve timeline.json, index.html e compositions/{hud,legendas,cartoes}.html.

A sincronia vem de assets/audio/duracoes.json (duracao de cada nKK.mp3) e de assets/audio/palavras.json
(Scribe, tempo por palavra), alinhados ao texto por difflib. O diorama e o lib/diorama.js copiado
para a pasta da peca; ele le window.__DIO = {events, cam, t_end, generico}.
"""
import json, re, math, html, difflib, subprocess
from pathlib import Path

W, H, FPS = 1080, 1920, 30
MAG, LAV, CIANO, NAVY, CREME, VERDE, AMARELO = "#A8F27A", "#B8C5BC", "#7FD3C4", "#101218", "#F4F6F9", "#A8F27A", "#F2C94C"
ERRO, FLO = "#FF6B5B", "#243D32"
FONTE = "@font-face { font-family: Sora; src: url('assets/Sora-Variable.ttf') format('truetype'); font-weight: 100 800; }"
IMPACTO = {"alarm", "horn", "buzzer", "sting", "thud", "zap", "water", "confetti", "generator", "bulldozer"}
# eventos de construcao da Parte 1 que, numa granja pronta, ficam no passado remoto
CONSTRUCAO = ["lots", "dozer", "stamp", "shed1", "shed2", "shed3", "equip", "tower", "poles", "fans_on", "canal", "lagoon",
              "fence", "portaria", "embarc", "compost", "visitor", "truck1_in", "truck2", "pigs", "sacks_start", "workers", "ghost_on"]
CONSTRUCAO_FIM = ["dozer_end", "sacks_end", "ghost_off", "truck1_out"]
NUNCA = ["blackout", "gen_on", "heat"]

FMT_JS = {
    "brl": '(v<0?"- R$ ":"R$ ")+Math.abs(Math.round(v)).toLocaleString("pt-BR")',
    "int": 'Math.round(v).toLocaleString("pt-BR")',
    "float1": 'v.toFixed(1).replace(".",",")',
    "float2": 'v.toFixed(2).replace(".",",")',
    "pct": 'Math.round(v)+"%"',
    "kg": 'v.toFixed(1).replace(".",",")+" kg"',
    "hhmm": '(Math.floor(v)+"").padStart(2,"0")+":"+(Math.round((v-Math.floor(v))*60)+"").padStart(2,"0")',
}
COR_JS = {
    "sinal": f'(v<0?"{MAG}":(v>0?"{VERDE}":"{CREME}"))',
    "fixa": f'"{CREME}"',
    "neg_mag": f'(v<0?"{MAG}":"{CREME}")',
}

def norm(w): return re.sub(r"[^\wÀ-ÿ']", "", w).lower()
def fmt_mi(v):
    a = abs(v)
    if a >= 1000000: s = f"{a/1e6:.1f}".replace(".", ",").replace(",0", ""); return f"R$ {s} mi"
    return f"R$ {a//1000:.0f} mil"

class Peca:
    def __init__(self, SEG, pausa_seg=None, lead=0.6, gap=0.35, gap_pausa=0.6, tail=2.2):
        self.SEG = SEG; self.ORD = sorted(SEG)
        self.DUR = {k: float(v) for k, v in json.load(open("assets/audio/duracoes.json")).items()}
        faltam = [k for k in self.ORD if k for k in [k] if k not in self.DUR]
        if faltam: raise SystemExit(f"sem duracao para {faltam}: rode narra.py")
        self.START = {}; t = lead
        for i, k in enumerate(self.ORD):
            self.START[k] = round(t, 3)
            prox = self.ORD[i + 1] if i + 1 < len(self.ORD) else None
            g = gap_pausa if (pausa_seg and (k == pausa_seg or prox == pausa_seg)) else gap
            t += self.DUR[k] + g
        self.T_END = round(t - gap + tail, 2); self.TOTAL = math.ceil(self.T_END)
        self._alinha()
        self.CAP = []; self.SFX = []; self.EV = {}; self.CAM = []
        self.hud = None; self.hud2 = None; self.VAL = []; self.VAL2 = []; self.DELTA = []; self.DOT = []; self.HUDJS = []
        self.cards = []; self.gen = {}; self.extra_audio = []; self.cenas = None; self.cena_nome = None
        self.pausa_seg = pausa_seg

    # ---------------- tempo
    def words(self, k): return [norm(w) for w in self.SEG[k].split()]
    def _alinha(self):
        P = Path("assets/audio/palavras.json"); PAL = json.load(open(P)) if P.exists() else {}
        self.TIMES = {}
        for k in self.ORD:
            sw = self.words(k); n = len(sw); S = self.START[k]; D = self.DUR[k]
            if k not in PAL:
                self.TIMES[k] = [(S + D * i / n, S + D * (i + 1) / n) for i in range(n)]; continue
            pw = [norm(x["w"]) for x in PAL[k]]; m = [None] * n
            for a, b, l in difflib.SequenceMatcher(None, sw, pw, autojunk=False).get_matching_blocks():
                for j in range(l): m[a + j] = (PAL[k][b + j]["s"], PAL[k][b + j]["e"])
            idx = [i for i, x in enumerate(m) if x]
            for i in range(n):
                if m[i]: continue
                pv = max([j for j in idx if j < i], default=None); nx = min([j for j in idx if j > i], default=None)
                t0 = m[pv][1] if pv is not None else 0.0; t1 = m[nx][0] if nx is not None else D
                lo = pv + 1 if pv is not None else 0; hi = nx if nx is not None else n; c = hi - lo
                m[i] = (t0 + (t1 - t0) * (i - lo) / c, t0 + (t1 - t0) * (i - lo + 1) / c)
            self.TIMES[k] = [(round(S + a, 3), round(S + b, 3)) for a, b in m]
            if len(idx) < 0.6 * n: print(f"aviso: segmento {k} so casou {len(idx)}/{n} palavras")
    def at(self, k, anchor, occ=1, nudge=0.0):
        sw = self.words(k); a = norm(anchor); n = 0
        for i, w in enumerate(sw):
            if (w == a) if len(a) <= 2 else w.startswith(a):
                n += 1
                if n == occ: return round(self.TIMES[k][i][0] - 0.04 + nudge, 3)
        raise SystemExit(f"ancora nao achada: {k} {anchor} x{occ}")
    def start(self, k): return self.START[k]
    def end(self, k): return round(self.START[k] + self.DUR[k], 3)

    # ---------------- cues
    def cap(self, t, l1, l2=""): self.CAP.append((round(t, 3), l1, l2))
    def sfx(self, t, n, vol=0.9): self.SFX.append((round(t, 3), n, vol))
    def ev(self, name, t): self.EV[name] = round(t, 3)
    def cam(self, t, az, el, hw, tx=0, tz=0): self.CAM.append((round(t, 3), round(az - 1.2 * t, 3), el, hw, tx, tz))
    def pausa(self, k=None, fim="Bora"):
        k = k or self.pausa_seg
        self.ev("pause_start", self.START[k] - 0.3); self.ev("pause_end", self.at(k, fim) - 0.15)
        self.sfx(self.START[k] - 0.3, "pause", 0.8); self.sfx(self.at(k, fim) - 0.15, "play", 0.8)
    def endcard(self, t, sub="segue a Licit"): self.ev("endcard", t); self.sfx(self.T_END - 2.0, "sting", 0.9); self.endcard_sub = sub
    def audio(self, src, t, dur, track, vol, fade=0.0):
        self.extra_audio.append((src, round(t, 3), round(dur, 3), track, vol, fade))
    def tiques(self, t0, t1, vol=0.22):
        tt = t0; j = 0
        while tt < t1 - 0.5:
            self.audio("tick_loop", tt, min(3.0, t1 - tt), 25, vol); tt += 2.95; j += 1

    # ---------------- HUD
    def hud_set(self, label, inicial, fmt="brl", cor="sinal", dots=0, top=196):
        self.hud = dict(label=label, inicial=inicial, fmt=FMT_JS.get(fmt, fmt), cor=COR_JS.get(cor, cor), dots=dots, top=top)
    def hud2_set(self, label, inicial, fmt="brl", cor="sinal"):
        self.hud2 = dict(label=label, inicial=inicial, fmt=FMT_JS.get(fmt, fmt), cor=COR_JS.get(cor, cor))
    def val(self, t, v, dur=0.9, ease="power2.out"): self.VAL.append((round(t, 3), v, dur, ease))
    def val2(self, t, v, dur=0.9, ease="power2.out"): self.VAL2.append((round(t, 3), v, dur, ease))
    def delta(self, t, texto, cor=MAG, dur=2.2): self.DELTA.append((round(t, 3), texto, cor, dur))
    def dot(self, t, i, cor): self.DOT.append((round(t, 3), i, cor))
    def hud_hide(self, t): self.HUDJS.append(f'tl.to("#hud-wrap", {{ opacity: 0, y: -30, duration: 0.4 }}, {t});')
    def hud_show(self, t): self.HUDJS.append(f'tl.to("#hud-wrap", {{ opacity: 1, y: 0, duration: 0.4 }}, {t});')
    def pulse(self, t, alvo="#hud-pill"): self.HUDJS.append(f'tl.to("{alvo}", {{ scale: 1.06, duration: 0.18, yoyo: true, repeat: 1 }}, {t});')
    def hud_js(self, js): self.HUDJS.append(js)

    # ---------------- cartoes extras e diorama
    def card(self, css, html_, js): self.cards.append((css, html_, js))
    def diorama(self, **kw): self.gen.update(kw)
    def cena(self, nome, extras=()):
        """Cena 3D alternativa (lib/cena_<nome>.js registrada em window.__CENAS): maternidade, creche, intestino, parte3.
        extras: scripts classicos carregados antes da cena (ex.: kit3d.js)."""
        self.cena_nome = nome; self.cena_extras = list(extras)
    def dual(self, cenas, rotulos=("GRANJA A", "GRANJA B")):
        """Duas granjas empilhadas: cenas = [dict(generico=..., cam=[...]), dict(...)] (cam no formato de self.CAM, ja com a deriva descontada por self.cam_lista)."""
        self.cenas = [dict(canvas="dio-a", y=560, h=640, **cenas[0]), dict(canvas="dio-b", y=1240, h=640, **cenas[1])]
        for c, r in zip(self.cenas, rotulos):
            self.card(*tag(f"rot-{c['canvas']}", 0.3, self.T_END, r, 60, c["y"] - 6, "", track=3))
    def cam_lista(self, keys):
        """Converte [(t, az, el, hw, tx, tz), ...] em lista com a deriva descontada (para cenas do modo dual)."""
        return [(round(t, 3), round(az - 1.2 * t, 3), el, hw, tx, tz) for (t, az, el, hw, tx, tz) in keys]
    def granja_pronta(self):
        for n in CONSTRUCAO: self.EV.setdefault(n, -100)
        for n in CONSTRUCAO_FIM: self.EV.setdefault(n, -99)
        self.gen["pronta"] = True

    # ---------------- escrita
    def _caps(self):
        self.CAP.sort(); out = []
        p0 = self.EV.get("pause_start", 1e9); p1 = self.EV.get("pause_end", 1e9)
        for i, (t, l1, l2) in enumerate(self.CAP):
            nxt = self.CAP[i + 1][0] if i + 1 < len(self.CAP) else self.T_END
            d = min(nxt - t - 0.04, 6.5)
            if p0 <= t < p1: continue
            if t < p0: d = min(d, p0 - t - 0.05)
            out.append((round(t, 3), round(max(d, 0.6), 3), l1, l2))
        return out
    def _dur_audio(self, n):
        P = Path("assets/audio/duracoes_sfx.json"); D = json.load(open(P)) if P.exists() else {}
        if n not in D:
            out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/audio/{n}.mp3"], capture_output=True, text=True).stdout.strip()
            D[n] = round(float(out), 3); json.dump(D, open(P, "w"), indent=0)
        return D[n]
    def write(self):
        for n in NUNCA: self.EV.setdefault(n, 1e9)
        self.EV.setdefault("orbit", 1e9); self.EV.setdefault("confetti", 1e9)
        self.EV.setdefault("pause_start", 1e9); self.EV.setdefault("pause_end", 1e9)
        if "endcard" not in self.EV: self.endcard(self.T_END - 4.0)
        self.SFX.sort(); CAPS = self._caps(); T_END, TOTAL, EV = self.T_END, self.TOTAL, self.EV
        json.dump({"start": self.START, "dur": self.DUR, "t_end": T_END, "total": TOTAL, "caps": CAPS, "sfx": self.SFX,
                   "events": EV, "cam": self.CAM, "val": self.VAL, "val2": self.VAL2, "delta": self.DELTA, "generico": self.gen},
                  open("timeline.json", "w"), ensure_ascii=False, indent=1)
        # ---- audio
        aud = []
        for k in self.ORD:
            aud.append(f'<audio id="n{k}" class="clip" src="assets/audio/n{k}.mp3" data-start="{self.START[k]}" data-duration="{round(self.DUR[k], 3)}" data-track-index="20" data-volume="1"></audio>')
        for i, (t, n, vol) in enumerate(self.SFX):
            v = round(min(1.0, vol / 0.8) * (0.7 if n in IMPACTO else 1.0), 3)
            aud.append(f'<audio id="sfx{i:02d}" class="clip" src="assets/audio/{n}.mp3" data-start="{t}" data-duration="{self._dur_audio(n)}" data-track-index="{21 + i % 4}" data-volume="{v}"></audio>')
        for i, (src, t, d, tr, vol, fade) in enumerate(self.extra_audio):
            d = round(min(d, self._dur_audio(src)), 3); f = f' data-fade-in="{fade}" data-fade-out="{fade}"' if fade else ""
            aud.append(f'<audio id="x{i:02d}" class="clip" src="assets/audio/{src}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{tr}" data-volume="{vol}"{f}></audio>')
        tt = 0.0; j = 0
        while tt < T_END:
            d = round(min(21.6, self._dur_audio("bed"), T_END - tt), 3)
            aud.append(f'<audio id="bed{j:02d}" class="clip" src="assets/audio/bed.mp3" data-start="{round(tt,3)}" data-duration="{d}" data-track-index="26" data-volume="0.07" data-fade-in="0.6" data-fade-out="0.6"></audio>')
            tt += 21.3; j += 1
        dio_obj = {"events": EV, "cam": self.CAM, "t_end": T_END, "generico": self.gen, "parte2": bool(self.gen.get("pronta")), "cena": self.cena_nome}
        cena_script = ("".join(f'<script src="{e}"></script>\n' for e in getattr(self, "cena_extras", [])) + f'<script src="cena_{self.cena_nome}.js"></script>\n') if self.cena_nome else ""
        canvases = f'<canvas id="dio-canvas" width="{W}" height="{H}"></canvas>'
        if self.cenas:
            dio_obj["cenas"] = [dict(canvas=c["canvas"], w=W, h=c["h"], generico=c.get("generico", {}), cam=c.get("cam")) for c in self.cenas]
            canvases = "".join(f'<canvas id="{c["canvas"]}" width="{W}" height="{c["h"]}" style="position:absolute; left:0; top:{c["y"]}px; width:{W}px; height:{c["h"]}px"></canvas>' for c in self.cenas)
        dio = json.dumps(dio_obj, ensure_ascii=False)
        Path("index.html").write_text(f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait" data-fps="{FPS}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="vendor/gsap.min.js"></script>
<style>
  {FONTE}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#101218; }}
  #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family: Sora, sans-serif; }}
  #dio {{ position:absolute; inset:0; z-index:0; background: #101218; }}
  #dio canvas {{ position:absolute; inset:0; width:{W}px; height:{H}px; display:block; }}
  #dio canvas[id^="dio-"] {{ inset:auto; }}
  #dio.gray canvas {{ filter: grayscale(1) brightness(0.55); }}
  #dio.worn canvas {{ filter: saturate(0.5) brightness(0.9); }}
  #dio.noite canvas {{ filter: brightness(0.45) saturate(0.7) hue-rotate(-15deg); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
  <div id="dio" data-layout-ignore>{canvases}</div>
  <div id="hud" data-composition-id="hud" data-composition-src="compositions/hud.html" data-start="0" data-duration="{TOTAL}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:2"></div>
  <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:3"></div>
  <div id="cartoes" data-composition-id="cartoes" data-composition-src="compositions/cartoes.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:4"></div>
  {chr(10).join("  " + a for a in aud)}
</div>
<script>
  window.__DIO = {dio};
  window.__hf = window.__hf || {{}}; window.__hf.buildReady = window.__hf.buildReady || {{}};
  window.__hf.buildReady["diorama"] = new Promise(function (r) {{ window.__dioReady = r; }});
  const tl = gsap.timeline({{ paused: true }});
  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
{cena_script}<script type="module" src="diorama.js"></script>
</body>
</html>
''')
        # ---- hud
        h = self.hud or dict(label="", inicial=0, fmt=FMT_JS["brl"], cor=COR_JS["fixa"], dots=0, top=196)
        dots = "".join(f'<i id="dot{i}"></i>' for i in range(1, h["dots"] + 1))
        dots_html = f'<div id="dots">{dots}</div>' if h["dots"] else ""
        hud2_html = (f'<div id="hud-pill2"><div class="lbl">{html.escape(self.hud2["label"])}</div><div id="hud-val2">0</div></div>' if self.hud2 else "")
        delta_html = []; js = []
        for i, (t, texto, cor, dur) in enumerate(self.DELTA):
            delta_html.append(f'<div id="hud-d{i}" class="clip hud-delta" data-start="{t}" data-duration="{dur}" data-track-index="{i%2}"><div class="in" style="color:{cor}">{html.escape(texto)}</div></div>')
            js.append(f'tl.fromTo("#hud-d{i} .in",{{y:-18,opacity:0,scale:0.9}},{{y:0,opacity:1,scale:1,duration:0.22,ease:"back.out(2)"}},{t}); tl.to("#hud-d{i} .in",{{opacity:0,duration:0.35}},{t+dur-0.4});')
        for (t, v, dur, ease) in self.VAL: js.append(f'tl.to(st,{{v:{v},duration:{dur},ease:"{ease}",onUpdate:paint}},{t});')
        for (t, v, dur, ease) in self.VAL2: js.append(f'tl.to(st2,{{v:{v},duration:{dur},ease:"{ease}",onUpdate:paint2}},{t});')
        for (t, i, cor) in self.DOT: js.append(f'tl.to("#dot{i}",{{backgroundColor:"{cor}",scale:1.25,duration:0.25,ease:"back.out(2)"}},{t}); tl.to("#dot{i}",{{scale:1,duration:0.2}},{t+0.25});')
        js += self.HUDJS
        hud_visivel = "" if self.hud else "display:none;"
        Path("compositions/hud.html").write_text(f'''<template>
<style>
  {FONTE}
  #root {{ position:absolute; inset:0; font-family: Sora, sans-serif; }}
  #hud-wrap {{ position:absolute; left:0; right:0; top:{h["top"]}px; text-align:center; {hud_visivel} }}
  #hud-pill, #hud-pill2 {{ display:inline-block; padding:14px 44px 16px; border-radius:40px; background:rgba(30,50,41,0.88); border:3px solid {LAV}; text-align:center; box-shadow:0 10px 40px rgba(16,18,24,0.5); vertical-align:top; }}
  #hud-pill2 {{ margin-left:18px; padding:12px 34px 14px; }}
  #hud-lbl, .lbl {{ color:{LAV}; font-size:28px; font-weight:700; letter-spacing:0.22em; }}
  #hud-val {{ color:{CREME}; font-size:62px; font-weight:700; letter-spacing:-0.01em; line-height:1.05; font-variant-numeric: tabular-nums; white-space:nowrap; }}
  #hud-val2 {{ color:{CREME}; font-size:50px; font-weight:700; letter-spacing:-0.01em; line-height:1.1; font-variant-numeric: tabular-nums; white-space:nowrap; }}
  #dots {{ display:flex; gap:14px; justify-content:center; margin-top:10px; }}
  #dots i {{ display:block; width:22px; height:22px; border-radius:50%; background:rgba(168,242,122,0.25); border:2px solid {LAV}; }}
  .hud-delta {{ position:absolute; left:0; right:0; top:{h["top"] + 140 + (48 if h["dots"] else 0)}px; text-align:center; }}
  .hud-delta .in {{ display:inline-block; font-size:38px; line-height:1.1; font-weight:700; letter-spacing:-0.01em; white-space:nowrap; }}
  #hud-logo {{ position:absolute; left:56px; bottom:84px; width:210px; opacity:0.96; filter: drop-shadow(0 4px 14px rgba(16,18,24,0.6)); }}
</style>
<div id="root" data-composition-id="hud" data-width="{W}" data-height="{H}">
  <div id="hud-wrap"><div id="hud-pill"><div id="hud-lbl">{html.escape(h["label"])}</div><div id="hud-val">0</div>{dots_html}</div>{hud2_html}</div>
  {chr(10).join("  " + d for d in delta_html)}
  <img id="hud-logo" src="assets/logo_wordmark.png" alt="" data-layout-ignore />
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  const st = {{ v: {h["inicial"]} }}; const el = document.querySelector("#hud-val");
  function paint() {{ const v = st.v; el.textContent = {h["fmt"]}; el.style.color = {h["cor"]}; }}
  paint();
  const st2 = {{ v: {self.hud2["inicial"] if self.hud2 else 0} }}; const el2 = document.querySelector("#hud-val2");
  function paint2() {{ if (!el2) return; const v = st2.v; el2.textContent = {self.hud2["fmt"] if self.hud2 else '""'}; el2.style.color = {self.hud2["cor"] if self.hud2 else '"#fff"'}; }}
  paint2();
  tl.fromTo("#hud-wrap", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 0.25);
  {chr(10).join("  " + x for x in js)}
  tl.to("#hud-logo", {{ opacity: 0, duration: 0.4 }}, {EV["endcard"]});
  window.__timelines["hud"] = tl;
</script>
</template>
''')
        # ---- legendas
        cap_html = []; cap_tw = []
        for i, (t, d, l1, l2) in enumerate(CAPS):
            n = max(len(l1), len(l2)); fs = 64 if n <= 22 else (54 if n <= 27 else (46 if n <= 32 else 40))  # linha longa encolhe, nunca quebra em 3
            l2h = f'<div class="l2" style="font-size:{fs}px">{html.escape(l2)}</div>' if l2 else ""
            cap_html.append(f'<div id="cap{i:02d}" class="clip cap" data-start="{t}" data-duration="{d}" data-track-index="{i%2}"><div class="in"><div class="l1" style="font-size:{fs}px">{html.escape(l1)}</div>{l2h}</div></div>')
            cap_tw.append(f'tl.fromTo("#cap{i:02d} .in",{{opacity:0,y:26,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.26,ease:"power3.out"}},{t});')
        top_cap = h["top"] + 212 + (48 if h["dots"] else 0) + (0 if self.hud else -200)
        Path("compositions/legendas.html").write_text(f'''<template>
<style>
  {FONTE}
  #root {{ position:absolute; inset:0; font-family: Sora, sans-serif; }}
  .cap {{ position:absolute; left:90px; right:90px; top:{top_cap}px; text-align:center; }}
  .cap .in {{ display:inline-block; padding:14px 36px 18px; border-radius:30px; background:rgba(16,18,24,0.62); }}
  .cap .l1 {{ color:{CREME}; font-size:64px; font-weight:700; line-height:1.12; letter-spacing:-0.015em; text-shadow:0 4px 24px rgba(16,18,24,0.7); }}
  .cap .l2 {{ color:{MAG}; font-size:64px; font-weight:700; line-height:1.12; letter-spacing:-0.015em; text-shadow:0 4px 24px rgba(16,18,24,0.7); }}
</style>
<div id="root" data-composition-id="legendas" data-width="{W}" data-height="{H}">
  {chr(10).join("  " + c for c in cap_html)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + x for x in cap_tw)}
  window.__timelines["legendas"] = tl;
</script>
</template>
''')
        # ---- cartoes
        p0, p1 = EV["pause_start"], EV["pause_end"]
        pausa_html = pausa_js = ""
        if p0 < 1e8:
            pausa_html = f'''  <div id="pausa" class="clip" data-start="{p0}" data-duration="{round(p1-p0,3)}" data-track-index="0" data-layout-allow-overlap>
    <div class="bg"></div><div class="ic"><i></i><i></i></div>
    <div class="t1">Pausa rapidinha!</div>
    <div class="t2">Deixa o like e segue a <b>Licit</b></div>
  </div>'''
            pausa_js = f'''  tl.fromTo("#pausa .bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {p0});
  tl.fromTo("#pausa .ic", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {p0 + 0.1});
  tl.fromTo("#pausa .t1", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {p0 + 0.25});
  tl.fromTo("#pausa .t2", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {p0 + 0.45});'''
        e0 = EV["endcard"]
        css_x = "\n".join(c for c, _, _ in self.cards); html_x = "\n".join(h_ for _, h_, _ in self.cards); js_x = "\n".join(j for _, _, j in self.cards)
        Path("compositions/cartoes.html").write_text(f'''<template>
<style>
  {FONTE}
  #root {{ position:absolute; inset:0; font-family: Sora, sans-serif; }}
  #pausa {{ position:absolute; inset:0; }}
  #pausa .bg {{ position:absolute; inset:0; background:rgba(16,18,24,0.62); }}
  #pausa .ic {{ position:absolute; left:50%; top:760px; width:230px; height:230px; margin-left:-115px; border-radius:50%; background:{CREME}; display:flex; align-items:center; justify-content:center; gap:26px; box-shadow:0 12px 50px rgba(0,0,0,0.5); }}
  #pausa .ic i {{ display:block; width:30px; height:92px; background:{NAVY}; border-radius:8px; }}
  #pausa .t1 {{ position:absolute; left:0; right:0; top:1040px; text-align:center; color:{CREME}; font-size:70px; font-weight:700; }}
  #pausa .t2 {{ position:absolute; left:0; right:0; top:1140px; text-align:center; color:{CREME}; font-size:38px; font-weight:700; opacity:0.95; }}
  #pausa .t2 b {{ color:{MAG}; }}
  .pil {{ display:inline-block; padding:22px 40px 26px; border-radius:40px; background:rgba(30,50,41,0.9); border:3px solid {LAV}; text-align:center; min-width:380px; }}
  .pil .k {{ color:{LAV}; font-size:28px; font-weight:700; letter-spacing:0.2em; }}
  .pil .v {{ color:{CREME}; font-size:60px; font-weight:700; line-height:1.1; white-space:nowrap; }}
  .tag {{ position:absolute; display:inline-block; padding:12px 28px 14px; border-radius:28px; background:rgba(16,18,24,0.78); color:{CREME}; font-size:34px; font-weight:700; white-space:nowrap; }}
  .tag.mag {{ color:{MAG}; }} .tag.verde {{ color:{VERDE}; }} .tag.amarelo {{ color:{AMARELO}; }}
  #fim {{ position:absolute; inset:0; }}
  #fim .bg {{ position:absolute; left:0; right:0; bottom:0; height:1150px; background:linear-gradient(180deg, rgba(16,18,24,0) 0%, rgba(16,18,24,0.9) 22%, rgba(16,18,24,0.97) 100%); }}
  #fim .logo {{ position:absolute; left:50%; top:1080px; width:340px; margin-left:-170px; }}
  #fim .logo img {{ width:340px; display:block; }}
  #fim .nome {{ position:absolute; left:50%; top:1440px; width:560px; margin-left:-280px; }}
  #fim .nome img {{ width:560px; display:block; }}
  #fim .sub {{ position:absolute; left:0; right:0; top:1640px; text-align:center; color:{LAV}; font-size:34px; font-weight:700; }}
{css_x}
</style>
<div id="root" data-composition-id="cartoes" data-width="{W}" data-height="{H}">
{pausa_html}
{html_x}
  <div id="fim" class="clip" data-start="{e0}" data-duration="{round(T_END-e0,3)}" data-track-index="0" data-layout-allow-overlap>
    <div class="bg"></div><div class="logo"><img src="assets/logo_marca.png" alt="" /></div><div class="nome"><img src="assets/logo_wordmark.png" alt="" /></div><div class="sub">{html.escape(getattr(self, "endcard_sub", "segue a Licit"))}</div>
  </div>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
{pausa_js}
{js_x}
  tl.fromTo("#fim .bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {e0});
  tl.fromTo("#fim .logo", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.6)" }}, {e0 + 0.15});
  tl.fromTo("#fim .nome", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {e0 + 0.35});
  tl.fromTo("#fim .sub", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {e0 + 0.55});
  window.__timelines["cartoes"] = tl;
</script>
</template>
''')
        pct = round(100 * p0 / T_END) if p0 < 1e8 else None
        print(f"segmentos: {len(self.ORD)}  fim da fala {self.end(self.ORD[-1])}s  T_END {T_END}s  TOTAL {TOTAL}s")
        print(f"legendas {len(CAPS)}  sfx {len(self.SFX)}  audios {len(aud)}  pausa {p0 if pct else '-'}-{p1 if pct else '-'} ({pct}%)")

def pilulas(id_, t0, t1, itens, top=1380, track=2, compacta=False):
    """Cartao de pilulas lado a lado. itens: [(k, v, classe)]; devolve (css, html, js) para Peca.card."""
    h = "".join(f'<div class="pil {c}"><div class="k">{html.escape(k)}</div><div class="v" id="{id_}-v{i}">{html.escape(v)}</div></div>' for i, (k, v, c) in enumerate(itens))
    css = f"  #{id_} {{ position:absolute; left:0; right:0; top:{top}px; display:flex; justify-content:center; gap:32px; }}\n  #{id_} .pil.mag .v {{ color:{MAG}; }} #{id_} .pil.verde .v {{ color:{VERDE}; }}"
    if compacta: css += f"\n  #{id_} .pil {{ min-width:200px; padding:14px 22px 18px; }} #{id_} .pil .v {{ font-size:44px; }} #{id_} .pil .k {{ font-size:28px; letter-spacing:0.1em; }}"
    html_ = f'  <div id="{id_}" class="clip" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}">{h}</div>'
    js = "".join(f'  tl.fromTo("#{id_} .pil:nth-child({i+1})", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, {t0 + 0.5*i});\n' for i in range(len(itens)))
    js += f'  tl.to("#{id_}", {{ opacity: 0, duration: 0.4 }}, {t1 - 0.4});'
    return css, html_, js

def tag(id_, t0, t1, texto, x, y, classe="", track=3):
    """Etiqueta flutuante (DOM) numa posicao fixa da tela."""
    css = ""
    html_ = f'  <div id="{id_}" class="clip tag {classe}" style="left:{x}px; top:{y}px" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}">{html.escape(texto)}</div>'
    js = f'  tl.fromTo("#{id_}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, {t0});\n  tl.to("#{id_}", {{ opacity: 0, duration: 0.3 }}, {t1 - 0.3});'
    return css, html_, js

def medidor(id_, t0, t1, label, esq, dir_, de, para, top=1200, track=3, cor_fim=VERDE):
    """Medidor horizontal: pino anda de `de` para `para` (0..1 da trilha) entre t0+0.3 e t0+1.7."""
    css = f"""  #{id_} {{ position:absolute; left:50%; top:{top}px; width:760px; margin-left:-380px; padding:22px 30px 26px; border-radius:34px; background:rgba(16,18,24,0.72); }}
  #{id_} .k {{ color:{LAV}; font-size:28px; font-weight:700; letter-spacing:0.2em; text-align:center; }}
  #{id_} .trilho {{ position:relative; height:28px; border-radius:14px; background:rgba(168,242,122,0.25); margin-top:12px; }}
  #{id_} .pino {{ position:absolute; top:-10px; left:0; width:48px; height:48px; margin-left:-24px; border-radius:50%; background:{MAG}; box-shadow:0 6px 20px rgba(0,0,0,0.4); }}
  #{id_} .esc {{ display:flex; justify-content:space-between; color:{CREME}; font-size:30px; font-weight:800; margin-top:12px; }}"""
    html_ = f'''  <div id="{id_}" class="clip" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}">
    <div class="k">{html.escape(label)}</div><div class="trilho"><div class="pino"></div></div>
    <div class="esc"><span>{html.escape(esq)}</span><span>{html.escape(dir_)}</span></div></div>'''
    js = f'''  tl.fromTo("#{id_}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {t0});
  tl.fromTo("#{id_} .pino", {{ x: {round(700*de)} }}, {{ x: {round(700*para)}, duration: 1.4, ease: "power2.inOut" }}, {t0 + 0.3});
  tl.to("#{id_} .pino", {{ backgroundColor: "{cor_fim}", duration: 0.3 }}, {t0 + 1.5});
  tl.to("#{id_}", {{ opacity: 0, duration: 0.4 }}, {t1 - 0.4});'''
    return css, html_, js

def barras(id_, t0, t1, itens, top=1430, altura=300, track=1):
    """Barras verticais. itens: [(valor_txt, legenda, cor, fracao_altura)]."""
    n = len(itens); gap = 44 if n <= 3 else 24; wb = min(220, int((900 - gap * (n - 1)) / n))
    cols = "".join(f'<div class="b"><div class="col" style="height:{max(6, round(100*f))}%;min-height:16px;background:{c}"></div><div class="lb">{html.escape(v)}<small>{html.escape(l)}</small></div></div>' for v, l, c, f in itens)
    css = f"""  #{id_} {{ position:absolute; left:90px; right:90px; top:{top}px; height:{altura}px; display:flex; align-items:flex-end; justify-content:center; gap:{gap}px; }}
  #{id_} .b {{ width:{wb}px; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:100%; }}
  #{id_} .col {{ width:{wb}px; border-radius:16px 16px 6px 6px; transform-origin:bottom; }}
  #{id_} .lb {{ margin-top:12px; color:{CREME}; font-size:30px; font-weight:800; text-align:center; line-height:1.1; }}
  #{id_} .lb small {{ display:block; color:{LAV}; font-size:28px; font-weight:700; }}"""
    html_ = f'  <div id="{id_}" class="clip" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}">{cols}</div>'
    js = "".join(f'  tl.fromTo("#{id_} .b:nth-child({i+1}) .col", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 1.2, ease: "power2.out" }}, {t0 + 1.1*i});\n' for i in range(len(itens)))
    js += f'  tl.fromTo("#{id_} .lb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4, stagger: 1.1 }}, {t0 + 0.5});\n  tl.to("#{id_}", {{ opacity: 0, duration: 0.4 }}, {t1 - 0.4});'
    return css, html_, js


def grafico_linhas(id_, t0, t1, series, xlabels=("", ""), top=1210, altura=470, track=2):
    """Cartao com grafico de linhas em SVG, cada linha desenhada no seu tempo. series: [dict(pts=[(x, y)] em 0..1,
    cor, label (legenda), valor (texto no fim da linha), estilo "solida" | "pontilhada", t_ini (absoluto), dur)]."""
    W, HS = 900, altura - 118; ML, MR, MT, MB = 34, 34, 46, 54; PW, PH = W - ML - MR, HS - MT - MB
    def XY(x, y): return (round(ML + x * PW, 1), round(MT + (1 - y) * PH, 1))
    defs, paths, labels, leg, js = [], [], [], [], []
    for i, sr in enumerate(series):
        pts = [XY(x, y) for x, y in sr["pts"]]; d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="16 16"' if sr.get("estilo") == "pontilhada" else ""
        defs.append(f'<clipPath id="{id_}-c{i}"><rect id="{id_}-r{i}" x="0" y="0" width="0" height="{HS}"/></clipPath>')
        paths.append(f'<path d="{d}" fill="none" stroke="{sr["cor"]}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"{dash} clip-path="url(#{id_}-c{i})"/>')
        ex, ey = pts[-1]; anchor = "end" if ex > W * 0.6 else "start"
        labels.append(f'<text id="{id_}-t{i}" x="{ex - 14 if anchor == "end" else ex + 14}" y="{max(30, ey - 18)}" text-anchor="{anchor}" fill="{sr["cor"]}" font-size="32" font-weight="700">{html.escape(sr.get("valor", ""))}</text>')
        sw = f'<svg width="64" height="12" viewBox="0 0 64 12"><path d="M4,6 L60,6" stroke="{sr["cor"]}" stroke-width="8" stroke-linecap="round"{dash.replace("16 16", "10 10")}/></svg>'
        leg.append(f'<div class="lg" id="{id_}-l{i}">{sw}<span class="k">{html.escape(sr["label"])}</span><span class="v" style="color:{sr["cor"]}">{html.escape(sr.get("valor", ""))}</span></div>')
        ti, du = sr["t_ini"], sr["dur"]
        js.append(f'  tl.fromTo("#{id_}-l{i}", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {ti});')
        js.append(f'  tl.to("#{id_}-r{i}", {{ attr: {{ width: {W} }}, duration: {du}, ease: "none" }}, {ti});')
        js.append(f'  tl.fromTo("#{id_}-t{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {ti + du});')
    grid = "".join(f'<line x1="{ML}" y1="{XY(0, g)[1]}" x2="{W - MR}" y2="{XY(0, g)[1]}" stroke="rgba(168,242,122,0.22)" stroke-width="2"/>' for g in (0.333, 0.667, 1.0))
    base = f'<line x1="{ML}" y1="{XY(0, 0)[1]}" x2="{W - MR}" y2="{XY(0, 0)[1]}" stroke="rgba(168,242,122,0.5)" stroke-width="3"/>'
    xl = f'<text x="{ML}" y="{HS - 14}" fill="{LAV}" font-size="28" font-weight="700">{html.escape(xlabels[0])}</text><text x="{W - MR}" y="{HS - 14}" text-anchor="end" fill="{LAV}" font-size="28" font-weight="700">{html.escape(xlabels[1])}</text>'
    css = f"""  #{id_} {{ position:absolute; left:90px; top:{top}px; width:{W}px; height:{altura}px; padding:18px 0 0; border-radius:34px; background:rgba(16,18,24,0.72); overflow:hidden; }}
  #{id_} .legs {{ display:flex; justify-content:center; gap:40px; height:62px; align-items:center; }}
  #{id_} .lg {{ display:flex; align-items:center; gap:12px; opacity:0; }}
  #{id_} .lg .k {{ color:{LAV}; font-size:28px; font-weight:700; letter-spacing:0.12em; }} #{id_} .lg .v {{ font-size:32px; font-weight:800; }}
  #{id_} svg.g {{ display:block; margin-top:8px; font-family:inherit; }}"""
    html_ = (f'  <div id="{id_}" class="clip" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}"><div class="legs">{"".join(leg)}</div>'
             f'<svg class="g" width="{W}" height="{HS}" viewBox="0 0 {W} {HS}"><defs>{"".join(defs)}</defs>{grid}{base}{"".join(paths)}{"".join(labels)}{xl}</svg></div>')
    js_ = f'  tl.fromTo("#{id_}", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {t0});\n' + "\n".join(js) + f'\n  tl.to("#{id_}", {{ opacity: 0, duration: 0.4 }}, {t1 - 0.4});'
    return css, html_, js_


def conversa(id_, t0, t1, msgs, top=1150, track=3, largura=760, contato="Licit"):
    """Cartao de conversa no formato de WhatsApp (tema escuro). msgs: [(t, quem, texto)] com quem = "eu" (direita,
    balao verde) ou "ia" (esquerda, balao cinza, com indicador "digitando" 1 s antes). Painel entra em t0 e sai em t1."""
    def esc(x): return html.escape(x)
    itens = []
    for i, (t, quem, texto) in enumerate(msgs):
        if quem == "ia":
            itens.append(f'<div class="msg ia dig" id="{id_}-d{i}"><span></span><span></span><span></span></div>')
        itens.append(f'<div class="msg {quem}" id="{id_}-m{i}">{esc(texto)}<div class="hora">{"" if quem == "ia" else "✓✓ "}agora</div></div>')
    css = f"""  #{id_} {{ position:absolute; left:50%; top:{top}px; width:{largura}px; margin-left:-{largura//2}px; border-radius:34px; overflow:hidden; background:#0B141A; border:3px solid #2A3942; box-shadow:0 18px 60px rgba(0,0,0,0.55); font-family: inherit; }}
  #{id_} .top {{ display:flex; align-items:center; gap:18px; padding:18px 26px; background:#202C33; }}
  #{id_} .top img {{ width:64px; height:64px; border-radius:50%; background:#0B141A; object-fit:contain; padding:6px; }}
  #{id_} .top .nome {{ color:#E9EDEF; font-size:32px; font-weight:800; line-height:1.1; }} #{id_} .top .st {{ color:#8696A0; font-size:28px; }}
  #{id_} .corpo {{ padding:18px 22px 22px; display:flex; flex-direction:column; gap:12px; min-height:120px; }}
  #{id_} .msg {{ max-width:84%; padding:14px 20px 10px; border-radius:22px; color:#E9EDEF; font-size:30px; font-weight:600; line-height:1.25; opacity:0; }}
  #{id_} .msg.eu {{ align-self:flex-end; background:#005C4B; border-bottom-right-radius:6px; }}
  #{id_} .msg.ia {{ align-self:flex-start; background:#202C33; border-bottom-left-radius:6px; }}
  #{id_} .msg .hora {{ color:#9DB4BC; font-size:28px; font-weight:500; text-align:right; margin-top:4px; }} #{id_} .msg.eu .hora {{ color:#8FD3C7; }}
  #{id_} .msg.dig {{ display:flex; gap:8px; align-items:center; padding:16px 24px; }} #{id_} .msg.dig span {{ width:12px; height:12px; border-radius:50%; background:#8696A0; display:inline-block; }}"""
    html_ = (f'  <div id="{id_}" class="clip" data-start="{t0}" data-duration="{round(t1-t0,3)}" data-track-index="{track}">'
             f'<div class="top"><img src="assets/logo_marca.png" alt=""><div><div class="nome">{esc(contato)}</div><div class="st">online</div></div></div>'
             f'<div class="corpo">{"".join(itens)}</div></div>')
    js = [f'  tl.fromTo("#{id_}", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {t0});', f'  tl.to("#{id_}", {{ opacity: 0, y: 40, duration: 0.4 }}, {t1 - 0.4});']
    for i, (t, quem, texto) in enumerate(msgs):
        if quem == "ia":
            js.append(f'  tl.fromTo("#{id_}-d{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {max(t0 + 0.2, t - 1.1)}); tl.to("#{id_}-d{i} span", {{ y: -6, duration: 0.25, stagger: 0.12, repeat: 3, yoyo: true }}, {max(t0 + 0.2, t - 1.1)}); tl.set("#{id_}-d{i}", {{ display: "none" }}, {t});')
        js.append(f'  tl.fromTo("#{id_}-m{i}", {{ opacity: 0, y: 18, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.6)" }}, {t});')
    return css, html_, "\n".join(js)
