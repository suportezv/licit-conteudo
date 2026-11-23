# Assinatura padrao do pack de anuncios (1080x1920, 30 fps).
# Uso: assinatura.py saida.mp4 t_campo t_fim_digitacao t_pilula t_url duracao
#   t_campo: quando o campo do CNPJ sobe e comeca a digitar (inicio de "Digita o CNPJ")
#   t_pilula: quando entra "Teste gratis, sem cartao";  t_url: quando entra o endereco
import sys,subprocess,math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'
out=sys.argv[1]; T_CAMPO,T_DIG,T_PIL,T_URL,DUR=[float(x) for x in sys.argv[2:7]]
FPS=30; W,H=1080,1920
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110)
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
ease=lambda x:1-(1-min(max(x,0),1))**3
def back(x,s=1.7):
    x=min(max(x,0),1)-1; return x*x*((s+1)*x+s)+1
L=Image.open(R+'assets/marca/logos/licit-estrela-branco.png').convert('RGBA').crop((198,198,3001,959))   # estrela + Licit
LW=640; sc=LW/L.width; L=L.resize((LW,int(L.height*sc)),Image.LANCZOS); LH=L.height
SX=int((1026-198)*sc); WX=int((1212-198)*sc)            # fim da estrela, inicio da palavra
STAR=L.crop((0,0,SX,LH)); WORD=L.crop((WX,0,LW,LH))
# fundo: grafite com bloco floresta subindo e grade tecnica discreta
grade=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(grade)
for x in range(0,W,90): g.line((x,0,x,H),fill=(255,255,255,10),width=1)
for y in range(0,H,90): g.line((0,y,W,y),fill=(255,255,255,10),width=1)
CNPJ='12.345.678/0001-90'; LY=560
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
for n in range(int(DUR*FPS)):
    t=n/FPS
    im=Image.new('RGB',(W,H),GRAF)
    k=ease(t/0.55)                                         # bloco floresta sobe de baixo
    d=ImageDraw.Draw(im); d.rectangle((0,int(H*(1-k)),W,H),fill=FLO)
    im.paste(grade,(0,0),grade)
    # estrela: chega de longe, subindo, sem girar
    a=back((t-0.10)/0.55); e2=ease((t-0.62)/0.42)          # e2: estrela desliza para a posicao do lockup
    if t>0.10:
        s=0.25+0.75*a if a<1 else 1.0; s=max(s,0.05)
        cx0=W/2; cx1=(W-LW)/2+SX/2; cx=cx0+(cx1-cx0)*e2
        cy=LY+LH/2+(1-ease((t-0.10)/0.55))*260
        st=STAR.resize((max(int(SX*s*(1.35-0.35*e2)),2),max(int(LH*s*(1.35-0.35*e2)),2)),Image.LANCZOS)
        al=int(255*min(max((t-0.10)/0.2,0),1)); st.putalpha(st.getchannel('A').point(lambda v:v*al//255))
        im.paste(st,(int(cx-st.width/2),int(cy-st.height/2)),st)
    # palavra Licit: revela da esquerda para a direita
    if e2>0:
        wv=int(WORD.width*ease((t-0.70)/0.45))
        if wv>0:
            wd=WORD.crop((0,0,wv,LH)); im.paste(wd,(int((W-LW)/2+WX),LY),wd)
    d=ImageDraw.Draw(im,'RGBA')
    # assinatura
    k=ease((t-1.05)/0.4)
    if k>0: d.text((W/2,LY+LH+70+20*(1-k)),'Toda a sua operação de licitações',font=font(40),fill=(255,255,255,int(215*k)),anchor='mm')
    # campo do CNPJ
    k=ease((t-T_CAMPO)/0.35)
    if k>0:
        y=1010+60*(1-k); al=int(255*k)
        d.text((150,y-58),'CNPJ da sua empresa',font=font(32),fill=(255,255,255,int(190*k)))
        d.rounded_rectangle((130,y,W-130,y+140),30,fill=(255,255,255,al))
        nchar=int(len(CNPJ)*min(max((t-T_CAMPO-0.25)/max(T_DIG-T_CAMPO-0.25,0.3),0),1))
        txt=CNPJ[:nchar]; f=font(54)
        d.text((176,y+70),txt if txt else '00.000.000/0000-00',font=f,fill=(16,18,24,al) if txt else (150,158,170,al),anchor='lm')
        if int(t*2.5)%2==0 and nchar<len(CNPJ) and txt: 
            x=176+d.textlength(txt,font=f)+6; d.rectangle((x,y+38,x+4,y+102),fill=(36,61,50,al))
        # lupa
        bx=W-130-140; d.rounded_rectangle((bx+14,y+14,bx+126,y+126),22,fill=(36,61,50,al)); d.ellipse((bx+46,y+44,bx+82,y+80),outline=(168,242,122,al),width=6); d.line((bx+78,y+78,bx+96,y+96),fill=(168,242,122,al),width=7)
    # pilula da oferta
    k=back((t-T_PIL)/0.38,2.2) if t>T_PIL else 0
    if k>0:
        txt='Teste grátis, sem cartão'; f=font(int(60*k),600); wtx=d.textlength(txt,font=f); hh=int(150*k); cy=1300
        d.rounded_rectangle((W/2-wtx/2-60*k,cy-hh/2,W/2+wtx/2+60*k,cy+hh/2),hh//2,fill=LIM+(255,)); d.text((W/2,cy),txt,font=f,fill=GRAF+(255,),anchor='mm')
    k=ease((t-T_PIL-0.35)/0.35)
    if k>0: d.text((W/2,1420+16*(1-k)),'30 dias para usar. Sem pedir cartão.',font=font(36),fill=(255,255,255,int(200*k)),anchor='mm')
    k=ease((t-T_URL)/0.35)
    if k>0: d.text((W/2,1600+16*(1-k)),'profissiolicit.ai',font=font(54,600),fill=(255,255,255,int(255*k)),anchor='mm')
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait(); print(out,DUR)
