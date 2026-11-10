import React from "react";
import { AbsoluteFill, Audio, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { carregaFontes } from "./fontes";
import { Fundo } from "./Fundo";
import { Cartao, MOCKS, NomeMock } from "./Mock";
import { Titulo, cores } from "./Slide";
import { Tema, marca } from "./marca";

carregaFontes();

export type PropsAnuncio = {
  abertura: string;
  gancho: string;
  /** [nome da etapa, tela do produto] */
  etapas: [string, NomeMock][];
  numero: number;
  oferta: string;
  chips: string[];
  acao: string;
  rodape: string;
  /** Arquivo de trilha em public/, ou vazio para sair sem trilha. */
  trilha?: string;
};

const curva = Easing.bezier(...marca.curva);
const M = 92; // margem lateral
const TOPO = 220; // area segura do 9:16
const BASE = 420;

/** 0 a 1 a partir de `ini` segundos da cena, com a curva do sistema. */
const useT = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (ini: number, dur = 0.4) =>
    interpolate(frame, [ini * fps, (ini + dur) * fps], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: curva });
};

/** A cena entra subindo por cima da anterior. */
const Cena: React.FC<{ t: Tema; children: React.ReactNode; entra?: boolean; grade?: boolean }> = ({ t, children, entra = true, grade = false }) => {
  const T = useT();
  const e = entra ? T(0, 0.38) : 1;
  return (
    <AbsoluteFill style={{ transform: `translateY(${(1 - e) * 100}%)`, overflow: "hidden", fontFamily: marca.fonte }}>
      <Fundo variante={t} grade={grade} />
      {children}
    </AbsoluteFill>
  );
};

const Sobe: React.FC<{ v: number; children: React.ReactNode; d?: number; estilo?: React.CSSProperties }> = ({ v, children, d = 40, estilo }) => (
  <div style={{ opacity: Math.min(1, v * 1.4), transform: `translateY(${(1 - v) * d}px)`, ...estilo }}>{children}</div>
);

const Som: React.FC<{ em: number; arquivo: string; volume?: number }> = ({ em, arquivo, volume = 0.55 }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.round(em * fps)} layout="none">
      <Audio src={staticFile(`sfx/${arquivo}.mp3`)} volume={volume} />
    </Sequence>
  );
};

/** 1. A estrela chega girando e a frase de abertura entra. */
const Abertura: React.FC<{ texto: string }> = ({ texto }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const T = useT();
  const s = spring({ frame, fps, config: { damping: 13, mass: 0.9 } });
  const recua = T(0.75, 0.5);
  return (
    <Cena t="escuro" entra={false} grade>
      <Img
        src={staticFile("estrela-licit-branco.svg")}
        style={{
          position: "absolute",
          width: 1500,
          left: width / 2 - 750,
          top: 260,
          transform: `scale(${interpolate(s, [0, 1], [0.05, 1]) * interpolate(recua, [0, 1], [0.62, 1.25])}) rotate(${interpolate(s, [0, 1], [-140, 0]) + recua * 14}deg)`,
          opacity: interpolate(recua, [0, 1], [1, 0.1]),
        }}
      />
      <AbsoluteFill style={{ padding: `${TOPO}px ${M}px ${BASE}px`, justifyContent: "center" }}>
        <Sobe v={T(0.85, 0.45)} d={70}>
          <Titulo texto={texto} t="escuro" tamanho={186} />
        </Sobe>
      </AbsoluteFill>
    </Cena>
  );
};

/** 2. O gancho, linha a linha. */
const Gancho: React.FC<{ texto: string }> = ({ texto }) => {
  const T = useT();
  const linhas = texto.split("\n");
  return (
    <Cena t="floresta">
      <Img src={staticFile("estrela-licit-branco.svg")} style={{ position: "absolute", width: 1500, right: -620, bottom: -260, opacity: 0.07, transform: `rotate(${12 + T(0, 3.6) * 10}deg)` }} />
      <AbsoluteFill style={{ padding: `${TOPO}px ${M}px ${BASE}px`, justifyContent: "center" }}>
        {linhas.map((l, i) => (
          <Sobe key={i} v={T(0.3 + i * 0.26, 0.4)} d={60}>
            <Titulo texto={l} t="floresta" tamanho={122} />
          </Sobe>
        ))}
      </AbsoluteFill>
    </Cena>
  );
};

