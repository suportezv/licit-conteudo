from PIL import Image, ImageDraw, ImageFont
import os
R='/home/user/licit-conteudo/'
F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249)
W,H=1024,1536
def wrap(d,t,f,mw):
    out=[]
    for par in t.split('\n'):
        l=''
        for w in par.split():
            n=(l+' '+w).strip()
            if d.textlength(n,font=f)<=mw: l=n
            else: out.append(l); l=w
        out.append(l)
    return out
# q09: tela do produto (marcador para a captura real)
im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im)
d.rounded_rectangle((70,170,W-70,H-170),36,fill=SUP)
d.text((120,230),'Licitações para sua empresa.',font=font(44,600),fill=GRAF)
d.text((120,300),'Digite o CNPJ',font=font(30),fill=AP)
d.rounded_rectangle((120,350,W-120,440),18,outline=FLO,width=4,fill=BR)
d.text((150,372),'00.000.000/0001-00',font=font(38),fill=GRAF)
d.rounded_rectangle((120,470,W-120,560),18,fill=FLO)
d.text((W/2,515),'Descobrir oportunidades grátis',font=font(32,600),fill=BR,anchor='mm')
y=620
for i in range(4):
    d.rounded_rectangle((120,y,W-120,y+150),18,fill=BR,outline=(220,224,230),width=2)
    d.text((150,y+22),'[Órgão]',font=font(26),fill=AP)
    d.text((150,y+60),'[Objeto da compra]',font=font(32,600),fill=GRAF)
    d.text((150,y+104),'[Valor]   ·   proposta até [data]',font=font(26),fill=FLO)
    y+=172
d.text((W/2,H-110),'MARCADOR: entra a captura real da busca',font=font(26),fill=LIM,anchor='mm')
im.save('q09.png')
# q11: fecho
im=Image.new('RGB',(W,H),FLO); d=ImageDraw.Draw(im)
lg=Image.open(R+'assets/marca/logos/licit-estrela-branco.png').convert('RGBA')
lw=520; lg=lg.resize((lw,int(lg.height*lw/lg.width)))
im.paste(lg,((W-lw)//2,430),lg)
d.rounded_rectangle((120,760,W-120,880),24,fill=BR)
d.text((W/2,820),'Digite o CNPJ',font=font(46),fill=AP,anchor='mm')
d.rounded_rectangle((120,930,W-120,1070),70,fill=LIM)
d.text((W/2,1000),'Teste grátis, sem cartão',font=font(54,600),fill=GRAF,anchor='mm')
d.text((W/2,1160),'profissiolicit.ai',font=font(44),fill=BR,anchor='mm')
im.save('q11.png')
# cartão de prova sobre o q05
im=Image.open('q05.png').convert('RGB'); d=ImageDraw.Draw(im,'RGBA')
d.rounded_rectangle((70,960,W-70,1330),30,fill=(16,18,24,235))
d.text((110,990),'[Prefeitura de cidade/UF]',font=font(32),fill=LIM)
d.text((110,1040),'[Objeto da compra]',font=font(46,600),fill=BR)
d.text((110,1110),'[R$ valor]',font=font(64,600),fill=BR)
d.text((110,1200),'Proposta até [data]',font=font(34),fill=BR)
d.text((110,1262),'Fonte: PNCP',font=font(28),fill=(170,178,190))
im.save('q05_cartao.png')
Q=[('01','0 a 1,5 s','Close frontal, luz do monitor','“Eu tenho [R$ valor] para comprar [objeto].”','q01.png'),
('02','1,5 a 3 s','Olha para a lente. Texto: Duas.','“Sabe quantas empresas vieram vender? Duas.”','q02.png'),
('03','3 a 7 s','Plano médio, serve o café','“Prazer, Norma. Pregoeira há dezenove anos. Com esse nome, eu ia ser o quê?”','q03.png'),
('04','7 a 10 s','Por cima do ombro, a tela dela','“[Prefeitura de cidade/UF], [objeto], [valor].”','q04.png'),
('05','10 a 14 s','Detalhe de lado + cartão de prova','“Proposta até [data]. Está publicado no PNCP desde [data].”','q05_cartao.png'),
('06','14 a 17 s','Perfil na janela, óculos na mão','“E eu não posso te ligar.”','q06.png'),
('07','17 a 20 s','Três quartos, mãos abertas','“Se eu aviso um, tenho que avisar todos. Então eu publico, e torço para você ver.”','q07.png'),
('08','20 a 23 s','Vira o monitor para a câmera','“Por isso eu gostei da Profissio Licit.”','q08.png'),
('09','23 a 29 s','Tela cheia: CNPJ digitado, lista','“Você digita o CNPJ e ela mostra o que o governo quer comprar da sua empresa. Depois ajuda no resto: edital, documento, prazo.”','q09.png'),
('10','29 a 33 s','Close frontal, meio sorriso','“Não garanto que você ganha. Garanto que quem não aparece não ganha.”','q10.png'),
('11','33 a 36 s','Fecho com a assinatura','“Digita o CNPJ. Teste grátis, sem cartão.”','q11.png')]
tw,th=420,630; cols=4; pad=36; capH=250
rows=-(-len(Q)//cols)
S=Image.new('RGB',(pad+cols*(tw+pad), 150+rows*(th+capH+pad)),GRAF); d=ImageDraw.Draw(S)
d.text((pad,40),'Roteiro 1  ·  Dona Norma: “Vieram duas”  ·  36 s',font=font(44,600),fill=BR)
for i,(n,t,img,fala,fn) in enumerate(Q):
    x=pad+(i%cols)*(tw+pad); y=150+(i//cols)*(th+capH+pad)
    S.paste(Image.open(fn).convert('RGB').resize((tw,th)),(x,y))
    d.rounded_rectangle((x+12,y+12,x+92,y+62),12,fill=LIM); d.text((x+52,y+37),n,font=font(28,600),fill=GRAF,anchor='mm')
    d.text((x,y+th+12),t,font=font(24,600),fill=LIM)
    d.text((x+150,y+th+12),'',font=font(22),fill=BR)
    yy=y+th+46
    for l in wrap(d,img,font(22),tw): d.text((x,yy),l,font=font(22),fill=(170,178,190)); yy+=28
    yy+=6
    for l in wrap(d,fala,font(23),tw): d.text((x,yy),l,font=font(23),fill=BR); yy+=30
S.save('STORYBOARD-R1.png'); S.convert('RGB').save('STORYBOARD-R1.jpg',quality=88)
T=S.copy(); T.thumbnail((1800,1800)); T.save('/tmp/claude-0/sb.jpg',quality=80)
