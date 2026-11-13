#!/usr/bin/env python3
"""Por Dentro da Licitação #2: a habilitação. Gerador da peça (HyperFrames)."""
SEG = {
"01": "A empresa deu o melhor lance, teve a proposta aceita e, mesmo assim, perdeu o contrato. Por causa de um documento. Essa é a habilitação: a fase em que o preço não ajuda mais.",
"02": "Lembra do pregão do episódio passado? Agora imagina que a empresa dois não passou na habilitação. O pregoeiro chama a próxima da fila: a sua empresa, com quatrocentos e trinta e oito mil.",
"03": "A lei divide a habilitação em quatro partes: jurídica, técnica, fiscal e trabalhista, e econômico-financeira. Cada uma responde a uma pergunta.",
"04": "A jurídica pergunta: essa empresa existe e pode fazer isso? Contrato social, e o objeto da empresa compatível com o que está sendo comprado.",
"05": "A técnica pergunta: ela já fez isso antes? Atestados de quem já recebeu o mesmo tipo de fornecimento. O edital pode exigir até metade da quantidade comprada.",
"06": "A fiscal e trabalhista pergunta: ela está em dia? CNPJ, certidões federal, estadual, municipal, do FGTS e trabalhista. E cada certidão tem a sua validade.",
"07": "Ô, pausa rapidinha. Deixa o like e segue a Licíte pra ver se essa empresa passa. Bora continuar.",
"08": "A econômico-financeira pergunta: ela aguenta o contrato? Balanço dos dois últimos anos, certidão de falência e, se o edital pedir, patrimônio mínimo de até dez por cento do valor.",
"09": "Agora a virada. O pregoeiro abre as certidões da sua empresa. A do FGTS venceu ontem. Inabilitada? Ainda não.",
"10": "Se ela venceu depois da data das propostas, a lei deixa atualizar o documento em diligência. O que não dá é trazer agora um documento que a empresa não tinha.",
"11": "E se a empresa for micro ou pequena, com pendência fiscal, ela ainda tem cinco dias úteis para regularizar, prorrogáveis por mais cinco.",
"12": "Certidão atualizada, quatro partes conferidas. Habilitada. Repara: o contrato não se perdeu no preço. Se perdeu, ou se salvou, no papel.",
"13": "Na Licíte, cada certidão fica com a validade à vista. E você, já teve certidão vencendo na véspera? Conta aqui. Na próxima: o recurso.",
}

import sys
sys.path.insert(0, "lib")
from hf_licit import Peca, tag, ERRO, FLO, CREME, LAV, MAG, NAVY

p = Peca(SEG, pausa_seg="07")
at, st = p.at, p.start
C3 = []
def cam(t, s, pos, look, fov=46, cut=True, mv=(0, 0, 0), dur=1.6): C3.append([round(t, 3), s, *pos, *look, fov, 1 if cut else 0, *mv, dur])
def cap(t, l1, l2=""): p.cap(t, l1, l2)
def sfx(t, n, v=0.9): p.sfx(t, n, v)
def chip(id_, t0, t1, texto, x, y, cls=""): p.card(*tag(id_, round(t0, 3), round(t1, 3), texto, x, y, cls))
E = p.ev
FH = 3.3
def andar(t, i, cut=True, dur=1.6):  # plano frontal de um andar da torre
    y = i * FH; cam(t, "torre", (0, y + 2.3, 13.8), (0, y + 2.55, 0), 52, cut=cut, mv=(0.1, 0.02, -0.2), dur=dur); FOCO.append([round(t + 0.05, 3), i])
def geral(t, cut=True, dur=1.6): cam(t, "torre", (0, 7.6, 26), (0, 8.6, 0), 46, cut=cut, mv=(0, 0, -0.3), dur=dur); FOCO.append([round(t + 0.05, 3), -1])
FOCO = [[0, -1]]
p.diorama(podio2=True)

