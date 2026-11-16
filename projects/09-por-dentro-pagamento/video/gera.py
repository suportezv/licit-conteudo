#!/usr/bin/env python3
"""Por Dentro da Licitação #4: do contrato ao pagamento. Gerador da peça (HyperFrames)."""
SEG = {
"01": "Ganhou a licitação. Agora vem a parte que quase ninguém mostra: a empresa ainda não recebeu nada. Entre o resultado e o dinheiro na conta, existem cinco etapas.",
"02": "Lembra da nossa empresa? Habilitada, recurso negado, homologada em quatrocentos e trinta e oito mil. A prefeitura convoca para assinar o contrato.",
"03": "Primeira etapa: o contrato. A empresa assina no prazo do edital, que pode ser prorrogado uma vez. Quem não assina perde a vaga e pode ser punida.",
"04": "Segunda: o empenho. É a nota em que o órgão reserva o dinheiro daquela compra. A lei proíbe despesa sem empenho prévio.",
"05": "Terceira: a entrega. Chega a ordem de fornecimento e o prazo começa a correr: trinta dias para entregar os computadores. Atrasou, entra a multa prevista no contrato.",
"06": "Quarta: o recebimento. Primeiro, o fiscal recebe de forma provisória. Depois o órgão confere quantidade e qualidade, e faz o recebimento definitivo.",
"07": "Ô, pausa rapidinha. Deixa o like e segue a Licíte pra ver quando o dinheiro cai. Bora continuar.",
"08": "Com o recebimento definitivo e a nota fiscal, vem a liquidação. É quando o órgão confirma que a empresa entregou o que devia e tem direito de receber.",
"09": "E só então chega o pagamento. Ele segue a ordem cronológica: o órgão paga na ordem em que as dívidas ficaram prontas, não por preferência.",
"10": "Repara: emitir a nota fiscal não é receber. Contrato, empenho, entrega, recebimento, liquidação e pagamento. Pular uma etapa costuma atrasar todas as outras.",
"11": "E o contrato não termina no pagamento. Os computadores têm doze meses de garantia, e a empresa responde por eles nesse período.",
"12": "No fim, tudo isso vira histórico. O atestado deste contrato é o que vai provar, na próxima licitação, que a empresa já fez isso antes.",
"13": "Na Licíte, o resultado fica junto do histórico, e a próxima licitação não precisa começar do zero. E você, já esperou muito para receber de um órgão público? Conta aqui.",
}

import sys
sys.path.insert(0, "lib")
from hf_licit import Peca, tag, ERRO, FLO, CREME, LAV, MAG, NAVY

p = Peca(SEG, pausa_seg="07")
at, st = p.at, p.start
C3 = []; FOCO = [[0, -1]]
def cam(t, s, pos, look, fov=46, cut=True, mv=(0, 0, 0), dur=1.6): C3.append([round(t, 3), s, *pos, *look, fov, 1 if cut else 0, *mv, dur])
def cap(t, l1, l2=""): p.cap(t, l1, l2)
def sfx(t, n, v=0.9): p.sfx(t, n, v)
def chip(id_, t0, t1, texto, x, y, cls=""): p.card(*tag(id_, round(t0, 3), round(t1, 3), texto, x, y, cls))
E = p.ev
def portao(t, i, dx=0.4, dist=8.6, cut=True, mv=(-0.12, 0.02, -0.18)):
    x = i * 7; cam(t, "trilha", (x + 3.6 + dx, 3.1, dist), (x + 2.6 + dx, 2.0, -3.2), 48, cut=cut, mv=mv)
GERAL = ((-9, 9.5, 15), (15, 1.2, -2.5))
p.diorama(podio2=True)
E("p2_cai", -6); E("p2_sobe", -5); E("homolog", 0.5)
p.hud_set("A RECEBER", 438000, fmt="brl", cor="fixa")
p.hud2_set("ETAPA", 0, fmt='(v<0.5?"início":Math.round(v)+" de 5")', cor="fixa")
p.hud_js('tl.set("#hud-wrap", { opacity: 0 }, 0.3);')

