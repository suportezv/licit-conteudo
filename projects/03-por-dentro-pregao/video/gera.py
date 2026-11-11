#!/usr/bin/env python3
"""Por Dentro da Licitação #1: o pregão eletrônico. Gerador da peça (HyperFrames)."""
SEG = {
"01": "Uma prefeitura vai comprar quatrocentos e oitenta mil reais em computadores. Sete empresas disputam, e nenhuma sabe quem são as outras. E já adianto: quem der o menor lance pode não levar.",
"02": "Isso é um pregão eletrônico, a modalidade da lei para bens e serviços comuns. O edital ficou no ar pelo menos oito dias úteis, e cada empresa mandou a proposta pelo sistema. A sua: quatrocentos e trinta e oito mil.",
"03": "Dez em ponto, o pregoeiro abre a sessão. Ninguém tem nome: cada empresa é um número. Ele confere as propostas e começa o que todo mundo veio ver: os lances.",
"04": "Cada lance tem que ser menor que o último da própria empresa. Você vê o melhor lance da sala, mas não sabe de quem é. E o relógio engana: lance nos dois minutos finais dá mais dois de prorrogação.",
"05": "Fim. Primeiro lugar: trezentos e noventa e nove mil. Segundo: quatrocentos e vinte e seis. Você: terceiro.",
"06": "Se a sua empresa fosse micro ou pequena, até cinco por cento acima do primeiro, teria cinco minutos para cobrir a oferta. Mas a distância é de quase dez por cento.",
"07": "Ô, pausa rapidinha. Deixa o like e segue a Licíte pra ver quem fica com esse contrato. Bora continuar.",
"08": "Aqui todo mundo acha que acabou. Não acabou. O pregoeiro confere a proposta do primeiro com o edital. O edital pede dezesseis gigas de memória. A proposta oferece oito. Desclassificada.",
"09": "A vez passa para o segundo. O pregoeiro tenta negociar um preço melhor. A empresa segura nos quatrocentos e vinte e seis mil, dentro do estimado. Aceita.",
"10": "Só agora vem a habilitação, e só de quem está em primeiro: contrato social, certidões, atestado de fornecimento. Documento que falta aqui derruba até o melhor preço.",
"11": "Habilitada. Você sobe para segundo. Quem discorda precisa dizer na hora que vai recorrer, senão perde o direito. Sem recurso, a autoridade homologa: quatrocentos e vinte e seis mil.",
"12": "Repara: o menor lance só abriu a fila. Levou quem cumpriu o edital, no preço e no papel. Na Licíte, você pergunta ao edital o que ele exige e a resposta vem com a página. Antes do primeiro lance.",
"13": "E você, já perdeu um pregão no detalhe? Conta aqui. Na próxima, a gente desmonta a habilitação.",
}

import sys, html
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

# ======================= 01: a prefeitura e as sete empresas
cam(0.0, "cidade", (0, 3.4, 42), (0, 4.6, 0), 46, mv=(0, 0.03, -0.6))
cap(0.6, "Uma prefeitura vai comprar", "R$ 480 mil em computadores")
sfx(0.05, "chord", 0.8); sfx(at("01", "prefeitura"), "whoosh", 0.6)
E("caixas", at("01", "computadores") - 0.3); [sfx(at("01", "computadores") - 0.3 + 0.07 * i, "pop_soft", 0.5) for i in (0, 4, 8)]
chip("c480", at("01", "quatrocentos"), at("01", "Sete") - 0.1, "R$ 480 mil", 380, 1180, "mag")
cam(at("01", "Sete") - 0.15, "predio", (-2.5, 3.6, 31), (0, 3.4, 0), 48, mv=(0.45, 0.04, -0.9)); sfx(at("01", "Sete") - 0.15, "whoosh", 0.6)
cap(at("01", "Sete"), "Sete empresas disputam", "e ninguém sabe quem é quem")
E("interroga", at("01", "nenhuma")); [sfx(at("01", "nenhuma") + 0.12 * i, "pop_low", 0.45) for i in (0, 3, 6)]
cam(at("01", "adianto") - 0.2, "predio", (0, 5.5, 9.5), (0, 4.4, 0), 44, cut=False, dur=2.8)
cap(at("01", "quem", 2), "Quem dá o menor lance", "pode não levar")
sfx(at("01", "levar"), "sting", 0.7)

