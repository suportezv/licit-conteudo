import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
G='/home/user/licit-conteudo/scripts/gera_imagem.py'
K=("Attachment 1 is the character Dona Marlene, attachment 2 is her warehouse. Keep EXACTLY the same woman (54-year-old Brazilian, round face, dyed copper-brown shoulder-length hair with grey roots pushed behind the ears, burgundy thin-frame reading glasses pushed up on top of her head, faded navy-blue polo shirt with a pen clipped to the collar, small gold chain with medal, small hoop earrings, old digital wristwatch) and the same place (small cleaning-supplies distributor: metal shelves with plain cardboard boxes, blank white and blue jugs, mop heads and brooms, worn laminate counter with a big calculator, roll-up door with daylight). Vertical 9:16 cinematic film still, photorealistic, 35mm look, shallow depth of field, fine grain. No text, no logos, no readable labels. SHOT: ")
Q={'m02':"tight frontal close-up, she looks straight into the lens, indignant and a bit hurt, eyebrows up, mouth closed, hands out of frame.",
'm03':"medium shot, she stands behind the worn counter leaning on it with both hands, the big calculator next to her hand, looking at the camera with a suspicious sideways look, mouth closed.",
'm04':"three-quarter medium close-up, she stands with arms crossed in front of the shelves, chin slightly up, firm look at the camera, mouth closed.",
'mon':"medium shot from the customer side of the counter: she stands behind the counter next to a chunky old beige flat computer monitor that is turned to face the camera; the monitor screen is a perfectly flat solid bright green rectangle (pure chroma key green, no reflections, nothing on it). One of her hands rests on top of the monitor frame, she looks at the camera, mouth closed. Calculator and clipboard on the counter.",
'ombro':"over-the-shoulder shot from behind her right shoulder: the back of her copper-brown hair with the glasses on top in soft focus in the foreground, in focus on the counter a chunky old beige flat computer monitor whose screen is a perfectly flat solid bright green rectangle (pure chroma key green, nothing on it), her hand on a mouse."}
def g(k):
    r=subprocess.run(['python3',G,'openai',K+Q[k],f'storyboard-r3/{k}.png','--tamanho','1024x1536','--qualidade','high','--ref','marlene/marlene_master.png','--ref','marlene/marlene_deposito.png'],capture_output=True,text=True,timeout=600)
    return (r.stdout+r.stderr).strip().splitlines()[-1]
with ThreadPoolExecutor(5) as ex:
    for x in ex.map(g,sys.argv[1:] or list(Q)): print(x)