# ======================= 01: ganhou, e ainda nao recebeu
cam(0.0, "cidade", (0, 7.6, 18.5), (0, 0.6, 6.0), 46, mv=(0, -0.05, -0.3)); sfx(0.05, "chord", 0.8); sfx(0.55, "stamp", 0.8)
cap(0.4, "Ganhou", "a licitação")
cap(at("01", "Agora"), "E ainda", "não recebeu nada")
cam(at("01", "Entre") - 0.15, "trilha", *GERAL, 50, mv=(0.55, -0.04, -0.2)); sfx(at("01", "Entre") - 0.15, "whoosh", 0.7)
p.hud_show(at("01", "dinheiro")); sfx(at("01", "dinheiro"), "register", 0.7)
cap(at("01", "Entre"), "Até o dinheiro na conta", "são cinco etapas")
chip("c5", at("01", "cinco"), st("02") - 0.3, "5 etapas", 420, 1250, "mag"); sfx(at("01", "cinco"), "pop_soft", 0.6)

# ======================= 02: o caso
cam(st("02") - 0.15, "podio", (-0.6, 4.4, 16), (-0.6, 3.0, 0), 44, mv=(0.25, 0, -0.35)); sfx(st("02") - 0.15, "whoosh", 0.6)
E("fv_festa", at("02", "Habilitada")); sfx(at("02", "Habilitada"), "levelup", 0.5)
cap(at("02", "Lembra"), "Habilitada, recurso negado", "homologada em R$ 438 mil")
cam(at("02", "prefeitura") - 0.15, "cidade", (0, 7.6, 18.5), (0, 0.6, 6.0), 46, mv=(0, -0.05, -0.25)); sfx(at("02", "prefeitura") - 0.15, "whoosh", 0.5)
cap(at("02", "prefeitura"), "A prefeitura convoca", "para assinar")

# ======================= 03: contrato
portao(st("03") - 0.15, 0); sfx(st("03") - 0.15, "whoosh", 0.6)
E("g1", st("03")); sfx(st("03") + 0.1, "levelup", 0.5); p.val2(st("03"), 1, 0.4)
cap(at("03", "Primeira"), "1. Contrato:", "assinado no prazo do edital")
E("assina", at("03", "assina")); sfx(at("03", "assina") + 0.2, "sacks", 0.3)
portao(at("03", "prorrogado") - 0.1, 0, dx=0.0, dist=10.0)
cap(at("03", "Quem"), "Não assinou?", "Perde a vaga e pode ser punida")
chip("a90", at("03", "Quem"), st("04") - 0.3, "Lei 14.133, art. 90", 560, 1250, "mag")
portao(at("03", "Quem") - 0.15, 0, dx=0.0, dist=10.0)

# ======================= 04: empenho
portao(st("04") - 0.15, 1); sfx(st("04") - 0.15, "whoosh", 0.6)
E("g2", st("04")); sfx(st("04") + 0.1, "levelup", 0.5); p.val2(st("04"), 2, 0.4)
cap(at("04", "Segunda"), "2. Empenho:", "o dinheiro reservado")
E("cofre", at("04", "nota")); sfx(at("04", "nota") + 0.2, "gate", 0.6)
E("moedas", at("04", "reserva")); [sfx(at("04", "reserva") + 0.08 * k, "coins", 0.35) for k in range(0, 12, 4)]
cap(at("04", "lei"), "Sem empenho,", "não há despesa")
chip("a60", at("04", "lei"), st("05") - 0.3, "Lei 4.320, art. 60", 600, 1250, "mag")

# ======================= 05: entrega
portao(st("05") - 0.15, 2, dx=0.6, dist=11.0); sfx(st("05") - 0.15, "whoosh", 0.6)
E("g3", st("05")); sfx(st("05") + 0.1, "levelup", 0.5); p.val2(st("05"), 3, 0.4)
cap(at("05", "Terceira"), "3. Entrega:", "o prazo começa a correr")
E("caminhao", at("05", "Chega")); sfx(at("05", "Chega"), "generator", 0.35)
E("cal30", at("05", "trinta")); p.tiques(at("05", "trinta"), at("05", "trinta") + 3.0, 0.2)
cap(at("05", "trinta"), "30 dias", "para entregar")
cap(at("05", "Atrasou"), "Atrasou?", "Multa prevista no contrato"); sfx(at("05", "Atrasou"), "error_click", 0.6)

