# Encaixa uma imagem 4:3 na tela do monitor de um clipe. Uso: compoe_tela.py clipe.mp4 conteudo.png saida.mp4 [verde|cinza]
import cv2,numpy as np,sys,subprocess
src,cont,out,modo=sys.argv[1],sys.argv[2],sys.argv[3],(sys.argv[4] if len(sys.argv)>4 else 'verde')
cap=cv2.VideoCapture(src); fps=cap.get(cv2.CAP_PROP_FPS); w=int(cap.get(3)); h=int(cap.get(4))
C=cv2.imread(cont); ch,cw=C.shape[:2]
LCD=len(sys.argv)>5 and sys.argv[5]=='lcd'   # tela de notebook: sem linhas de varredura nem canto escuro
# aparencia de monitor de tubo: menos contraste, cantos mais escuros, reflexo leve, linhas de varredura
Cf=C.astype(np.float32)*0.86+14
yy,xx=np.mgrid[0:ch,0:cw].astype(np.float32); r=((xx/cw-0.5)**2+(yy/ch-0.5)**2)**0.5
Cf*=(1-(0.10 if LCD else 0.34)*np.clip(r-0.25,0,1)**1.4)[...,None]
Cf+=(26*np.clip(1-((xx/cw-0.18)**2+(yy/ch-0.10)**2)**0.5/0.55,0,1)**2)[...,None]
if not LCD: Cf[1::3]*=0.955
Cf*=np.array([1.03,1.0,0.96],np.float32)          # leve frio de tubo (BGR)
C=cv2.GaussianBlur(Cf.clip(0,255).astype(np.uint8),(0,0),0.7 if LCD else 1.1)
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
ref=None; box=None
def ordena(q):
    q=q.reshape(4,2).astype(np.float32); s_=q.sum(1); d=np.diff(q,axis=1).ravel()
    return np.array([q[s_.argmin()],q[d.argmin()],q[s_.argmax()],q[d.argmax()]],np.float32)
def mascara(f):
    global ref,box
    if modo=='verde':
        hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); m=((hsv[...,0]>40)&(hsv[...,0]<85)&(hsv[...,1]>110)&(hsv[...,2]>90)).astype(np.uint8)*255
    else:
        if ref is None:
            sx,sy=int(w*0.37),int(h*0.535); ref=f[sy-15:sy+15,sx-15:sx+15].reshape(-1,3).mean(0); box=(int(w*0.10),int(h*0.38),int(w*0.64),int(h*0.70))
        d=np.abs(f.astype(int)-ref).max(2); m=(d<24).astype(np.uint8)*255; bm=np.zeros_like(m); bm[box[1]:box[3],box[0]:box[2]]=255; m&=bm
        m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
    return cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
quads=[]; areas=[]
while True:
    ok,f=cap.read()
    if not ok: break
    m=mascara(f); cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if not cs: continue
    c=max(cs,key=cv2.contourArea); ar=cv2.contourArea(c)
    if ar<0.01*w*h: continue
    hull=cv2.convexHull(c); q=None
    for e in (0.02,0.03,0.05,0.08):
        ap=cv2.approxPolyDP(hull,e*cv2.arcLength(hull,True),True)
        if len(ap)==4: q=ordena(ap); break
    if q is None: q=ordena(cv2.boxPoints(cv2.minAreaRect(hull)))
    quads.append(q); areas.append(ar)
areas=np.array(areas); bons=[q for q,a_ in zip(quads,areas) if a_>=0.985*areas.max()]
quad=np.median(np.array(bons),axis=0).astype(np.float32); print('quadrilatero fixo de',len(bons),'quadros')
cen=quad.mean(0); Q=(cen+(quad-cen)*1.045).astype(np.float32)
M=cv2.getPerspectiveTransform(np.float32([[0,0],[cw,0],[cw,ch],[0,ch]]),Q)
wp=cv2.warpPerspective(C,M,(w,h),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
cap.release(); cap=cv2.VideoCapture(src); n=0
while True:
    ok,f=cap.read()
    if not ok: break
    m=mascara(f)
    key=cv2.dilate(m,np.ones((9,9),np.uint8))
    if modo=='verde': key=cv2.morphologyEx(key,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    al=cv2.GaussianBlur(key,(5,5),0).astype(np.float32)[...,None]/255
    f=(f.astype(np.float32)*(1-al)+wp*al).clip(0,255).astype(np.uint8)
    p.stdin.write(f.tobytes()); n+=1
p.stdin.close(); p.wait(); print(out,n,'quadros')
