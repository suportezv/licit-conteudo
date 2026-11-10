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

/*
 * LINHA DO TEMPO UNICA, em segundos. Cada elemento visual e o seu efeito
 * sonoro leem o MESMO numero: e isso que mantem som e imagem juntos.
 * Os efeitos em public/sfx foram aparados para comecar a soar no instante 0
 * (silenceremove a -40 dB). O "tick" da biblioteca e um toc fraco que some
 * por baixo da trilha (25 dB abaixo dela, medido); as linhas usam "tique",
 * um toque curto de 1,85 kHz gerado por ffmpeg (aevalsrc) para este filme.
 * Tempos das cenas sao locais (a partir do inicio da cena).
 */
export const TL = {
  virada: 0.7, // a cena nova sobe por cima da anterior, que recua
  abertura: { fim: 3.2, estrela: 0, linhas: [1.0, 1.28] },
  gancho: { fim: 8.5, primeira: 0.55, passo: 0.42 },
  etapa: { dur: 3.3, numero: 0.42, nome: 0.55, cartao: 0.85, linhas: [1.35, 1.72, 2.09] },
  oferta: { conta: 0.62, contaDur: 1.1, texto: 1.82, chips: [2.4, 2.8], rodape: 3.35 },
  total: 30,
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

/** Segundos desde o inicio da cena, para os movimentos continuos (nada fica parado). */
const useSeg = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return frame / fps;
};

const Cena: React.FC<{ t: Tema; children: React.ReactNode; grade?: boolean }> = ({ t, children, grade = false }) => (
  <AbsoluteFill style={{ overflow: "hidden", fontFamily: marca.fonte }}>
    <Fundo variante={t} grade={grade} />
    {children}
  </AbsoluteFill>
);

const Sobe: React.FC<{ v: number; children: React.ReactNode; d?: number; estilo?: React.CSSProperties }> = ({ v, children, d = 40, estilo }) => (
  <div style={{ opacity: Math.min(1, v * 1.4), transform: `translateY(${(1 - v) * d}px)`, ...estilo }}>{children}</div>
);

const Som: React.FC<{ em: number; arquivo: string; volume?: number }> = ({ em, arquivo, volume = 0.5 }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.round(em * fps)} layout="none">
      <Audio src={staticFile(`sfx/${arquivo}.mp3`)} volume={volume} />
    </Sequence>
  );
};

/** 1. A estrela chega girando, recua e segue girando devagar; a frase entra em duas linhas. */
const Abertura: React.FC<{ texto: string }> = ({ texto }) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  const T = useT();
  const seg = useSeg();
  const A = TL.abertura;
  const s = spring({ frame, fps, config: { damping: 13, mass: 0.9 } });
  const recua = T(A.linhas[0] - 0.1, 0.6);
  const linhas = texto.split("\n");
  return (
    <Cena t="escuro" grade>
      <Img
        src={staticFile("estrela-licit-branco.svg")}
        style={{
          position: "absolute",
          width: 1500,
          left: width / 2 - 750,
          top: 260,
          transform: `translateY(${interpolate(s, [0, 1], [220, 0])}px) scale(${interpolate(s, [0, 1], [0.05, 1]) * interpolate(recua, [0, 1], [0.62, 1.3])})`, // a estrela nunca gira: chega de longe
          opacity: interpolate(recua, [0, 1], [1, 0.1]),
        }}
      />
      <AbsoluteFill style={{ padding: `${TOPO}px ${M}px ${BASE}px`, justifyContent: "center" }}>
        <div style={{ transform: `scale(${1 + Math.max(0, seg - A.linhas[1]) * 0.012})`, transformOrigin: "left center" }}>
          {linhas.map((l, i) => (
            <Sobe key={i} v={T(A.linhas[i], 0.42)} d={80}>
              <Titulo texto={l} t="escuro" tamanho={186} />
            </Sobe>
          ))}
        </div>
      </AbsoluteFill>
    </Cena>
  );
};

/** 2. O gancho, linha a linha, com aproximacao lenta enquanto se le. */
const Gancho: React.FC<{ texto: string }> = ({ texto }) => {
  const T = useT();
  const seg = useSeg();
  const G = TL.gancho;
  const linhas = texto.split("\n");
  return (
    <Cena t="floresta">
      <Img
        src={staticFile("estrela-licit-branco.svg")}
        style={{ position: "absolute", width: 1500, right: -620, bottom: -260, opacity: 0.07, transform: `translateY(${-seg * 6}px)` }}
      />
      <AbsoluteFill style={{ padding: `${TOPO}px ${M}px ${BASE}px`, justifyContent: "center" }}>
        <div style={{ transform: `scale(${1 + seg * 0.006})`, transformOrigin: "left center" }}>
          {linhas.map((l, i) => (
            <Sobe key={i} v={T(G.primeira + i * G.passo, 0.4)} d={60}>
              <Titulo texto={l} t="floresta" tamanho={122} />
            </Sobe>
          ))}
        </div>
      </AbsoluteFill>
    </Cena>
  );
};