# ======================= 06: recebimento
portao(st("06") - 0.15, 3); sfx(st("06") - 0.15, "whoosh", 0.6)
E("g4", st("06")); E("caixas", st("06")); sfx(st("06") + 0.1, "levelup", 0.5); p.val2(st("06"), 4, 0.4)
[sfx(st("06") + 0.12 * k + 0.2, "pop_low", 0.4) for k in range(0, 6, 2)]
cap(at("06", "Quarta"), "4. Recebimento:", "primeiro provisório")
E("prov", at("06", "provisória")); sfx(at("06", "provisória"), "stamp", 0.8)
E("def", at("06", "definitivo")); sfx(at("06", "definitivo"), "stamp", 0.9)
cam(at("06", "Depois") - 0.1, "trilha", (25.8, 2.6, 4.6), (24.2, 1.9, -3.0), 44, mv=(-0.12, 0.02, -0.1)); sfx(at("06", "Depois") - 0.1, "whoosh", 0.4)
cap(at("06", "Depois"), "Quantidade e qualidade conferidas:", "recebimento definitivo")
chip("a140", at("06", "Depois"), st("07") - 0.3, "Lei 14.133, art. 140", 560, 1250, "mag")

# ======================= 07: pausa
p.pausa("07", fim="Bora")

# ======================= 08: liquidacao
portao(at("08", "Com") - 0.2, 4, dx=0.4, dist=10.5); sfx(at("08", "Com") - 0.2, "whoosh", 0.6)
E("g5", at("08", "Com")); sfx(at("08", "Com") + 0.1, "levelup", 0.5); p.val2(at("08", "Com"), 5, 0.4)
E("liq", at("08", "liquidação")); sfx(at("08", "liquidação"), "stamp", 0.9)
cap(at("08", "Com"), "Recebimento definitivo", "e nota fiscal")
cap(at("08", "liquidação"), "5. Liquidação:", "o direito de receber confirmado")
cam(at("08", "quando") - 0.1, "trilha", (30.4, 2.9, 5.0), (30.1, 2.6, -3.5), 44, mv=(0.1, 0, -0.08)); sfx(at("08", "quando") - 0.1, "whoosh", 0.4)

# ======================= 09: pagamento na ordem cronologica
cam(st("09") - 0.15, "trilha", (33.6, 3.0, 9.4), (33.4, 1.6, -2.4), 46, mv=(-0.1, 0, -0.2)); sfx(st("09") - 0.15, "whoosh", 0.6)
cap(at("09", "E"), "E só então", "o pagamento")
E("fila1", at("09", "ordem")); E("fila2", at("09", "dívidas")); E("fila3", at("09", "prontas"))
[sfx(at("09", w), "pop_soft", 0.5) for w in ("ordem", "dívidas", "prontas")]
cap(at("09", "órgão"), "Na ordem em que as dívidas", "ficaram prontas")
chip("a141", at("09", "órgão"), st("10") - 0.3, "Lei 14.133, art. 141", 560, 1250, "mag")
E("cai", at("09", "prontas") + 0.9); sfx(at("09", "prontas") + 0.9, "coins", 0.7); sfx(at("09", "prontas") + 1.2, "register", 0.7)
p.val(at("09", "prontas") + 0.9, 0, 1.2)

# ======================= 10: a licao
cam(st("10") - 0.15, "trilha", *GERAL, 50, mv=(0.5, -0.04, -0.2)); sfx(st("10") - 0.15, "whoosh", 0.6)
cap(at("10", "Repara"), "Nota fiscal emitida", "não é dinheiro na conta")
E("tudo", at("10", "Contrato")); [sfx(at("10", w), "pop_soft", 0.55) for w in ("Contrato", "empenho", "entrega", "recebimento", "liquidação", "pagamento")]
cap(at("10", "Pular"), "Pular uma etapa", "atrasa as outras")