/** 3. Uma etapa: numeral gigante, o verbo e a tela do produto montando. */
const Etapa: React.FC<{ n: number; nome: string; mock: NomeMock; t: Tema; dur: number }> = ({ n, nome, mock, t, dur }) => {
  const T = useT();
  const c = cores(t);
  const Mock = MOCKS[mock];
  const num = T(0.08, 0.4);
  const card = T(0.22, 0.45);
  return (
    <Cena t={t}>
      <div
        style={{
          position: "absolute",
          right: M - 20,
          top: TOPO - 60,
          fontSize: 420,
          fontWeight: 600,
          letterSpacing: "-0.06em",
          lineHeight: 1,
          color: c.destaque,
          opacity: num,
          transform: `translateX(${(1 - num) * 120}px)`,
        }}
      >
        {String(n).padStart(2, "0")}
      </div>
      <Img src={staticFile("licit-estrela-branco.svg")} style={{ position: "absolute", left: M, top: TOPO, width: 230 }} />
      <AbsoluteFill style={{ padding: `${TOPO + 380}px ${M}px ${BASE}px` }}>
        <Sobe v={T(0.14, 0.4)} d={50}>
          <div style={{ fontSize: 150, fontWeight: 500, letterSpacing: "-0.045em", lineHeight: 1, color: c.texto }}>{nome}</div>
        </Sobe>
        <div style={{ marginTop: 56, opacity: Math.min(1, card * 1.5), transform: `translateY(${(1 - card) * 160}px) rotate(${(n % 2 ? -1.5 : 1.5) * card}deg)` }}>
          <Cartao largura={896}>
            <Mock p={T(0.35, dur - 0.75)} />
          </Cartao>
        </div>
        {/* progresso das cinco etapas */}
        <div style={{ position: "absolute", left: M, right: M, bottom: BASE - 10, display: "flex", gap: 12 }}>
          {[1, 2, 3, 4, 5].map((k) => (
            <div key={k} style={{ flex: 1, height: 10, borderRadius: 5, background: c.borda, overflow: "hidden" }}>
              <div style={{ height: 10, width: k < n ? "100%" : k === n ? `${T(0, dur) * 100}%` : "0%", background: c.destaque }} />
            </div>
          ))}
        </div>
      </AbsoluteFill>
    </Cena>
  );
};