# ======================= 02: o edital e a proposta
cam(st("02") - 0.1, "escritorio", (0.9, 2.75, 3.8), (-0.3, 2.2, -3), 50, mv=(0, -0.02, -0.08)); sfx(st("02") - 0.1, "whoosh", 0.6)
cap(at("02", "Isso"), "Isso é um pregão eletrônico", "bens e serviços comuns")
chip("cmod", at("02", "modalidade"), at("02", "edital") - 0.2, "Lei 14.133", 680, 1250, "mag")
E("edital_abre", at("02", "edital")); sfx(at("02", "edital"), "whoosh", 0.7); [sfx(at("02", "edital") + 0.18 * i, "pop_soft", 0.55) for i in range(4)]
cap(at("02", "edital"), "Edital no ar por pelo menos", "8 dias úteis")
p.diorama(cal=[[at("02", "edital"), 1], [at("02", "pelo") + 0.2, 4], [at("02", "oito"), 8]])
sfx(at("02", "oito"), "calendar", 0.8)
E("edital_fecha", at("02", "cada") - 0.2); E("tela_proposta", at("02", "proposta")); E("envelope", at("02", "proposta") + 0.1)
cap(at("02", "cada"), "Cada empresa manda a proposta", "pelo sistema")
sfx(at("02", "proposta") + 0.1, "whoosh", 0.8)
cam(at("02", "A", 3) - 0.15, "escritorio", (2.3, 2.05, -3.2), (0.2, 1.8, -0.4), 38, mv=(-0.03, 0, 0.02)); sfx(at("02", "A", 3) - 0.15, "whoosh", 0.5)
cap(at("02", "A", 3), "A sua proposta:", "R$ 438 mil")
p.hud_set("SEU LANCE", 438000, fmt="brl", cor="fixa")
p.hud2_set("CLASSIFICAÇÃO", 0, fmt='(v<0.5?"?":Math.round(v)+"º")', cor="fixa")
p.hud_js('tl.set("#hud-wrap", { opacity: 0 }, 0.3);'); p.hud_show(at("02", "quatrocentos")); sfx(at("02", "quatrocentos"), "register", 0.8)

# ======================= 03: a sala do pregao
cam(st("03") - 0.1, "arena", (0, 8.5, 19), (0, 4.4, -4), 50, mv=(0, -0.12, -0.35)); sfx(st("03") - 0.1, "whoosh", 0.7)
cap(at("03", "Dez"), "Dez em ponto", "abre a sessão")
cam(at("03", "pregoeiro") - 0.1, "arena", (1.3, 2.35, -3.6), (0, 1.85, -7.1), 40, mv=(-0.05, 0, 0.05)); sfx(at("03", "pregoeiro") - 0.1, "whoosh", 0.5)
p.diorama(preg_modo=[[at("03", "pregoeiro"), 1], [at("03", "Ninguém"), 0], [at("08", "pregoeiro"), 1], [at("08", "edital"), 0], [at("09", "pregoeiro"), 1], [at("09", "empresa"), 0]])
cap(at("03", "pregoeiro"), "O pregoeiro conduz", "a disputa")
cam(at("03", "Ninguém") - 0.15, "arena", (0.4, 2.7, 0.2), (5.4, 1.9, 3.8), 46, mv=(0.04, 0, 0.02)); sfx(at("03", "Ninguém") - 0.15, "whoosh", 0.5)
cap(at("03", "Ninguém"), "Ninguém tem nome:", "cada empresa é um número")
[sfx(at("03", "número") + 0.1 * i, "pop_low", 0.4) for i in (0, 2, 4)]
cam(at("03", "confere") - 0.1, "arena", (0, 7.5, -4.5), (0, 1.0, 4.5), 62, mv=(0, 0, 0.12)); E("confere", at("03", "propostas"))
cap(at("03", "confere"), "Ele confere as propostas", "")
[sfx(at("03", "propostas") + 0.15 * i, "stamp", 0.45) for i in range(0, 7, 2)]
cam(at("03", "começa") - 0.1, "arena", (0, 6.1, 3.6), (0, 6.1, -9.5), 50, mv=(0, 0, -0.2)); sfx(at("03", "começa") - 0.1, "whoosh", 0.6)
cap(at("03", "começa"), "E começam", "os lances")
p.diorama(placar_modo=[[0, 0], [at("03", "lances"), 1], [at("05", "Fim") - 0.1, 2], [st("09"), 4], [at("09", "Aceita") - 0.1, 3]])

