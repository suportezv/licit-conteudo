# Roteiro 5 "Quarenta editais, tres eram nossos": Claudia, analista de licitacao de uma empresa de manutencao e reforma predial.
import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','storyboard-r1'))
import gera_omni as G
from concurrent.futures import ThreadPoolExecutor
G.VOZ=json.load(open('../claudia/voz/VOZ.json'))['voice_id']
G.BASE=("Animate this image as the first frame of a realistic vertical video. Keep the woman's face, hair, glasses, clothes and the office exactly as in the image. Static camera. "
        "She speaks in Brazilian Portuguese with a clear, competent, slightly tired voice and dry humour, at a brisk natural conversational pace, finishing the whole line well before the video ends. "
        "Audio: only her voice and quiet office room tone. Do not add music, text or subtitles. ")
G.IMG={'c01':'a','c02':'b','c03':'c','c04':'c','c05':'f','c06':'c','c07':'c','c08':'h'}
FL="One continuous fluid sentence at a natural conversational pace, no long pauses, no hand gestures below the desk. "
G.C={
'c01':(7,"She says to the camera, word for word, tired, with only a short breath between the two sentences: \"Essa semana eu li quarenta editais inteiros. Trinta e sete não serviam pra nossa empresa.\" On the second sentence she shakes her head slightly."),
'c02':(5,FL+"She says to the camera, word for word, dry and tired: \"E pra não perder prazo, eu trabalho todo sábado.\" She raises her eyebrows on 'sábado'."),
'c03':(4,"She says to the camera, word for word, lighter: \"Na Profíssio Licíti é diferente.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee)."),
'c04':(6,FL+"She glances at the laptop and back to the camera and says, word for word, pleased: \"Coloquei o C-N-P-J da empresa e apareceu só o que serve pra gente.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota, said once). Her hand stays resting on the laptop edge the whole time."),
'c05':(9,"We see her from behind, her voice is heard. The laptop stays completely still and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it); her hand never goes in front of the screen. She nods toward the screen and says, word for word: \"Olha essa: Sete Lagoas, Minas Gerais. Um milhão e duzentos e cinquenta mil reais pra reformar o prédio da prefeitura.\" ('Sete Lagoas' is a city name)."),
'c06':(5,"She says to the camera, word for word: \"E antes de ler oitenta páginas, eu pergunto ao edital.\" She raises one finger on 'pergunto'."),
'c07':(6,"She says to the camera, word for word, with a short pause between the sentences: \"Ele responde com a página. Eu confiro e decido.\" She gives a small firm nod at the end."),
'c08':(6,"She says to the camera right away, word for word, light and relieved, with only a short breath between the sentences: \"Agora eu só leio o edital que serve. E hoje eu saio no horário.\" Immediately after the last word she smiles, turns and walks out of the frame with her handbag."),
}
if __name__=='__main__':
    ks=sys.argv[1:] or list(G.C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(G.gera,ks))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if os.path.exists(f'omni/{k}.mp4'): print(G.voz(k))
