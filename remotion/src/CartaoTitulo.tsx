import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { carregaFontes } from "./fontes";
import { Fundo } from "./Fundo";
import { Tema, marca, tema } from "./marca";

carregaFontes();

export type PropsCartao = {
  /** Uma ou mais linhas curtas; "\n" quebra a linha onde o roteiro mandar. */
  titulo: string;
  /** Palavra do titulo que recebe a cor de destaque do tema. Opcional. */
  destaque?: string;
  /** Rotulo pequeno em caixa alta, acima do titulo. Opcional. */
  rotulo?: string;
  /** Linha de fecho. O padrao e a categoria aprovada da marca. */
  rodape?: string;
  tema?: Tema;
  /** "institucional" = Profissio Licit com P; "produto" = estrela + Licit. */
  assinatura?: "institucional" | "produto";
};

const LOGO = {
  institucional: { escuro: "profissio-licit-branco.svg", claro: "profissio-licit-grafite.svg", largura: 0.34 },
  produto: { escuro: "licit-estrela-branco.svg", claro: "licit-estrela-degrade.svg", largura: 0.22 },
};

/**
 * Cartao de titulo no molde dos modelos sociais da marca: assinatura no topo,
 * fio e rotulo, titulo em Sora 500 alinhado a esquerda, categoria no rodape.
 * Revelacao linha a linha, com a curva de movimento do sistema.
 */
export const CartaoTitulo: React.FC<PropsCartao> = ({
  titulo,
  destaque,
  rotulo,
  rodape = marca.categoria,
  tema: t = "escuro",
  assinatura = "institucional",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const c = tema(t);
  const linhas = titulo.split("\n");
  const margem = Math.round(width * 0.085);
  const curva = Easing.bezier(...marca.curva);
  const entra = (inicio: number, dur = 0.5) =>
    interpolate(frame, [inicio * fps, (inicio + dur) * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: curva,
    });
  const logo = LOGO[assinatura];
  const arquivo = t === "claro" ? logo.claro : logo.escuro;
  // area segura do 9:16: 220px no topo e 420px na base
  const vertical = height > width;
  const topo = vertical ? 220 : margem;
  const base = vertical ? 420 : margem;

  return (
    <AbsoluteFill>
      <Fundo variante={t} />
      <AbsoluteFill
        style={{
          padding: `${topo}px ${margem}px ${base}px`,
          fontFamily: marca.fonte,
          color: c.texto,
          justifyContent: "space-between",
        }}
      >
        <div style={{ opacity: entra(0.1) }}>
          <Img src={staticFile(arquivo)} style={{ width: width * logo.largura, display: "block" }} />
        </div>

        <div>
          {rotulo ? (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 20,
                marginBottom: 36,
                opacity: entra(0.35),
              }}
            >
              <div style={{ width: 56, height: 2, backgroundColor: c.destaque }} />
              <div
                style={{
                  fontSize: 22,
                  fontWeight: marca.peso.titulo,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  color: c.destaque,
                }}
              >
                {rotulo}
              </div>
            </div>
          ) : null}
          <div
            style={{
              fontSize: Math.round(width * 0.074),
              fontWeight: marca.peso.titulo,
              letterSpacing: marca.trackingTitulo,
              lineHeight: 1.16,
            }}
          >
            {linhas.map((linha, i) => {
              const e = entra(0.55 + i * 0.18);
              return (
                <div
                  key={i}
                  style={{ opacity: e, transform: `translateY(${interpolate(e, [0, 1], [18, 0])}px)` }}
                >
                  {linha.split(" ").map((p, j) => {
                    const eh =
                      destaque && p.replace(/[.,!?]/g, "").toLowerCase() === destaque.toLowerCase();
                    return (
                      <span key={j} style={{ color: eh ? c.destaque : c.texto }}>
                        {p}{" "}
                      </span>
                    );
                  })}
                </div>
              );
            })}
          </div>
        </div>

        <div style={{ opacity: entra(0.55 + linhas.length * 0.18 + 0.3) }}>
          <div style={{ height: 1, backgroundColor: c.borda, marginBottom: 28 }} />
          <div style={{ fontSize: 26, fontWeight: marca.peso.corpo, color: c.textoSecundario }}>{rodape}</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
