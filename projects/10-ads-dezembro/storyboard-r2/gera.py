# Roteiro 2 "Por uma certidao": clipes pelo Gemini Omni + voz da Dona Norma. Reusa o motor do roteiro 1.
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','storyboard-r1'))
import gera_omni as G
from concurrent.futures import ThreadPoolExecutor
VERDE="The monitor stays completely still, facing the camera, and its screen stays a flat solid bright green rectangle the whole time (it is a chroma key, do not change it, nothing appears on it). Her hands never go in front of the screen. "
G.IMG={}
G.C={
'r01':(5,"Her hand holds the wooden rubber stamp hesitating above the paper form, without stamping. She looks at the camera, regretful, and says, word for word: \"Ontem eu inabilitei o menor preço do pregão.\" Then she slowly puts the stamp down on the desk beside the paper."),
'r02':(5,"After a short beat she says to the camera, word for word, dry and a little sorry: \"Por uma certidão vencida há três dias.\" She gives a small slow shake of the head."),
'r03':(4,"Leaning back in the chair with arms crossed, she says to the camera, word for word, honest and tired: \"E não, eu não gosto de fazer isso.\""),
'r04':(6,"With both palms open above the files she says to the camera, word for word, counting each sentence with a small hand gesture: \"A empresa era boa. A proposta era boa. O papel estava vencido.\""),
'r05':(8,"She holds her glasses in her hand, looks down at first, then lifts her eyes to the camera and says, word for word, calm and fair: \"A culpa não é dela. A regra é igual pra todo mundo. Faltou alguém avisar antes.\" She finishes well before the video ends and stays silent for the last second."),
'r06':(5,VERDE+"Leaning beside the monitor with a relieved small smile, she says to the camera, word for word: \"A Profíssio Licíti avisa.\" ('Profíssio Licíti' is a product name, pronounced pro-FEE-see-oh lee-SEE-chee). She taps the top of the monitor frame once."),
'r07':(8,VERDE+"Leaning beside the monitor, she explains to the camera, word for word: \"Ela guarda os documentos da empresa e mostra o que vence antes da entrega.\" She finishes well before the video ends and nods."),
'r08':(9,"She points at the monitor with the pen, glancing between the screen and the camera, and says, word for word: \"E tem licitação aberta agora. Nova Santa Rosa, Paraná: seiscentos e cinquenta mil reais pra reformar uma quadra de esportes.\" ('Nova Santa Rosa' is a town name). She finishes well before the video ends."),
'r09':(4,"Hands crossed on the files, she says warmly to the camera, word for word: \"Eu prefiro mil vezes habilitar.\" Right after, her face opens into a wide genuine smile."),
}
if __name__=='__main__':
    ks=sys.argv[1:] or list(G.C)
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(G.gera,ks))
    tot=0
    for k,st,tok in res: print(k,st,tok); tot+=tok
    print('tokens de video',tot,'~US$ %.2f'%(tot*12/1e6))
    for k in ks:
        if os.path.exists(f'omni/{k}.mp4'): print(G.voz(k))
