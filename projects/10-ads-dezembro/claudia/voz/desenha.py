import os,json,base64,urllib.request
EK=os.environ['ELEVENLABS_API_KEY']
D=("A 43-year-old Brazilian woman, bidding analyst in an office. Native Brazilian Portuguese, neutral urban accent from the southeast. Clear, articulate mid-pitched voice, competent and a little tired, dry sense of humour, speaks at a brisk natural conversational pace, matter-of-fact. Not an announcer. Clean studio recording.")
T="Abri quarenta editais essa semana. Três eram pra nós. Eu nunca perdi um prazo. Mas olha como: planilha, alarme e sábado. Eu não quero mais licitação. Quero só as nossas."
def post(u,b):
    r=urllib.request.Request('https://api.elevenlabs.io'+u,json.dumps(b).encode(),{'xi-api-key':EK,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=180))
d=post('/v1/text-to-voice/design',{'voice_description':D,'text':T,'model_id':'eleven_ttv_v3'})
ids={}
for l,p in zip('ABC',d['previews']):
    open(f'claudia/voz/claudia_voz_{l}.mp3','wb').write(base64.b64decode(p['audio_base_64'])); ids[l]=p['generated_voice_id']
v=post('/v1/text-to-voice',{'voice_name':'Claudia (Licit)','voice_description':D,'generated_voice_id':ids['A']})
json.dump({'voice_id':v['voice_id'],'name':'Claudia (Licit)','origem':'previa A (provisoria)','descricao':D,'previas_geradas':ids},open('claudia/voz/VOZ.json','w'),ensure_ascii=False,indent=1)
print('ok',list(ids))
