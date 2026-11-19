# Quadros 1080x1920 com os textos de tela (fora a legenda)
from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249)
W,H=1080,1920
def base(fn):
    im=Image.open(fn).convert('RGB'); s=H/im.height; im=im.resize((int(im.width*s),H),Image.LANCZOS)
    x=(im.width-W)//2; return im.crop((x,0,x+W,H))
def pill(d,cx,cy,t,f,fg,bg,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
import os; os.makedirs('telas',exist_ok=True)
for n in ['01','03','04','07','08','10']: base(f'q{n}.png').save(f'telas/t{n}.png')
im=base('q02.png'); d=ImageDraw.Draw(im); pill(d,W/2,1230,'Duas.',font(150,600),GRAF,LIM,(70,40)); im.save('telas/t02.png')
im=base('q03.png'); d=ImageDraw.Draw(im,'RGBA'); d.rounded_rectangle((60,1090,700,1230),28,fill=(16,18,24,225)); d.text((100,1112),'Dona Norma',font=font(52,600),fill=BR); d.text((100,1176),'pregoeira há 19 anos',font=font(34),fill=LIM); im.save('telas/t03.png')
im=base('q05.png'); d=ImageDraw.Draw(im,'RGBA')
d.rounded_rectangle((60,330,W-60,860),36,fill=(16,18,24,238))
d.text((110,372),'Prefeitura de Uberlândia/MG',font=font(40),fill=LIM)
d.text((110,440),'Material de limpeza',font=font(60,600),fill=BR)
d.text((110,514),'para a rede municipal de ensino',font=font(36),fill=(200,206,214))
d.text((110,590),'R$ 2.783.423',font=font(96,600),fill=BR)
d.text((110,724),'Proposta até 30/11/2026',font=font(40),fill=BR)
d.text((110,788),'Fonte: PNCP',font=font(30),fill=(150,158,170))
im.save('telas/t05.png')
im=base('q06.png'); d=ImageDraw.Draw(im); pill(d,W/2,1250,'Eu não posso te ligar.',font(70,600),GRAF,LIM); im.save('telas/t06.png')
im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
d.rounded_rectangle((60,250,W-60,1330),40,fill=SUP)
d.text((110,310),'Licitações para sua empresa.',font=font(50,600),fill=GRAF); d.text((110,388),'Digite o CNPJ',font=font(32),fill=AP)
d.rounded_rectangle((110,440,W-110,540),20,outline=FLO,width=4,fill=BR); d.text((144,464),'12.345.678/0001-90',font=font(42),fill=GRAF)
d.rounded_rectangle((110,570,W-110,670),20,fill=FLO); d.text((W/2,620),'Descobrir oportunidades grátis',font=font(36,600),fill=BR,anchor='mm')
y=720
for a,b,c in [('Prefeitura de Uberlândia/MG','Material de limpeza','R$ 2.783.423  ·  até 30/11'),('[órgão]','[objeto da compra]','[valor]  ·  até [data]'),('[órgão]','[objeto da compra]','[valor]  ·  até [data]')]:
    d.rounded_rectangle((110,y,W-110,y+175),20,fill=BR,outline=(220,224,230),width=2)
    d.text((144,y+22),a,font=font(28),fill=AP); d.text((144,y+62),b,font=font(38,600),fill=GRAF); d.text((144,y+118),c,font=font(28),fill=FLO); y+=195
pill(d,W/2,170,'profissiolicit.ai',font(44,600),GRAF,LIM)
im.save('telas/t09.png')
im=Image.new('RGB',(W,H),FLO); d=ImageDraw.Draw(im)
lg=Image.open(R+'assets/marca/logos/licit-estrela-branco.png').convert('RGBA'); lw=560; lg=lg.resize((lw,int(lg.height*lw/lg.width))); im.paste(lg,((W-lw)//2,520),lg)
d.rounded_rectangle((130,860,W-130,990),26,fill=BR); d.text((W/2,925),'Digite o CNPJ',font=font(50),fill=AP,anchor='mm')
pill(d,W/2,1110,'Teste grátis, sem cartão',font(58,600),GRAF,LIM,(56,42)); d.text((W/2,1290),'profissiolicit.ai',font=font(48),fill=BR,anchor='mm')
im.save('telas/t11.png')
im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
pill(d,W/2,330,'E ela ajuda no resto',font(56,600),GRAF,LIM)
y=500
for a,b in [('Edital','cada exigência com a página'),('Documento','validade conferida antes da entrega'),('Prazo','o que falta e até quando')]:
    d.rounded_rectangle((90,y,W-90,y+250),32,fill=SUP); d.text((140,y+48),a,font=font(72,600),fill=FLO); d.text((140,y+150),b,font=font(38),fill=AP); y+=290
im.save('telas/t09b.png')