# ======================= 01: perdeu por um documento
cam(0.0, "podio", (-1.0, 4.2, 17), (-1.0, 2.8, 0), 46, mv=(0, 0, -0.45))
sfx(0.05, "chord", 0.8)
cap(0.5, "Melhor lance,", "proposta aceita")
p.hud_set("SEU LANCE", 438000, fmt="brl", cor="fixa")
p.hud2_set("HABILITAÇÃO", 0, fmt='Math.round(v)+" de 4"', cor="fixa")
p.hud_js('tl.set("#hud-wrap", { opacity: 0 }, 0.3);')
cap(at("01", "mesmo"), "e mesmo assim", "perdeu o contrato")
p.diorama(podio_x=[[at("01", "perdeu"), st("02") + 1.0]]); sfx(at("01", "perdeu"), "error_click", 0.8)
E("p2_cai", at("01", "contrato") + 0.1); sfx(at("01", "contrato") + 0.15, "thud", 0.7)
cam(at("01", "Por") - 0.15, "arena", (0.9, 3.7, -3.3), (0, 1.1, -6.0), 42, mv=(-0.03, -0.02, 0.03)); sfx(at("01", "Por") - 0.15, "whoosh", 0.6)
E("inab", at("01", "documento") + 0.2); sfx(at("01", "documento") - 0.3, "whoosh", 0.5); sfx(at("01", "documento") + 0.2, "stamp", 0.9)
cap(at("01", "Por"), "Por causa de", "um documento")
geral(at("01", "Essa") - 0.15); sfx(at("01", "Essa") - 0.15, "whoosh", 0.7)
cap(at("01", "habilitação"), "Habilitação: a fase em que", "o preço não ajuda mais")
sfx(at("01", "preço"), "sting", 0.6)

# ======================= 02: o pregao do episodio passado
cam(st("02") - 0.15, "arena", (0, 8.5, 19), (0, 4.4, -4), 50, mv=(0, -0.12, -0.35)); sfx(st("02") - 0.15, "whoosh", 0.7)
cap(at("02", "Lembra"), "Lembra do pregão", "do episódio passado?")
cam(at("02", "Agora") - 0.15, "arena", (0, 6.1, 3.6), (0, 6.1, -9.5), 50, mv=(0, 0, -0.2)); sfx(at("02", "Agora") - 0.15, "whoosh", 0.5)
p.diorama(placar_modo=[[0, 3], [at("02", "passou") - 0.1, 5], [st("09"), 6], [at("10", "atualizar"), 7], [at("12", "Habilitada") - 0.1, 8]])
sfx(at("02", "passou"), "alarm", 0.6)
cap(at("02", "Agora"), "A empresa 02", "não passou na habilitação")
cam(at("02", "pregoeiro") - 0.15, "arena", (1.3, 2.35, -3.6), (0, 1.85, -7.1), 40, mv=(-0.05, 0, 0.05)); sfx(at("02", "pregoeiro") - 0.15, "whoosh", 0.5)
p.diorama(preg_modo=[[at("02", "pregoeiro"), 1], [at("02", "sua") - 0.3, 0], [at("09", "pregoeiro"), 1], [at("09", "FGTS") - 0.2, 0]])
cap(at("02", "pregoeiro"), "O pregoeiro chama", "a próxima da fila")
E("inab_fim", at("02", "sua") - 0.2)
cam(at("02", "sua") - 0.2, "podio", (-0.8, 4.4, 16), (-0.6, 3.0, 0), 44, mv=(0.25, 0, -0.35)); sfx(at("02", "sua") - 0.2, "whoosh", 0.6)
E("p2_sobe", at("02", "sua")); sfx(at("02", "sua") + 0.1, "levelup", 0.7)
cap(at("02", "sua"), "A sua empresa", "R$ 438 mil")
p.hud_show(at("02", "quatrocentos")); sfx(at("02", "quatrocentos"), "register", 0.7)

# ======================= 03: quatro partes
geral(st("03") - 0.15); sfx(st("03") - 0.15, "whoosh", 0.6)
cap(at("03", "A"), "A lei divide em", "quatro partes")
for i, (w, nome) in enumerate([("jurídica", "Jurídica"), ("técnica", "Técnica"), ("fiscal", "Fiscal e trabalhista"), ("econômico", "Econômico-financeira")]):
    t0 = at("03", w); chip(f"q{i}", t0, at("03", "Cada") - 0.1, f"{i + 1}. {nome}", 150, 1150 + 92 * i, "mag" if i == 0 else ""); sfx(t0, "pop_soft", 0.55)
cam(at("03", "Cada") - 0.15, "torre", (6.5, 2.2, 18), (0, 6.4, 0), 48, mv=(-0.25, 0.05, -0.3)); FOCO.append([round(at("03", "Cada") - 0.1, 3), -1]); sfx(at("03", "Cada") - 0.15, "whoosh", 0.5)
cap(at("03", "Cada"), "Cada uma responde", "a uma pergunta")

