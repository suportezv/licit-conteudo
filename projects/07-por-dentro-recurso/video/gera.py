#!/usr/bin/env python3
"""Por Dentro da Licitação #3: o recurso. Gerador da peça (HyperFrames)."""
SEG = {
"01": "A sua empresa foi habilitada. Contrato quase na mão. Aí, na sessão, uma concorrente escreve uma frase só: tenho intenção de recorrer. E tudo para.",
"02": "Lembra do episódio passado? A empresa dois caiu na habilitação, e a sua, com quatrocentos e trinta e oito mil, foi habilitada depois de atualizar a certidão do FGTS em diligência.",
"03": "A empresa dois não gostou. Para ela, a certidão vencida devia ter derrubado você. E ela tem um caminho para contestar: o recurso.",
"04": "Primeiro, a intenção. Ela precisa ser dita na hora, logo que o resultado sai. Quem fica calado na sessão perde o direito de recorrer depois.",
"05": "Depois, as razões. A empresa dois tem três dias úteis para escrever por que a decisão está errada. E não basta discordar: tem que apontar a regra do edital ou da lei.",
"06": "Enquanto isso, o processo fica suspenso. Nada de homologação, nada de contrato, até a decisão final.",
"07": "Ô, pausa rapidinha. Deixa o like e segue a Licíte pra ver quem leva. Bora continuar.",
"08": "Agora é a sua vez. Você tem o mesmo prazo, três dias úteis, para as contrarrazões. É onde você mostra a sua versão, com documento e data.",
"09": "E a sua defesa é simples: a certidão venceu depois da entrega das propostas. A lei permite atualizar em diligência. Você não trouxe documento novo, atualizou um que já tinha.",
"10": "O recurso vai primeiro para o pregoeiro. Ele tem três dias úteis para rever a própria decisão. Se mantiver, manda para a autoridade superior, que decide em até dez dias úteis.",
"11": "Decisão: recurso negado. A habilitação continua de pé, a autoridade homologa, e a prefeitura chama a sua empresa para assinar o contrato.",
"12": "Repara: recurso não se ganha no grito, nem com o texto mais longo. Ganha quem tem a regra, o documento e a data do seu lado. E quem não perde o prazo.",
"13": "Na Licíte, cada tarefa da licitação tem responsável e prazo. E você, já respondeu a um recurso? Conta aqui. Na próxima: do contrato ao pagamento.",
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
EST_H = [0.3, 0.3, 0.3, 0.9, 1.7]
def estacao(t, i, cut=True, dx=1.2):  # plano de uma estacao do caminho do recurso
    x = i * 6; h = EST_H[i]; cam(t, "rito", (x + dx, h + 3.1, 9.8), (x + 0.2, h + 2.0, 0), 50, cut=cut, mv=(-0.18, 0.02, -0.18))
PLACAR = ((0, 6.1, 3.6), (0, 6.1, -9.5))
p.diorama(podio2=True)
E("p2_cai", -6); E("p2_sobe", -5)

# ======================= 01: habilitada, e a intencao de recorrer
cam(0.0, "arena", *PLACAR, 50, mv=(0, 0, -0.25))
sfx(0.05, "chord", 0.8)
p.diorama(placar_modo=[[0, 8], [at("01", "tudo") - 0.1, 9], [at("11", "negado"), 10]])
cap(0.4, "Habilitada.", "Contrato quase na mão")
cam(at("01", "Contrato") - 0.1, "arena", (-2.0, 2.35, 2.5), (-3.25, 1.95, 5.7), 38, mv=(0.03, 0, -0.03)); sfx(at("01", "Contrato") - 0.1, "whoosh", 0.4)
cam(at("01", "Aí") - 0.15, "arena", (0.6, 3.9, -3.2), (-4.6, 3.0, 3.2), 50, mv=(-0.05, 0, 0.05)); sfx(at("01", "Aí") - 0.15, "whoosh", 0.6)
E("balao", at("01", "escreve")); E("balao_fim", st("02") - 0.2); sfx(at("01", "escreve"), "pop_soft", 0.7)
cap(at("01", "escreve"), "Uma frase só:", "intenção de recorrer")
cam(at("01", "tudo") - 0.15, "arena", *PLACAR, 50, mv=(0, 0, -0.15)); sfx(at("01", "tudo") - 0.1, "alarm", 0.7)
cap(at("01", "tudo"), "E tudo", "para")

# ======================= 02: o caso do episodio passado
cam(st("02") - 0.15, "podio", (-0.6, 4.4, 16), (-0.6, 3.0, 0), 44, mv=(0.25, 0, -0.35)); sfx(st("02") - 0.15, "whoosh", 0.6)
cap(at("02", "Lembra"), "No episódio passado", "a empresa 02 caiu")
p.hud_set("SEU LANCE", 438000, fmt="brl", cor="fixa")
p.hud2_set("PRAZO", 0, fmt='(v<0.5?"na sessão":Math.round(v)+(Math.round(v)==1?" dia útil":" dias úteis"))', cor="fixa")
p.hud_js('tl.set("#hud-wrap", { opacity: 0 }, 0.3);'); p.hud_show(at("02", "quatrocentos")); sfx(at("02", "quatrocentos"), "register", 0.7)
cap(at("02", "habilitada"), "Habilitada depois de atualizar", "a certidão em diligência")
cam(at("02", "habilitada") - 0.15, "linha", (-0.5, 2.7, 11), (-0.5, 2.9, 0), 46, mv=(0.25, 0.03, -0.35)); sfx(at("02", "habilitada") - 0.15, "whoosh", 0.5)
E("dil", -1); E("seta", -1)

# ======================= 03: o caminho do recurso
cam(st("03") - 0.15, "rito", (-8.5, 6.8, 9.5), (11, 1.4, -1.0), 50, mv=(0.35, -0.03, -0.15)); sfx(st("03") - 0.15, "whoosh", 0.7)
cap(at("03", "A"), "A empresa 02", "não gostou")
cam(at("03", "Para") - 0.1, "rito", (-2.4, 2.7, 5.6), (-4.2, 1.9, 1.0), 42, mv=(0.08, 0, -0.08)); sfx(at("03", "Para") - 0.1, "whoosh", 0.4)
cam(at("03", "caminho") - 0.15, "rito", (-8.5, 6.8, 9.5), (11, 1.4, -1.0), 50, mv=(0.45, -0.03, -0.15)); sfx(at("03", "caminho") - 0.15, "whoosh", 0.5)
cap(at("03", "caminho"), "O caminho para contestar:", "o recurso")
sfx(at("03", "recurso"), "sting", 0.6)

# ======================= 04: a intencao
estacao(st("04") - 0.15, 0); sfx(st("04") - 0.15, "whoosh", 0.6)
E("st1", st("04")); sfx(st("04") + 0.1, "levelup", 0.5); p.val2(st("04"), 0, 0.2)
cap(at("04", "Primeiro"), "1. Intenção:", "na hora, na sessão")
cam(at("04", "Ela") - 0.1, "rito", (0.6, 2.0, 4.0), (-0.4, 1.7, 0.2), 44, mv=(0.1, 0, -0.1)); sfx(at("04", "Ela") - 0.1, "whoosh", 0.4)
estacao(at("04", "Quem") - 0.15, 0)
E("porta", at("04", "perde")); sfx(at("04", "perde") + 0.35, "thud", 0.7)
cap(at("04", "Quem"), "Ficou calado na sessão?", "Perdeu o direito de recorrer")
chip("a165a", at("04", "Quem"), st("05") - 0.3, "Lei 14.133, art. 165", 560, 1250, "mag")

# ======================= 05: as razoes
estacao(st("05") - 0.15, 1); sfx(st("05") - 0.15, "whoosh", 0.6)
E("st2", st("05")); sfx(st("05") + 0.1, "levelup", 0.5)
cap(at("05", "Depois"), "2. Razões:", "3 dias úteis")
E("raz_d", at("05", "três")); [sfx(at("05", "três") + 0.35 * k, "metal_click", 0.45) for k in range(3)]; p.val2(at("05", "três"), 3, 0.5)
E("raz_escreve", at("05", "escrever")); sfx(at("05", "escrever"), "sacks", 0.3)
cap(at("05", "basta") - 0.25, "Não basta discordar:", "tem que apontar a regra")

# ======================= 06: suspenso
cam(st("06") - 0.15, "rito", (33.4, 3.4, 7.5), (31, 2.2, 0), 46, mv=(-0.2, 0, -0.15)); sfx(st("06") - 0.15, "whoosh", 0.6)
E("suspenso", at("06", "suspenso")); sfx(at("06", "suspenso"), "gate", 0.6)
cap(at("06", "Enquanto"), "O processo fica", "suspenso")
cap(at("06", "Nada"), "Sem homologação", "e sem contrato")
chip("a168", at("06", "Nada"), st("07") - 0.4, "Lei 14.133, art. 168", 560, 1660, "mag")

# ======================= 07: pausa
p.pausa("07", fim="Bora")

# ======================= 08: as contrarrazoes
estacao(at("08", "Agora") - 0.2, 2); sfx(at("08", "Agora") - 0.2, "whoosh", 0.6)
E("st3", at("08", "Agora")); sfx(at("08", "Agora") + 0.1, "levelup", 0.5)
cap(at("08", "Agora"), "3. Sua vez:", "contrarrazões")
cam(at("08", "três") - 0.1, "rito", (12.9, 2.5, 4.4), (12.4, 0.6, 1.2), 46, mv=(-0.12, 0, -0.1)); sfx(at("08", "três") - 0.1, "whoosh", 0.4)
estacao(at("08", "onde") - 0.15, 2)
E("con_d", at("08", "três")); [sfx(at("08", "três") + 0.35 * k, "metal_click", 0.45) for k in range(3)]
p.val2(at("08", "três"), 3, 0.4); p.val2(at("08", "três") + 1.4, 2, 0.4); p.val2(at("08", "três") + 2.8, 1, 0.4)
E("con_escreve", at("08", "contrarrazões"))
cap(at("08", "onde"), "A sua versão", "com documento e data")

# ======================= 09: a defesa na balanca
cam(st("09") - 0.15, "balanca", (0.4, 5.2, 17.5), (0.4, 4.9, 0), 50, mv=(0, 0, -0.15)); sfx(st("09") - 0.15, "whoosh", 0.6)
cap(at("09", "E"), "A defesa", "é simples")
cam(at("09", "certidão") - 0.1, "balanca", (1.6, 5.0, 12.5), (2.2, 4.9, 0.6), 46, mv=(-0.1, 0, -0.15)); sfx(at("09", "certidão") - 0.1, "whoosh", 0.4)
cam(at("09", "Você") - 0.15, "balanca", (0.4, 5.2, 17.5), (0.4, 4.9, 0), 50, mv=(0, 0, -0.2)); sfx(at("09", "Você") - 0.15, "whoosh", 0.4)
E("chips", at("09", "certidão")); [sfx(at("09", "certidão") + 0.9 * k, "pop_soft", 0.6) for k in range(3)]
cap(at("09", "certidão"), "Venceu depois", "da entrega das propostas")
E("pesa", at("09", "Você")); sfx(at("09", "Você"), "thud", 0.6)
cap(at("09", "Você"), "Não é documento novo:", "é o mesmo, atualizado")

# ======================= 10: pregoeiro e autoridade superior
estacao(st("10") - 0.15, 3); sfx(st("10") - 0.15, "whoosh", 0.6)
E("st4", st("10")); sfx(st("10") + 0.1, "levelup", 0.5)
cap(at("10", "O"), "4. O pregoeiro", "pode rever")
E("preg_d", at("10", "três")); [sfx(at("10", "três") + 0.35 * k, "metal_click", 0.45) for k in range(3)]; p.val2(at("10", "três"), 3, 0.5)
estacao(at("10", "Se") - 0.15, 4); sfx(at("10", "Se") - 0.15, "whoosh", 0.6)
E("st5", at("10", "autoridade")); sfx(at("10", "autoridade"), "levelup", 0.5)
cap(at("10", "Se"), "5. A autoridade superior", "decide em até 10 dias úteis")
E("aut_d", at("10", "decide")); [sfx(at("10", "decide") + 0.12 * k, "metal_click", 0.35) for k in range(0, 10, 2)]; p.val2(at("10", "decide"), 10, 0.8)

# ======================= 11: negado, homologado
cam(st("11") - 0.15, "balanca", (-1.6, 4.4, 11), (-2.6, 3.4, 0), 46, mv=(0.1, 0, -0.15)); sfx(st("11") - 0.15, "whoosh", 0.6)
E("negado", at("11", "negado")); sfx(at("11", "negado"), "stamp", 1.0)
cap(at("11", "Decisão"), "Recurso", "negado")
cam(at("11", "A") - 0.15, "rito", (33.4, 3.4, 7.5), (31, 2.2, 0), 46, mv=(-0.2, 0, -0.15)); sfx(at("11", "A") - 0.15, "whoosh", 0.5)
E("destrava", at("11", "continua")); sfx(at("11", "continua") + 0.1, "gate", 0.7)
E("homolog2", at("11", "homologa")); sfx(at("11", "homologa"), "stamp", 0.9)
cap(at("11", "A"), "Habilitação de pé.", "Homologado")
cam(at("11", "prefeitura") - 0.15, "cidade", (0, 7.6, 18.5), (0, 0.6, 6.0), 46, mv=(0, -0.05, -0.25)); sfx(at("11", "prefeitura") - 0.15, "whoosh", 0.5)
E("homolog", at("11", "prefeitura") + 0.2); sfx(at("11", "prefeitura") + 0.3, "confetti", 0.6)
p.diorama(confete=[[at("11", "prefeitura") + 0.3, "cidade", 0, 3.0, 6.2]])
cap(at("11", "prefeitura"), "Hora de assinar", "o contrato")

# ======================= 12: a licao
cam(st("12") - 0.15, "balanca", (-2.0, 4.4, 8.5), (-3.3, 3.6, 0), 44, mv=(0.15, 0, -0.15)); sfx(st("12") - 0.15, "whoosh", 0.5)
cam(at("12", "Ganha") - 0.15, "balanca", (0, 5.2, 20.5), (0, 2.6, 5.2), 46, mv=(0, -0.05, -0.4)); E("fichas_on", at("12", "Ganha") - 0.15); sfx(at("12", "Ganha") - 0.15, "whoosh", 0.5)
cap(at("12", "Repara"), "Recurso não se ganha", "no grito")
for k, w in enumerate(["regra", "documento", "data", "prazo"]):
    E(f"ficha{k + 1}", at("12", w)); sfx(at("12", w), "pop_soft", 0.7)
cap(at("12", "Ganha"), "Regra, documento", "e data do seu lado")
cap(at("12", "quem", 2) - 0.2, "E nenhum prazo", "perdido")

# ======================= 13: a Licit e o fecho
cam(st("13") - 0.2, "escritorio", (0.9, 2.75, 3.8), (-0.3, 2.2, -3), 50, mv=(0, -0.02, -0.1)); sfx(st("13") - 0.2, "whoosh", 0.6)
p.diorama(prot_modo=[[0, 0]])
cap(at("13", "Na"), "Na Licit, cada tarefa", "com responsável e prazo")
k0, k1 = at("13", "Na"), at("13", "você") + 0.2
TAR = [("24", "NOV", "Enviar contrarrazões do recurso", "A", "Ana", "av"), ("26", "NOV", "Acompanhar a decisão do pregoeiro", "C", "Carlos", "ok"), ("15", "DEZ", "Renovar a certidão FGTS", "A", "Ana", "ok")]
linhas = "".join(f'<div class="ln" id="tl{i}"><div class="dt {c}"><b>{d}</b><span>{m}</span></div><div class="tx">{tx}</div><div class="av"><i>{a}</i>{n}</div></div>' for i, (d, m, tx, a, n, c) in enumerate(TAR))
p.card(f"""  #prod {{ position:absolute; left:100px; width:880px; top:1100px; border-radius:34px; background:#F4F6F9; box-shadow:0 22px 70px rgba(0,0,0,0.45); overflow:hidden; }}
  #prod .top {{ display:flex; align-items:center; gap:18px; padding:20px 30px; background:{FLO}; }}
  #prod .top img {{ height:44px; }} #prod .top span {{ color:#B8C5BC; font-size:28px; font-weight:500; }}
  #prod .corpo {{ padding:10px 26px 6px; }}
  #prod .ln {{ display:flex; align-items:center; gap:20px; padding:16px 0; border-bottom:2px solid #E2E7E3; }}
  #prod .dt {{ width:84px; height:84px; border-radius:18px; background:#E6EBE7; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#101218; }}
  #prod .dt b {{ font-size:36px; line-height:1; }} #prod .dt span {{ font-size:28px; color:#59616E; font-weight:600; }}
  #prod .dt.av {{ background:#FBE3B4; }} #prod .tx {{ flex:1; font-size:32px; font-weight:500; color:#101218; line-height:1.2; }}
  #prod .av {{ display:flex; align-items:center; gap:10px; font-size:28px; color:#59616E; }} #prod .av i {{ font-style:normal; width:42px; height:42px; border-radius:50%; background:{FLO}; color:#fff; display:flex; align-items:center; justify-content:center; font-weight:600; }}
  #prod .ilu {{ color:#59616E; font-size:28px; text-align:right; padding:8px 30px 20px; }}""",
f"""  <div id="prod" class="clip" data-start="{round(k0,3)}" data-duration="{round(k1-k0,3)}" data-track-index="2">
    <div class="top"><img src="assets/logo_wordmark.png" alt=""><span>Tarefas da licitação</span></div>
    <div class="corpo">{linhas}</div>
    <div class="ilu">exemplo ilustrativo</div></div>""",
f"""  tl.fromTo("#prod", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, {round(k0,3)});
  tl.fromTo("#prod .ln", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.3, stagger: 0.18, ease: "power2.out" }}, {round(k0 + 0.35,3)});
  tl.fromTo("#tl0 .dt", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, {round(at('13','prazo'),3)});
  tl.to("#prod", {{ opacity: 0, y: 40, duration: 0.4 }}, {round(k1-0.4,3)});""")
p.hud_js(f'tl.to("#hud-logo", {{ opacity: 0, duration: 0.2 }}, {round(k0,3)}); tl.to("#hud-logo", {{ opacity: 0.96, duration: 0.3 }}, {round(k1,3)});')
[sfx(k0 + 0.35 + 0.18 * i, "pop_soft", 0.45) for i in range(3)]; sfx(at("13", "prazo"), "alert", 0.5)
cam(at("13", "você") - 0.15, "arena", (0, 8.5, 19), (0, 4.4, -4), 50, mv=(0, -0.12, -0.4)); sfx(at("13", "você") - 0.15, "whoosh", 0.5)
cap(at("13", "você"), "Já respondeu a um recurso?", "Conta aqui")
p.hud_hide(at("13", "Na", 2) - 0.3)
p.endcard(at("13", "Na", 2) - 0.2, sub="Próximo episódio: do contrato ao pagamento")

# ======================= expressoes e cena
p.diorama(expr=[[0, "alivio"], [at("01", "escreve"), "susto"], [st("02"), "neutro"], [st("04"), "foco"], [at("05", "basta") - 0.25, "duvida"],
                [at("08", "Agora"), "foco"], [at("11", "negado"), "alivio"]])
E("fv_festa", at("11", "prefeitura"))
p.diorama(cam3=C3)
p.cena("recurso", extras=["kit3d.js"])
p.write()
