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

// Sem rotulo nem pagina no padrao: o --props e fundido com isto, e o que sobrar aqui aparece na peca.
const SLIDE: PropsSlide = { tipo: "capa", titulo: "Título\nde *exemplo*." };

const ANUNCIO: PropsAnuncio = {
  abertura: "Chegou\na *Licit*.",
  gancho: "Seu próximo\ncontrato pode\nestar numa\n*licitação* que\nvocê não viu.",
  etapas: [
    ["Encontre", "busca"],
    ["Analise", "chat"],
    ["Prepare", "checklist"],
    ["Acompanhe", "tarefas"],
    ["Confira", "resultado"],
  ],
  numero: 30,
  oferta: "dias para usar\na Licit.",
  chips: ["Sem cartão", "Comece até 19/dez"],
  acao: "Link na bio",
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
    {/* Filme de anuncio 9:16, 20 s. */}
    <Composition id="Anuncio" component={Anuncio} durationInFrames={606} fps={30} width={1080} height={1920} defaultProps={ANUNCIO} />
  </>
);
