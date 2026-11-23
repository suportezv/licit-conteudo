from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249); AL=(196,92,38)
W,H=1080,1920
def novo(): im=Image.new('RGBA',(W,H),(0,0,0,0)); return im,ImageDraw.Draw(im)
def pill(d,cx,cy,t,f,fg=GRAF,bg=LIM,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
im,d=novo(); pill(d,W/2,1310,'Vencida há três dias.',font(74,600)); im.save('ov/o02.png')
im,d=novo(); d.rounded_rectangle((60,1250,700,1390),28,fill=(16,18,24,230)); d.text((100,1272),'Dona Norma',font=font(52,600),fill=BR); d.text((100,1336),'pregoeira',font=font(34),fill=LIM); im.save('ov/o03.png')
im,d=novo(); pill(d,W/2,1330,'Faltou alguém avisar antes.',font(62,600)); im.save('ov/o05.png')
im,d=novo(); d.rounded_rectangle((60,960,W-60,1460),36,fill=(16,18,24,240))
d.text((110,996),'Prefeitura de Bocaiúva/MG',font=font(40),fill=LIM); d.text((110,1060),'Material de limpeza',font=font(60,600),fill=BR)
d.text((110,1134),'para as secretarias municipais',font=font(36),fill=(200,206,214)); d.text((110,1200),'R$ 669.575',font=font(96,600),fill=BR)
d.text((110,1330),'Proposta até 02/12/2026',font=font(40),fill=BR); d.text((110,1394),'Fonte: PNCP',font=font(30),fill=(150,158,170)); im.save('ov/o08.png')
DOCS=[('Certidão federal','válida até 14/03/2027','Em dia',False),('Certidão trabalhista','válida até 02/02/2027','Em dia',False),('Certidão do FGTS','vence em 3 dias','Vence antes da entrega',True)]
def docs(n,full=True):
    if full:
        im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im); pill(d,W/2,330,'Documentos da empresa',font(56,600)); y=500; x0,x1=90,W-90; hh=260; fs=(56,36,34)
    else:
        im=Image.new('RGB',(1024,768),GRAF); d=ImageDraw.Draw(im); d.text((40,28),'Documentos da empresa',font=font(44,600),fill=BR); y=110; x0,x1=40,984; hh=196; fs=(46,30,28)
    for a,b,c,al in DOCS[:n]:
        d.rounded_rectangle((x0,y,x1,y+hh),28,fill=SUP,outline=AL if al else None,width=6 if al else 0)
        d.text((x0+44,y+hh*0.14),a,font=font(fs[0],600),fill=FLO); d.text((x0+44,y+hh*0.48),b,font=font(fs[1]),fill=AP)
        f=font(fs[2],600); tw=d.textlength(c,font=f); px=x0+44
        d.rounded_rectangle((px,y+hh*0.70,px+tw+40,y+hh*0.70+fs[2]+18),(fs[2]+18)//2,fill=AL if al else (220,236,226)); d.text((px+20,y+hh*0.70+7),c,font=f,fill=BR if al else FLO)
        y+=hh+(30 if full else 18)
    return im
for n in range(4): docs(n).save(f'telas/tdoc_{n}.png')
docs(3,False).save('telas/m_docs.png')
im=Image.new('RGB',(1024,768),SUP); d=ImageDraw.Draw(im)
d.rectangle((0,0,1024,90),fill=FLO); d.text((40,26),'Aviso de contratação',font=font(36,600),fill=BR); d.text((984,32),'PNCP',font=font(28,600),fill=LIM,anchor='ra')
d.text((40,130),'Prefeitura de Bocaiúva/MG',font=font(34),fill=AP); d.text((40,186),'Material de limpeza',font=font(64,600),fill=GRAF)
d.text((40,270),'para as secretarias municipais',font=font(32),fill=AP); d.text((40,350),'R$ 669.575',font=font(110,600),fill=FLO)
d.rounded_rectangle((40,520,984,620),18,fill=BR,outline=(215,220,228),width=2); d.text((70,546),'Proposta até 02/12/2026',font=font(40,600),fill=GRAF)
d.text((40,670),'Publicado no PNCP',font=font(34),fill=AP); im.save('telas/m_pncp.png')