# ======================= 04: lances e relogio
L = [(0.25, 4, 472000), (1.2, 1, 465000), (2.1, 3, 458000), (3.0, 6, 452000), (3.9, 2, 447000), (4.7, 3, 443000), (5.6, 5, 441000), (6.5, 1, 433000), (7.4, 2, 429000), (8.2, 3, 438000), (9.3, 7, 431000), (10.4, 1, 421000), (11.5, 2, 426000), (12.4, 1, 412000), (13.6, 1, 399000)]
T4 = st("04"); lances = [[round(T4 + dt, 3), i, v] for dt, i, v in L]
p.diorama(lances=lances); [sfx(t, "metal_click", 0.55) for t, i, v in lances]
cam(T4 - 0.1, "arena", (-2.0, 2.35, 2.5), (-3.25, 1.95, 5.7), 38, mv=(0.03, 0, -0.03)); sfx(T4 - 0.1, "whoosh", 0.5)
cap(at("04", "Cada"), "Cada lance precisa ser menor", "que o seu último")
cam(at("04", "Você") - 0.15, "arena", (0, 6.1, 3.6), (0, 6.1, -9.5), 50, mv=(0, 0, -0.2)); sfx(at("04", "Você") - 0.15, "whoosh", 0.5)
cap(at("04", "Você"), "Você vê o melhor lance", "mas não sabe de quem é")
cam(at("04", "relógio") - 0.15, "arena", (0, 5.2, -2.3), (0, 3.0, -9.5), 50, mv=(0, 0, -0.08)); sfx(at("04", "relógio") - 0.15, "whoosh", 0.5)
cap(at("04", "relógio"), "Lance nos 2 minutos finais", "ganha mais 2")
j1, j2 = at("04", "dá") + 0.05, at("04", "prorrogação") + 0.1
p.diorama(relogio=[[at("03", "lances"), 125], [at("04", "relógio"), 55], [j1 - 0.05, 9], [j1, 120], [j2 - 0.05, 104], [j2, 120], [at("05", "Fim") - 0.15, 0]])
chip("p1", j1, j1 + 1.5, "+2:00", 640, 1200, "mag"); chip("p2", j2, j2 + 1.4, "+2:00", 640, 1200, "mag"); sfx(j1, "levelup", 0.6); sfx(j2, "levelup", 0.6)
chip("ff", j2 + 0.5, at("05", "Fim") - 0.15, "▶▶", 470, 1500, "")
p.tiques(at("04", "relógio"), at("05", "Fim") - 0.1, 0.25)

# ======================= 05: resultado da disputa
sfx(at("05", "Fim") - 0.1, "buzzer", 0.6)
cap(at("05", "Fim"), "Fim da disputa", "")
cam(at("05", "Primeiro") - 0.3, "podio", (-1.5, 4.0, 18), (0, 2.6, 0), 46, mv=(0.3, 0.02, -0.55)); sfx(at("05", "Primeiro") - 0.3, "whoosh", 0.6)
E("podio", at("05", "Primeiro") - 0.1); [sfx(at("05", "Primeiro") - 0.1 + 0.25 * k, "pop_low", 0.5) for k in (0, 1, 2)]
cap(at("05", "Primeiro"), "1º R$ 399 mil", "2º R$ 426 mil")
cap(at("05", "Você"), "Você: 3º lugar", "R$ 438 mil")
p.val2(at("05", "terceiro"), 3, 0.4); sfx(at("05", "terceiro"), "error_click", 0.6)

