import React from "react";
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { carregaFontes } from "./fontes";
import { Fundo } from "./Fundo";
import { Tema, marca, tema } from "./marca";

carregaFontes();

export type PropsSlide = {
  /** capa e fecho sao areas de marca (com grade); etapa e passos carregam dado (plano chapado). */
  tipo: "capa" | "etapa" | "passos" | "fecho";
  tema?: Tema;
  assinatura?: "institucional" | "produto";
  rotulo?: string;
  titulo: string;
  destaque?: string;
  apoio?: string;
  /** "01" na etapa. */
  numero?: string;
  /** Cartao de dados: rotulo pequeno + linhas [chave, valor]. */
  cartaoRotulo?: string;
  linhas?: [string, string][];
  /** Lista numerada (tipo "passos"). */
  passos?: string[];
  /** "02/07" no canto. */
  pagina?: string;
  rodape?: string;
  /** Linha final a direita do rodape ("Arraste", "Link na bio"). */
  acao?: string;
};

const LOGO = {
  institucional: { escuro: "profissio-licit-branco.svg", claro: "profissio-licit-grafite.svg", largura: 300 },
  produto: { escuro: "licit-estrela-branco.svg", claro: "licit-estrela-degrade.svg", largura: 190 },
};

const Titulo: React.FC<{ texto: string; destaque?: string; cor: string; corDestaque: string; tamanho: number }> = ({
  texto,
  destaque,
  cor,
  corDestaque,
  tamanho,
}) => (
  <div style={{ fontSize: tamanho, fontWeight: marca.peso.titulo, letterSpacing: marca.trackingTitulo, lineHeight: 1.14 }}>
    {texto.split("\n").map((linha, i) => (
      <div key={i}>
        {linha.split(" ").map((p, j) => {
          const eh = destaque && p.replace(/[.,!?]/g, "").toLowerCase() === destaque.toLowerCase();
          return (
            <span key={j} style={{ color: eh ? corDestaque : cor }}>
              {p}{" "}
            </span>
          );
        })}
      </div>
    ))}
  </div>
);

/** Uma tela de carrossel 4:5 no molde dos modelos sociais da marca. */
export const Slide: React.FC<PropsSlide> = ({
  tipo,
  tema: t = "escuro",
  assinatura = "produto",
  rotulo,
  titulo,
  destaque,
  apoio,
  numero,
  cartaoRotulo,
  linhas,
  passos,
  pagina,
  rodape = "Toda a sua operação de licitações",
  acao,
}) => {
  const { width } = useVideoConfig();
  const c = tema(t);
  const m = 92;
  const logo = LOGO[assinatura];
  const marcaArea = tipo === "capa" || tipo === "fecho";
  const painel = t === "floresta" ? "#1D3329" : c.painel;

  return (
    <AbsoluteFill>
      <Fundo variante={t} grade={marcaArea} />
      <AbsoluteFill
        style={{ padding: m, fontFamily: marca.fonte, color: c.texto, justifyContent: "space-between" }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <Img src={staticFile(t === "claro" ? logo.claro : logo.escuro)} style={{ width: logo.largura, display: "block" }} />
          {pagina ? <div style={{ fontSize: 26, color: c.textoApagado, fontWeight: 500 }}>{pagina}</div> : null}
        </div>

        <div>
          {rotulo || numero ? (
            <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 34 }}>
              <div style={{ width: 56, height: 2, backgroundColor: c.destaque }} />
              <div
                style={{ fontSize: 24, fontWeight: 500, letterSpacing: "0.08em", textTransform: "uppercase", color: c.destaque }}
              >
                {numero ? `${numero}  ${rotulo ?? ""}` : rotulo}
              </div>
            </div>
          ) : null}
          <Titulo texto={titulo} destaque={destaque} cor={c.texto} corDestaque={c.destaque} tamanho={marcaArea ? 92 : 62} />
          {apoio ? (
            <div style={{ fontSize: 34, lineHeight: 1.42, color: c.textoSecundario, marginTop: 34, maxWidth: width - m * 2 - 40 }}>
              {apoio}
            </div>
          ) : null}

          {linhas ? (
            <div style={{ marginTop: 48, backgroundColor: painel, border: `1px solid ${c.borda}`, borderRadius: marca.raio.lg, padding: "10px 36px" }}>
              {cartaoRotulo ? (
                <div
                  style={{ fontSize: 20, letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 500, color: c.textoApagado, padding: "22px 0 6px" }}
                >
                  {cartaoRotulo}
                </div>
              ) : null}
              {linhas.map(([k, v], i) => (
                <div
                  key={i}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "baseline",
                    gap: 28,
                    padding: "24px 0",
                    borderTop: i === 0 ? "none" : `1px solid ${c.borda}`,
                  }}
                >
                  <div style={{ fontSize: 30, color: c.texto, flex: 1 }}>{k}</div>
                  {v ? <div style={{ fontSize: 28, color: c.textoSecundario, textAlign: "right", maxWidth: "52%" }}>{v}</div> : null}
                </div>
              ))}
            </div>
          ) : null}

          {passos ? (
            <div style={{ marginTop: 52 }}>
              {passos.map((p, i) => (
                <div
                  key={i}
                  style={{ display: "flex", gap: 30, alignItems: "baseline", padding: "30px 0", borderTop: `1px solid ${c.borda}` }}
                >
                  <div style={{ fontSize: 26, fontWeight: 500, color: c.destaque, width: 48 }}>{String(i + 1).padStart(2, "0")}</div>
                  <div style={{ fontSize: 38, lineHeight: 1.3, flex: 1 }}>{p}</div>
                </div>
              ))}
            </div>
          ) : null}
        </div>

        <div>
          <div style={{ height: 1, backgroundColor: c.borda, marginBottom: 26 }} />
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 26 }}>
            <div style={{ color: c.textoSecundario }}>{rodape}</div>
            {acao ? <div style={{ color: c.destaque, fontWeight: 500 }}>{acao}</div> : null}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
