import { continueRender, delayRender, staticFile } from "remotion";

/**
 * Sora variavel (SIL OFL 1.1), embutida em public/ para o render nao depender
 * de rede. A licenca acompanha o arquivo (public/Sora-OFL.txt).
 */
let carregada = false;
export const carregaFontes = () => {
  if (carregada || typeof document === "undefined") return;
  carregada = true;
  const espera = delayRender("Sora");
  const sora = new FontFace("Sora", `url(${staticFile("Sora-Variable.ttf")}) format("truetype")`, {
    weight: "100 800",
  });
  sora
    .load()
    .then((f) => {
      (document.fonts as unknown as { add(f: FontFace): void }).add(f);
      continueRender(espera);
    })
    .catch(() => continueRender(espera));
};
