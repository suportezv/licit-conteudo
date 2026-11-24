import json,subprocess,os
GAP=0.12; FPS=30; R1='../storyboard-r1/'
X=['ffmpeg','-nostdin','-v','error','-y']
os.makedirs('tmp',exist_ok=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
def Wd(k): return json.load(open(f'omni/{k}.json'))
def anc(k,word,fim=False):
    for w in Wd(k):
        if w['text'].lower().strip('.,:?!').startswith(word): return w['end' if fim else 'start']
    raise SystemExit(f'ancora {k} {word}')
def nivela(src,dst,ss=None,t=None):
    cut=(['-ss',f'{ss:.3f}','-t',f'{t:.3f}'] if ss is not None else [])
    subprocess.run(X+cut+['-i',src,'-ar','48000','-ac','1','tmp/x.wav'],timeout=60)
    m=subprocess.run(['ffmpeg','-nostdin','-i','tmp/x.wav','-af','volumedetect','-f','null','-'],capture_output=True,text=True,timeout=60).stderr
    mean=float(m.split('mean_volume:')[1].split('dB')[0])
    subprocess.run(X+['-i','tmp/x.wav','-af',f'volume={-21-mean:.2f}dB,alimiter=limit=0.8,afade=t=in:d=0.03',dst],timeout=60)
SEG=['c01','c02','c03','c04','c05','c06','c07','c08']
PRE={'c01':0.5,'c08':0.25}; POS={'c01':0.4,'c02':0.5,'c03':0.5,'c04':0.3,'c05':0.4,'c08':1.25}
t=0.0; A={}; words=[]
for k in SEG:
    w=Wd(k); a=max(w[0]['start']-PRE.get(k,0.22),0); b=min(w[-1]['end']+POS.get(k,0.22),dur(f'omni/{k}.mp4'))
    nivela(f'omni/{k}_norma.mp3',f'tmp/{k}.wav',a,b-a)
    A[k]=(t,a,b-a)
    for x in w: words.append((t+x['start']-a,t+x['end']-a,x['text']))
    t+=b-a+GAP+{'c04':1.9,'c07':0.4}.get(k,0)
s=lambda k:A[k][0]; rel=lambda k,word,fim=False:anc(k,word,fim)-A[k][1]
T0=t; LEAD=0.95
subprocess.run(X+['-i','audio/f11.wav','-af','atempo=1.08','tmp/f11a.wav'],timeout=60); nivela('tmp/f11a.wav','tmp/q11.wav')
f11=[(x['text'],x['start']/1.08,x['end']/1.08) for x in json.load(open('audio/f11.json'))]
tw=lambda p,fim=False:[b if fim else a for x,a,b in f11 if x.lower().startswith(p)][0]
A['q11']=(T0+LEAD,0,dur('tmp/q11.wav'))
T_CAMPO=LEAD-0.1; T_DIG=LEAD+tw('cnpj',True); T_PIL=LEAD+tw('teste')-0.05; T_URL=LEAD+f11[-1][2]+0.25; DASS=T_URL+2.3
subprocess.run(['/usr/bin/python3','../assinatura.py','tmp/ass.mp4']+[f'{v:.2f}' for v in (T_CAMPO,T_DIG,T_PIL,T_URL,DASS)],timeout=600)
FIM=T0+DASS
tb=s('c04')+rel('c04','gente',True)+0.3; t5=s('c05'); o5=A['c05'][1]
P=[('c','omni/c01',s('c01'),A['c01'][1],None,0),
   ('c','omni/c02',s('c02'),A['c02'][1],None,0),
   ('c','omni/c03',s('c03'),A['c03'][1],'o03',0.3),
   ('c','omni/c04',s('c04'),A['c04'][1],None,0),
   ('g','t09_0',tb,0,None,0),('g','t09_1',tb+0.4,0,None,0),('g','t09_2',tb+0.8,0,None,0),('g','t09_3',tb+1.2,0,None,0),
   ('c','omni/c05_tela',t5,o5,None,0),
   ('c','omni/c05_tela',t5+rel('c05','sete')+0.6,o5+rel('c05','sete')+0.6,'o05',0.12),
   ('c','omni/c06',s('c06'),A['c06'][1],None,0),
   ('g','tq_1',s('c06')+rel('c06','pergunto')-0.08,0,None,0),
   ('g','tq_2',s('c07')+rel('c07','responde')-0.08,0,None,0),('g','tq_3',s('c07')+rel('c07','eu')-0.08,0,None,0),
   ('c','omni/c08',s('c08'),A['c08'][1],None,0),
   ('a','tmp/ass',T0,0,None,0)]
clips=[]
for i,(tp,src,ini,off,ov,ovt) in enumerate(P):
    fim=P[i+1][2] if i+1<len(P) else FIM
    n=round(fim*FPS)-round(ini*FPS); o=f'tmp/c{i:02d}.mp4'
    enc=['-frames:v',str(n),'-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',o]
    if tp=='g': subprocess.run(X+['-loop','1','-i',f'telas/{src}.png','-vf',f'fps={FPS},format=yuv420p']+enc,timeout=600)
    else:
        base=f"[0:v]fps={FPS},scale=1080:1920:flags=lanczos"+(",crop=iw/1.28:ih/1.28:(iw-iw/1.28)/2:ih*0.06,scale=1080:1920:flags=lanczos" if src.endswith("c03") else "")+(",unsharp=5:5:0.5" if tp=='c' else "")+",setsar=1,tpad=stop_mode=clone:stop_duration=2[v]"
        cmd=X+['-ss',f'{max(off,0):.3f}','-i',f'{src}.mp4']
        if ov:
            cmd+=['-loop','1','-i',f'ov/{ov}.png']; fc=base+f";[1:v]format=rgba,fade=t=in:st={ovt:.2f}:d=0.18:alpha=1[o];[v][o]overlay=0:0:enable='gte(t,{ovt:.2f})'[x]"
        else: fc=base+";[v]null[x]"
        subprocess.run(cmd+['-filter_complex',fc,'-map','[x]']+enc,timeout=600)
    clips.append(o)
open('tmp/l.txt','w').write(''.join(f"file '{os.path.basename(c)}'\n" for c in clips))
subprocess.run(X+['-f','concat','-safe','0','-i','tmp/l.txt','-c','copy','tmp/v.mp4'],timeout=300)
def ts(x): h=int(x//3600); m=int(x%3600//60); return f"{h}:{m:02d}:{x%60:05.2f}"
sub=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: L,Sora,84,&H00FFFFFF,&H00FFFFFF,&H00181210,&H80000000,1,0,0,0,100,100,-1,0,1,7,2,2,60,60,300,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
DEST={'sábado.','cnpj','horário.'}
FIX={'Proficio':'Profissio','proficio':'Profissio','Licite':'Licit','licite':'Licit','1.250.000':'1,25 milhão','80':'oitenta','40':'quarenta'}
blk=[]
def flush():
    global blk
    if not blk: return
    a=blk[0][0]; b=blk[-1][1]-0.02
    txt=' '.join(('{\\c&H7AF2A8&}'+w+'{\\c&HFFFFFF&}') if w.lower() in DEST else w for _,_,w in blk)
    sub.append(f"Dialogue: 0,{ts(a)},{ts(b)},L,,0,0,0,,{txt}\n"); blk=[]
for a,b,w in words:
    w=FIX.get(w,w)
    if blk and (a-blk[-1][1]>0.35 or len(blk)>=3 or sum(len(x[2]) for x in blk)+len(w)>17 or blk[-1][2][-1] in '.?!:'): flush()
    blk.append((a,b,w))
flush(); open('tmp/l.ass','w').write(''.join(sub))
S='/home/user/licit-conteudo/remotion/public/sfx/'; TR='/home/user/licit-conteudo/remotion/public/trilha-tech-warm-33s.mp3'
ev=[('tique',tb+0.4,0.45),('tique',tb+0.8,0.45),('tique',tb+1.2,0.45),('move',s('c03')+0.3,0.3),
    ('sweep',P[9][2]+0.12,0.3),('sweep',P[11][2],0.3),('tique',P[12][2],0.45),('ping',P[13][2],0.4),
    ('swell',T0+0.05,0.35),('typing',T0+T_CAMPO+0.2,0.3),('pop',T0+T_PIL,0.5),('shimmer',T0+T_URL,0.35)]
ks=SEG+['q11']; cmd=X[:]; fc=[]; mix=[]
for i,k in enumerate(ks):
    cmd+=['-i',f'tmp/{k}.wav']; fc.append(f"[{i}]adelay={int(A[k][0]*1000)}:all=1[a{i}]"); mix.append(f'[a{i}]')
n=len(ks)
for j,(nm,tt,vol) in enumerate(ev):
    cmd+=['-i',S+nm+'.mp3']; fc.append(f"[{n+j}]volume={vol},adelay={int(tt*1000)}:all=1[e{j}]"); mix.append(f'[e{j}]')
cmd+=['-stream_loop','-1','-i',TR]; mi=n+len(ev)
fc.append(f"[{mi}]volume=0.09,atrim=0:{FIM},afade=t=in:d=1.5,afade=t=out:st={FIM-1.5}:d=1.5[m]"); mix.append('[m]')
fc.append(''.join(mix)+f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{FIM},loudnorm=I=-14.6:TP=-1.5:LRA=11,alimiter=limit=0.84[o]")
subprocess.run(cmd+['-filter_complex',';'.join(fc),'-map','[o]','-ar','48000','tmp/a.wav'],timeout=300)
OUT='Licit_Ad05_Claudia_v2.mp4'
subprocess.run(X+['-i','tmp/v.mp4','-i','tmp/a.wav','-vf',"ass=tmp/l.ass:fontsdir=/home/user/licit-conteudo/assets/fonts",'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],timeout=900)
print('dur',dur(OUT),[(p[1].split('/')[-1],round(p[2],2)) for p in P])