/** 4. A oferta: o bloco verde, o 30 contando e as condicoes. */
const Oferta: React.FC<{ numero: number; texto: string; chips: string[]; acao: string; rodape: string }> = ({ numero, texto, chips, acao, rodape }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = useT();
  const c = cores("acento");
  const conta = Math.round(T(0.3, 0.9) * numero);
  const pulso = spring({ frame: frame - Math.round(1.2 * fps), fps, config: { damping: 9 } });
  return (
    <Cena t="acento">
      <Img
        src={staticFile("estrela-licit-preto.svg")}
        style={{ position: "absolute", width: 1500, right: -560, bottom: -120, opacity: 0.1, transform: `rotate(${12 + T(0, 6) * 16}deg)` }}
      />
      <Img src={staticFile("profissio-licit-preto.svg")} style={{ position: "absolute", left: M, top: TOPO, width: 420, opacity: T(0.5, 0.4) }} />
      <AbsoluteFill style={{ padding: `${TOPO}px ${M}px ${BASE}px`, justifyContent: "center", color: c.texto }}>
        <div
          style={{
            fontSize: 640,
            fontWeight: 600,
            letterSpacing: "-0.07em",
            lineHeight: 0.84,
            marginLeft: -26,
            transform: `scale(${interpolate(pulso, [0, 1], [0.94, 1])})`,
            transformOrigin: "left bottom",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {conta}
        </div>
        <Sobe v={T(1.25, 0.4)} d={50}>
          <div style={{ fontSize: 112, fontWeight: 500, letterSpacing: "-0.04em", lineHeight: 1.06, marginTop: 24 }}>
            {texto.split("\n").map((l, i) => (
              <div key={i}>{l}</div>
            ))}
          </div>
        </Sobe>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 18, marginTop: 50 }}>
          {chips.map((ch, i) => {
            const e = spring({ frame: frame - Math.round((2.0 + i * 0.35) * fps), fps, config: { damping: 11 } });
            return (
              <span
                key={ch}
                style={{
                  display: "inline-block",
                  transform: `scale(${e})`,
                  background: i === 0 ? marca.grafite : "transparent",
                  color: i === 0 ? marca.acento : marca.grafite,
                  border: i === 0 ? "none" : `3px solid ${marca.grafite}`,
                  fontSize: 44,
                  fontWeight: 600,
                  padding: "18px 38px",
                  borderRadius: 60,
                }}
              >
                {ch}
              </span>
            );
          })}
        </div>
      </AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: M,
          right: M,
          bottom: BASE - 40,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          opacity: T(3.0, 0.4),
          fontFamily: marca.fonte,
        }}
      >
        <div style={{ fontSize: 30, color: c.textoSecundario }}>{rodape}</div>
        <span style={{ background: marca.grafite, color: marca.acento, fontSize: 34, fontWeight: 600, padding: "14px 32px", borderRadius: 50 }}>{acao}</span>
      </div>
    </Cena>
  );
};

/** Filme de anuncio, 9:16, 20 s, sem narracao: abertura, gancho, cinco etapas e a oferta. */
export const Anuncio: React.FC<PropsAnuncio> = ({ abertura, gancho, etapas, numero, oferta, chips, acao, rodape, trilha }) => {
  const { fps, durationInFrames } = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const A = 2.4; // fim da abertura
  const B = 6.2; // fim do gancho
  const DUR = 1.6; // cada etapa
  const C = B + etapas.length * DUR;
  const vol = (fr: number) =>
    interpolate(fr, [0, fps * 0.6, durationInFrames - fps * 1.4, durationInFrames], [0, 0.42, 0.42, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: marca.grafite }}>
      {trilha ? <Audio src={staticFile(trilha)} volume={vol} /> : null}
      <Som em={0.05} arquivo="sweep" />
      <Som em={0.85} arquivo="pop" />
      <Som em={A} arquivo="move" volume={0.45} />
      {etapas.map((_, i) => (
        <React.Fragment key={i}>
          <Som em={B + i * DUR} arquivo="move" volume={0.4} />
          <Som em={B + i * DUR + 0.3} arquivo="click" volume={0.5} />
        </React.Fragment>
      ))}
      <Som em={C} arquivo="swell" volume={0.5} />
      <Som em={C + 0.3} arquivo="counter" volume={0.5} />
      <Som em={C + 2.0} arquivo="pop" />
      <Som em={C + 2.35} arquivo="pop" />
      <Som em={C + 3.0} arquivo="shimmer" volume={0.45} />

      <Sequence durationInFrames={f(A) + f(0.4)}>
        <Abertura texto={abertura} />
      </Sequence>
      <Sequence from={f(A)} durationInFrames={f(B - A) + f(0.4)}>
        <Gancho texto={gancho} />
      </Sequence>
      {etapas.map(([nome, mock], i) => (
        <Sequence key={nome} from={f(B + i * DUR)} durationInFrames={f(DUR) + f(0.4)}>
          <Etapa n={i + 1} nome={nome} mock={mock} t={i % 2 ? "floresta" : "escuro"} dur={DUR} />
        </Sequence>
      ))}
      <Sequence from={f(C)}>
        <Oferta numero={numero} texto={oferta} chips={chips} acao={acao} rodape={rodape} />
      </Sequence>
    </AbsoluteFill>
  );
};
