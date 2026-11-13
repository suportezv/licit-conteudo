#!/usr/bin/env python3
"""Transcreve cada segmento da narracao com o Scribe (ElevenLabs) e grava
assets/audio/palavras.json: {segmento: [{w, s, e}, ...]} com tempo por palavra."""
import json, os, subprocess, sys
from pathlib import Path
KEY = os.environ["ELEVENLABS_API_KEY"]
out = {}
for p in sorted(Path("assets/audio").glob("n[0-9][0-9].mp3")):
    k = p.stem[1:]
    r = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text",
        "-H", f"xi-api-key: {KEY}", "-F", "model_id=scribe_v1", "-F", "language_code=por",
        "-F", "timestamps_granularity=word", "-F", "tag_audio_events=false", "-F", f"file=@{p}"],
        capture_output=True, text=True)
    try: j = json.loads(r.stdout)
    except Exception: print(k, "ERRO", r.stdout[:200], r.stderr[:200]); sys.exit(1)
    if "words" not in j: print(k, "ERRO", json.dumps(j)[:300]); sys.exit(1)
    ws = [{"w": w["text"], "s": round(w["start"], 3), "e": round(w["end"], 3)} for w in j["words"] if w.get("type") == "word"]
    out[k] = ws
    print(k, len(ws), "palavras", ws[0]["s"], "->", ws[-1]["e"], "|", j.get("text", "")[:80])
json.dump(out, open("assets/audio/palavras.json", "w"), ensure_ascii=False, indent=0)
print("ok", len(out))
