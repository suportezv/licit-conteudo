/**
 * Tokens de marca da Profissio Licit. Este e o UNICO arquivo com paleta e
 * fonte no Remotion: todo o resto le daqui.
 *
 * Fonte: `design-system/fonte/licit-tokens.json` (edicao 1.1, 29/09/2026),
 * espelho do Drive da marca. Os nomes seguem os do token, em camelCase.
 * Mudou na fonte, muda aqui; nunca o contrario.
 */
export const marca = {
  // Paleta aprovada (brandApproved)
  floresta: "#243D32",
  grafite: "#101218",
  acento: "#A8F27A",
  superficie: "#F4F6F9",
  branco: "#FFFFFF",
  apoio: "#59616E",
  /** So existe no degrade da estrela (preto -> floresta). Nunca em texto. */
  pretoDegrade: "#000000",

  // Tema escuro, o padrao da marca (themeProposals.dark)
  escuro: {
    fundo: "#101218",
    painel: "#171C20",
    elevado: "#1E2723",
    selecionado: "#243D32",
    texto: "#F4F6F9",
    textoSecundario: "#B8C5BC",
    textoApagado: "#95A49C",
    borda: "#35413C",
    destaque: "#A8F27A",
  },
  // Tema claro (themeProposals.light). O acento NAO e texto em fundo claro
  // (1,34:1 sobre branco): o destaque aqui e a floresta.
  claro: {
    fundo: "#F4F6F9",
    painel: "#FFFFFF",
    elevado: "#EDF2ED",
    selecionado: "#E1F4D4",
    texto: "#101218",
    textoSecundario: "#59616E",
    textoApagado: "#59616E",
    borda: "#D8E0D9",
    destaque: "#243D32",
  },

  fonte: 'Sora, Arial, sans-serif',
  /** Titulos em 500, corpo em 400, 600 so em enfase pontual. */
  peso: { corpo: 400, titulo: 500, enfase: 600 },
  trackingTitulo: "-0.035em",
  raio: { xs: 4, sm: 8, md: 12, lg: 16 },
  /** cubic-bezier(0.2, 0, 0, 1), a curva de movimento do sistema. */
  curva: [0.2, 0, 0, 1] as const,
  /** Categoria aprovada (D15). Unico texto fixo de marca. */
  categoria: "IA para licitação de Obras",
} as const;

export type Tema = "escuro" | "floresta" | "claro";

/** Cores de uma peca por tema. "floresta" usa a tinta do escuro sobre #243D32. */
export const tema = (t: Tema) =>
  t === "claro"
    ? { ...marca.claro, linha: marca.grafite }
    : t === "floresta"
      ? { ...marca.escuro, fundo: marca.floresta, borda: "#3A5347", linha: marca.superficie }
      : { ...marca.escuro, linha: marca.superficie };
