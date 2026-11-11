#!/usr/bin/env python3
"""Versao em video (9:16, para Shorts e TikTok) de cada carrossel: as telas 4:5 com zoom lento, transicao de arrastar,
narracao do Juliano, whoosh em cada troca, trilha da marca baixa e barra de progresso. Master -14 LUFS."""
import json, os, subprocess, sys
from PIL import Image
AQ = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(AQ, "..", ".."))
WH = os.path.join(R, "projects/03-por-dentro-pregao/video/assets/audio/whoosh.mp3")
TRILHA = os.path.join(R, "remotion/public/trilha-tech-warm-33s.mp3")
TR, LEAD, TAIL = 0.4, 0.35, 0.6
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def run(a): r = subprocess.run(a, capture_output=True, text=True); (r.returncode and sys.exit(r.stderr[-2000:]))
N = json.load(open(os.path.join(AQ, "narracao.json")))
for peca in sys.argv[1:] or N:
    n = len(N[peca]); tmp = os.path.join(AQ, "video", "tmp"); os.makedirs(tmp, exist_ok=True)
    nd = [dur(os.path.join(AQ, f"video/audio/{peca}-{i+1:02d}.mp3")) for i in range(n)]
    D = [LEAD + d + 0.45 + (TR if 0 < i < n - 1 else TR / 2) + (1.6 if i == n - 1 else 0) for i, d in enumerate(nd)]
    clips = []
    for i in range(n):
        png = os.path.join(AQ, f"out/{peca}-{i+1:02d}.png"); im = Image.open(png).convert("RGB")
        bg = "#%02x%02x%02x" % im.getpixel((6, 700)); fr = round(D[i] * 30)
        out = os.path.join(tmp, f"c{i}.mp4"); clips.append(out)
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", "30", "-t", f"{D[i]:.3f}", "-i", png, "-vf",
             f"scale=2160:-1,zoompan=z='1+0.05*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1350:fps=30,pad=1080:1920:0:285:color={bg},format=yuv420p",
             "-c:v", "libx264", "-crf", "16", "-preset", "medium", out])
    # encadeia com xfade (arrastar para a esquerda, como o carrossel)
    args = ["ffmpeg", "-v", "error", "-y"]; [args.extend(["-i", c]) for c in clips]
    f = []; prev = "[0:v]"; off = 0.0; starts = [0.0]
    for i in range(1, n):
        off += D[i - 1] - TR; starts.append(off); lab = f"[x{i}]"
        f.append(f"{prev}[{i}:v]xfade=transition=slideleft:duration={TR}:offset={off:.3f}{lab}"); prev = lab
    T = off + D[-1]
    f.append(f"color=c=0xA8F27A:s=1080x12:d={T:.3f}[bar];{prev}[bar]overlay=x='-W+W*t/{T:.3f}':y=1868:shortest=1[v]")
    # audio: narracao, whoosh nas trocas, trilha baixa em loop
    ai = n; aud = []
    for i in range(n):
        args.extend(["-i", os.path.join(AQ, f"video/audio/{peca}-{i+1:02d}.mp3")]); ms = int((starts[i] + LEAD + (TR / 2 if i else 0)) * 1000)
        aud.append(f"[{ai}:a]adelay={ms}|{ms}[n{i}]"); ai += 1
    for i in range(1, n):
        args.extend(["-i", WH]); ms = int(max(0, starts[i] - 0.05) * 1000); aud.append(f"[{ai}:a]volume=0.5,adelay={ms}|{ms}[w{i}]"); ai += 1
    args.extend(["-stream_loop", "-1", "-i", TRILHA]); aud.append(f"[{ai}:a]atrim=0:{T:.3f},volume=0.16,afade=t=in:d=0.8,afade=t=out:st={T-1.5:.3f}:d=1.5[tr]")
    mix = "".join(f"[n{i}]" for i in range(n)) + "".join(f"[w{i}]" for i in range(1, n)) + "[tr]"
    aud.append(f"{mix}amix=inputs={n + n - 1 + 1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    final = os.path.join(AQ, f"video/{peca}-shorts.mp4")
    args += ["-filter_complex", ";".join(f + aud), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{T:.3f}", final]
    run(args); print(final, round(T, 1), "s")
