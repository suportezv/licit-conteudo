#!/usr/bin/env python3
"""Narra as telas dos carrosseis (voz Juliano, mesma do Por Dentro) e confere cada faixa pelo Scribe."""
import json, os, subprocess, sys
K = os.environ["ELEVENLABS_API_KEY"]; VOZ = "wHnxjlY53t8X9Oi14Awz"
SET = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.12}
N = json.load(open("narracao.json")); os.makedirs("video/audio", exist_ok=True)
ALVO = [a.split(":") for a in sys.argv[1:]] or [[p, None] for p in N]
for peca, so in ALVO:
    L = N[peca]
    for i, t in enumerate(L):
        if so and i + 1 != int(so): continue
        b = {"text": t, "model_id": "eleven_multilingual_v2", "voice_settings": SET}
        if i: b["previous_text"] = L[i - 1]
        if i + 1 < len(L): b["next_text"] = L[i + 1]
        out = f"video/audio/{peca}-{i+1:02d}.mp3"
        r = subprocess.run(["curl", "-sS", "-o", out, "-w", "%{http_code}", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
                            "-H", f"xi-api-key: {K}", "-H", "Content-Type: application/json", "-d", json.dumps(b, ensure_ascii=False)], capture_output=True, text=True)
        if r.stdout != "200": sys.exit(f"{out} HTTP {r.stdout}")
        tmp = out + ".t.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,loudnorm=I=-19:TP=-2", "-ar", "44100", tmp], check=True); os.replace(tmp, out)
        s = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", f"xi-api-key: {K}", "-F", "model_id=scribe_v1", "-F", "language_code=por", "-F", f"file=@{out}"], capture_output=True, text=True)
        print(out, "|", json.loads(s.stdout).get("text", "?"))
