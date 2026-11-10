import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { carregaFontes } from "./fontes";
import { Fundo } from "./Fundo";
import { Cartao, MOCKS, NomeMock } from "./Mock";
import { Tema, marca, tema } from "./marca";

carregaFontes();

export type PropsSlide = {
  tipo: "capa" | "etapa" | "numero" | "tempo" | "passos" | "fecho";
  tema?: Tema;
  assinatura?: "institucional" | "produto";
  rotulo?: string;
  /** "\n" quebra a linha; *palavras entre asteriscos* ganham a pilula de destaque. */
  titulo: string;
  apoio?: string;
  /** Numeral gigante: "01" na etapa, "30" na capa da oferta. */
  numero?: string;
  /** Tela do produto em miniatura. */
  mock?: NomeMock;
  giro?: number;
  /** Etiquetas curtas (pilulas). */
  chips?: string[];
  passos?: string[];
  /** Linha do tempo: [marco, texto]. */
  marcos?: [string, string][];
  /** Etapa atual de 5, para a barra de progresso. */
  etapa?: number;
  pagina?: string;
  rodape?: string;
  acao?: string;
};

const LOGOS: Record<string, Record<string, [string, number]>> = {
  institucional: { claro: ["profissio-licit-preto.svg", 300], escuro: ["profissio-licit-branco.svg", 300] },
  produto: { claro: ["licit-estrela-preto.svg", 190], escuro: ["licit-estrela-branco.svg", 190] },
};

export const cores = (t: Tema) => {
  const c = tema(t);
  const claro = t === "claro" || t === "acento";
  return {
    ...c,
    claro,
    pilulaFundo: t === "acento" ? marca.grafite : t === "claro" ? marca.floresta : marca.acento,
    pilulaTexto: t === "acento" ? marca.acento : t === "claro" ? marca.branco : marca.grafite,
    estrela: claro ? "estrela-licit-preto.svg" : "estrela-licit-branco.svg",
  };
};

/** Titulo com quebras manuais e *destaque* em pilula levemente girada. */
export const Titulo: React.FC<{ texto: string; t: Tema; tamanho: number; peso?: number }> = ({ texto, t, tamanho, peso = 500 }) => {
  const c = cores(t);
  return (
    <div style={{ fontSize: tamanho, fontWeight: peso, letterSpacing: "-0.04em", lineHeight: 1.08, color: c.texto }}>
      {texto.split("\n").map((linha, i) => (
        <div key={i}>
          {linha.split(/(\*[^*]+\*)/).map((parte, j) =>
            parte.startsWith("*") ? (
              <span
                key={j}
                style={{
                  display: "inline-block",
                  background: c.pilulaFundo,
                  color: c.pilulaTexto,
                  padding: `0 ${tamanho * 0.18}px ${tamanho * 0.06}px`,
                  margin: `${tamanho * 0.04}px 0`,
                  borderRadius: tamanho * 0.2,
                  transform: "rotate(-1.5deg)",
                }}
              >
                {parte.slice(1, -1)}
              </span>
            ) : (
              <span key={j}>{parte}</span>
            ),
          )}
        </div>
      ))}
    </div>
  );
};

const Pilula: React.FC<{ texto: string; t: Tema; cheia?: boolean; tam?: number }> = ({ texto, t, cheia = true, tam = 30 }) => {
  const c = cores(t);
  return (
    <span
      style={{
        display: "inline-block",
        background: cheia ? c.pilulaFundo : "transparent",
        color: cheia ? c.pilulaTexto : c.texto,
        border: cheia ? "none" : `2px solid ${c.texto}`,
        fontSize: tam,
        fontWeight: 600,
        padding: `${tam * 0.42}px ${tam * 0.85}px`,
        borderRadius: tam * 1.2,
        whiteSpace: "nowrap",
      }}
    >
      {texto}
    </span>
  );
};