# ======================= 04: juridica
andar(st("04") - 0.15, 0); sfx(st("04") - 0.15, "whoosh", 0.6)
cap(at("04", "A"), "Existe e pode", "fazer isso?")
cam(at("04", "Contrato") - 0.15, "torre", (2.6, 2.1, 8.2), (0, 1.4, 0), 48, mv=(-0.18, 0, -0.1)); sfx(at("04", "Contrato") - 0.15, "whoosh", 0.4)
cap(at("04", "Contrato"), "Contrato social: o objeto", "bate com a compra")
E("jur_ok", at("04", "compatível")); sfx(at("04", "compatível"), "pop_soft", 0.6); sfx(at("04", "compatível") + 0.5, "levelup", 0.6)
E("t_jur", at("04", "compatível") + 0.6); p.val2(at("04", "compatível") + 0.6, 1, 0.4)

# ======================= 05: tecnica
andar(st("05") - 0.15, 1); sfx(st("05") - 0.15, "whoosh", 0.6)
cap(at("05", "A"), "Já fez isso", "antes?")
E("at", at("05", "Atestados")); [sfx(at("05", "Atestados") + 0.35 * k + 0.3, "pop_soft", 0.5) for k in range(3)]
cap(at("05", "Atestados"), "Atestados de quem já recebeu", "o mesmo fornecimento")
E("barra", at("05", "edital")); cam(at("05", "edital") - 0.15, "torre", (1.6, FH + 2.1, 9.6), (0.4, FH + 1.7, -0.5), 46, mv=(-0.15, 0, -0.08)); sfx(at("05", "edital") - 0.15, "whoosh", 0.4); sfx(at("05", "metade"), "pop_low", 0.6)
cap(at("05", "edital"), "Exigência de até metade", "da quantidade comprada")
E("t_tec", at("05", "comprada") + 0.4); sfx(at("05", "comprada") + 0.4, "levelup", 0.6); p.val2(at("05", "comprada") + 0.4, 2, 0.4)

# ======================= 06: fiscal e trabalhista
andar(st("06") - 0.15, 2); sfx(st("06") - 0.15, "whoosh", 0.6)
cap(at("06", "A"), "Está em", "dia?")
E("certs", at("06", "CNPJ")); [sfx(at("06", "CNPJ") + 0.18 * k + 0.1, "pop_soft", 0.45) for k in range(6)]
cap(at("06", "CNPJ"), "CNPJ e certidões federal, estadual", "municipal, FGTS e trabalhista")
E("fgts_pisca", at("06", "validade")); sfx(at("06", "validade"), "alert", 0.6)
cam(at("06", "E", 2) - 0.15, "torre", (2.6, 2 * FH + 1.9, 6.2), (1.4, 2 * FH + 1.5, 0.2), 42, mv=(-0.1, 0, -0.08)); sfx(at("06", "E", 2) - 0.15, "whoosh", 0.4)
cap(at("06", "E", 2), "E cada certidão", "tem a sua validade")

# ======================= 07: pausa
p.pausa("07", fim="Bora")

# ======================= 08: economico-financeira
andar(at("08", "A") - 0.2, 3); sfx(at("08", "A") - 0.2, "whoosh", 0.6)
cap(at("08", "A"), "Aguenta", "o contrato?")
cap(at("08", "Balanço"), "Balanço dos dois últimos anos", "e certidão de falência")
E("eco_ok", at("08", "patrimônio")); cam(at("08", "Balanço") - 0.15, "torre", (-1.2, 3 * FH + 1.6, 13.0), (0, 3 * FH + 2.0, 0), 50, mv=(0.2, 0.02, -0.12)); sfx(at("08", "Balanço") - 0.15, "whoosh", 0.4); sfx(at("08", "patrimônio"), "pop_low", 0.6)
cap(at("08", "patrimônio"), "Patrimônio mínimo, se pedido:", "até 10% do valor")
E("t_eco", at("08", "valor")); sfx(at("08", "valor"), "levelup", 0.6); p.val2(at("08", "valor"), 3, 0.4)

# ======================= 09: a virada
cam(st("09") - 0.15, "arena", (0, 6.1, 3.6), (0, 6.1, -9.5), 50, mv=(0, 0, -0.2)); sfx(st("09") - 0.15, "whoosh", 0.7)
cap(at("09", "Agora"), "Agora", "a virada")
cam(at("09", "pregoeiro") - 0.15, "arena", (1.3, 2.35, -3.6), (0, 1.85, -7.1), 40, mv=(-0.05, 0, 0.05)); sfx(at("09", "pregoeiro") - 0.15, "whoosh", 0.5)
cap(at("09", "pregoeiro"), "O pregoeiro abre", "as suas certidões")
cam(at("09", "certidões") - 0.1, "arena", (0, 4.0, 5.0), (0, 3.25, -3.6), 40, mv=(0, 0, -0.25)); E("fgts_abre", at("09", "certidões")); sfx(at("09", "certidões"), "whoosh", 0.6)
E("fgts_venc", at("09", "venceu")); sfx(at("09", "venceu"), "alarm", 0.8)
cap(at("09", "A", 2), "A do FGTS", "venceu ontem")
cap(at("09", "Inabilitada"), "Inabilitada?", ""); sfx(at("09", "Inabilitada"), "error_click", 0.6)
cap(at("09", "Ainda"), "Ainda não.", ""); sfx(at("09", "Ainda"), "sting", 0.6)

