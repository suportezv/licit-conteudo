#!/usr/bin/env python3
"""Renderiza as tres pecas de estreia a partir de pecas.json.

    python3 projects/01-estreia/gera.py            # tudo
    python3 projects/01-estreia/gera.py etapas     # so um carrossel
    python3 projects/01-estreia/gera.py anuncio

Saida em projects/01-estreia/out/ (fora do git).
"""
import json, os, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
REM = os.path.normpath(os.path.join(AQUI, "..", "..", "remotion"))
OUT = os.path.join(AQUI, "out"); os.makedirs(OUT, exist_ok=True)
P = json.load(open(os.path.join(AQUI, "pecas.json"), encoding="utf8"))
quais = sys.argv[1:] or ["governo", "prazos"]

def remotion(*args):
    r = subprocess.run(["npx", "--no-install", "remotion", *args], cwd=REM, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stdout[-1500:] + r.stderr[-1500:])

for nome in ("governo", "prazos"):
    if nome not in quais: continue
    telas = P[nome]
    for i, t in enumerate(telas, 1):
        props = dict(t); props.setdefault("rodape", P["rodape"]); props["pagina"] = f"{i:02d}/{len(telas):02d}"
        pf = os.path.join(OUT, "_props.json"); json.dump(props, open(pf, "w"), ensure_ascii=False)
        dst = os.path.join(OUT, f"{nome}-{i:02d}.png")
        remotion("still", "src/index.ts", "Slide", dst, f"--props={pf}")
        print(dst)
if "anuncio" in quais:
    pf = os.path.join(OUT, "_props.json"); json.dump(P["anuncio"], open(pf, "w"), ensure_ascii=False)
    bruto = os.path.join(OUT, "_anuncio-bruto.mp4"); final = os.path.join(OUT, "anuncio-chegou-a-licit.mp4")
    remotion("render", "src/index.ts", "Anuncio", bruto, f"--props={pf}", "--codec=h264", "--crf=16", "--concurrency=4")
    # master em -14 LUFS, pico -1 dBTP
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", bruto, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,volume=-0.6dB",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", final], check=True)
    os.remove(bruto); print(final)