# ======================= 06: empate ficto (5%)
cam(at("06", "Se") - 0.1, "podio", (1.0, 6.0, 16), (0, 3.2, 0), 46, cut=False, dur=2.0)
cap(at("06", "micro"), "Micro ou pequena empresa", "até 5% acima do 1º")
p.diorama(faixa=[[at("06", "cinco") - 0.1, at("07", "Ô") - 0.4]])
sfx(at("06", "cinco"), "pop_soft", 0.6)
cap(at("06", "teria"), "tem 5 minutos", "para cobrir a oferta")
chip("t5", at("06", "minutos"), at("06", "Mas") - 0.1, "5:00", 470, 1150, "mag")
cap(at("06", "Mas"), "Mas a distância", "é de quase 10%")
chip("d10", at("06", "quase"), st("07") - 0.3, "9,8% acima", 600, 1230, "erro"); sfx(at("06", "quase"), "error_click", 0.6)
# regua 5%
r0 = at("06", "acima") - 0.1; r1 = st("07") - 0.35
p.card(f"""  #regua {{ position:absolute; left:90px; width:900px; top:1440px; padding:22px 34px 28px; border-radius:30px; background:rgba(16,18,24,0.82); }}
  #regua .k {{ color:{LAV}; font-size:28px; font-weight:600; letter-spacing:0.12em; }}
  #regua .tr {{ position:relative; height:26px; margin-top:42px; border-radius:13px; background:rgba(244,246,249,0.14); }}
  #regua .faixa {{ position:absolute; left:0; top:0; height:26px; width:51%; border-radius:13px; background:{MAG}; transform-origin:left; }}
  #regua .mk {{ position:absolute; top:-46px; font-size:28px; font-weight:600; color:{CREME}; white-space:nowrap; transform:translateX(-50%); }}
  #regua .pt {{ position:absolute; top:-6px; width:38px; height:38px; margin-left:-19px; border-radius:50%; }}
  #regua .esc {{ position:relative; height:40px; margin-top:16px; }} #regua .esc span {{ position:absolute; transform:translateX(-50%); color:{CREME}; font-size:30px; font-weight:600; }}
  .tag.erro {{ color:{ERRO}; }}""",
f"""  <div id="regua" class="clip" data-start="{round(r0,3)}" data-duration="{round(r1-r0,3)}" data-track-index="1">
    <div class="k">FAIXA DO EMPATE FICTO (5%)</div>
    <div class="tr"><div class="faixa"></div><div class="mk" style="left:0%">1º</div><div class="mk" style="left:51%">+5%</div><div class="mk" id="rg-voce" style="left:100%;color:{ERRO}">você</div>
      <div class="pt" style="left:0%;background:{CREME}"></div><div class="pt" id="rg-pt" style="left:100%;background:{ERRO}"></div></div>
    <div class="esc"><span style="left:0%">399</span><span style="left:51%">419</span><span style="left:100%">438</span></div></div>""",
f"""  tl.fromTo("#regua", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {round(r0,3)});
  tl.fromTo("#regua .faixa", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power2.out" }}, {round(r0 + 0.3,3)});
  tl.fromTo("#rg-pt, #rg-voce", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {round(at('06','Mas'),3)});
  tl.to("#regua", {{ opacity: 0, duration: 0.3 }}, {round(r1-0.3,3)});""")

# ======================= 07: pausa
p.pausa("07", fim="Bora")

