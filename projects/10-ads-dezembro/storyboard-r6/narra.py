# Roteiro 6 "Quantos voce abriu?": tela e voz, Juliano (voz da marca).
import sys,json,subprocess,os,urllib.request
sys.path.insert(0,'../storyboard-r1'); import gera_omni as G
V='wHnxjlY53t8X9Oi14Awz'
F={'n1':'Você já recebe aviso de licitação no celular todo dia. Quantos você abriu?',
'n2':'Porque achar a licitação é só o começo. Depois vem o edital: oitenta páginas, e uma linha que decide se a sua empresa pode participar.',
'n3':'Esta está aberta agora: Lagoa da Prata, Minas Gerais. Seiscentos e sessenta mil reais pra ampliar uma creche.',
'n4':'Na Profíssio Licíte, você digita o CNPJ e vê as licitações abertas pra sua empresa. Cada exigência aparece com a página do edital. E cada documento, com a validade.',
'n5':'Digita o CNPJ da sua empresa e descubra as licitações abertas pra ela. Teste grátis, sem cartão.'}
ks=sys.argv[1:] or list(F); L=list(F)
for k in ks:
    i=L.index(k); b={'text':F[k],'model_id':'eleven_multilingual_v2','voice_settings':{'stability':0.45,'similarity_boost':0.8,'style':0.35,'speed':1.12}}
    if i>0: b['previous_text']=F[L[i-1]]
    r=urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{V}?output_format=mp3_44100_128',json.dumps(b).encode(),{'xi-api-key':G.EK,'Content-Type':'application/json'})
    open(f'audio/{k}.mp3','wb').write(urllib.request.urlopen(r,timeout=120).read())
    s=json.loads(G.mp('https://api.elevenlabs.io/v1/speech-to-text',[('model_id','scribe_v1'),('language_code','pt'),('timestamps_granularity','word')],f'audio/{k}.mp3','file'))
    w=[x for x in s['words'] if x['type']=='word']; json.dump(w,open(f'audio/{k}.json','w'),ensure_ascii=False); print(k,round(w[-1]['end'],2),s['text'])