# ======================= 11: garantia
cam(st("11") - 0.15, "trilha", (25.6, 3.8, 9.0), (23.8, 3.5, -3.0), 46, mv=(-0.15, 0, -0.2)); sfx(st("11") - 0.15, "whoosh", 0.6)
cap(at("11", "E"), "O contrato não termina", "no pagamento")
E("garantia", at("11", "garantia") - 0.2); sfx(at("11", "garantia") - 0.2, "sting", 0.6)
cap(at("11", "computadores"), "12 meses de garantia", "e a empresa responde")

# ======================= 12: vira atestado
FH = 3.3
cam(st("12") - 0.15, "torre", (0, FH + 2.3, 13.8), (0, FH + 2.55, 0), 52, mv=(0.1, 0.02, -0.2)); FOCO.append([round(st("12") - 0.1, 3), 1]); sfx(st("12") - 0.15, "whoosh", 0.6)
E("t_jur", -1); E("jur_ok", -1); E("certs", -1); E("t_fis", -1); E("t_eco", -1); E("eco_ok", -1)
cap(at("12", "No"), "No fim, tudo isso", "vira histórico")
E("at", at("12", "atestado")); [sfx(at("12", "atestado") + 0.35 * k + 0.3, "pop_soft", 0.5) for k in range(3)]
E("barra", at("12", "atestado") + 0.6); E("t_tec", at("12", "fez") - 0.2); sfx(at("12", "fez") - 0.2, "levelup", 0.6)
cap(at("12", "atestado"), "O atestado deste contrato", "prova que a empresa já fez")


# ======================= cortes intermediarios (dead_stretch do check)
def corte(t, s, pos, look, fov=44, mv=(0.08, 0, -0.08)): cam(t, s, pos, look, fov, mv=mv); sfx(t, "whoosh", 0.35)
corte(at("02", "homologada") - 0.1, "arena", (-2.0, 2.35, 2.5), (-3.25, 1.95, 5.7), 38, mv=(0.03, 0, -0.03))
corte(at("03", "assina") - 0.1, "trilha", (4.4, 2.4, 3.2), (3, 1.8, -3.6), 42)
corte(at("04", "reserva") - 0.1, "trilha", (11.8, 2.8, 3.4), (10, 1.7, -3.4), 46)
corte(at("05", "trinta") - 0.1, "trilha", (19.0, 3.4, 3.8), (17.6, 3.1, -3.4), 44)
corte(at("06", "fiscal") - 0.1, "trilha", (28.0, 2.4, 3.0), (25.2, 1.5, -2.8), 44)
corte(at("06", "qualidade") - 0.1, "trilha", (25.2, 2.8, 3.8), (23.9, 2.0, -3.1), 44)
corte(at("08", "entregou") - 0.1, "trilha", (29.4, 2.8, 1.0), (29.0, 2.5, -3.6), 42)
corte(at("09", "ordem") - 0.1, "trilha", (32.4, 1.7, 2.8), (32.4, 1.0, -2.0), 44)
corte(at("09", "prontas") + 0.5, "trilha", (33.6, 3.0, 9.4), (33.4, 1.6, -2.4), 46, mv=(-0.1, 0, -0.2))
corte(at("10", "Contrato") - 0.1, "trilha", (1.0, 6.5, 13.0), (5.0, 2.5, -2.0), 50, mv=(2.3, 0, 0))
corte(at("11", "garantia") - 0.1, "trilha", (24.8, 4.6, 3.6), (24.0, 4.4, -2.9), 44)
corte(at("12", "atestado") - 0.1, "torre", (-1.0, FH + 2.0, 4.6), (-2.4, FH + 1.0, 0.6), 44)