# ======================= 08: a virada (desclassificacao)
cam(at("08", "Aqui") - 0.2, "podio", (0, 3.8, 15), (0, 3.0, 0), 42, mv=(0, 0, -0.3))
cap(at("08", "Aqui"), "Acabou?", "")
cam(at("08", "Não") - 0.1, "arena", (1.3, 2.35, -3.6), (0, 1.85, -7.1), 40, mv=(-0.05, 0, 0.05)); sfx(at("08", "Não") - 0.1, "whoosh", 0.6)
cap(at("08", "Não"), "Não acabou.", "Agora vem o julgamento")
cam(at("08", "edital") - 0.2, "raiox", (0, 3.4, 15.5), (0, 2.5, 0), 46, mv=(0, -0.02, -0.3)); sfx(at("08", "edital") - 0.2, "whoosh", 0.7)
E("rx_abre", at("08", "edital")); sfx(at("08", "edital") + 0.2, "gate", 0.6)
cap(at("08", "confere"), "A proposta do 1º", "conferida com o edital")
E("rx_ed", at("08", "dezesseis")); sfx(at("08", "dezesseis"), "pop_soft", 0.7)
cap(at("08", "O", 3), "O edital pede", "16 GB de memória")
E("rx_pr", at("08", "oferece")); sfx(at("08", "oferece"), "error_click", 0.8)
cap(at("08", "A", 2), "A proposta oferece", "8 GB")
E("rx_x", at("08", "Desclassificada") - 0.05); sfx(at("08", "Desclassificada") - 0.05, "alarm", 0.8)
cap(at("08", "Desclassificada"), "Desclassificada", "")

# ======================= 09: o segundo, negociacao
cam(st("09") - 0.15, "podio", (0, 4.4, 18), (0, 2.8, 0), 46, mv=(0, 0, -0.25)); sfx(st("09") - 0.15, "whoosh", 0.6)
E("cai", st("09")); E("troca", at("09", "passa")); p.diorama(podio_x=[[st("09"), at("09", "passa") + 0.8]])
sfx(st("09") + 0.05, "thud", 0.7); sfx(at("09", "passa"), "whoosh", 0.5)
cap(at("09", "A", 1), "A vez passa", "para o 2º colocado")
E("arena_fora", st("09"))
cam(at("09", "pregoeiro") - 0.15, "arena", (-10.2, 5.0, 11.2), (-2.2, 1.9, -3.0), 44, mv=(0.32, -0.04, -0.3)); sfx(at("09", "pregoeiro") - 0.15, "whoosh", 0.5)
cap(at("09", "tenta"), "O pregoeiro tenta", "negociar um preço melhor")
chip("n1", at("09", "negociar"), at("09", "segura") - 0.1, "Consegue melhorar?", 330, 1180, "")
chip("n2", at("09", "segura"), at("09", "Aceita") - 0.2, "Ficamos em R$ 426 mil", 250, 1280, "mag"); sfx(at("09", "segura"), "pop_soft", 0.6)
cap(at("09", "segura"), "R$ 426 mil", "dentro do estimado")
cam(at("09", "estimado") - 0.1, "arena", (0, 6.1, 3.6), (0, 6.1, -9.5), 50, mv=(0, 0, -0.2)); sfx(at("09", "estimado") - 0.1, "whoosh", 0.5)
cap(at("09", "Aceita"), "Proposta aceita", ""); sfx(at("09", "Aceita"), "stamp", 0.8)

# ======================= 10: habilitacao
cam(st("10") - 0.15, "habil", (-0.8, 6.4, 6.8), (0, 0.8, 0.0), 46, mv=(0.14, -0.08, -0.16)); sfx(st("10") - 0.15, "whoosh", 0.6)
cap(at("10", "Só"), "Só agora: habilitação", "e só de quem está em 1º")
docs_t = [at("10", "contrato"), at("10", "certidões"), at("10", "atestado")]
p.diorama(docs=docs_t); [sfx(t, "whoosh", 0.45) for t in docs_t]; [sfx(t + 0.55, "pop_soft", 0.5) for t in docs_t]
cap(at("10", "contrato"), "Contrato social, certidões", "atestado de fornecimento")
cap(at("10", "Documento"), "Faltou documento?", "Cai até o melhor preço")
chip("falta", at("10", "Documento"), at("10", "preço") + 0.6, "falta 1 documento = fora", 210, 1300, "erro"); sfx(at("10", "falta"), "error_click", 0.6)

