/**
 * Tokens de marca da Profissio Licit. Este e o UNICO arquivo com paleta e
 * fonte: todo o resto do Remotion le daqui.
 *
 * PENDENTE: a identidade visual da Profissio Licit ainda nao foi definida
 * neste estudio. Os valores abaixo sao um PROVISORIO NEUTRO (grafite e
 * cinzas), escolhido de proposito para nao parecer marca de ninguem. Nao sao
 * a paleta da Profissio.ai nem a de nenhum estudio irmao. Quando a equipe
 * entregar paleta e fonte, trocar aqui e nada mais precisa mudar.
 */
export const marca = {
  /** Cor da palavra de destaque e dos acentos. PENDENTE. */
  acento: "#3A4250",
  /** Manchas do fundo, da mais forte para a mais suave. PENDENTE. */
  mancha1: "#8E97A6",
  mancha2: "#A9B0BC",
  mancha3: "#BFC5CE",
  mancha4: "#D0D4DB",
  /** Base clara do fundo. PENDENTE. */
  fundo: "#F3F4F6",
  /** Cor do texto. PENDENTE. */
  tinta: "#14171C",
  /** Sem rede de fontes no render: fonte de marca entra como asset local. PENDENTE. */
  fonte: 'system-ui, -apple-system, "Segoe UI", "Liberation Sans", sans-serif',
} as const;
