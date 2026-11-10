import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { carregaFontes } from "./fontes";
import { Fundo } from "./Fundo";
import { marca, tema } from "./marca";

carregaFontes();

export type PropsAnuncio = {
  abertura: string;
  promessa: string;
  etapas: string[];
  oferta: string;
  prazo: string;
  rodape: string;
  /** Arquivo de trilha em public/, ou vazio para sair mudo. */
  trilha?: string;
};

const curva = Easing.bezier(...marca.curva);

/** Entra em `ini` e sai em `fim` (segundos do bloco), com a curva do sistema. */
const useEntra = (fps: number) => {
  const frame = useCurrentFrame();
  return (ini: number, fim?: number, dur = 0.45) => {
    const a = interpolate(frame, [ini * fps, (ini + dur) * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: curva,
    });
    if (fim === undefined) return a;
    const b = interpolate(frame, [(fim - 0.3) * fps, fim * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
    return Math.min(a, b);
  };
};

const Linhas: React.FC<{ texto: string; ini: number; fim?: number; tamanho: number; destaque?: string }> = ({
  texto,
  ini,
  fim,
  tamanho,
  destaque,
}) => {
  const { fps } = useVideoConfig();
  const entra = useEntra(fps);
  const c = tema("escuro");
  return (
    <div style={{ fontSize: tamanho, fontWeight: marca.peso.titulo, letterSpacing: marca.trackingTitulo, lineHeight: 1.14 }}>
      {texto.split("\n").map((l, i) => {
        const e = entra(ini + i * 0.16, fim);
        return (
          <div key={i} style={{ opacity: e, transform: `translateY(${interpolate(e, [0, 1], [18, 0])}px)` }}>
            {l.split(" ").map((p, j) => (
              <span key={j} style={{ color: destaque && p.replace(/[.,]/g, "") === destaque ? c.destaque : c.texto }}>
                {p}{" "}
              </span>
            ))}
          </div>
        );
      })}
    </div>
  );
};

/**
 * Filme de anuncio, 9:16, 18 s, sem narracao. Quatro estados que se sucedem
 * sem corte seco: abertura, promessa, as cinco etapas e a oferta.
 */
export const Anuncio: React.FC<PropsAnuncio> = ({ abertura, promessa, etapas, oferta, prazo, rodape, trilha }) => {
  const frame = useCurrentFrame();
  const { fps, width, durationInFrames } = useVideoConfig();
  const entra = useEntra(fps);
  const c = tema("escuro");
  const m = Math.round(width * 0.085);
  const T = { a: 0, b: 3.6, c: 8.2, d: 13.2 };
  // o fundo passa de grafite a floresta no estado final
  const paraFloresta = interpolate(frame, [(T.d - 0.4) * fps, (T.d + 0.5) * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const vol = (f: number) =>
    interpolate(f, [0, fps * 0.8, durationInFrames - fps * 1.5, durationInFrames], [0, 0.5, 0.5, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });

  return (
    <AbsoluteFill>
      <Fundo variante="escuro" />
      <AbsoluteFill style={{ opacity: paraFloresta }}>
        <Fundo variante="floresta" />
      </AbsoluteFill>
      {trilha ? <Audio src={staticFile(trilha)} volume={vol} /> : null}

      <AbsoluteFill style={{ padding: `220px ${m}px 420px`, fontFamily: marca.fonte, color: c.texto }}>
        {/* assinatura: estrela + Licit ate a oferta; institucional no fecho */}
        <div style={{ height: 90, position: "relative" }}>
          <Img
            src={staticFile("licit-estrela-branco.svg")}
            style={{ width: width * 0.24, position: "absolute", opacity: Math.min(entra(0.2), 1 - paraFloresta) }}
          />
          <Img
            src={staticFile("profissio-licit-branco.svg")}
            style={{ width: width * 0.4, position: "absolute", opacity: Math.min(entra(T.d + 0.3), paraFloresta) }}
          />
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: "center", position: "relative" }}>
          <Sequence from={0} durationInFrames={Math.round(T.b * fps)} layout="none">
            <div style={{ position: "absolute", left: 0, right: 0 }}>
              <Linhas texto={abertura} ini={0.7} fim={T.b} tamanho={Math.round(width * 0.105)} destaque="Licit" />
            </div>
          </Sequence>
          <Sequence from={Math.round(T.b * fps)} durationInFrames={Math.round((T.c - T.b) * fps)} layout="none">
            <div style={{ position: "absolute", left: 0, right: 0 }}>
              <Linhas texto={promessa} ini={0.15} fim={T.c - T.b} tamanho={Math.round(width * 0.078)} />
            </div>
          </Sequence>
          <Sequence from={Math.round(T.c * fps)} durationInFrames={Math.round((T.d - T.c) * fps)} layout="none">
            <Etapas etapas={etapas} dur={T.d - T.c} />
          </Sequence>
          <Sequence from={Math.round(T.d * fps)} layout="none">
            <div style={{ position: "absolute", left: 0, right: 0 }}>
              <Linhas texto={oferta} ini={0.4} tamanho={Math.round(width * 0.098)} destaque="30" />
              <Prazo texto={prazo} ini={1.3} />
            </div>
          </Sequence>
        </div>

        <div style={{ opacity: entra(1.2) }}>
          <div style={{ height: 1, backgroundColor: c.borda, marginBottom: 28 }} />
          <div style={{ fontSize: 28, color: c.textoSecundario }}>{rodape}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Prazo: React.FC<{ texto: string; ini: number }> = ({ texto, ini }) => {
  const { fps } = useVideoConfig();
  const entra = useEntra(fps);
  const c = tema("escuro");
  const e = entra(ini);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 22, marginTop: 44, opacity: e }}>
      <div style={{ width: interpolate(e, [0, 1], [0, 64]), height: 2, backgroundColor: c.destaque }} />
      <div style={{ fontSize: 38, color: c.texto }}>{texto}</div>
    </div>
  );
};

const Etapas: React.FC<{ etapas: string[]; dur: number }> = ({ etapas, dur }) => {
  const { fps } = useVideoConfig();
  const entra = useEntra(fps);
  const c = tema("escuro");
  return (
    <div style={{ position: "absolute", left: 0, right: 0 }}>
      {etapas.map((et, i) => {
        const e = entra(0.15 + i * 0.5, dur);
        return (
          <div
            key={et}
            style={{
              display: "flex",
              alignItems: "baseline",
              gap: 34,
              padding: "26px 0",
              borderTop: `1px solid ${c.borda}`,
              opacity: e,
              transform: `translateY(${interpolate(e, [0, 1], [14, 0])}px)`,
            }}
          >
            <div style={{ fontSize: 30, fontWeight: 500, color: c.destaque, width: 60 }}>{String(i + 1).padStart(2, "0")}</div>
            <div style={{ fontSize: 76, fontWeight: 500, letterSpacing: marca.trackingTitulo }}>{et}</div>
          </div>
        );
      })}
    </div>
  );
};
