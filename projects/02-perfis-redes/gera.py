"""Pack de perfil das redes da Profissio Licit: avatares, capa do LinkedIn e
capas de destaque do Instagram. Gera um HTML por peca e fotografa com o
Chromium do Playwright (render.js). Paleta so do Design System."""
import json, math, pathlib, subprocess

AQUI = pathlib.Path(__file__).resolve().parent
REPO = AQUI.parents[1]
SAIDA = AQUI / "out"
HTML = AQUI / "html"
FONTE = (REPO / "remotion/public/Sora-Variable.ttf").as_uri()

FLO, GRA, ACE, SUP, BRA, APO = "#243D32", "#101218", "#A8F27A", "#F4F6F9", "#FFFFFF", "#59616E"

# Caminho oficial da estrela (assets/marca/logos/estrela-licit-*.svg), so recolorido.
ESTRELA_D = ("M 500 95 C 522 95 539 111 544 135 C 575 344 696 426 900 459 C 954 468 954 532 900 541 "
             "C 696 574 575 656 544 865 C 535 917 465 917 456 865 C 425 656 304 574 100 541 "
             "C 46 532 46 468 100 459 C 304 426 425 344 456 135 C 461 111 478 95 500 95 Z "
             "M 356.07 537.56 A 149 149 0 0 1 624.96 417.85 C 527 430 433 474 356.07 537.56 Z "
             "M 646.736 473.126 A 149 149 0 0 1 376.456 582.319 C 457 523 552 489 646.736 473.126 Z")
# Caixa da forma: x 59.5..940.5, y 95..904 -> centro (500, 499.5), 881 x 809.

def estrela(cx, cy, larg, cor, rot=0, op=1):
    """Estrela centrada em (cx, cy) com largura 'larg'."""
    s = larg / 881
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-500 -499.5)" opacity="{op}">'
            f'<path d="{ESTRELA_D}" fill="{cor}" fill-rule="evenodd"/></g>')

def arcos(cx, cy, r0, passo, n, cor, op, larg=2):
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{r0+i*passo}" fill="none" stroke="{cor}" stroke-width="{larg}" opacity="{op}"/>' for i in range(n))

def grade(w, h, passo, cor, op, larg=1.5):
    v = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>' for x in range(0, w + 1, passo))
    hz = "".join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in range(0, h + 1, passo))
    return f'<g stroke="{cor}" stroke-width="{larg}" opacity="{op}">{v}{hz}</g>'

def topografia(w, h, cor, op, n=14, passo=46, x0=0.15):
    out = []
    for i in range(n):
        dx = w * x0 + i * passo
        out.append(f'<path d="M{dx} {-80} C{dx+w*.45} {h*.18} {dx-w*.25} {h*.5} {dx+w*.1} {h*.68} S{dx+w*.5} {h*.92} {dx+w*.2} {h+80}" '
                   f'fill="none" stroke="{cor}" stroke-width="2" opacity="{op}"/>')
    return "".join(out)

def pagina(w, h, fundo, svg, extra_html="", css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Sora;src:url('{FONTE}') format('truetype');font-weight:100 800}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{fundo};font-family:Sora,sans-serif}}
svg.bg{{position:absolute;inset:0}}
{css}
</style></head><body>
<svg class="bg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{svg}</svg>{extra_html}</body></html>"""

PECAS = []
def peca(nome, w, h, html, escalas=(1,)):
    (HTML / f"{nome}.html").write_text(html)
    PECAS.append({"nome": nome, "w": w, "h": h, "escalas": list(escalas)})

# ---------- Avatares (1080x1080, recorte circular; estrela dentro do circulo seguro) ----------
A = 1080
# Instagram: bloco verde-limao, estrela grafite, arcos floresta saindo do canto.
peca("instagram-avatar", A, A, pagina(A, A, ACE,
     arcos(A, A, 260, 70, 12, FLO, .16) + estrela(540, 540, 600, GRA)))
# TikTok: grafite, estrela verde-limao levemente girada, topografia em limao.
peca("tiktok-avatar", A, A, pagina(A, A, GRA,
     topografia(A, A, ACE, .10, n=12, passo=52, x0=.05) + estrela(540, 540, 600, ACE, rot=-8)))
# LinkedIn: floresta, estrela branca, grade tecnica. Logo da pagina: 400x400.
L = 400
peca("linkedin-logo", L, L, pagina(L, L, FLO,
     grade(L, L, 40, SUP, .07, 1) + estrela(200, 200, 236, BRA)), escalas=(1, 2))

# ---------- Capa do LinkedIn (pagina de empresa: 1128x191, exportada em 2x) ----------
W, H = 1128, 191
def painel(cor, cor_arco, op):
    pts = f"790,{H} 860,0 {W},0 {W},{H}"
    return (f'<clipPath id="pn"><polygon points="{pts}"/></clipPath><polygon points="{pts}" fill="{cor}"/>'
            f'<g clip-path="url(#pn)">{arcos(1010, 96, 70, 34, 9, cor_arco, op, 1.2)}</g>')
