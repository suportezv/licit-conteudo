from PIL import Image, ImageDraw, ImageFont
import os
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
GRAF=(16,18,24,255); LIM=(168,242,122,255); BR=(255,255,255,255)
W,H=1080,1920; os.makedirs('ov',exist_ok=True)
def novo(): im=Image.new('RGBA',(W,H),(0,0,0,0)); return im,ImageDraw.Draw(im)
def pill(d,cx,cy,t,f,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=LIM); d.text((cx,cy),t,font=f,fill=GRAF,anchor='mm')
im,d=novo(); pill(d,W/2,1290,'Duas.',font(150,600),(70,40)); im.save('ov/o02.png')
im,d=novo(); d.rounded_rectangle((60,1250,700,1390),28,fill=(16,18,24,230)); d.text((100,1272),'Dona Norma',font=font(52,600),fill=BR); d.text((100,1336),'pregoeira',font=font(34),fill=LIM); im.save('ov/o03.png')
im,d=novo(); d.rounded_rectangle((60,960,W-60,1460),36,fill=(16,18,24,240))
d.text((110,996),'Prefeitura de Uberlândia/MG',font=font(40),fill=LIM); d.text((110,1060),'Material de limpeza',font=font(60,600),fill=BR)
d.text((110,1134),'para a rede municipal de ensino',font=font(36),fill=(200,206,214,255)); d.text((110,1200),'R$ 2.783.423',font=font(96,600),fill=BR)
d.text((110,1330),'Proposta até 30/11/2026',font=font(40),fill=BR); d.text((110,1394),'Fonte: PNCP',font=font(30),fill=(150,158,170,255)); im.save('ov/o05.png')
im,d=novo(); pill(d,W/2,1330,'Eu não posso te ligar.',font(70,600)); im.save('ov/o06.png')
