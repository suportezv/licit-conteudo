# Troca das compras citadas nos anuncios 1, 2 e 4 por obras com prazo no fim de dezembro (24/nov/2026).
import subprocess,json
from PIL import Image, ImageDraw, ImageFont
R='/home/user/licit-conteudo/'; F=R+'assets/fonts/Sora-Variable.ttf'; W,H=1080,1920
GRAF=(16,18,24); FLO=(36,61,50); LIM=(168,242,122); BR=(255,255,255); AP=(89,97,110); SUP=(244,246,249)
def font(s,w=500):
    f=ImageFont.truetype(F,s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def pill(d,cx,cy,t,f,fg=GRAF,bg=LIM,pad=(44,22)):
    w=d.textlength(t,font=f); h=f.size
    d.rounded_rectangle((cx-w/2-pad[0],cy-h/2-pad[1],cx+w/2+pad[0],cy+h/2+pad[1]),(h+2*pad[1])//2,fill=bg); d.text((cx,cy),t,font=f,fill=fg,anchor='mm')
CAPAO=dict(orgao='Município de Capão do Leão',cidade='Capão do Leão/RS',cid='Prefeitura de Capão do Leão/RS',obj='Reforma da quadra de escola',l1='Reforma da quadra esportiva',l2='da escola municipal',objeto='Execução da obra de construção e reforma da quadra esportiva da Escola Municipal de Ensino Fundamental Elberto Madruga',valor='R$ 993.310,91',v='R$ 993.310',fim='30/12/2026',pncp='87691507000117-1-000083/2026')
NSR=dict(orgao='Município de Nova Santa Rosa',cidade='Nova Santa Rosa/PR',cid='Prefeitura de Nova Santa Rosa/PR',obj='Reforma de quadra esportiva',l1='Reforma da quadra',l2='e construção de arquibancada',objeto='Reforma da quadra, iluminação, infraestrutura, construção de arquibancada e sala multiuso da quadra poliesportiva do Núcleo Municipal de Integração e Capacitação',valor='R$ 659.352,15',v='R$ 659.352',fim='28/12/2026',pncp='77116663000109-1-000002/2027')
GUA=dict(orgao='Município de Guarantã do Norte',cidade='Guarantã do Norte/MT',cid='Prefeitura de Guarantã do Norte/MT',obj='Obra do refeitório de escola',l1='Reforma e construção',l2='do refeitório de uma escola',objeto='Execução dos serviços remanescentes da reforma e da construção do refeitório e calçada da Escola Estadual Albert Einstein',valor='R$ 1.490.080,83',v='R$ 1.490.080',fim='28/12/2026',pncp='03239019000183-1-000088/2026')
QUA=dict(cid='Prefeitura de Quaraí/RS',obj='Reforma de unidade de saúde',v='R$ 411.798',fim='29/12/2026')
SLP=dict(cid='Prefeitura de Sete Lagoas/MG',obj='Revitalização de praça',v='R$ 823.772',fim='28/12/2026')
LDP=dict(cid='Prefeitura de Lagoa da Prata/MG',obj='Ampliação de creche',v='R$ 660.837',fim='29/12/2026')
def card(c,out):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle((60,1010,W-60,1500),36,fill=(16,18,24,240))
    d.text((110,1046),c['cid'],font=font(40),fill=LIM); d.text((110,1108),c['l1'],font=font(60,600),fill=BR); d.text((110,1182),c['l2'],font=font(44,600),fill=BR)
    d.text((110,1262),c['v'],font=font(96,600),fill=BR); d.text((110,1386),'Proposta até '+c['fim'],font=font(40),fill=BR); d.text((110,1444),'Fonte: PNCP',font=font(30),fill=(150,158,170)); im.save(out)
def busca(L,n):
    im=Image.new('RGB',(W,H),GRAF); d=ImageDraw.Draw(im); pill(d,W/2,170,'profissiolicit.ai',font(44,600))
    d.rounded_rectangle((60,250,W-60,1420),40,fill=SUP); d.text((110,310),'Licitações para sua empresa.',font=font(50,600),fill=GRAF); d.text((110,388),'Digite o CNPJ',font=font(32),fill=AP)
    d.rounded_rectangle((110,440,W-110,540),20,outline=FLO,width=4,fill=BR); d.text((144,464),'12.345.678/0001-90',font=font(42),fill=GRAF)
    d.rounded_rectangle((110,570,W-110,670),20,fill=FLO); d.text((W/2,620),'Descobrir oportunidades grátis',font=font(36,600),fill=BR,anchor='mm'); y=720
    for c in L[:n]:
        d.rounded_rectangle((110,y,W-110,y+205),20,fill=BR,outline=(220,224,230),width=2); d.text((144,y+24),c['cid'],font=font(28),fill=AP); d.text((144,y+66),c['obj'],font=font(40,600),fill=GRAF)
        d.text((144,y+132),f"{c['v']}  ·  até {c['fim'][:5]}",font=font(32),fill=FLO); d.text((W-144,y+24),'PNCP',font=font(24,600),fill=(150,158,170),anchor='ra'); y+=225
    return im
def busca_mon(L,out):
    im=Image.new('RGB',(1024,768),GRAF); d=ImageDraw.Draw(im); d.rounded_rectangle((30,30,994,738),28,fill=SUP); d.text((70,60),'Licitações para sua empresa.',font=font(44,600),fill=GRAF)
    d.rounded_rectangle((70,130,640,206),14,outline=FLO,width=3,fill=BR); d.text((92,146),'12.345.678/0001-90',font=font(36),fill=GRAF)
    d.rounded_rectangle((660,130,954,206),14,fill=FLO); d.text((807,168),'Descobrir grátis',font=font(30,600),fill=BR,anchor='mm'); y=236
    for c in L:
        d.rounded_rectangle((70,y,954,y+150),14,fill=BR,outline=(220,224,230),width=2); d.text((94,y+14),c['cid'],font=font(24),fill=AP); d.text((94,y+48),c['obj'],font=font(36,600),fill=GRAF); d.text((94,y+100),f"{c['v']}  ·  até {c['fim'][:5]}",font=font(28),fill=FLO); y+=164
    im.save(out)
pg=lambda c,out:dict(out=out,id=c['pncp'].replace('-1-','/').replace('-','/'),num=c['pncp'].split('-')[-1],orgao=c['orgao'],cidade=c['cidade'],objeto=c['objeto'],valor=c['valor'],fim=c['fim'],pncp=c['pncp'],mod='Concorrência eletrônica')
subprocess.run(['node','tela_pncp.js',json.dumps([pg(CAPAO,'storyboard-r1/telas/m_pncp.png'),pg(NSR,'storyboard-r2/telas/m_pncp.png'),pg(GUA,'storyboard-r4/telas/m_pncp.png')])],check=True)
card(CAPAO,'storyboard-r1/ov/o05.png'); card(NSR,'storyboard-r2/ov/o08.png'); card(GUA,'storyboard-r4/ov/o04.png')
L1=[CAPAO,QUA,SLP]; L4=[GUA,LDP,NSR]
for n in range(4): busca(L1,n).save(f'storyboard-r1/telas/t09_{n}.png'); busca(L4,n).save(f'storyboard-r4/telas/t09_{n}.png')
busca_mon(L1,'storyboard-r1/telas/m_busca.png')
C='storyboard-r1/compoe_tela.py'
J=[('storyboard-r1/omni/q04o.mp4','storyboard-r1/telas/m_pncp.png','storyboard-r1/omni/q04_tela.mp4',[]),
   ('storyboard-r1/omni/q08b.mp4','storyboard-r1/telas/m_busca.png','storyboard-r1/omni/q08b_tela.mp4',[]),
   ('storyboard-r1/omni/q04o.mp4','storyboard-r2/telas/m_pncp.png','storyboard-r2/omni/r08a_tela.mp4',[]),
   ('storyboard-r4/omni/f04.mp4','storyboard-r4/telas/m_pncp.png','storyboard-r4/omni/f04_tela.mp4',['verde','lcd'])]
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(lambda j:subprocess.run(['/usr/bin/python3',C,j[0],j[1],j[2]]+j[3],capture_output=True,text=True).stdout.strip()[-60:],J): print(r)