# ======================= 13: a Licit e o fecho
cam(st("13") - 0.2, "escritorio", (0.9, 2.75, 3.8), (-0.3, 2.2, -3), 50, mv=(0, -0.02, -0.1)); sfx(st("13") - 0.2, "whoosh", 0.6)
p.diorama(prot_modo=[[0, 0]])
cap(at("13", "Na"), "Na Licit, resultado", "junto do histórico")
k0, k1 = at("13", "Na"), at("13", "você") + 0.2
HIST = [("Aquisição de computadores", "Contrato R$ 438.000", "Atestado salvo", "ok"), ("Material de escritório", "3º lugar", "Proposta guardada", "neu"), ("Mobiliário escolar", "Inabilitada", "Faltou atestado", "av")]
linhas = "".join(f'<div class="ln" id="hl{i}"><div class="tx"><b>{a}</b><span>{b}</span></div><div class="st {c}">{s_}</div></div>' for i, (a, b, s_, c) in enumerate(HIST))
p.card(f"""  #prod {{ position:absolute; left:100px; width:880px; top:1090px; border-radius:34px; background:#F4F6F9; box-shadow:0 22px 70px rgba(0,0,0,0.45); overflow:hidden; }}
  #prod .top {{ display:flex; align-items:center; gap:18px; padding:20px 30px; background:{FLO}; }}
  #prod .top img {{ height:44px; }} #prod .top span {{ color:#B8C5BC; font-size:28px; font-weight:500; }}
  #prod .corpo {{ padding:8px 28px 4px; }}
  #prod .ln {{ display:flex; align-items:center; justify-content:space-between; gap:16px; padding:16px 0; border-bottom:2px solid #E2E7E3; }}
  #prod .tx {{ display:flex; flex-direction:column; gap:4px; }} #prod .tx b {{ font-size:32px; font-weight:600; color:#101218; }} #prod .tx span {{ font-size:28px; color:#59616E; }}
  #prod .st {{ font-size:28px; font-weight:600; padding:6px 16px 8px; border-radius:16px; white-space:nowrap; }}
  #prod .st.ok {{ color:{FLO}; background:#E1F4D4; }} #prod .st.neu {{ color:#59616E; background:#E6EBE7; }} #prod .st.av {{ color:#7A4A00; background:#FBE3B4; }}
  #prod .ilu {{ color:#59616E; font-size:28px; text-align:right; padding:8px 30px 20px; }}""",
f"""  <div id="prod" class="clip" data-start="{round(k0,3)}" data-duration="{round(k1-k0,3)}" data-track-index="2">
    <div class="top"><img src="assets/logo_wordmark.png" alt=""><span>Histórico de participações</span></div>
    <div class="corpo">{linhas}</div>
    <div class="ilu">exemplo ilustrativo</div></div>""",
f"""  tl.fromTo("#prod", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(k0,3)});
  tl.fromTo("#prod .ln", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.18, ease: "power2.out" }}, {round(k0 + 0.35,3)});
  tl.fromTo("#hl0 .st", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {round(at('13','próxima'),3)});
  tl.to("#prod", {{ opacity: 0, y: 40, duration: 0.4 }}, {round(k1-0.4,3)});""")
p.hud_js(f'tl.to("#hud-logo", {{ opacity: 0, duration: 0.2 }}, {round(k0,3)}); tl.to("#hud-logo", {{ opacity: 0.96, duration: 0.3 }}, {round(k1,3)});')
[sfx(k0 + 0.35 + 0.18 * i, "pop_soft", 0.45) for i in range(3)]
cam(at("13", "você") - 0.15, "trilha", *GERAL, 50, mv=(0.5, -0.04, -0.25)); sfx(at("13", "você") - 0.15, "whoosh", 0.5)
cap(at("13", "você"), "Já esperou muito para receber", "de um órgão público? Conta aqui")
p.hud_hide(at("13", "Conta") - 0.3)
p.endcard(at("13", "Conta") - 0.2, sub="Por Dentro da Licitação")

# ======================= expressoes e cena
p.diorama(expr=[[0, "alivio"], [at("01", "Agora"), "duvida"], [st("02"), "alivio"], [st("03"), "foco"], [at("05", "Atrasou"), "tenso"], [st("08"), "foco"], [at("09", "prontas") + 0.9, "alivio"]])
p.diorama(cam3=sorted(C3, key=lambda k: k[0]), torre_foco=sorted(FOCO))
p.cena("pagamento", extras=["kit3d.js"])
p.write()