CSS_CAPA = """
.txt{position:absolute;left:252px;top:0;height:191px;display:flex;flex-direction:column;justify-content:center;gap:12px}
h1{font-weight:500;font-size:38px;line-height:1.08;letter-spacing:-0.035em}
p{font-weight:400;font-size:15px;line-height:1.3}
.pil{display:inline-block;padding:0 12px 3px;border-radius:999px;margin-left:2px}
.url{position:absolute;right:26px;bottom:16px;font-size:12px;font-weight:500;letter-spacing:.02em}
"""
peca("linkedin-capa", W, H, pagina(W, H, GRA,
     grade(W, H, 24, SUP, .045, 1)
     + painel(FLO, ACE, .14)
     + estrela(1010, 96, 250, ACE, rot=-8),
     f"""<div class="txt"><h1 style="color:{SUP}">Toda a sua operação<br>de <span class="pil" style="background:{ACE};color:{GRA}">licitações</span></h1>
<p style="color:#B8C5BC">Venda para o governo. Saiba o que fazer em cada etapa.</p></div>""", CSS_CAPA), escalas=(1, 2))
# Variante de lancamento, para trocar ate 19/dez.
peca("linkedin-capa-lancamento", W, H, pagina(W, H, ACE,
     painel(GRA, ACE, .16)
     + estrela(1010, 96, 250, ACE, rot=-8),
     f"""<div class="txt"><h1 style="color:{GRA}">30 dias para usar a Licit.<br>Sem cartão.</h1>
<p style="color:#1F3A2C">Para quem começa até 19 de dezembro. <b style="font-weight:600">profissiolicit.ai</b></p></div>""", CSS_CAPA), escalas=(1, 2))

# ---------- Capas de destaque do Instagram (1080x1920; o app recorta o circulo central) ----------
DW, DH = 1080, 1920
CX, CY = 540, 960
def destaque(nome, fundo, desenho, borda):
    peca(f"destaque-{nome}", DW, DH, pagina(DW, DH, fundo,
         desenho))

TXT = lambda t, cor, tam, peso=500, dy=0: (f'<text x="{CX}" y="{CY+dy}" text-anchor="middle" dominant-baseline="central" '
      f'font-family="Sora" font-weight="{peso}" font-size="{tam}" letter-spacing="-0.035em" fill="{cor}">{t}</text>')

destaque("licit", GRA, estrela(CX, CY, 660, ACE, rot=-8), ACE)
destaque("oferta", ACE, TXT("30", GRA, 470, dy=-70) + TXT("dias", GRA, 150, dy=200)
         + estrela(CX + 300, CY - 280, 120, FLO), GRA)
passos = "".join(
    f'<circle cx="{CX-320+i*160}" cy="{CY}" r="{52 if i==0 else 36}" fill="{ACE if i==0 else SUP}"/>' for i in range(5))
destaque("etapas", FLO, f'<line x1="{CX-320}" y1="{CY}" x2="{CX+320}" y2="{CY}" stroke="{SUP}" stroke-width="9" opacity=".55"/>' + passos, SUP)
destaque("primeira", SUP, TXT("1ª", FLO, 480, dy=-30) + f'<rect x="{CX-200}" y="{CY+210}" width="400" height="20" rx="10" fill="{FLO}"/>', FLO)
doc = (f'<rect x="{CX-170}" y="{CY-220}" width="340" height="440" rx="34" fill="none" stroke="{FLO}" stroke-width="22"/>'
       + "".join(f'<rect x="{CX-100}" y="{CY-120+i*80}" width="{200 if i<3 else 120}" height="20" rx="10" fill="{FLO}"/>' for i in range(4))
       + f'<rect x="{CX-100}" y="{CY-120}" width="200" height="20" rx="10" fill="{ACE}" opacity="0"/>')
destaque("blog", BRA, f'<g transform="translate({CX} {CY}) scale(1.35) translate({-CX} {-CY})">{doc}</g>', FLO)
balao = (f'<path d="M{CX-240} {CY-190} h480 a50 50 0 0 1 50 50 v260 a50 50 0 0 1 -50 50 h-300 l-110 90 v-90 h-70 '
         f'a50 50 0 0 1 -50 -50 v-260 a50 50 0 0 1 50 -50 z" fill="none" stroke="{SUP}" stroke-width="22" stroke-linejoin="round"/>'
         + TXT("?", ACE, 260, dy=-12))
destaque("perguntas", GRA, f'<g transform="translate({CX} {CY-20}) scale(1.25) translate({-CX} {-CY})">{balao}</g>', SUP)

json.dump(PECAS, open(HTML / "pecas.json", "w"), indent=1)