/** 3. Uma etapa: numeral gigante, o verbo e a tela do produto chegando de longe, em 3D. */
const Etapa: React.FC<{ n: number; nome: string; mock: NomeMock; t: Tema }> = ({ n, nome, mock, t }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const T = useT();
  const seg = useSeg();
  const E = TL.etapa;
  const c = cores(t);
  const Mock = MOCKS[mock];
  const num = T(E.numero, 0.45);
  const card = spring({ frame: frame - Math.round(E.cartao * fps), fps, config: { damping: 15, mass: 1.1 } });
  const linhas = E.linhas.reduce((soma, ini) => soma + T(ini, 0.32), 0);
  const lado = n % 2 ? -1 : 1;
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
          transform: `translateX(${(1 - num) * 160 - seg * 6}px)`,
        }}
      >
        {String(n).padStart(2, "0")}
      </div>
      <Img src={staticFile("licit-estrela-branco.svg")} style={{ position: "absolute", left: M, top: TOPO, width: 230 }} />
      <AbsoluteFill style={{ padding: `${TOPO + 380}px ${M}px ${BASE}px` }}>
        <Sobe v={T(E.nome, 0.4)} d={50}>
          <div style={{ fontSize: 150, fontWeight: 500, letterSpacing: "-0.045em", lineHeight: 1, color: c.texto }}>{nome}</div>
        </Sobe>
        <div style={{ marginTop: 56, perspective: 1300, perspectiveOrigin: "50% 30%" }}>
          <div
            style={{
              opacity: Math.min(1, card * 2),
              transformStyle: "preserve-3d",
              transform: [
                `translateY(${(1 - card) * 260 + Math.sin(seg * 1.6) * 7}px)`,
                `translateZ(${(1 - card) * -700}px)`,
                `rotateX(${(1 - card) * 58}deg)`,
                `rotateY(${(1 - card) * 26 * lado + Math.sin(seg * 1.1) * 2.2}deg)`,
                `rotate(${1.5 * lado * card}deg)`,
              ].join(" "),
            }}
          >
            <Cartao largura={896}>
              <Mock p={linhas} />
            </Cartao>
          </div>
        </div>
        <div style={{ position: "absolute", left: M, right: M, bottom: BASE - 10, display: "flex", gap: 12 }}>
          {[1, 2, 3, 4, 5].map((k) => (
            <div key={k} style={{ flex: 1, height: 10, borderRadius: 5, background: c.borda, overflow: "hidden" }}>
              <div style={{ height: 10, width: k < n ? "100%" : k === n ? `${T(0, E.dur) * 100}%` : "0%", background: c.destaque }} />
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
  const seg = useSeg();
  const O = TL.oferta;
  const c = cores("acento");
  const conta = Math.round(T(O.conta, O.contaDur) * numero);
  const pulso = spring({ frame: frame - Math.round((O.conta + O.contaDur) * fps), fps, config: { damping: 9 } });
  return (
    <Cena t="acento">
      <Img
        src={staticFile("estrela-licit-preto.svg")}
        style={{ position: "absolute", width: 1500, right: -560, bottom: -120, opacity: 0.1, transform: `translateY(${-seg * 6}px)` }}
      />
      <Img src={staticFile("profissio-licit-preto.svg")} style={{ position: "absolute", left: M, top: TOPO, width: 420, opacity: T(O.conta, 0.4) }} />
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
            opacity: T(O.conta - 0.08, 0.16),
          }}
        >
          {conta}
        </div>
        <Sobe v={T(O.texto, 0.4)} d={50}>
          <div style={{ fontSize: 112, fontWeight: 500, letterSpacing: "-0.04em", lineHeight: 1.06, marginTop: 24 }}>
            {texto.split("\n").map((l, i) => (
              <div key={i}>{l}</div>
            ))}
          </div>
        </Sobe>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 18, marginTop: 50 }}>
          {chips.map((ch, i) => {
            const e = spring({ frame: frame - Math.round(O.chips[i] * fps), fps, config: { damping: 11 } });
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
          opacity: T(O.rodape, 0.4),
          transform: `translateY(${(1 - T(O.rodape, 0.4)) * 30}px)`,
          fontFamily: marca.fonte,
        }}
      >
        <div style={{ fontSize: 30, color: c.textoSecundario }}>{rodape}</div>
        <span style={{ background: marca.grafite, color: marca.acento, fontSize: 34, fontWeight: 600, padding: "14px 32px", borderRadius: 50 }}>{acao}</span>
      </div>
    </Cena>
  );
};

/**
 * Uma cena do filme. Entra subindo por cima da anterior (o movimento da versao
 * aprovada), com profundidade em camadas: quem sai recua para o fundo
 * (diminui, escurece, desfoca de leve); quem entra sobe com sombra e cantos
 * arredondados que se abrem ate a tela cheia; o conteudo da cena chega um
 * pouco depois do proprio fundo, como uma camada mais perto da camera.
 */