# ======================= 10: a diligencia
cam(st("10") - 0.15, "linha", (-0.5, 2.7, 11), (-0.5, 2.9, 0), 46, mv=(0.22, 0.03, -0.4)); E("fgts_fecha", st("10") - 0.15); sfx(st("10") - 0.15, "whoosh", 0.6)
cap(at("10", "Se"), "Venceu depois da data", "das propostas?")
E("seta", at("10", "atualizar")); E("dil", at("10", "diligência")); sfx(at("10", "atualizar"), "whoosh", 0.6); sfx(at("10", "diligência"), "levelup", 0.8)
cap(at("10", "a", 2), "Dá para atualizar", "em diligência")
chip("art64", at("10", "diligência"), at("10", "tinha") + 0.3, "Lei 14.133, art. 64", 560, 1250, "mag")
cam(at("10", "que") - 0.15, "linha", (2.9, 2.7, 11.5), (2.9, 2.9, 0), 46, mv=(0.1, 0, -0.2)); sfx(at("10", "que") - 0.15, "whoosh", 0.5)
cap(at("10", "que"), "Documento que não existia", "não entra depois")
E("doc_novo", at("10", "tinha")); sfx(at("10", "tinha"), "error_click", 0.8)

# ======================= 11: micro e pequena
cam(st("11") - 0.15, "linha", (0, 8.6, -4.8), (0, 0.6, -14.4), 50, mv=(0, -0.05, -0.15)); sfx(st("11") - 0.15, "whoosh", 0.6)
E("cal_on", st("11") - 0.2); E("cal_badge", at("11", "micro")); sfx(at("11", "micro"), "pop_soft", 0.6)
cap(at("11", "micro"), "Micro ou pequena empresa", "com pendência fiscal")
E("cal1", at("11", "cinco")); [sfx(at("11", "cinco") + 0.16 * k, "metal_click", 0.4) for k in range(5)]
cap(at("11", "cinco"), "5 dias úteis", "para regularizar")
E("cal2", at("11", "mais")); [sfx(at("11", "mais") + 0.16 * k, "metal_click", 0.4) for k in range(5)]
cap(at("11", "prorrogáveis"), "prorrogáveis", "por mais 5")
chip("lc123", at("11", "cinco"), st("12") - 0.3, "LC 123, art. 43", 600, 1250, "mag")

# ======================= 12: habilitada
andar(st("12") - 0.15, 2); sfx(st("12") - 0.15, "whoosh", 0.6)
E("fgts_recarga", at("12", "Certidão")); sfx(at("12", "Certidão") + 0.1, "levelup", 0.7)
E("t_fis", at("12", "atualizada") + 0.4)
cap(at("12", "Certidão"), "Certidão", "atualizada")
geral(at("12", "quatro") - 0.15); sfx(at("12", "quatro") - 0.15, "whoosh", 0.6)
E("torre_ok", at("12", "quatro")); [sfx(at("12", "quatro") + 0.15 * k, "pop_soft", 0.5) for k in range(4)]; p.val2(at("12", "quatro"), 4, 0.5)
cap(at("12", "quatro"), "Quatro partes", "conferidas")
sfx(at("12", "Habilitada"), "stamp", 0.9); sfx(at("12", "Habilitada") + 0.1, "confetti", 0.6)
p.diorama(confete=[[at("12", "Habilitada") + 0.1, "torre", 0, 7.5, 4.0]])
cap(at("12", "Habilitada"), "Habilitada", "")
cam(at("12", "Repara") - 0.15, "podio", (0, 4.2, 15), (0, 3.0, 0), 44, mv=(0, 0, -0.3)); sfx(at("12", "Repara") - 0.15, "whoosh", 0.5)
E("fv_festa", at("12", "Repara"))
cap(at("12", "Repara"), "O contrato não se perdeu", "no preço")
cam(at("12", "Se") - 0.15, "habil", (-0.8, 6.4, 6.8), (0, 0.8, 0.0), 46, mv=(0.14, -0.08, -0.16)); sfx(at("12", "Se") - 0.15, "whoosh", 0.6)
docs_t = [at("12", "Se") - 0.05, at("12", "perdeu", 2), at("12", "ou"), at("12", "salvou")]
p.diorama(docs=docs_t); [sfx(t + 0.55, "pop_soft", 0.5) for t in docs_t]
E("carimbo", at("12", "papel")); sfx(at("12", "papel"), "stamp", 0.9)
cap(at("12", "Se"), "Se perdeu, ou se salvou,", "no papel")

