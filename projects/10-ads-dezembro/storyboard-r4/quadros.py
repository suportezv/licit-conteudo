import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
G='/home/user/licit-conteudo/scripts/gera_imagem.py'
P=("Attachment 1 is Rafael: a 31-year-old Brazilian man, medium brown skin, short dark curly hair with low fade, short beard, round thin black metal glasses, charcoal-grey crewneck sweatshirt with sleeves pushed up, white t-shirt at the collar, black smartwatch. Attachment 2 is Seu Jorge: a 62-year-old Brazilian man, dark brown skin, short grey hair receding at the temples, thick grey moustache, light-blue short-sleeved button shirt with a pen and folded reading glasses in the chest pocket, dark trousers, steel watch. Keep EXACTLY the same two men. When a third attachment is given, it shows their office: keep the same office. ")
O=("PLACE: the small modest office of their construction company in a commercial room: a wooden desk with a laptop, rolled blueprints and a scale ruler, a white hard hat and a yellow hard hat on a shelf, floor-tile and brick samples, a wall with a pinned building plan and a wall calendar, a grey filing cabinet, a coffee thermos, daylight from a side window. ")
S="Vertical 9:16 cinematic film still, photorealistic, 35mm look, shallow depth of field, fine grain. No readable text, no logos, no captions. SHOT: "
Q={'a':"two-shot from a low side angle: Rafael sits at the desk in the foreground with his hands on the laptop keyboard, looking at the laptop; Seu Jorge stands behind his shoulder with arms crossed, skeptical, chin raised, looking down at the camera. Both mouths closed.",
'b':"medium close-up single of Seu Jorge standing with arms crossed in the office, skeptical, looking straight at the camera, mouth closed. Rafael is not in the frame.",
'c':"medium single of Seu Jorge standing with both hands resting on the back of an office chair, arms uncrossed, looking away toward the window with a bitter thoughtful expression, mouth closed. Rafael is not in the frame.",
'd':"frontal medium close-up single of Rafael sitting at the desk behind the open laptop (we see the back of the laptop lid), hands on the keyboard, looking at the camera with a confident half grin, mouth closed. Seu Jorge is not in the frame.",
'e':"three-quarter medium close-up single of Rafael sitting at the desk, turned to the camera, one open hand gesturing toward the laptop beside him (we see the laptop from the side, screen not visible), eyebrows up, mouth closed. Seu Jorge is not in the frame.",
'f':"over-the-shoulder shot from behind Rafael's right shoulder: the back of his curly head and round glasses in soft focus in the foreground; in focus on the desk the open laptop whose screen is a perfectly flat solid bright green rectangle (pure chroma key green, nothing on it, no reflections); his hand on the trackpad. Blueprints beside the laptop.",
'g':"two-shot: Seu Jorge, now wearing his reading glasses, has pulled a chair next to Rafael and leans in toward the laptop with his hand reaching for the mouse on the desk, interested; Rafael leans back amused, looking at him. We see the back of the laptop lid. Both mouths closed."}
def g(k,extra=[]):
    r=subprocess.run(['python3',G,'openai',P+O+S+Q[k],f'storyboard-r4/{k}.png','--tamanho','1024x1536','--qualidade','high','--ref','rafael/rafael_master.png','--ref','jorge/jorge_master.png']+extra,capture_output=True,text=True,timeout=600)
    return (r.stdout+r.stderr).strip().splitlines()[-1]
if __name__=='__main__':
    ks=sys.argv[1:] or list(Q)
    if 'a' in ks: print(g('a')); ks=[k for k in ks if k!='a']
    with ThreadPoolExecutor(6) as ex:
        for x in ex.map(lambda k:g(k,['--ref','storyboard-r4/a.png']),ks): print(x)