const Face: React.FC<{ ini: number; fim: number | null; children: React.ReactNode }> = ({ ini, fim, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const V = TL.virada;
  const t = frame / fps;
  const ease = (x: number) => curva(Math.max(0, Math.min(1, x)));
  const entra = ini === 0 ? 1 : ease((t - ini) / V);
  // o conteudo atrasa um pouco em relacao ao fundo da cena: paralaxe
  const conteudo = ini === 0 ? 1 : ease((t - ini - 0.08) / V);
  const sai = fim === null ? 0 : ease((t - fim) / V);
  if (t < ini || (fim !== null && t > fim + V)) return null;
  const subindo = entra < 1;
  return (
    <AbsoluteFill
      style={{
        transform: subindo
          ? `translateY(${(1 - entra) * 100}%) scale(${1.06 - 0.06 * entra})`
          : `translateY(${-sai * 7}%) scale(${1 - 0.12 * sai})`,
        transformOrigin: "50% 0%",
        borderRadius: subindo ? (1 - entra) * 90 : sai * 60,
        overflow: "hidden",
        boxShadow: subindo ? `0 -50px 120px rgba(0,0,0,${0.75 * (1 - entra)})` : "none",
        filter: sai > 0 ? `blur(${sai * 6}px)` : "none",
      }}
    >
      <Sequence from={Math.round(ini * fps)} layout="none">
        <AbsoluteFill style={{ transform: `translateY(${(1 - conteudo) * 14}%)` }}>{children}</AbsoluteFill>
      </Sequence>
      <AbsoluteFill style={{ backgroundColor: "#000", opacity: sai * 0.6, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};

/** Filme de anuncio, 9:16, 30 s, sem narracao: abertura, gancho, cinco etapas e a oferta. */
export const Anuncio: React.FC<PropsAnuncio> = ({ abertura, gancho, etapas, numero, oferta, chips, acao, rodape, trilha }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const t = frame / fps;
  const V = TL.virada;

  // inicio de cada cena, em segundos do filme
  const inicios = [0, TL.abertura.fim, TL.gancho.fim];
  etapas.forEach((_, i) => inicios.push(TL.gancho.fim + (i + 1) * TL.etapa.dur));
  const iniEtapa = (i: number) => TL.gancho.fim + i * TL.etapa.dur;
  const iniOferta = iniEtapa(etapas.length);
  const fimDe = (i: number) => (i + 1 < inicios.length ? inicios[i + 1] : null);

  const vol = (fr: number) =>
    interpolate(fr, [0, fps * 0.6, durationInFrames - fps * 1.6, durationInFrames], [0, 0.3, 0.3, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const G = TL.gancho;
  const linhasGancho = gancho.split("\n");
  const E = TL.etapa;
  const O = TL.oferta;

  return (
    <AbsoluteFill style={{ backgroundColor: "#07080B" }}>
      {trilha ? <Audio src={staticFile(trilha)} volume={vol} /> : null}

      {/* efeitos: todos lidos da mesma linha do tempo das imagens */}
      <Som em={TL.abertura.estrela} arquivo="sweep" volume={0.5} />
      {TL.abertura.linhas.map((s, i) => (
        <Som key={`a${i}`} em={s} arquivo={i === 1 ? "pop" : "tique"} volume={i === 1 ? 0.55 : 0.6} />
      ))}
      {inicios.slice(1).map((s, i) => (
        <Som key={`v${i}`} em={s} arquivo={s === iniOferta ? "swell" : "move"} volume={0.45} />
      ))}
      {linhasGancho.map((l, i) => (
        <Som key={`g${i}`} em={TL.abertura.fim + G.primeira + i * G.passo} arquivo={l.includes("*") ? "pop" : "tique"} volume={l.includes("*") ? 0.55 : 0.6} />
      ))}
      {etapas.map((_, i) => (
        <React.Fragment key={`e${i}`}>
          <Som em={iniEtapa(i) + E.nome} arquivo="click" volume={0.45} />
          <Som em={iniEtapa(i) + E.cartao} arquivo="pop" volume={0.45} />
          {E.linhas.map((s, k) => (
            <Som key={k} em={iniEtapa(i) + s} arquivo="tique" volume={0.5} />
          ))}
        </React.Fragment>
      ))}
      <Som em={iniOferta + O.conta} arquivo="counter" volume={0.5} />
      <Som em={iniOferta + O.texto} arquivo="pop" volume={0.5} />
      {O.chips.map((s, i) => (
        <Som key={`c${i}`} em={iniOferta + s} arquivo="pop" volume={0.55} />
      ))}
      <Som em={iniOferta + O.rodape} arquivo="shimmer" volume={0.4} />

      <AbsoluteFill>
        <Face ini={0} fim={fimDe(0)}>
          <Abertura texto={abertura} />
        </Face>
        <Face ini={inicios[1]} fim={fimDe(1)}>
          <Gancho texto={gancho} />
        </Face>
        {etapas.map(([nome, mock], i) => (
          <Face key={nome} ini={inicios[2 + i]} fim={fimDe(2 + i)}>
            <Etapa n={i + 1} nome={nome} mock={mock} t={i % 2 ? "floresta" : "escuro"} />
          </Face>
        ))}
        <Face ini={iniOferta} fim={null}>
          <Oferta numero={numero} texto={oferta} chips={chips} acao={acao} rodape={rodape} />
        </Face>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
