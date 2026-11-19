import json,subprocess,os
T=1.15; GAP=0.14; FPS=30
X=['ffmpeg','-nostdin','-v','error','-y']
os.makedirs('tmp',exist_ok=True)
def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
def w0(k,word):
    for w in json.load(open(f'audio/f{k}.json')):
        if w['text'].lower().strip('.,:?!').startswith(word): return w['start']/T
    raise SystemExit(f'ancora {k} {word}')
segs=['01','02','03','04','06','07','08','10','11']
t=0.0; A={}; words=[]
for k in segs:
    subprocess.run(X+['-i',f'audio/f{k}.wav','-af',f'atempo={T}',f'tmp/f{k}.wav'],timeout=60)
    A[k]=(t,dur(f'tmp/f{k}.wav'))
    for w in json.load(open(f'audio/f{k}.json')): words.append((t+w['start']/T,t+w['end']/T,w['text']))
    t+=A[k][1]+GAP
FIM=t+1.4
s=lambda k:A[k][0]
# planos: (tipo, fonte, inicio, offset na fonte, overlay, overlay a partir de)
P=[('c','q01',0,0,None,0),
   ('c','q02',s('02'),0,'o02',w0('02','duas')),
   ('c','q03',s('03'),0,'o03',0.5),
   ('c','q04',s('04'),0.3,None,0),
   ('c','q05',s('04')+w0('04','r$')-0.05,w0('04','r$')-0.05,'o05',0.15),
   ('c','q06',s('06'),0,'o06',0.7),
   ('c','q07',s('07'),0,None,0),
   ('c','q08',s('08'),0.5,None,0),
   ('g','t09',s('08')+w0('08','você')-0.1,0,None,0),
   ('g','t09b',s('08')+w0('08','depois')-0.1,0,None,0),
   ('c','q10',s('10'),0,None,0),
   ('g','t11',s('11')-0.05,0,None,0)]
clips=[]
for i,(tp,src,ini,off,ov,ovt) in enumerate(P):
    fim=P[i+1][2] if i+1<len(P) else FIM
    if i==0: ini=0
    n=round(fim*FPS)-round(ini*FPS); o=f'tmp/c{i:02d}.mp4'
    enc=['-frames:v',str(n),'-an','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',o]
    if tp=='g':
        vf=f"scale=2160:3840,zoompan=z='1+0.03*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps={FPS}"
        subprocess.run(X+['-loop','1','-i',f'telas/{src}.png','-vf',vf]+enc,timeout=600)
    else:
        base=f"[0:v]fps={FPS},scale=1080:1920,setsar=1,tpad=stop_mode=clone:stop_duration=2[v]"
        cmd=X+['-ss',f'{max(off,0):.3f}','-i',f'clipes/{src}.mp4']
        if ov:
            cmd+=['-loop','1','-i',f'ov/{ov}.png']; fc=base+f";[1:v]format=rgba,fade=t=in:st={ovt:.2f}:d=0.18:alpha=1[o];[v][o]overlay=0:0:enable='gte(t,{ovt:.2f})'[x]"
        else: fc=base+";[v]null[x]"
        subprocess.run(cmd+['-filter_complex',fc,'-map','[x]']+enc,timeout=600)
    clips.append(o)
open('tmp/l.txt','w').write(''.join(f"file '{os.path.basename(c)}'\n" for c in clips))
subprocess.run(X+['-f','concat','-safe','0','-i','tmp/l.txt','-c','copy','tmp/v.mp4'],timeout=300)
def ts(x): h=int(x//3600); m=int(x%3600//60); return f"{h}:{m:02d}:{x%60:05.2f}"
sub=["[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: L,Sora,84,&H00FFFFFF,&H00FFFFFF,&H00181210,&H80000000,1,0,0,0,100,100,-1,0,1,7,2,2,60,60,300,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"]
DEST={'duas','duas.','ligar','ligar.','cnpj','cnpj.','grátis','grátis,','aparece','aparece,','publicar'}
FIX={'Proficio':'Profissio','Licite':'Licit','Pregueira.':'Pregoeira.'}
blk=[]
def flush():
    global blk
    if not blk: return
    a=blk[0][0]; b=blk[-1][1]+0.05
    txt=' '.join(('{\\c&H7AF2A8&}'+w+'{\\c&HFFFFFF&}') if w.lower() in DEST else w for _,_,w in blk)
    sub.append(f"Dialogue: 0,{ts(a)},{ts(b)},L,,0,0,0,,{txt}\n"); blk=[]
for a,b,w in words:
    w=FIX.get(w,w)
    if blk and (a-blk[-1][1]>0.35 or len(blk)>=3 or sum(len(x[2]) for x in blk)+len(w)>17 or blk[-1][2][-1] in '.?!:'): flush()
    blk.append((a,b,w))
flush(); open('tmp/l.ass','w').write(''.join(sub))
S='/home/user/licit-conteudo/remotion/public/sfx/'; TR='/home/user/licit-conteudo/remotion/public/trilha-tech-warm-33s.mp3'
ev=[('pop',s('02')+w0('02','duas'),0.45),('sweep',P[4][2]+0.15,0.3),('click',P[3][2]+0.4,0.35),('move',P[7][2]+0.3,0.3),('typing',P[8][2]+0.2,0.3),('tique',P[9][2]+0.3,0.45),('tique',P[9][2]+1.0,0.45),('tique',P[9][2]+1.7,0.45),('shimmer',P[11][2]+0.1,0.35)]
cmd=X[:]; fc=[]; mix=[]
for i,k in enumerate(segs):
    cmd+=['-i',f'tmp/f{k}.wav']; fc.append(f"[{i}]adelay={int(A[k][0]*1000)}:all=1[a{i}]"); mix.append(f'[a{i}]')
n=len(segs)
for j,(nm,tt,vol) in enumerate(ev):
    cmd+=['-i',S+nm+'.mp3']; fc.append(f"[{n+j}]volume={vol},adelay={int(tt*1000)}:all=1[e{j}]"); mix.append(f'[e{j}]')
cmd+=['-stream_loop','-1','-i',TR]; mi=n+len(ev)
fc.append(f"[{mi}]volume=0.09,atrim=0:{FIM},afade=t=in:d=1.5,afade=t=out:st={FIM-1.5}:d=1.5[m]"); mix.append('[m]')
fc.append(''.join(mix)+f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{FIM},loudnorm=I=-14.6:TP=-1.5:LRA=11,alimiter=limit=0.84[o]")
subprocess.run(cmd+['-filter_complex',';'.join(fc),'-map','[o]','-ar','48000','tmp/a.wav'],timeout=300)
OUT='Licit_Ad01_DonaNorma_v1.mp4'
subprocess.run(X+['-i','tmp/v.mp4','-i','tmp/a.wav','-vf',"ass=tmp/l.ass:fontsdir=/home/user/licit-conteudo/assets/fonts",'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],timeout=900)
print('dur',dur(OUT),[(p[1],round(p[2],2)) for p in P])