# ======================= 13: a Licit e o fecho
cam(st("13") - 0.2, "escritorio", (0.9, 2.75, 3.8), (-0.3, 2.2, -3), 50, mv=(0, -0.02, -0.1)); sfx(st("13") - 0.2, "whoosh", 0.6)
p.diorama(prot_modo=[[0, 0]])
cap(at("13", "Na"), "Na Licit, cada certidão", "com a validade à vista")
k0, k1 = at("13", "Na"), at("13", "E") + 0.2
CERT = [("CNPJ", "válida", "ok"), ("Federal", "válida até 02/03", "ok"), ("Estadual", "válida até 20/01", "ok"), ("FGTS", "vence em 15 nov", "av"), ("Trabalhista", "válida até 10/04", "ok")]
linhas = "".join(f'<div class="ln" id="cl{i}"><span class="n">{n}</span><span class="v {c}">{v}</span></div>' for i, (n, v, c) in enumerate(CERT))
p.card(f"""  #prod {{ position:absolute; left:110px; width:860px; top:1100px; border-radius:34px; background:#F4F6F9; box-shadow:0 22px 70px rgba(0,0,0,0.45); overflow:hidden; }}
  #prod .top {{ display:flex; align-items:center; gap:18px; padding:20px 30px; background:{FLO}; }}
  #prod .top img {{ height:44px; }} #prod .top span {{ color:#B8C5BC; font-size:28px; font-weight:500; }}
  #prod .corpo {{ padding:14px 30px 10px; }}
  #prod .ln {{ display:flex; justify-content:space-between; align-items:center; padding:16px 0; border-bottom:2px solid #E2E7E3; font-size:34px; }}
  #prod .ln .n {{ color:#101218; font-weight:600; }} #prod .ln .v {{ font-weight:500; padding:6px 16px 8px; border-radius:16px; font-size:30px; }}
  #prod .v.ok {{ color:{FLO}; background:#E1F4D4; }} #prod .v.av {{ color:#7A4A00; background:#FBE3B4; }}
  #prod .ilu {{ color:#59616E; font-size:28px; text-align:right; padding:8px 30px 20px; }}""",
f"""  <div id="prod" class="clip" data-start="{round(k0,3)}" data-duration="{round(k1-k0,3)}" data-track-index="2">
    <div class="top"><img src="assets/logo_wordmark.png" alt=""><span>Documentos da empresa</span></div>
    <div class="corpo">{linhas}</div>
    <div class="ilu">exemplo ilustrativo</div></div>""",
f"""  tl.fromTo("#prod", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(k0,3)});
  tl.fromTo("#prod .ln", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.14, ease: "power2.out" }}, {round(k0 + 0.35,3)});
  tl.fromTo("#cl3 .v", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {round(at('13','validade'),3)});
  tl.to("#prod", {{ opacity: 0, y: 40, duration: 0.4 }}, {round(k1-0.4,3)});""")
p.hud_js(f'tl.to("#hud-logo", {{ opacity: 0, duration: 0.2 }}, {round(k0,3)}); tl.to("#hud-logo", {{ opacity: 0.96, duration: 0.3 }}, {round(k1,3)});')
[sfx(k0 + 0.35 + 0.14 * i, "pop_soft", 0.45) for i in range(5)]; sfx(at("13", "validade"), "alert", 0.5)
cam(at("13", "E") - 0.15, "arena", (0, 8.5, 19), (0, 4.4, -4), 50, mv=(0, -0.12, -0.4)); sfx(at("13", "E") - 0.15, "whoosh", 0.5)
cap(at("13", "E"), "Já teve certidão vencendo", "na véspera? Conta aqui")
p.hud_hide(at("13", "Na", 2) - 0.3)
p.endcard(at("13", "Na", 2) - 0.2, sub="Próximo episódio: o recurso")

# ======================= expressoes e cena
p.diorama(expr=[[0, "neutro"], [at("01", "perdeu"), "tenso"], [at("02", "sua"), "alivio"], [st("03"), "foco"], [at("06", "validade"), "duvida"],
                [at("09", "venceu"), "susto"], [at("09", "Ainda"), "duvida"], [at("10", "diligência"), "alivio"], [at("12", "Habilitada"), "alivio"]])
p.diorama(cam3=C3, torre_foco=FOCO)
p.cena("habil", extras=["kit3d.js"])
p.write()