# ======================= 11: habilitada, recurso, homologacao
E("carimbo", at("11", "Habilitada")); sfx(at("11", "Habilitada"), "stamp", 0.9)
p.diorama(confete=[[at("11", "Habilitada") + 0.1, "habil", 0, 2.5, 0], [at("11", "homologa") + 0.1, "cidade", 0, 3.0, 6.2]])
sfx(at("11", "Habilitada") + 0.1, "confetti", 0.6)
cap(at("11", "Habilitada"), "Habilitada", "")
cam(at("11", "Você") - 0.15, "podio", (-1.0, 4.0, 13), (-1.2, 3.0, 0), 42, mv=(0, 0, -0.2)); sfx(at("11", "Você") - 0.15, "whoosh", 0.5)
p.val2(at("11", "segundo"), 2, 0.4); sfx(at("11", "segundo"), "levelup", 0.8)
p.diorama(fv_modo=[[0, 0], [at("06", "Mas"), 1], [st("07") - 0.3, 0], [at("11", "sobe"), 2], [at("11", "Quem") - 0.2, 0]])
cap(at("11", "Você"), "Você sobe", "para 2º")
cam(at("11", "Quem") - 0.15, "arena", (-2.0, 2.35, 2.5), (-3.25, 1.95, 5.7), 38, mv=(0.03, 0, -0.03)); sfx(at("11", "Quem") - 0.15, "whoosh", 0.5)
cap(at("11", "Quem"), "Discorda? Diga na hora", "que vai recorrer")
chip("rec", at("11", "recorrer"), at("11", "Sem") - 0.1, "Intenção de recurso: agora", 180, 1250, "mag"); sfx(at("11", "recorrer"), "alert", 0.6)
cam(at("11", "Sem") - 0.15, "cidade", (0, 7.6, 18.5), (0, 0.6, 6.0), 46, mv=(0, -0.05, -0.25)); sfx(at("11", "Sem") - 0.15, "whoosh", 0.6)
cap(at("11", "Sem"), "Sem recurso", "a autoridade homologa")
E("homolog", at("11", "homologa")); sfx(at("11", "homologa"), "stamp", 1.0); sfx(at("11", "homologa") + 0.1, "confetti", 0.6)
cap(at("11", "quatrocentos"), "Homologado", "R$ 426 mil")

