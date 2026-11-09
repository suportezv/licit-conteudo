import React from "react";
import { Composition } from "remotion";
import { CartaoTitulo } from "./CartaoTitulo";

// Texto de exemplo, neutro de proposito: tagline, CTA e URL da Profissio Licit
// estao PENDENTES (ver FRAMEWORK.md). Trocar quando a marca for definida.
const EXEMPLO = {
  titulo: "Título de exemplo do estúdio",
  destaque: "exemplo",
  rodape: "Profissio Licit",
};

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="CartaoTituloVertical"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        ...EXEMPLO,
      }}
    />
    <Composition
      id="CartaoTituloQuadrado"
      component={CartaoTitulo}
      durationInFrames={150}
      fps={30}
      width={1080}
      height={1080}
      defaultProps={{
        ...EXEMPLO,
      }}
    />
  </>
);
