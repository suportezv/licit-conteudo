# Falas do roteiro 1 na voz da Dona Norma (eleven_v3). Uso: python3 narra.py [ids...]
import json,os,subprocess,sys,urllib.request,uuid
K=os.environ['ELEVENLABS_API_KEY']; V='a16c9WjbxD7rsBrbu5UX'
F={
'01':"[deadpan][speaking briskly] Eu tenho duzentos e trinta mil reais pra comprar material de limpeza.",
'02':"[deadpan][speaking briskly] Sabe quantas empresas vieram vender? [flatly] Duas.",
'03':"[wry][speaking briskly] Prazer, Norma. Pregoeira. Com esse nome, eu ia ser o quê?",
'04':"[speaking briskly] Olha Uberlândia: dois milhões e setecentos mil em material de limpeza. Tá aberto no PNCP.",
'06':"[sighs] E eu não posso te ligar.",
'07':"[speaking briskly] Eu só posso publicar, e torcer pra você ver.",
'08':"[brightening][speaking briskly] Na Profissio Licíte, você digita o CNPJ e vê o que o governo quer comprar de você. Depois, ela ajuda no resto: edital, documento, prazo.",
'10':"[warmly] Não garanto que você ganha. Garanto que quem não aparece, não ganha.",
'11':"[speaking briskly] Digita o CNPJ. Teste grátis, sem cartão.",
}
def stt(p):
    b=uuid.uuid4().hex; data=open(p,'rb').read()
    body=b''.join([f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k,v in [('model_id','scribe_v1'),('language_code','pt'),('timestamps_granularity','word')]])+f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode()+data+f'\r\n--{b}--\r\n'.encode()
    r=urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text',data=body,headers={'xi-api-key':K,'Content-Type':f'multipart/form-data; boundary={b}'})
    return json.load(urllib.request.urlopen(r,timeout=120))
if __name__=='__main__':
    for k in (sys.argv[1:] or sorted(F)):
        b=json.dumps({"text":F[k],"model_id":"eleven_v3","language_code":"pt","voice_settings":{"stability":0.5}}).encode()
        r=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V}?output_format=mp3_44100_192",data=b,headers={"xi-api-key":K,"Content-Type":"application/json"})
        open('audio/raw.mp3','wb').write(urllib.request.urlopen(r,timeout=180).read())
        o=f'audio/f{k}.wav'
        X=['ffmpeg','-nostdin','-v','error','-y']
        subprocess.run(X+['-i','audio/raw.mp3','-af','silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse','-ar','48000','-ac','1','audio/a.wav'],timeout=60)
        subprocess.run(X+['-i','audio/a.wav','-af','silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse','audio/b.wav'],timeout=60)
        m=subprocess.run(['ffmpeg','-nostdin','-i','audio/b.wav','-af','volumedetect','-f','null','-'],capture_output=True,text=True,timeout=60).stderr
        mean=float(m.split('mean_volume:')[1].split('dB')[0]); 
        subprocess.run(X+['-i','audio/b.wav','-af',f'volume={-21-mean:.2f}dB,alimiter=limit=0.8','-ar','48000',o],timeout=60)
        s=stt(o); json.dump([w for w in s['words'] if w['type']=='word'],open(f'audio/f{k}.json','w'),ensure_ascii=False)
        d=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o]).decode().strip()
        print(k,d,'|',s['text'])
    [os.remove('audio/'+x) for x in ('raw.mp3','a.wav','b.wav')]
