import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { Tema, tema } from "./marca";

/**
 * Fundo do estudio na gramatica da marca: plano chapado com uma grade tecnica
 * discreta num dos lados (fundo "03 Grade Tecnica" do kit). Sem brilho difuso,
 * sem ruido e sem movimento atras do texto: o manual pede superficie plana
 * onde ha leitura. A grade so respira de leve na opacidade.
 */
export const Fundo: React.FC<{ variante?: Tema }> = ({ variante = "escuro" }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, width, height } = useVideoConfig();
  const c = tema(variante);
  const passo = 64;
  const inicio = Math.round((width * 0.56) / passo) * passo;
  const colunas = Array.from({ length: Math.ceil((width - inicio) / passo) + 1 }, (_, i) => inicio + i * passo);
  const linhas = Array.from({ length: Math.ceil(height / passo) + 1 }, (_, i) => i * passo);
  const op = interpolate(frame, [0, durationInFrames], [0.045, 0.06]);

  return (
    <AbsoluteFill style={{ backgroundColor: c.fundo }}>
      <svg width={width} height={height} style={{ position: "absolute", inset: 0 }}>
        <defs>
          <linearGradient id="some" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0" stopColor="#fff" stopOpacity="0" />
            <stop offset="0.35" stopColor="#fff" stopOpacity="1" />
          </linearGradient>
          <mask id="mascara">
            <rect x={inicio} y={0} width={width - inicio} height={height} fill="url(#some)" />
          </mask>
        </defs>
        <g stroke={c.linha} strokeWidth={1} opacity={op} mask="url(#mascara)">
          {colunas.map((x) => (
            <line key={`c${x}`} x1={x} y1={0} x2={x} y2={height} />
          ))}
          {linhas.map((y) => (
            <line key={`l${y}`} x1={inicio} y1={y} x2={width} y2={y} />
          ))}
        </g>
      </svg>
    </AbsoluteFill>
  );
};
