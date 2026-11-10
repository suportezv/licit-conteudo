"""Folha de conferencia: avatares no recorte circular (grande e no tamanho do app),
destaques recortados como o Instagram mostra e a capa do LinkedIn com o logo por cima."""
import pathlib
A = pathlib.Path(__file__).resolve().parent; O = (A / "out").as_uri()
FONTE = (A.parents[1] / "remotion/public/Sora-Variable.ttf").as_uri()
av = [("Instagram", "instagram-avatar", "50%"), ("TikTok", "tiktok-avatar", "50%"), ("LinkedIn", "linkedin-logo@2x", "8px")]
des = ["licit", "oferta", "etapas", "primeira", "blog", "perguntas"]
h = f"""<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:Sora;src:url('{FONTE}')}}
body{{margin:0;padding:48px;width:1400px;background:#1A1D22;color:#F4F6F9;font-family:Sora}}
h2{{font-weight:500;font-size:22px;margin:36px 0 18px;letter-spacing:-.02em}} small{{color:#95A49C;font-size:14px}}
.row{{display:flex;gap:40px;align-items:flex-end}} .c{{display:flex;flex-direction:column;align-items:center;gap:10px;font-size:14px;color:#B8C5BC}}
.capa{{position:relative;width:1128px;margin-bottom:70px}} .capa img.c1{{width:1128px;display:block}}
.capa .lg{{position:absolute;left:16px;top:120px;width:128px;height:128px;border-radius:8px;border:4px solid #1A1D22}}
</style><h2>Avatares <small>recorte do app, em 300 px e no tamanho real do feed (56 px)</small></h2><div class=row>"""
for n, f, r in av:
    h += f'<div class=c><img src="{O}/{f}.png" style="width:300px;border-radius:{r}"><img src="{O}/{f}.png" style="width:56px;border-radius:{r if r!="8px" else "4px"}">{n}</div>'
h += '</div><h2>Destaques do Instagram <small>o que o perfil mostra (círculo central)</small></h2><div class=row>'
for d in des:
    h += f'<div class=c><div style="width:150px;height:150px;border-radius:50%;overflow:hidden;border:3px solid #35413C;padding:3px;background:#1A1D22"><img src="{O}/destaque-{d}.png" style="width:144px;height:256px;object-fit:cover;margin-top:-56px;border-radius:50%;clip-path:circle(72px at 72px 128px)"></div>{d}</div>'
h += '</div><h2>Capa do LinkedIn <small>1128 x 191, com o logo da página por cima como no desktop</small></h2>'
for f in ["linkedin-capa@2x", "linkedin-capa-lancamento@2x"]:
    h += f'<div class=capa><img class=c1 src="{O}/{f}.png"><img class=lg src="{O}/linkedin-logo@2x.png"></div>'
(A / "html/previa.html").write_text(h)
