# Roteiro 4 "Digita ai, quero ver": Rafael e Seu Jorge, socios de uma construtora. Um falante por clipe.
import sys,os,json
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','storyboard-r1'))
import gera_omni as G
from concurrent.futures import ThreadPoolExecutor
VOZ={'j':json.load(open('../jorge/voz/VOZ.json'))['voice_id'],'f':json.load(open('../rafael/voz/VOZ.json'))['voice_id']}
G.BASE=("Animate this image as the first frame of a realistic vertical video. Keep the faces, hair, clothes and the office exactly as in the image. Static camera. "
        "Only ONE person speaks in this clip, in Brazilian Portuguese, at a natural conversational pace, finishing the whole line well before the video ends. Anyone else in the frame stays silent with the mouth closed. "
        "Audio: only that one voice and quiet office room tone. Do not add music, text or subtitles. ")
J="The older man with the grey moustache speaks with a deep, dry, slow voice. "
R="The young man with glasses and beard speaks with a light, quick, friendly voice. "
G.IMG={'j01':'a','j02':'b','f03':'d','f04':'f','j05':'c','f06':'e','f07':'e','j08':'g'}
G.C={
'j01':(5,J+"Standing with arms crossed behind the young man, he says to the camera, word for word, skeptical: \"Licitação? Eu já caí nessa em dois mil e quatro.\" The young man keeps typing on the laptop without speaking."),
'j02':(4,J+"With arms crossed he tilts his chin toward the laptop off frame and says, word for word, as a dare: \"Então mostra aí. Quero ver.\""),
'f03':(6,R+"He types on the laptop and says, word for word: \"Tá bom. Coloquei o C-N-P-J da construtora. Pronto.\" (C-N-P-J is an acronym spelled letter by letter in Portuguese: cê, ene, pê, jota). On 'pronto' he presses one key with a small flourish and looks up at the camera with a grin."),
'f04':(9,R+"We see him from behind, his voice is heard. The laptop stays completely still and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it); his hand never goes in front of the screen. He nods toward the screen and says, word for word, getting excited: \"Olha essa: Sarandi, Paraná. Um milhão e trezentos mil reais pra construir um centro de assistência social. É exatamente o que a gente faz.\" The older man in the background stays silent."),
'j05':(7,J+"Looking away, then turning his eyes to the camera, he says, word for word, bitter: \"Em dois mil e quatro eu perdi por causa de uma certidão. Ninguém me avisou.\" He taps the back of the chair once with his fingers."),
'f06':(5,R+"Pointing at the laptop with his open hand he says to the camera, word for word: \"A Profíssio Licíti avisa.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee)."),
'f07':(8,R+"He explains to the camera, word for word, counting two things on his fingers: \"Mostra a exigência com a página do edital, e o documento que vence antes da entrega.\""),
'j08':(5,J+"Wearing his reading glasses, he grabs the mouse on the desk, pulls it toward himself and says, word for word, gruff and interested: \"Me dá isso aqui.\" The young man raises both hands and laughs silently, without speaking."),
}
if __name__=='__main__':
    ks=sys.argv[1:] or list(G.C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(G.gera,ks))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if os.path.exists(f'omni/{k}.mp4'):
            G.VOZ=VOZ[k[0]]; print(G.voz(k))
