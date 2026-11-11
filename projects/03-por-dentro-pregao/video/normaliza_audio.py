#!/usr/bin/env python3
"""Nivela os arquivos de audio do projeto para o mix nao depender de sorte:
narracao nKK.mp3 em -19 LUFS, efeitos de um tiro em -28 LUFS (9 dB abaixo da voz).
bed.mp3 e tick_loop.mp3 ficam como estao (o data-volume deles ja foi medido).
Ganho linear por arquivo (filtro volume), sem compressao, recodificado a 192 kbps."""
import json, re, subprocess, sys
from pathlib import Path
ALVO_VOZ, ALVO_SFX = -19.0, -28.0
EXCLUI = {"bed", "tick_loop"}
def lufs(p):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    r = re.findall(r"I:\s+(-?[\d.]+) LUFS", out); return float(r[-1]) if r else None
rel = {}
for p in sorted(Path("assets/audio").glob("*.mp3")):
    if p.stem in EXCLUI: continue
    voz = bool(re.fullmatch(r"n\d\d", p.stem)); alvo = ALVO_VOZ if voz else ALVO_SFX
    i = lufs(p)
    if i is None or i < -60: print(p.name, "sem medida, pulado"); continue
    g = alvo - i
    tmp = p.with_suffix(".tmp.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-af", f"volume={g:.2f}dB", "-ar", "44100", "-codec:a", "libmp3lame", "-b:a", "192k", str(tmp)], check=True)
    tmp.replace(p); rel[p.stem] = (round(i, 1), round(lufs(p), 1))
for k, (a, b) in rel.items(): print(f"{k:14s} {a:7.1f} -> {b:6.1f} LUFS")