/** Uma tela de carrossel 4:5. */
export const Slide: React.FC<PropsSlide> = (p) => {
  const t = p.tema ?? "escuro";
  const c = cores(t);
  const m = 84;
  const [logo, larguraLogo] = LOGOS[p.assinatura ?? "produto"][c.claro ? "claro" : "escuro"];
  const Mock = p.mock ? MOCKS[p.mock] : null;
  const rodape = p.rodape ?? "Toda a sua operação de licitações";

  return (
    <AbsoluteFill style={{ fontFamily: marca.fonte, color: c.texto, overflow: "hidden" }}>
      <Fundo variante={t} grade={p.tipo === "capa" || p.tipo === "fecho"} />

      {/* estrela gigante, sangrando pelo canto: e o grafismo de marca */}
      {p.tipo !== "etapa" ? (
        <Img
          src={staticFile(c.estrela)}
          style={{
            position: "absolute",
            width: 1150,
            right: -420,
            bottom: p.tipo === "numero" ? -330 : -480,
            opacity: t === "acento" ? 0.1 : 0.07,
            transform: "rotate(12deg)",
          }}
        />
      ) : null}

      {/* numeral gigante da etapa */}
      {p.tipo === "etapa" && p.numero ? (
        <div
          style={{
            position: "absolute",
            right: m - 14,
            top: 44,
            fontSize: 330,
            fontWeight: 600,
            letterSpacing: "-0.06em",
            lineHeight: 1,
            color: c.destaque,
            opacity: 0.95,
          }}
        >
          {p.numero}
        </div>
      ) : null}

      <AbsoluteFill style={{ padding: m, justifyContent: "space-between" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", height: 70 }}>
          <Img src={staticFile(logo)} style={{ width: larguraLogo, display: "block" }} />
          {p.pagina && p.tipo !== "etapa" ? <div style={{ fontSize: 26, color: c.textoApagado, fontWeight: 500 }}>{p.pagina}</div> : null}
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", justifyContent: p.tipo === "etapa" ? "flex-start" : "center", paddingTop: p.tipo === "etapa" ? 118 : 0 }}>
          {p.rotulo ? (
            <div style={{ marginBottom: 30 }}>
              <Pilula texto={p.rotulo} t={t} cheia={false} tam={24} />
            </div>
          ) : null}

          {p.tipo === "numero" && p.numero ? (
            <div style={{ fontSize: 520, fontWeight: 600, letterSpacing: "-0.07em", lineHeight: 0.82, color: c.texto, marginLeft: -22, marginBottom: 26 }}>
              {p.numero}
            </div>
          ) : null}

          <Titulo
            texto={p.titulo}
            t={t}
            tamanho={p.tipo === "capa" ? 108 : p.tipo === "fecho" ? 96 : p.tipo === "numero" ? 86 : p.tipo === "etapa" ? 66 : 78}
          />

          {p.apoio ? (
            <div style={{ fontSize: p.tipo === "etapa" ? 32 : 36, lineHeight: 1.36, color: c.textoSecundario, marginTop: p.tipo === "etapa" ? 22 : 30, maxWidth: 860 }}>{p.apoio}</div>
          ) : null}

          {p.chips ? (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 16, marginTop: 40 }}>
              {p.chips.map((ch, i) => (
                <Pilula key={ch} texto={ch} t={t} cheia={i === 0} tam={32} />
              ))}
            </div>
          ) : null}

          {Mock ? (
            <div style={{ marginTop: 40, transform: "scale(0.9)", transformOrigin: "top left", width: 1013, height: 0 }}>
              <Cartao largura={1013} giro={p.giro ?? 0}>
                <Mock p={1} />
              </Cartao>
            </div>
          ) : null}

          {p.passos ? (
            <div style={{ marginTop: 44 }}>
              {p.passos.map((ps, i) => (
                <div key={i} style={{ display: "flex", gap: 30, alignItems: "center", padding: "22px 0" }}>
                  <div
                    style={{
                      width: 92,
                      height: 92,
                      borderRadius: 46,
                      background: c.pilulaFundo,
                      color: c.pilulaTexto,
                      fontSize: 46,
                      fontWeight: 600,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                    }}
                  >
                    {i + 1}
                  </div>
                  <div style={{ fontSize: 44, lineHeight: 1.2, fontWeight: 500, letterSpacing: "-0.02em" }}>{ps}</div>
                </div>
              ))}
            </div>
          ) : null}

          {p.marcos ? (
            <div style={{ marginTop: 56, position: "relative", paddingLeft: 64 }}>
              <div style={{ position: "absolute", left: 21, top: 26, bottom: 60, width: 4, background: c.pilulaFundo, opacity: 0.5 }} />
              {p.marcos.map(([marco, texto], i) => (
                <div key={i} style={{ position: "relative", marginBottom: 44 }}>
                  <div
                    style={{
                      position: "absolute",
                      left: -64,
                      top: 6,
                      width: 46,
                      height: 46,
                      borderRadius: 23,
                      background: i === p.marcos!.length - 1 ? "transparent" : c.pilulaFundo,
                      border: `4px solid ${c.pilulaFundo}`,
                      boxSizing: "border-box",
                    }}
                  />
                  <div style={{ fontSize: 30, fontWeight: 600, color: c.destaque, letterSpacing: "0.04em", textTransform: "uppercase" }}>{marco}</div>
                  <div style={{ fontSize: 42, lineHeight: 1.22, fontWeight: 500, letterSpacing: "-0.02em", marginTop: 6 }}>{texto}</div>
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div>
          {p.etapa ? (
            <div style={{ display: "flex", gap: 10, marginBottom: 26 }}>
              {[1, 2, 3, 4, 5].map((n) => (
                <div key={n} style={{ flex: 1, height: 8, borderRadius: 4, background: n <= p.etapa! ? c.destaque : c.borda }} />
              ))}
            </div>
          ) : (
            <div style={{ height: 1, backgroundColor: c.borda, marginBottom: 26 }} />
          )}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 26, minHeight: 56 }}>
            <div style={{ color: c.textoSecundario }}>{rodape}</div>
            {p.acao ? <Pilula texto={p.acao} t={t} tam={26} /> : p.pagina && p.tipo === "etapa" ? <div style={{ color: c.textoApagado }}>{p.pagina}</div> : null}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
