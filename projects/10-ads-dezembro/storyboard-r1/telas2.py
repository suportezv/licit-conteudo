# Telas do produto (cheias 1080x1920) e conteudos 4:3 para o monitor
from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249)
W,H=1080,1920
COMPRAS=[('Prefeitura de Uberlândia/MG','Material de limpeza','R$ 2.783.423','até 30/11'),
         ('Prefeitura de Bocaiúva/MG','Material de limpeza','R$ 669.575','até 02/12'),
         ('Prefeitura de Capim Grosso/BA','Limpeza, higiene e descartáveis','R$ 7.863.777','até 04/12')]
def pill(d,cx,cy,t,f,fg,bg,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
def busca(n,cnpj='12.345.678/0001-90'):
    im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
    pill(d,W/2,170,'profissiolicit.ai',font(44,600),GRAF,LIM)
    d.rounded_rectangle((60,250,W-60,1420),40,fill=SUP)
    d.text((110,310),'Licitações para sua empresa.',font=font(50,600),fill=GRAF); d.text((110,388),'Digite o CNPJ',font=font(32),fill=AP)
    d.rounded_rectangle((110,440,W-110,540),20,outline=FLO,width=4,fill=BR); d.text((144,464),cnpj,font=font(42),fill=GRAF)
    d.rounded_rectangle((110,570,W-110,670),20,fill=FLO); d.text((W/2,620),'Descobrir oportunidades grátis',font=font(36,600),fill=BR,anchor='mm')
    y=720
    for a,b,c,e in COMPRAS[:n]:
        d.rounded_rectangle((110,y,W-110,y+205),20,fill=BR,outline=(220,224,230),width=2)
        d.text((144,y+24),a,font=font(28),fill=AP); d.text((144,y+66),b,font=font(40,600),fill=GRAF); d.text((144,y+132),f'{c}  ·  {e}',font=font(32),fill=FLO)
        d.text((W-144,y+24),'PNCP',font=font(24,600),fill=(150,158,170),anchor='ra'); y+=225
    return im
for n in range(4): busca(n).save(f'telas/t09_{n}.png')
busca(0,'').save('telas/t09_vazio.png')
ITENS=[('Edital','cada exigência com a página'),('Documento','validade conferida antes da entrega'),('Prazo','o que falta e até quando')]
def resto(n):
    im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
    pill(d,W/2,330,'E ela ajuda no resto',font(56,600),GRAF,LIM); y=500
    for a,b in ITENS[:n]:
        d.rounded_rectangle((90,y,W-90,y+250),32,fill=SUP); d.text((140,y+48),a,font=font(72,600),fill=FLO); d.text((140,y+150),b,font=font(38),fill=AP); y+=290
    return im
for n in range(4): resto(n).save(f'telas/t09b_{n}.png')
# conteudos 4:3 do monitor (1024x768)
h=Image.open('telas/home_site.png').convert('RGB'); h=h.crop((0,0,2360,1770)).resize((1024,768),Image.LANCZOS); h.save('telas/m_home.png')
im=Image.new('RGB',(1024,768),SUP); d=ImageDraw.Draw(im)
d.rectangle((0,0,1024,90),fill=FLO); d.text((40,26),'Aviso de contratação',font=font(36,600),fill=BR); d.text((984,32),'PNCP',font=font(28,600),fill=LIM,anchor='ra')
d.text((40,130),'Prefeitura de Uberlândia/MG',font=font(34),fill=AP); d.text((40,186),'Material de limpeza',font=font(64,600),fill=GRAF)
d.text((40,270),'para a rede municipal de ensino',font=font(32),fill=AP); d.text((40,350),'R$ 2.783.423',font=font(110,600),fill=FLO)
d.rounded_rectangle((40,520,984,620),18,fill=BR,outline=(215,220,228),width=2); d.text((70,546),'Proposta até 30/11/2026',font=font(40,600),fill=GRAF)
d.text((40,670),'Publicado no PNCP',font=font(34),fill=AP); im.save('telas/m_pncp.png')
im=Image.new('RGB',(1024,768),GRAF); d=ImageDraw.Draw(im)
d.rounded_rectangle((30,30,994,738),28,fill=SUP); d.text((70,60),'Licitações para sua empresa.',font=font(44,600),fill=GRAF)
d.rounded_rectangle((70,130,640,206),14,outline=FLO,width=3,fill=BR); d.text((92,146),'12.345.678/0001-90',font=font(36),fill=GRAF)
d.rounded_rectangle((660,130,954,206),14,fill=FLO); d.text((807,168),'Descobrir grátis',font=font(30,600),fill=BR,anchor='mm')
y=236
for a,b,c,e in COMPRAS:
    d.rounded_rectangle((70,y,954,y+150),14,fill=BR,outline=(220,224,230),width=2); d.text((94,y+14),a,font=font(24),fill=AP); d.text((94,y+48),b,font=font(36,600),fill=GRAF); d.text((94,y+100),f'{c}  ·  {e}',font=font(28),fill=FLO); y+=164
im.save('telas/m_busca.png')
im=Image.new('RGB',(1024,768),GRAF); d=ImageDraw.Draw(im); y=40
for a,b in ITENS:
    d.rounded_rectangle((40,y,984,y+210),24,fill=SUP); d.text((80,y+34),a,font=font(68,600),fill=FLO); d.text((80,y+130),b,font=font(36),fill=AP); y+=234
im.save('telas/m_resto.png')
