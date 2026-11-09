import React from "react";
import { Composition } from "remotion";
import { CartaoTitulo, PropsCartao } from "./CartaoTitulo";

// Texto dos modelos sociais do kit da marca (04_Social). Sao propostas
// editoriais do proprio kit, nao promessa de produto: ver FRAMEWORK.md.
const EXEMPLO: PropsCartao = {
  rotulo: "Análise com referência",
  titulo: "Cada exigência,\ncom sua\nreferência.",
  destaque: "referência",
  tema: "escuro",
  assinatura: "institucional",
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
  </>
);
