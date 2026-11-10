import React from "react";
import { Composition, Still } from "remotion";
import { Anuncio, PropsAnuncio } from "./Anuncio";
import { CartaoTitulo, PropsCartao } from "./CartaoTitulo";
import { PropsSlide, Slide } from "./Slide";

// Texto dos modelos sociais do kit da marca (04_Social). Sao propostas
// editoriais do proprio kit, nao promessa de produto: ver FRAMEWORK.md.
const EXEMPLO: PropsCartao = {
  rotulo: "Análise com referência",
  titulo: "Cada exigência,\ncom sua\nreferência.",
  destaque: "referência",
  tema: "escuro",
  assinatura: "institucional",
};

const SLIDE: PropsSlide = { tipo: "capa", titulo: "Título\nde exemplo.", rotulo: "Exemplo", pagina: "01/01" };

const ANUNCIO: PropsAnuncio = {
  abertura: "Chegou\na Licit.",
  promessa: "Venda para o governo.\nSaiba o que fazer\nem cada etapa.",
  etapas: ["Encontre", "Analise", "Prepare", "Acompanhe", "Confira"],
  oferta: "30 dias\npara usar\na Licit.",
  prazo: "Comece até 9 de dezembro.",
  rodape: "Toda a sua operação de licitações",
  trilha: "",
};

const formatos = [
  { id: "CartaoTituloVertical", width: 1080, height: 1920 },
  { id: "CartaoTituloQuadrado", width: 1080, height: 1080 },
  { id: "CartaoTituloRetrato", width: 1080, height: 1350 },
];

export const RemotionRoot: React.FC = () => (
  <>
    {formatos.map((f) => (
      <Composition
        key={f.id}
        id={f.id}
        component={CartaoTitulo}
        durationInFrames={150}
        fps={30}
        width={f.width}
        height={f.height}
        defaultProps={EXEMPLO}
      />
    ))}
    {/* Tela de carrossel 4:5: os dados de cada peca vem por --props. */}
    <Still id="Slide" component={Slide} width={1080} height={1350} defaultProps={SLIDE} />
    {/* Filme de anuncio 9:16, 18 s. */}
    <Composition id="Anuncio" component={Anuncio} durationInFrames={540} fps={30} width={1080} height={1920} defaultProps={ANUNCIO} />
  </>
);
