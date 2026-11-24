# Roteiro 5 "Quarenta editais, tres eram nossos": Claudia, analista de licitacao de uma empresa de manutencao e reforma predial.
import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','storyboard-r1'))
import gera_omni as G
from concurrent.futures import ThreadPoolExecutor
G.VOZ=json.load(open('../claudia/voz/VOZ.json'))['voice_id']
G.BASE=("Animate this image as the first frame of a realistic vertical video. Keep the woman's face, hair, glasses, clothes and the office exactly as in the image. Static camera. "
        "She speaks in Brazilian Portuguese with a clear, competent, slightly tired voice and dry humour, at a brisk natural conversational pace, finishing the whole line well before the video ends. "
        "Audio: only her voice and quiet office room tone. Do not add music, text or subtitles. ")
G.IMG={'c01':'a','c02':'b','c03':'c','c04':'c','c05':'f','c06':'c','c07':'c','c08':'g'}
G.C={
'c01':(6,"She clicks the mouse once, sighs through her nose and says to the camera, word for word, with a short pause between the two sentences: \"Abri quarenta editais essa semana. Três eram pra nós.\""),
'c02':(8,"She says to the camera, word for word, dry and ironic: \"Eu nunca perdi um prazo. Mas olha como: planilha, alarme e sábado.\" On 'planilha' she tilts her head back toward the monitors, on 'alarme' she taps the phone on the desk once with a finger, on 'sábado' she raises her eyebrows with a tired half smile."),
'c03':(4,"She says to the camera, word for word, lighter: \"Na Profíssio Licíti é diferente.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee)."),
'c04':(7,"She says to the camera, word for word: \"Coloquei o C-N-P-J. E veio só o que tem a ver com a empresa.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota; say it once, then a short pause, then the second sentence starting with the words 'E veio só'). She pats the edge of the laptop once."),
'c05':(9,"We see her from behind, her voice is heard. The laptop stays completely still and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it); her hand never goes in front of the screen. She nods toward the screen and says, word for word: \"Olha essa: Sete Lagoas, Minas Gerais. Um milhão e duzentos e cinquenta mil reais pra reformar o prédio da prefeitura.\" ('Sete Lagoas' is a city name)."),
'c06':(5,"She says to the camera, word for word: \"E antes de ler oitenta páginas, eu pergunto ao edital.\" She raises one finger on 'pergunto'."),
'c07':(6,"She says to the camera, word for word, with a short pause between the sentences: \"Ele responde com a página. Eu confiro e decido.\" She gives a small firm nod at the end."),
'c08':(7,"She looks at the camera and says, word for word, calm and decided, with a short pause between the sentences: \"Eu não quero mais licitação. Quero só as nossas.\" Only AFTER the last word she slowly closes the laptop lid with her hand and gives a small satisfied closed-mouth smile."),
}
if __name__=='__main__':
    ks=sys.argv[1:] or list(G.C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(G.gera,ks))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if os.path.exists(f'omni/{k}.mp4'): print(G.voz(k))
