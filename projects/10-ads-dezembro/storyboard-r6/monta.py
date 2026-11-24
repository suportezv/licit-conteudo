# Anuncio 6 "Quantos voce abriu?": motion em PIL, narracao do Juliano, assinatura padrao do pack.
import json,subprocess,os,math
from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'; FPS=30; W,H=1080,1920
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249); AL=(196,92,38); CEL=(30,33,42)
X=['ffmpeg','-nostdin','-v','error','-y']; os.makedirs('tmp',exist_ok=True)
_f={}
def font(s,w=500):
    if (s,w) not in _f:
        f=ImageFont.truetype(F,s)
        try: f.set_variation_by_axes([w])
        except Exception: pass
        _f[(s,w)]=f
    return _f[(s,w)]
cl=lambda x:min(max(x,0),1); ease=lambda x:1-(1-cl(x))**3
def back(x,s=1.7): x=cl(x)-1; return x*x*((s+1)*x+s)+1
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
def nivela(src,dst):
    subprocess.run(X+['-i',src,'-ar','48000','-ac','1','tmp/x.wav'],timeout=60)
    m=subprocess.run(['ffmpeg','-nostdin','-i','tmp/x.wav','-af','volumedetect','-f','null','-'],capture_output=True,text=True,timeout=60).stderr
    mean=float(m.split('mean_volume:')[1].split('dB')[0])
    subprocess.run(X+['-i','tmp/x.wav','-af',f'volume={-21-mean:.2f}dB,alimiter=limit=0.8',dst],timeout=60)
SEG=['n1','n2','n3','n4']; GAP=0.3; S={}; words=[]; t=0.35
Wd=lambda k:json.load(open(f'audio/{k}.json'))
for k in SEG:
    nivela(f'audio/{k}.mp3',f'tmp/{k}.wav'); S[k]=t
    for x in Wd(k): words.append((t+x['start'],t+x['end'],x['text']))
    t+=dur(f'tmp/{k}.wav')+GAP
def at(k,word,fim=False,occ=1):
    n=0
    for w in Wd(k):
        if w['text'].lower().strip('.,:?!').startswith(word):
            n+=1
            if n==occ: return S[k]+w['end' if fim else 'start']
    raise SystemExit(f'ancora {k} {word}')
T0=t; LEAD=0.95
nivela('audio/n5.mp3','tmp/n5.wav'); f5=Wd('n5'); tw=lambda p,fim=False:[x['end' if fim else 'start'] for x in f5 if x['text'].lower().startswith(p)][0]
for x in f5: words.append((T0+LEAD+x['start'],T0+LEAD+x['end'],x['text']))
T_CAMPO=LEAD-0.1; T_DIG=LEAD+tw('cnpj',True); T_PIL=LEAD+tw('teste')-0.05; T_URL=LEAD+f5[-1]['end']+0.25; DASS=T_URL+2.3
subprocess.run(['/usr/bin/python3','../assinatura.py','tmp/ass.mp4']+[f'{v:.2f}' for v in (T_CAMPO,T_DIG,T_PIL,T_URL,DASS)],timeout=600)
FIM=T0+DASS
# ---------- ancoras
tQ=at('n1','quantos'); tB=S['n2']; tDep=at('n2','depois'); t80=at('n2','80'); tLin=at('n2','uma'); tC=S['n3']-0.1; tVal=at('n3','r$'); tD=S['n4']-0.1
tLag=at('n3','lagoa'); tMin=at('n3','minas'); tPg=at('n4','página')-0.1
tCn=at('n4','você'); tCnF=at('n4','cnpj',True); tVe=at('n4','vê'); tEx=at('n4','cada')-0.1; tDoc=at('n4','documento')-0.15
grade=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(grade)
for x in range(0,W,90): g.line((x,0,x,H),fill=(255,255,255,9))
for y in range(0,H,90): g.line((0,y,W,y),fill=(255,255,255,9))
def fundo(c=GRAF):
    im=Image.new('RGB',(W,H),c); im.paste(grade,(0,0),grade); return im
