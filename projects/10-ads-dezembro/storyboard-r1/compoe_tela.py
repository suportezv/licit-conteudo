# Encaixa uma imagem 4:3 na tela do monitor de um clipe. Uso: compoe_tela.py clipe.mp4 conteudo.png saida.mp4 [verde|cinza]
import cv2,numpy as np,sys,subprocess
src,cont,out,modo=sys.argv[1],sys.argv[2],sys.argv[3],(sys.argv[4] if len(sys.argv)>4 else 'verde')
cap=cv2.VideoCapture(src); fps=cap.get(cv2.CAP_PROP_FPS); w=int(cap.get(3)); h=int(cap.get(4))
C=cv2.imread(cont); ch,cw=C.shape[:2]
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',str(fps),'-i','-','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
quad=None; ref=None; n=0; falhas=0
def ordena(q):
    q=q.reshape(4,2).astype(np.float32); s=q.sum(1); d=np.diff(q,axis=1).ravel()
    return np.array([q[s.argmin()],q[d.argmin()],q[s.argmax()],q[d.argmax()]],np.float32)
while True:
    ok,f=cap.read()
    if not ok: break
    if modo=='verde':
        hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV); m=((hsv[...,0]>40)&(hsv[...,0]<85)&(hsv[...,1]>110)&(hsv[...,2]>90)).astype(np.uint8)*255
    else:
        if ref is None:
            sx,sy=int(w*0.37),int(h*0.535); ref=f[sy-15:sy+15,sx-15:sx+15].reshape(-1,3).mean(0)
            box=(int(w*0.10),int(h*0.38),int(w*0.64),int(h*0.70))
        d=np.abs(f.astype(int)-ref).max(2); m=(d<24).astype(np.uint8)*255; bm=np.zeros_like(m); bm[box[1]:box[3],box[0]:box[2]]=255; m&=bm
        m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if cs:
        c=max(cs,key=cv2.contourArea)
        if cv2.contourArea(c)>0.01*w*h:
            hull=cv2.convexHull(c); q=None
            for e in (0.02,0.03,0.05,0.08):
                a=cv2.approxPolyDP(hull,e*cv2.arcLength(hull,True),True)
                if len(a)==4: q=ordena(a); break
            if q is None: q=ordena(cv2.boxPoints(cv2.minAreaRect(hull)))
            quad=q if quad is None else 0.5*quad+0.5*q
        else: falhas+=1
    else: falhas+=1
    if quad is not None:
        # sangra 3 px para cobrir a borda da tela
        cen=quad.mean(0); Q=(cen+(quad-cen)*1.045).astype(np.float32)
        M=cv2.getPerspectiveTransform(np.float32([[0,0],[cw,0],[cw,ch],[0,ch]]),Q)
        wp=cv2.warpPerspective(C,M,(w,h),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_REPLICATE)
        qm=np.zeros((h,w),np.uint8); cv2.fillConvexPoly(qm,Q.astype(np.int32),255)
        key=cv2.dilate(m,np.ones((9,9),np.uint8))             # so onde havia tela (mao na frente fica)
        if modo=='verde':                                    # some com o resto de verde na borda
            key=cv2.morphologyEx(key,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
        a=cv2.GaussianBlur(key,(5,5),0).astype(np.float32)[...,None]/255
        tela=wp.astype(np.float32)*0.93+8                    # leve perda de contraste de monitor
        f=(f.astype(np.float32)*(1-a)+tela*a).clip(0,255).astype(np.uint8)
    p.stdin.write(f.tobytes()); n+=1
p.stdin.close(); p.wait(); print(out,n,'quadros, sem tela em',falhas)
