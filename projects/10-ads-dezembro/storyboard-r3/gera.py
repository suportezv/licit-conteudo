# Roteiro 3 "Compraram de fora": Dona Marlene. Clipes pelo Gemini Omni + voz dela por speech-to-speech.
import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','storyboard-r1'))
import gera_omni as G
from concurrent.futures import ThreadPoolExecutor
G.VOZ=json.load(open('../marlene/voz/VOZ.json'))['voice_id']
G.BASE=("Animate this image as the first frame of a realistic vertical video. Keep the woman's face, hair, clothes and the warehouse exactly as in the image. Static camera. "
        "She speaks in Brazilian Portuguese with a firm, direct, slightly rough voice, at a brisk natural conversational pace, finishing the whole line well before the video ends. "
        "Audio: only her voice and quiet warehouse room tone. Do not add music, text or subtitles. ")
VERDE="The computer monitor stays completely still and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it). Her hands never go in front of the screen. "
G.IMG={'m05':'mon','m06':'mon','m07':'mon'}
G.C={
'm01':(5,"She walks slowly toward the camera down the aisle with the clipboard in her hand and says, word for word: \"Vinte anos vendendo material de limpeza nessa cidade.\""),
'm02':(5,"She says to the camera, word for word, indignant: \"E a prefeitura daqui comprou de uma empresa de fora.\" She shakes her head once."),
'm03':(6,"Leaning on the counter, she says to the camera, word for word, a bit embarrassed: \"Eu achava que licitação era coisa de quem tem conhecido.\" She taps the calculator once with a finger."),
'm04':(6,"With arms crossed she says to the camera, word for word, firm, with a short pause between the sentences: \"Não é. Ela não é maior do que eu. Ela apareceu.\" On the last sentence she uncrosses her arms and points one finger down at the floor."),
'm05':(5,VERDE+"With one hand on top of the monitor frame she says to the camera, word for word: \"Aí eu conheci a Profíssio Licíti.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee)."),
'm06':(8,VERDE+"She says to the camera, word for word: \"Digitei o C-N-P-J e apareceu o que está aberto pra o que eu vendo.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota). She taps the top of the monitor frame once and raises her eyebrows, impressed."),
'm07':(9,VERDE+"She points at the monitor frame from the side with her pen and says to the camera, word for word: \"Olha essa: Capim Grosso, Bahia. Sete milhões e oitocentos mil reais em limpeza, higiene e descartáveis.\" ('Capim Grosso' is a town name). She finishes well before the video ends."),
'm08':(6,"She hugs the clipboard against her chest, looks straight at the camera and says, word for word, decided: \"A próxima eu vou ler antes de dizer que não é pra mim.\" She ends with a short firm nod and a small proud closed-mouth smile."),
}
SILENCIO={'ombro':(4,"Animate this image as the first frame of a realistic vertical video, seen from behind a woman's shoulder at a shop counter. The camera is locked off on a tripod: absolutely static, no zoom, no pan. The computer monitor stays completely still and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it). Her hand moves the mouse a little and clicks once; her head tilts slightly as she reads. Nothing passes in front of the screen. No speech. Audio: quiet room tone and one mouse click. No music, no text.")}
if __name__=='__main__':
    ks=sys.argv[1:] or list(G.C)+list(SILENCIO)
    base=G.BASE
    def um(k):
        if k in SILENCIO:
            G.C[k]=SILENCIO[k]; b=G.BASE; G.BASE=""; r=G.gera(k); G.BASE=b; return r
        return G.gera(k)
    res=[um(k) for k in ks if k in SILENCIO]
    with ThreadPoolExecutor(4) as ex: res+=list(ex.map(um,[k for k in ks if k not in SILENCIO]))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if k not in SILENCIO and os.path.exists(f'omni/{k}.mp4'): print(G.voz(k))