def pill(d,cx,cy,t,f,fg=GRAF,bg=LIM,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
AV=['Pavimentação de ruas','Reforma de escola municipal','Construção de unidade de saúde','Manutenção predial','Ampliação de creche','Drenagem urbana','Reforma de quadra esportiva','Iluminação pública','Construção de praça','Reforma de posto de saúde','Rede de água','Cobertura de ginásio','Calçamento','Muro de contenção']
TN=[0.3+0.36*i for i in range(40) if 0.3+0.36*i<tB-0.2]
def cenaA(t):
    im=fundo(); d=ImageDraw.Draw(im)
    px0,py0,px1,py1=200,430,880,1640
    d.rounded_rectangle((px0-14,py0-14,px1+14,py1+14),70,fill=(52,56,68)); d.rounded_rectangle((px0,py0,px1,py1),58,fill=CEL)
    d.rounded_rectangle((W/2-80,py0+22,W/2+80,py0+50),14,fill=(52,56,68))
    n=sum(1 for x in TN if t>=x)
    lay=Image.new('RGB',(px1-px0,py1-py0-90),CEL); ld=ImageDraw.Draw(lay)
    for i,x in enumerate(TN):
        if t<x: continue
        pos=sum(1 for z in TN if x<z<=t)          # quantos chegaram depois
        ult=max([z for z in TN if z<=t]); k=ease((t-ult)/0.25)
        y=20+(pos-(1-k) if x!=ult else 0)*172
        if x==ult: y=20-170*(1-back((t-x)/0.3))
        if y>1150: continue
        ld.rounded_rectangle((24,y,656,y+152),28,fill=SUP)
        ld.rounded_rectangle((46,y+26,106,y+86),16,fill=FLO); ld.text((76,y+56),'!',font=font(40,600),fill=LIM,anchor='mm')
        ld.text((128,y+24),'Novo aviso de licitação',font=font(28),fill=AP); ld.text((128,y+66),AV[i%len(AV)],font=font(34,600),fill=GRAF)
        ld.text((634,y+24),'agora',font=font(24),fill=(150,158,170),anchor='ra')
    im.paste(lay,(px0,py0+70))
    k=back((t-0.15)/0.4)
    if k>0:
        d.text((W/2,250),str(n),font=font(int(150*max(k,0.1)),600),fill=BR,anchor='mm'); d.text((W/2,350),'avisos esta semana',font=font(38),fill=(200,206,214),anchor='mm')
    k=back((t-tQ)/0.35)
    if t>=tQ: pill(d,W/2,1760+40*(1-k),'0 abertos',font(64,600))
    return im
def pagina(d,x0,y0,x1,y1,scroll,hl):
    d.rounded_rectangle((x0,y0,x1,y1),18,fill=BR)
    d.rectangle((x0,y0,x1,y0+110),fill=(232,235,240)); d.text((x0+50,y0+34),'EDITAL DE LICITAÇÃO',font=font(34,600),fill=GRAF)
    yy=y0+150-(scroll%46); i=int(scroll//46)
    while yy<y1-40:
        if yy>y0+125:
            wl=(x1-x0-100)*(0.55+0.45*abs(math.sin(i*1.7)))
            if i%9==0: d.rectangle((x0+50,yy,x0+50+260,yy+16),fill=(120,128,140))
            else: d.rectangle((x0+50,yy,x0+50+wl,yy+12),fill=(205,210,218))
        yy+=46; i+=1
    if hl>0:
        ym=(y0+y1)/2+40; d.rectangle((x0+30,ym-34,x0+30+(x1-x0-60)*hl,ym+34),fill=LIM)
        if hl>0.9: d.text((x0+56,ym),'Atestado de capacidade técnica',font=font(38 if x1-x0>760 else 32,600),fill=GRAF,anchor='lm')
def cenaB(t):
    im=fundo(); d=ImageDraw.Draw(im)
    k=ease((t-tDep+0.15)/0.45)
    if k<1:                                            # o aviso cresce no centro
        s=ease((t-tB)/(tDep-tB)); w=632+240*s; h=152+60*s; cy=760-60*s
        d.rounded_rectangle((W/2-w/2,cy-h/2,W/2+w/2,cy+h/2),30,fill=SUP)
        d.text((W/2-w/2+50,cy-44),'Novo aviso de licitação',font=font(int(28+10*s)),fill=AP); d.text((W/2-w/2+50,cy+2),'Ampliação de creche',font=font(int(34+14*s),600),fill=GRAF)
    if k>0:
        sc=0 if t<t80 else 2600*ease((t-t80)/(tLin-t80)) if t<tLin else 2600
        pg=1 if t<t80 else min(80,1+int(79*cl((t-t80)/max(tLin-t80-0.1,0.3))))
        y0=360+H*(1-k)*0.6; z=ease((t-tLin)/0.4)
        x0=140-40*z; x1=940+40*z
        pagina(d,x0,y0,x1,y0+1180,sc,ease((t-tLin-0.1)/0.35) if t>tLin else 0)
        pill(d,W/2,250,f'página {pg} de 80',font(52,600))
    return im
def cenaC(t):
    im=fundo(FLO); d=ImageDraw.Draw(im); k=back((t-tC-0.05)/0.45,1.2)
    pill(d,W/2,470,'Aberta agora',font(52,600))
    y=640+80*(1-k)
    d.rounded_rectangle((70,y,W-70,y+760),44,fill=GRAF)
    ka=ease((t-tLag)/0.35); kb=ease((t-tMin-0.5)/0.35)
    if ka>0: d.text((130+40*(1-ka),y+60),'Prefeitura de Lagoa da Prata/MG',font=font(42),fill=LIM)
    if kb>0: d.text((130+40*(1-kb),y+140),'Ampliação da creche',font=font(70,600),fill=BR); d.text((130+40*(1-kb),y+232),'Risoleta Neves',font=font(52,600),fill=BR)
    v=int(660837*ease((t-tVal+0.1)/0.7)) if t>tVal-0.1 else 0
    if v: d.text((130,y+350),'R$ '+f'{v:,}'.replace(',','.'),font=font(118,600),fill=BR)
    k2=ease((t-tVal-0.6)/0.35)
    if k2>0:
        d.text((130,y+530),'Proposta até 29/12/2026',font=font(46),fill=(255,255,255)); d.text((130,y+620),'Fonte: PNCP',font=font(34),fill=(150,158,170))
    return im
CNPJ='12.345.678/0001-90'
LST=[('Prefeitura de Lagoa da Prata/MG','Ampliação de creche','R$ 660.837','até 29/12'),('Prefeitura de Sete Lagoas/MG','Reforma do prédio da prefeitura','R$ 1.250.661','até 28/12'),('Prefeitura de Capão do Leão/RS','Reforma de quadra de escola','R$ 993.310','até 30/12')]
def cenaD(t):
    im=fundo(); d=ImageDraw.Draw(im); pill(d,W/2,190,'profissiolicit.ai',font(44,600))
    if t<tEx:
        d.rounded_rectangle((60,290,W-60,1500),40,fill=SUP)
        d.text((110,350),'Licitações para sua empresa.',font=font(50,600),fill=GRAF); d.text((110,428),'Digite o CNPJ',font=font(32),fill=AP)
        d.rounded_rectangle((110,480,W-110,580),20,outline=FLO,width=4,fill=BR)
        n=int(len(CNPJ)*cl((t-tCn)/max(tCnF-tCn,0.4))); d.text((144,504),CNPJ[:n]+('|' if n<len(CNPJ) and int(t*4)%2 else ''),font=font(42),fill=GRAF)
        pr=cl((t-tCnF)/0.15)-cl((t-tCnF-0.15)/0.2); d.rounded_rectangle((110+6*pr,610+4*pr,W-110-6*pr,710-4*pr),20,fill=FLO); d.text((W/2,660),'Descobrir oportunidades grátis',font=font(36,600),fill=BR,anchor='mm')
        y=760
        for i,(a,b,c,e) in enumerate(LST):
            k=back((t-tVe-0.3*i)/0.35,1.2)
            if t>=tVe+0.3*i:
                yy=y+50*(1-k); d.rounded_rectangle((110,yy,W-110,yy+205),20,fill=BR,outline=(220,224,230),width=2)
                d.text((144,yy+24),a,font=font(28),fill=AP); d.text((144,yy+66),b,font=font(40,600),fill=GRAF); d.text((144,yy+132),f'{c}  ·  {e}',font=font(32),fill=FLO); d.text((W-144,yy+24),'PNCP',font=font(24,600),fill=(150,158,170),anchor='ra')
            y+=225
    else:
        k=back((t-tEx)/0.4,1.2); y=420+70*(1-k)
        d.rounded_rectangle((90,y,W-90,y+330),32,fill=SUP); d.text((140,y+44),'Exigência do edital',font=font(34),fill=AP)
        d.text((140,y+100),'Atestado de',font=font(58,600),fill=FLO); d.text((140,y+172),'capacidade técnica',font=font(58,600),fill=FLO)
        f=font(34,600); tx='Edital, p. 14'; wv=d.textlength(tx,font=f); kp=back((t-tPg)/0.3)
        if t>=tPg: d.rounded_rectangle((140,y+254+8*(1-kp),140+wv+48,y+312+8*(1-kp)),29,fill=LIM); d.text((164,y+263+8*(1-kp)),tx,font=f,fill=GRAF)
        if tPg<=t<tDoc+0.35:
            kk=back((t-tPg-0.1)/0.4,1.2)-ease((t-tDoc)/0.35); py=820+90*(1-kk)+(900*ease((t-tDoc)/0.35))
            pagina(d,170,py,W-170,py+640,640,ease((t-tPg-0.35)/0.35))
        DOCS=[('Certidão federal','válida até 14/03/2027','Em dia',False),('Certidão do FGTS','vence em 3 dias','Vence antes da entrega',True)]
        for i,(a,b,c,al) in enumerate(DOCS):
            tt=tDoc+0.35*i
            if t<tt: continue
            k=back((t-tt)/0.4,1.2); yy=820+300*i+70*(1-k)
            d.rounded_rectangle((90,yy,W-90,yy+260),32,fill=SUP,outline=AL if al else None,width=6 if al else 0)
            d.text((140,yy+36),a,font=font(56,600),fill=FLO); d.text((140,yy+120),b,font=font(36),fill=AP)
            f=font(32,600); wv=d.textlength(c,font=f); d.rounded_rectangle((140,yy+182,140+wv+44,yy+234),26,fill=AL if al else (220,236,226)); d.text((162,yy+190),c,font=f,fill=BR if al else FLO)
    return im
CEN=[(0,cenaA),(tB,cenaB),(tC,cenaC),(tD,cenaD)]
p=subprocess.Popen(X+['-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','tmp/corpo.mp4'],stdin=subprocess.PIPE)
N=round(T0*FPS)
for n in range(N):
    t=n/FPS; i=max(j for j,(a,_) in enumerate(CEN) if t>=a); a,fn=CEN[i]; im=fn(t)
    if i>0 and t-a<0.4:                                # quem entra sobe por cima; quem sai recua e escurece
        k=ease((t-a)/0.4); ant=CEN[i-1][1](t)
        s=1-0.06*k; an=ant.resize((int(W*s),int(H*s)),Image.BILINEAR); base=Image.new('RGB',(W,H),(0,0,0)); base.paste(an,((W-an.width)//2,(H-an.height)//2))
        base=Image.blend(base,Image.new('RGB',(W,H),(0,0,0)),0.55*k); base.paste(im,(0,int(H*(1-k))))
        ImageDraw.Draw(base,'RGBA').rectangle((0,int(H*(1-k))-40,W,int(H*(1-k))),fill=(0,0,0,70)); im=base
    p.stdin.write(im.tobytes())
p.stdin.close(); p.wait()
open('tmp/l.txt','w').write("file 'corpo.mp4'\nfile 'ass.mp4'\n")
subprocess.run(X+['-f','concat','-safe','0','-i','tmp/l.txt','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','tmp/v.mp4'],timeout=600)
def ts(x): h=int(x//3600); m=int(x%3600//60); return f"{h}:{m:02d}:{x%60:05.2f}"
sub=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: L,Sora,64,&H00FFFFFF,&H00FFFFFF,&H00181210,&H80000000,1,0,0,0,100,100,-1,0,1,6,2,2,60,60,110,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
FIX={'Proficio':'Profissio','Licite,':'Licit,','Licite':'Licit','80':'oitenta','660.000':'660 mil'}
blk=[]
def flush():
    global blk
    if not blk: return
    sub.append(f"Dialogue: 0,{ts(blk[0][0])},{ts(blk[-1][1]-0.02)},L,,0,0,0,,{' '.join(w for _,_,w in blk)}\n"); blk=[]
for a,b,w in words:
    w=FIX.get(w,w)
    if blk and (a-blk[-1][1]>0.35 or len(blk)>=4 or sum(len(x[2]) for x in blk)+len(w)>22 or blk[-1][2][-1] in '.?!:'): flush()
    blk.append((a,b,w))
flush(); open('tmp/l.ass','w').write(''.join(sub))
Sx=R+'remotion/public/sfx/'; TR=R+'remotion/public/trilha-tech-warm-33s.mp3'
ev=[('pop',x,0.22) for x in TN]+[('ping',tQ,0.4),('sweep',tB,0.3),('sweep',tDep-0.15,0.3),('typing',t80,0.25),('pop',tLin+0.1,0.45),('sweep',tC,0.3),('ping',tVal+0.6,0.4),('sweep',tD,0.3),('typing',tCn,0.25)]
ev+=[('tique',tVe+0.3*i,0.45) for i in range(3)]+[('move',tEx,0.3),('pop',tPg,0.4),('tique',tLag,0.4),('tique',tMin+0.5,0.4),('tique',tDoc,0.45),('tique',tDoc+0.35,0.45),('swell',T0+0.05,0.35),('typing',T0+T_CAMPO+0.2,0.3),('pop',T0+T_PIL,0.5),('shimmer',T0+T_URL,0.35)]
ev=[e for e in ev if os.path.exists(Sx+e[0]+'.mp3')]
cmd=X[:]; fc=[]; mix=[]
for i,k in enumerate(SEG+['n5']):
    cmd+=['-i',f'tmp/{k}.wav']; fc.append(f"[{i}]adelay={int((S[k] if k in S else T0+LEAD)*1000)}:all=1[a{i}]"); mix.append(f'[a{i}]')
n=len(SEG)+1
for j,(nm,tt,vol) in enumerate(ev):
    cmd+=['-i',Sx+nm+'.mp3']; fc.append(f"[{n+j}]volume={vol},adelay={int(max(tt,0)*1000)}:all=1[e{j}]"); mix.append(f'[e{j}]')
cmd+=['-stream_loop','-1','-i',TR]; mi=n+len(ev)
fc.append(f"[{mi}]volume=0.10,atrim=0:{FIM},afade=t=in:d=1.0,afade=t=out:st={FIM-1.5}:d=1.5[m]"); mix.append('[m]')
fc.append(''.join(mix)+f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{FIM},loudnorm=I=-14.6:TP=-1.5:LRA=11,alimiter=limit=0.84[o]")
subprocess.run(cmd+['-filter_complex',';'.join(fc),'-map','[o]','-ar','48000','tmp/a.wav'],timeout=300)
OUT='Licit_Ad06_TelaEVoz_v1.mp4'
subprocess.run(X+['-i','tmp/v.mp4','-i','tmp/a.wav','-vf',f"ass=tmp/l.ass:fontsdir={R}assets/fonts",'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],timeout=900)
print('dur',dur(OUT),round(T0,2),[round(x,2) for x in (tQ,tB,tDep,t80,tLin,tC,tVal,tD,tCn,tVe,tEx,tDoc)])
