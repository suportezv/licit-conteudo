import json,os,base64,urllib.request
K=os.environ['GEMINI_API_KEY']
P=("Animate this image as the first frame of a realistic vertical video. The woman looks straight into the camera and says in Brazilian Portuguese, in a dry deadpan low voice: \"Sabe quantas empresas vieram vender? Duas.\" On the last word, 'Duas', she raises two fingers next to her face with one eyebrow raised. Keep her face, hair, clothes and the office exactly as in the image. Static camera. Audio: only her voice and quiet office room tone. Do not add music, text or subtitles.")
body={"model":"gemini-omni-1.2-flash","input":[{"type":"image","data":base64.b64encode(open('q02.jpg','rb').read()).decode(),"mime_type":"image/jpeg"},{"type":"text","text":P}],"response_format":{"type":"video","duration":"4s","resolution":"720p"}}
r=urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions",data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":K})
try: d=json.load(urllib.request.urlopen(r,timeout=900))
except urllib.error.HTTPError as e: print('HTTP',e.code,e.read().decode()[:1200]); raise SystemExit
print({k:(v if k not in('steps','outputs') else '...') for k,v in d.items()})
n=0
for s in d.get('steps',[]):
    for c in s.get('content',[]) if isinstance(s.get('content'),list) else []:
        if c.get('type')=='video' and c.get('data'): open(f'omni_q02_{n}.mp4','wb').write(base64.b64decode(c['data'])); n+=1; print('video salvo')
        elif c.get('type')=='video': print('video ref',{k:v for k,v in c.items() if k!='data'})
        elif s.get('type')!='user_input': print(s.get('type'),json.dumps(c)[:300])
