# Clipes do anuncio 1 pelo Gemini Omni (Interactions API) + voz da Dona Norma por speech-to-speech.
# Uso: python3 gera_omni.py [ids]   (nao regenera clipe que ja existe em omni/)
import json,os,base64,urllib.request,subprocess,sys,uuid,io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
GK=os.environ['GEMINI_API_KEY']; EK=os.environ['ELEVENLABS_API_KEY']; VOZ='AHgZJh5DUFzVkrYaKD4J'
BASE=("Animate this image as the first frame of a realistic vertical video. Keep the woman's face, hair, clothes and the office exactly as in the image. Static camera. "
      "She speaks in Brazilian Portuguese with a dry, calm, low voice, at a natural conversational pace, finishing the whole line before the video ends. "
      "Audio: only her voice and quiet office room tone. Do not add music, text or subtitles. ")
C={
'q01':(5,"She glances from the monitor to the camera and says, word for word, dry: \"Eu tenho duzentos e trinta mil reais pra reformar uma escola.\""),
'q05':(8,"She points at the monitor with the pen, glancing between the screen and the camera, and says, word for word: \"Olha: Capão do Leão, Rio Grande do Sul. Novecentos e noventa mil reais pra reformar a quadra de uma escola. Está aberto no P-N-C-P.\" ('Capão do Leão' is a town name, pronounced ka-PAUN du le-AUN; P-N-C-P is an acronym spelled letter by letter in Portuguese: pê, ene, cê, pê). She finishes well before the video ends."),
'q02':(5,"For the first second she stays still with both hands resting on the files. Then she says, word for word: \"Sabe quantas empresas vieram vender? Duas.\" Only on the last word, 'Duas', she lifts her right hand next to her face showing EXACTLY TWO fingers: index and middle finger extended in a V, while thumb, ring finger and little finger stay folded closed. Never three fingers. Deadpan, one eyebrow raised."),
'q03':(6,"She pours coffee from the steel thermos into the small glass. She says, word for word, with dry humor: \"Prazer, Norma. Pregoeira.\" ('Pregoeira' is pronounced pre-go-EI-ra, with a clear 'go' sound, it means auctioneer). She makes a short comic pause, looks straight at the camera with a deadpan face, then adds: \"Com esse nome, eu ia ser o quê?\" Immediately after, she shrugs one shoulder and raises both eyebrows with a tiny smirk, as a punchline."),
'q08':(5,"The monitor stays completely still, facing the camera, and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it). Her hands stay on the monitor frame, never in front of the screen. Leaning beside the monitor, pleased, she says to the camera, word for word: \"Por isso eu gostei da Profíssio Licíti.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee)."),
'q08b':(7,"The monitor stays completely still, facing the camera, and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it). Her hands never go in front of the screen. She taps the top of the monitor once and says to the camera, word for word: \"Você digita o C-N-P-J e vê o que o governo quer comprar de você.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota)."),
'q08c':(8,"The monitor stays completely still, facing the camera, and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it). Her hands never go in front of the screen. She counts on her fingers beside the monitor and says to the camera, word for word, finishing well before the video ends: \"Depois, ela ajuda no resto: edital, documento, prazo.\" After the last word 'prazo' she nods and stays silent for the final second."),
}
IMG={'q02':'q02b','q08':'q08g','q08b':'q08g','q08c':'q08g'}
def img(k):
    im=Image.open(IMG.get(k,k)+'.png').convert('RGB'); s=1280/im.height; im=im.resize((int(im.width*s),1280),Image.LANCZOS); x=(im.width-720)//2
    b=io.BytesIO(); im.crop((x,0,x+720,1280)).save(b,'JPEG',quality=92); return base64.b64encode(b.getvalue()).decode()
def gera(k):
    o=f'omni/{k}.mp4'
    if os.path.exists(o): return k,'ja existe',0
    d,p=C[k]
    body={"model":"gemini-omni-1.2-flash","input":[{"type":"image","data":img(k),"mime_type":"image/jpeg"},{"type":"text","text":BASE+p}],"response_format":{"type":"video","duration":f"{d}s","resolution":"720p"}}
    r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":GK})
    try: j=json.load(urllib.request.urlopen(r,timeout=900))
    except urllib.error.HTTPError as e: return k,'HTTP %s %s'%(e.code,e.read().decode()[:300]),0
    tok=sum(m['tokens'] for m in j.get('usage',{}).get('output_tokens_by_modality',[]) if m['modality']=='video')
    for s in j.get('steps',[]):
        for c in (s.get('content') or []):
            if isinstance(c,dict) and c.get('type')=='video' and c.get('data'):
                open(o,'wb').write(base64.b64decode(c['data'])); return k,'ok',tok
    return k,'sem video: '+json.dumps(j)[:300],tok
def mp(url,campos,arq,nome):
    b=uuid.uuid4().hex
    body=b''.join(f'--{b}\r\nContent-Disposition: form-data; name="{a}"\r\n\r\n{v}\r\n'.encode() for a,v in campos)+f'--{b}\r\nContent-Disposition: form-data; name="{nome}"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()+open(arq,'rb').read()+f'\r\n--{b}--\r\n'.encode()
    return urllib.request.urlopen(urllib.request.Request(url,data=body,headers={'xi-api-key':EK,'Content-Type':f'multipart/form-data; boundary={b}'}),timeout=180).read()
def voz(k):
    X=['ffmpeg','-nostdin','-v','error','-y']
    subprocess.run(X+['-i',f'omni/{k}.mp4','-vn','-ar','44100','-ac','1',f'omni/{k}_a.mp3'],timeout=60)
    s=json.loads(mp('https://api.elevenlabs.io/v1/speech-to-text',[('model_id','scribe_v1'),('language_code','pt'),('timestamps_granularity','word')],f'omni/{k}_a.mp3','file'))
    json.dump([w for w in s['words'] if w['type']=='word'],open(f'omni/{k}.json','w'),ensure_ascii=False)
    if not os.path.exists(f'omni/{k}_norma.mp3'):
        open(f'omni/{k}_norma.mp3','wb').write(mp(f'https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}?output_format=mp3_44100_128',[('model_id','eleven_multilingual_sts_v2'),('remove_background_noise','true')],f'omni/{k}_a.mp3','audio'))
    w=json.load(open(f'omni/{k}.json'))
    return k,s['text'],(w[0]['start'],w[-1]['end']) if w else None
if __name__=='__main__':
    ks=sys.argv[1:] or list(C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(gera,[k for k in ks if k in C]))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if os.path.exists(f'omni/{k}.mp4'): print(voz(k))
