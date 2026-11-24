import sys; sys.path.insert(0,'../storyboard-r1')
from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249)
W,H=1080,1920
COMPRAS=[('Prefeitura de Sete Lagoas/MG','Reforma do prédio da prefeitura','R$ 1.250.661','até 28/12'),
         ('Prefeitura de Poços de Caldas/MG','Reforma de escola municipal','R$ 1.553.970','até 21/12'),
         ('Prefeitura de Capão do Leão/RS','Reforma de quadra de escola','R$ 993.310','até 30/12')]
def pill(d,cx,cy,t,f,fg=GRAF,bg=LIM,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
def busca(n):
    im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
    pill(d,W/2,170,'profissiolicit.ai',font(44,600))
    d.rounded_rectangle((60,250,W-60,1420),40,fill=SUP)
    d.text((110,310),'Licitações para sua empresa.',font=font(50,600),fill=GRAF); d.text((110,388),'Digite o CNPJ',font=font(32),fill=AP)
    d.rounded_rectangle((110,440,W-110,540),20,outline=FLO,width=4,fill=BR); d.text((144,464),'12.345.678/0001-90',font=font(42),fill=GRAF)
    d.rounded_rectangle((110,570,W-110,670),20,fill=FLO); d.text((W/2,620),'Descobrir oportunidades grátis',font=font(36,600),fill=BR,anchor='mm')
    y=720
    for a,b,c,e in COMPRAS[:n]:
        d.rounded_rectangle((110,y,W-110,y+205),20,fill=BR,outline=(220,224,230),width=2)
        d.text((144,y+24),a,font=font(28),fill=AP); d.text((144,y+66),b,font=font(40,600),fill=GRAF); d.text((144,y+132),f'{c}  ·  {e}',font=font(32),fill=FLO)
        d.text((W-144,y+24),'PNCP',font=font(24,600),fill=(150,158,170),anchor='ra'); y+=225
    return im
for n in range(4): busca(n).save(f'telas/t09_{n}.png')
# cartao de prova
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle((60,1010,W-60,1500),36,fill=(16,18,24,240))
d.text((110,1046),'Prefeitura de Sete Lagoas/MG',font=font(40),fill=LIM); d.text((110,1108),'Reforma do prédio',font=font(60,600),fill=BR)
d.text((110,1182),'da prefeitura municipal',font=font(44,600),fill=BR); d.text((110,1262),'R$ 1.250.661',font=font(96,600),fill=BR)
d.text((110,1386),'Proposta até 28/12/2026',font=font(40),fill=BR); d.text((110,1444),'Fonte: PNCP',font=font(30),fill=(150,158,170)); im.save('ov/o05.png')
# pergunta ao edital
def perg(n):
    im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im); pill(d,W/2,330,'Pergunte ao edital',font(56,600))
    if n>=1:
        d.rounded_rectangle((250,470,W-90,690),32,fill=FLO); d.text((300,510),'Precisa de',font=font(50,600),fill=BR); d.text((300,580),'visita técnica?',font=font(50,600),fill=BR)
    if n>=2:
        d.rounded_rectangle((90,740,W-200,1130),32,fill=SUP); d.text((140,780),'Sim. A visita é facultativa',font=font(42,600),fill=GRAF)
        d.text((140,842),'e deve ser agendada',font=font(42),fill=GRAF); d.text((140,900),'até dois dias antes',font=font(42),fill=GRAF); d.text((140,958),'da sessão.',font=font(42),fill=GRAF)
        f=font(34,600); t='Edital, p. 14'; tw=d.textlength(t,font=f); d.rounded_rectangle((140,1036,140+tw+48,1096),30,fill=LIM); d.text((164,1046),t,font=f,fill=GRAF)
    if n>=3:
        d.rounded_rectangle((90,1190,W-90,1330),32,outline=LIM,width=4); d.text((W/2,1260),'Você confere e decide.',font=font(48,600),fill=BR,anchor='mm')
    return im
for n in range(4): perg(n).save(f'telas/tq_{n}.png')
