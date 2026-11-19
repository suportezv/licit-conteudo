# Clipes do anuncio 1 pelo Gemini Omni (Interactions API) + voz da Dona Norma por speech-to-speech.
# Uso: python3 gera_omni.py [ids]   (nao regenera clipe que ja existe em omni/)
import json,os,base64,urllib.request,subprocess,sys,uuid,io
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
GK=os.environ['GEMINI_API_KEY']; EK=os.environ['ELEVENLABS_API_KEY']; VOZ='a16c9WjbxD7rsBrbu5UX'
BASE=("Animate this image as the first frame of a realistic vertical video. Keep the woman's face, hair, clothes and the office exactly as in the image. Static camera. "
      "She speaks in Brazilian Portuguese with a dry, calm, low voice, at a natural conversational pace, finishing the whole line before the video ends. "
      "Audio: only her voice and quiet office room tone. Do not add music, text or subtitles. ")
C={
'q01':(5,"She glances from the monitor to the camera and says: \"Eu tenho duzentos e trinta mil reais pra comprar material de limpeza.\""),
'q03':(5,"She pours coffee from the steel thermos into the small glass while looking at the camera with a dry half smile and says: \"Prazer, Norma. Pregoeira. Com esse nome, eu ia ser o quê?\""),
'q05':(8,"She points at the monitor with the pen, glancing between the screen and the camera, and says, word for word: \"Olha Uberlândia. Dois milhões e setecentos mil reais em material de limpeza. Está aberto no P-N-C-P.\" (the last word is an acronym spelled letter by letter in Portuguese: pê, ene, cê, pê)"),
'q06':(4,"She sighs, lowers the glasses in her hand, looks down and says quietly: \"E eu não posso te ligar.\""),
'q07':(5,"She opens both palms above the files in a small helpless shrug and says to the camera: \"Eu só posso publicar, e torcer pra você ver.\""),
'q08':(5,"She turns the old monitor toward the camera with both hands, leans beside it, pleased, and says, word for word: \"Por isso eu gostei da Profíssio Licíti.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee). The monitor screen stays a plain blank pale grey."),
'q10':(7,"Hands crossed on the files, she says kindly to the camera, word for word: \"Não garanto que você ganha. Garanto que quem não aparece, não ganha.\" She ends with a knowing half smile."),
'q11':(5,"Hands crossed on the files, she says to the camera, friendly and direct, word for word: \"Digita o C-N-P-J. Teste grátis, sem cartão.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota)"),
}
def img(k):
    im=Image.open({'q11':'q10'}.get(k,k)+'.png').convert('RGB'); s=1280/im.height; im=im.resize((int(im.width*s),1280),Image.LANCZOS); x=(im.width-720)//2
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
        open(f'omni/{k}_norma.mp3','wb').write(mp(f'https://api.elevenlabs.io/v1/speech-to-speech/{VOZ}?output_format=mp3_44100_192',[('model_id','eleven_multilingual_sts_v2'),('remove_background_noise','true')],f'omni/{k}_a.mp3','audio'))
    w=json.load(open(f'omni/{k}.json'))
    return k,s['text'],(w[0]['start'],w[-1]['end']) if w else None
if __name__=='__main__':
    ks=sys.argv[1:] or list(C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(gera,[k for k in ks if k in C]))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks+(['q02'] if not sys.argv[1:] else []):
        if os.path.exists(f'omni/{k}.mp4'): print(voz(k))
