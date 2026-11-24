import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
G='/home/user/licit-conteudo/scripts/gera_imagem.py'
P=("Attachment 1 is Claudia: "+open('claudia/base.txt').read().split('CHARACTER:')[1].split('STYLE:')[0].strip()+" Keep EXACTLY the same woman, same face, glasses, ponytail, mustard blazer. Attachment 2 is her desk in the office of a building-maintenance and renovation company: keep the same office, desk, two monitors with sticky notes, laptop at the right, shelves with binders, big window with late-afternoon light. ")
S="Vertical 9:16 cinematic film still, photorealistic, 35mm look, shallow depth of field, fine grain. No readable text, no logos, no captions. SHOT: "
Q={'a':"medium shot from the side of the desk: Claudia sits at her desk, body toward the two monitors (blurred spreadsheets and documents, sticky notes around), one hand on the mouse, her face turned to the camera with a tired, knowing look, mouth closed.",
'b':"medium close-up: Claudia sitting at the desk turned to the camera, elbows on the desk, both hands resting together on the open notebook, a smartphone lying on the desk next to her, monitors blurred behind her. Dry, ironic, tired half smile, mouth closed.",
'c':"medium close-up: Claudia sitting turned to the camera, now relaxed and more awake, one hand resting on the edge of the open laptop beside her (we see the laptop from the side, screen not visible), monitors blurred behind. Small confident smile, mouth closed.",
'f':"over-the-shoulder shot from behind Claudia's right shoulder: the back of her ponytail and the mustard blazer shoulder in soft focus in the foreground; in sharp focus on the desk the open laptop whose screen is a perfectly flat solid bright green rectangle (pure chroma key green, nothing on it, no reflections); her hand rests on the desk beside the laptop, not on it.",
'g':"medium shot: Claudia sitting at the desk facing the camera, calm and decided, her right hand on top of the open lid of the laptop in front of her (we see the back of the laptop lid), as if about to close it. Monitors with sticky notes blurred behind. Mouth closed."}
def g(k):
    r=subprocess.run(['python3',G,'openai',P+S+Q[k],f'storyboard-r5/{k}.png','--tamanho','1024x1536','--qualidade','high','--ref','claudia/claudia_master.png','--ref','claudia/claudia_mesa.png'],capture_output=True,text=True,timeout=600)
    return (r.stdout+r.stderr).strip().splitlines()[-1]
if __name__=='__main__':
    with ThreadPoolExecutor(5) as ex:
        for x in ex.map(g,sys.argv[1:] or list(Q)): print(x)
