#!/usr/bin/env python3
"""Normaliza o audio de um MP4 para o alvo de loudness da agencia (-14 LUFS, true peak -1 dBTP)
com o loudnorm do ffmpeg em duas passagens, sem recodificar o video.

uso: finaliza_audio.py entrada.mp4 saida.mp4 [--lufs -14] [--tp -1] [--lra 11]
Imprime a medicao antes e depois."""
import argparse, json, re, subprocess, sys

def medir(p):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = {}
    for chave, rx in [("I", r"I:\s+(-?[\d.]+) LUFS"), ("LRA", r"LRA:\s+([\d.]+) LU"), ("TP", r"Peak:\s+(-?[\d.]+) dBFS")]:
        r = re.findall(rx, out)
        m[chave] = float(r[-1]) if r else None
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("--lufs", type=float, default=-14.0); ap.add_argument("--tp", type=float, default=-1.0); ap.add_argument("--lra", type=float, default=11.0)
    a = ap.parse_args()
    antes = medir(a.entrada); print("antes :", antes)
    # passagem 1: medicao do loudnorm
    f1 = f"loudnorm=I={a.lufs}:TP={a.tp}:LRA={a.lra}:print_format=json"
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", a.entrada, "-af", f1, "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(err[err.rfind("{"):])
    f2 = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA={a.lra}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true:print_format=summary")
    # passagem 2: aplica, video copiado, audio AAC 192k 48 kHz
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", a.entrada, "-af", f2, "-ar", "48000",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.saida], capture_output=True, text=True)
    if r.returncode: print(r.stderr[-2000:]); sys.exit(1)
    depois = medir(a.saida); print("depois:", depois)
    if depois["I"] is None or abs(depois["I"] - a.lufs) > 1.0:
        print(f"AVISO: integrado {depois['I']} fora de +-1 LU do alvo {a.lufs}"); sys.exit(2)

if __name__ == "__main__":
    main()
