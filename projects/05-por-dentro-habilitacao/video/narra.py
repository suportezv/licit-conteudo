#!/usr/bin/env python3
"""Gera (ou regera) segmentos da narracao na ElevenLabs a partir do SEG do gera.py,
com previous_text/next_text para continuidade, e valida cada um com o Scribe.
uso: narra.py 12 19        (chaves do SEG; sem argumentos gera todos)
Grava assets/audio/nKK.mp3 e atualiza assets/audio/duracoes.json."""
import ast, json, os, re, subprocess, sys
from pathlib import Path
KEY = os.environ["ELEVENLABS_API_KEY"]
VOZ = "wHnxjlY53t8X9Oi14Awz"      # Juliano Magalhaes, escolhida pelo usuario em 11/nov/2026
MODELO = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.12}
src = Path("gera.py").read_text()
m = re.search(r"^SEG = (\{.*?^\})", src, re.S | re.M)
SEG = ast.literal_eval(m.group(1)); ORD = sorted(SEG)
alvo = sys.argv[1:] or ORD
DUR_P = Path("assets/audio/duracoes.json"); DUR = json.load(open(DUR_P)) if DUR_P.exists() else {}
for k in alvo:
    i = ORD.index(k)
    body = {"text": SEG[k], "model_id": MODELO, "voice_settings": SETTINGS}
    if i > 0: body["previous_text"] = SEG[ORD[i - 1]]
    if i + 1 < len(ORD): body["next_text"] = SEG[ORD[i + 1]]
    out = f"assets/audio/n{k}.mp3"
    r = subprocess.run(["curl", "-sS", "-o", out, "-w", "%{http_code}", "-X", "POST",
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
        "-H", f"xi-api-key: {KEY}", "-H", "Content-Type: application/json", "-d", json.dumps(body, ensure_ascii=False)],
        capture_output=True, text=True)
    if r.stdout.strip() != "200": print(k, "HTTP", r.stdout, open(out).read()[:300]); sys.exit(1)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
    DUR[k] = round(d, 3)
    st = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", f"xi-api-key: {KEY}",
        "-F", "model_id=scribe_v1", "-F", "language_code=por", "-F", f"file=@{out}"], capture_output=True, text=True)
    try: texto = json.loads(st.stdout).get("text", "?")
    except Exception: texto = st.stdout[:200]
    print(f"{k} {d:.2f}s | STT: {texto}")
json.dump(dict(sorted(DUR.items())), open(DUR_P, "w"), indent=0)
print("duracoes.json atualizado")