# ======================= 12: a licao e a Licit
cam(st("12") - 0.15, "podio", (0, 4.2, 18), (0, 2.8, 0), 46, mv=(0, 0, -0.3)); sfx(st("12") - 0.15, "whoosh", 0.5)
cap(at("12", "Repara"), "O menor lance", "só abriu a fila")
cap(at("12", "Levou"), "Levou quem cumpriu o edital", "no preço e no papel")
cam(at("12", "Na") - 0.2, "escritorio", (0.9, 2.75, 3.8), (-0.3, 2.2, -3), 50, mv=(0, -0.02, -0.1)); sfx(at("12", "Na") - 0.2, "whoosh", 0.6)
p.diorama(prot_modo=[[0, 0]])
cap(at("12", "Na"), "Na Licit, pergunte ao edital", "e veja a página")
k0, k1 = at("12", "Na"), st("13") + 1.6
q_t, r_t = at("12", "pergunta"), at("12", "resposta")
p.card(f"""  #prod {{ position:absolute; left:110px; width:860px; top:1120px; border-radius:34px; background:#F4F6F9; box-shadow:0 22px 70px rgba(0,0,0,0.45); overflow:hidden; }}
  #prod .top {{ display:flex; align-items:center; gap:18px; padding:20px 30px; background:{FLO}; }}
  #prod .top img {{ height:44px; }} #prod .top span {{ color:#B8C5BC; font-size:28px; font-weight:500; }}
  #prod .corpo {{ padding:26px 30px 30px; display:flex; flex-direction:column; gap:18px; }}
  #prod .q {{ align-self:flex-end; max-width:80%; padding:18px 26px; border-radius:24px 24px 6px 24px; background:{FLO}; color:#F4F6F9; font-size:34px; font-weight:500; line-height:1.25; }}
  #prod .r {{ align-self:flex-start; max-width:88%; padding:18px 26px; border-radius:24px 24px 24px 6px; background:#FFFFFF; border:2px solid #D8E0D9; color:#101218; font-size:34px; font-weight:500; line-height:1.3; }}
  #prod .r b {{ font-weight:600; }} #prod .ref {{ display:inline-block; margin-top:12px; padding:6px 16px 8px; border-radius:16px; background:#E1F4D4; color:{FLO}; font-size:28px; font-weight:600; }}
  #prod .ilu {{ color:#59616E; font-size:28px; text-align:right; padding:0 30px 20px; }}""",
f"""  <div id="prod" class="clip" data-start="{round(k0,3)}" data-duration="{round(k1-k0,3)}" data-track-index="2">
    <div class="top"><img src="assets/logo_wordmark.png" alt=""><span>Edital: aquisição de computadores</span></div>
    <div class="corpo"><div class="q" id="pq">Qual a memória mínima exigida?</div>
      <div class="r" id="pr"><b>16 GB</b> por equipamento.<br><span class="ref">Edital, página 18</span></div></div>
    <div class="ilu">exemplo ilustrativo</div></div>""",
f"""  tl.fromTo("#prod", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(k0,3)});
  tl.fromTo("#pq", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {round(q_t,3)});
  tl.fromTo("#pr", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.6)" }}, {round(r_t,3)});
  tl.fromTo("#pr .ref", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {round(at('12','página'),3)});
  tl.to("#prod", {{ opacity: 0, y: 40, duration: 0.4 }}, {round(k1-0.4,3)});""")
p.hud_js(f'tl.to("#hud-logo", {{ opacity: 0, duration: 0.2 }}, {round(k0,3)}); tl.to("#hud-logo", {{ opacity: 0.96, duration: 0.3 }}, {round(k1,3)});')
sfx(q_t, "pop_soft", 0.6); sfx(r_t, "pop_soft", 0.7)
cam(at("12", "Antes") - 0.1, "escritorio", (2.3, 2.05, -3.2), (0.2, 1.8, -0.4), 38, mv=(-0.03, 0, 0.02))
cap(at("12", "Antes"), "Antes do primeiro lance", "")

# ======================= 13: fecho
cam(st("13") - 0.1, "arena", (0, 8.5, 19), (0, 4.4, -4), 50, mv=(0, -0.12, -0.4)); sfx(st("13") - 0.1, "whoosh", 0.5)
cap(at("13", "E"), "Você já perdeu um pregão", "no detalhe? Conta aqui")
p.hud_hide(at("13", "Na") - 0.3)
p.endcard(at("13", "Na") - 0.2, sub="Próximo episódio: a habilitação")

# ======================= expressoes e cena
p.diorama(expr=[[0, "neutro"], [at("02", "edital"), "foco"], [at("02", "A", 3), "neutro"], [st("04"), "tenso"], [at("04", "relógio"), "susto"], [at("05", "Fim"), "tenso"], [at("05", "terceiro"), "duvida"],
                [at("06", "Mas"), "tenso"], [at("08", "Desclassificada"), "susto"], [at("09", "passa"), "alivio"], [at("11", "Quem"), "foco"], [at("12", "Na"), "alivio"]])
p.diorama(cam3=C3)
p.cena("pregao", extras=["kit3d.js"])
p.write()
