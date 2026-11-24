# Fecho novo do pack (24/nov): grava f11 na voz de cada anuncio. Uso: python3 cta.py
import sys,json,subprocess,os,shutil,urllib.request
sys.path.insert(0,'storyboard-r1'); import gera_omni as G
T='Digita o CNPJ da sua empresa e descubra as licitações abertas pra ela. Teste grátis, sem cartão.'
V={'storyboard-r1':'norma','storyboard-r3':'marlene','storyboard-r4':'rafael'}
for d,p in V.items():
    v=json.load(open(f'{p}/voz/VOZ.json'))['voice_id']; a=f'{d}/audio/'
    if os.path.exists(a+'f11.wav') and not os.path.exists(a+'f11_curto.wav'):
        shutil.copy(a+'f11.wav',a+'f11_curto.wav'); shutil.copy(a+'f11.json',a+'f11_curto.json')
    r=urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{v}?output_format=mp3_44100_128',json.dumps({'text':T,'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.3}}).encode(),{'xi-api-key':G.EK,'Content-Type':'application/json'})
    open(a+'f11.mp3','wb').write(urllib.request.urlopen(r,timeout=120).read())
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',a+'f11.mp3','-ar','48000','-ac','1',a+'f11.wav'])
    s=json.loads(G.mp('https://api.elevenlabs.io/v1/speech-to-text',[('model_id','scribe_v1'),('language_code','pt'),('timestamps_granularity','word')],a+'f11.mp3','file'))
    json.dump([w for w in s['words'] if w['type']=='word'],open(a+'f11.json','w'),ensure_ascii=False); print(d,s['text'],round(s['words'][-1]['end'],2))
