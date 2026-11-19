import json,subprocess,os
T=1.15; GAP=0.14; FPS=30
X=['ffmpeg','-nostdin','-v','error','-y']
os.makedirs('tmp',exist_ok=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
def w0(k,word,occ=1):
    n=0
    for w in json.load(open(f'audio/f{k}.json')):
        if w['text'].lower().strip('.,:?!').startswith(word):
            n+=1
            if n==occ: return w['start']/T
    raise SystemExit(f'ancora {k} {word}')
segs=['01','02','03','04','06','07','08','10','11']
t=0.25; A={}; words=[]
for k in segs:
    subprocess.run(X+['-i',f'audio/f{k}.wav','-af',f'atempo={T}',f'tmp/f{k}.wav'],timeout=60)
    A[k]=(t,dur(f'tmp/f{k}.wav'))
    for w in json.load(open(f'audio/f{k}.json')): words.append((t+w['start']/T,t+w['end']/T,w['text']))
    t+=A[k][1]+GAP
FIM=t+1.3
s=lambda k:A[k][0]
# planos: (imagem, inicio)
P=[('t01',0),('t02',s('02')-0.07),('t03',s('03')-0.07),('t04',s('04')-0.07),('t05',s('04')+w0('04','r$')-0.1),
   ('t06',s('06')-0.07),('t07',s('07')-0.07),('t08',s('08')-0.07),('t09',s('08')+w0('08','você')-0.1),('t09b',s('08')+w0('08','depois')-0.1),
   ('t10',s('10')-0.07),('t11',s('11')-0.07)]
clips=[]
for i,(img,ini) in enumerate(P):
    fim=P[i+1][1] if i+1<len(P) else FIM
    n=round(fim*FPS)-round(ini*FPS)
    graf=img in('t09','t09b','t11')
    z0,z1=(1.0,1.03) if graf else ((1.0,1.09) if i%2==0 else (1.09,1.0))
    dx='iw/2-(iw/zoom/2)' if graf else (f'iw/2-(iw/zoom/2)+{(-1)**i*30}*on/{n}')
    vf=f"scale=2160:3840,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='{dx}':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={FPS},format=yuv420p"
    o=f'tmp/c{i:02d}.mp4'
    subprocess.run(X+['-loop','1','-i',f'telas/{img}.png','-vf',vf,'-frames:v',str(n),'-c:v','libx264','-crf','16','-preset','fast',o],timeout=600)
    clips.append(o)
open('tmp/l.txt','w').write(''.join(f"file '{os.path.basename(c)}'\n" for c in clips))
subprocess.run(X+['-f','concat','-safe','0','-i','tmp/l.txt','-c','copy','tmp/v.mp4'],timeout=300)
# legenda em blocos de ate 3 palavras
def ts(x): h=int(x//3600); m=int(x%3600//60); return f"{h}:{m:02d}:{x%60:05.2f}"
sub=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: L,Sora,84,&H00FFFFFF,&H00FFFFFF,&H00181210,&H80000000,1,0,0,0,100,100,-1,0,1,7,2,2,60,60,330,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
DEST={'duas','duas.','ligar','ligar.','cnpj','cnpj.','grátis','grátis,','aparece','aparece,','publicar'}
blk=[]
def flush():
    global blk
    if not blk: return
    a=blk[0][0]; b=blk[-1][1]+0.05
    txt=' '.join(('{\\c&H7AF2A8&}'+w+'{\\c&HFFFFFF&}') if w.lower() in DEST else w for _,_,w in blk)
    sub.append(f"Dialogue: 0,{ts(a)},{ts(b)},L,,0,0,0,,{txt}\n"); blk=[]
FIX={'Proficio':'Profissio','Licite':'Licit','R$':'R$'}
for i,(a,b,w) in enumerate(words):
    w=FIX.get(w,w)
    if blk and (a-blk[-1][1]>0.35 or len(blk)>=3 or sum(len(x[2]) for x in blk)+len(w)>17 or blk[-1][2][-1] in '.?!:'): flush()
    blk.append((a,b,w))
flush()
open('tmp/l.ass','w').write(''.join(sub))
# som
S='/home/user/licit-conteudo/remotion/public/sfx/'; TR='/home/user/licit-conteudo/remotion/public/trilha-tech-warm-33s.mp3'
ev=[('pop',s('02')+w0('02','duas'),0.5),('sweep',P[4][1],0.35),('click',P[3][1]+0.3,0.4),('move',P[7][1]+0.4,0.35),('typing',P[8][1]+0.2,0.35),('tique',P[9][1]+0.3,0.5),('tique',P[9][1]+1.0,0.5),('tique',P[9][1]+1.7,0.5),('shimmer',P[11][1]+0.1,0.4)]
cmd=X[:]; fc=[]; mix=[]
for i,k in enumerate(segs):
    cmd+=['-i',f'tmp/f{k}.wav']; fc.append(f"[{i}]adelay={int(A[k][0]*1000)}:all=1[a{i}]"); mix.append(f'[a{i}]')
n=len(segs)
for j,(nm,tt,vol) in enumerate(ev):
    cmd+=['-i',S+nm+'.mp3']; fc.append(f"[{n+j}]volume={vol},adelay={int(tt*1000)}:all=1[e{j}]"); mix.append(f'[e{j}]')
cmd+=['-stream_loop','-1','-i',TR]; mi=n+len(ev)
fc.append(f"[{mi}]volume=0.10,atrim=0:{FIM},afade=t=in:d=1.5,afade=t=out:st={FIM-1.5}:d=1.5[m]"); mix.append('[m]')
fc.append(''.join(mix)+f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{FIM},loudnorm=I=-14.6:TP=-1.5:LRA=11,alimiter=limit=0.84[o]")
subprocess.run(cmd+['-filter_complex',';'.join(fc),'-map','[o]','-ar','48000','tmp/a.wav'],timeout=300)
OUT='Licit_Ad01_DonaNorma_animatic.mp4'
subprocess.run(X+['-i','tmp/v.mp4','-i','tmp/a.wav','-vf',"ass=tmp/l.ass:fontsdir=/home/user/licit-conteudo/assets/fonts",'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],timeout=900)
print('dur',dur(OUT),[(p,round(i,2)) for p,i in P])
