import React from "react";
import { marca, ui } from "./marca";

/**
 * Telas do produto em miniatura, com os textos do site (cenario ilustrativo
 * da licitacao de informatica). `p` de 0 a 1 revela as linhas em sequencia:
 * 1 nas pecas estaticas, animado no video.
 */
// `p` conta quantas linhas ja entraram: 0 nada, 1 a primeira, 2.5 a terceira pela metade.
// No video cada linha soma a sua propria entrada, no tempo exato do efeito sonoro.
const aparece = (p: number, i: number, _n?: number) => {
  const v = Math.max(0, Math.min(1, p - i));
  return { opacity: v, transform: `translateY(${(1 - v) * 26}px) scale(${0.96 + 0.04 * v})` };
};

export const Cartao: React.FC<{ children: React.ReactNode; largura?: number; giro?: number; estilo?: React.CSSProperties }> = ({
  children,
  largura = 860,
  giro = 0,
  estilo,
}) => (
  <div
    style={{
      width: largura,
      background: ui.fundo,
      color: ui.texto,
      borderRadius: 32,
      padding: 40,
      boxShadow: "0 40px 90px rgba(0,0,0,0.42), 0 6px 18px rgba(0,0,0,0.22)",
      transform: `rotate(${giro}deg)`,
      fontFamily: marca.fonte,
      ...estilo,
    }}
  >
    {children}
  </div>
);

const Chip: React.FC<{ texto: string; tipo?: "neutro" | "sucesso" | "aviso" | "info" | "acao"; tam?: number }> = ({
  texto,
  tipo = "neutro",
  tam = 24,
}) => {
  const cor = {
    neutro: [ui.elevado, ui.secundario],
    sucesso: [ui.sucessoFundo, ui.sucessoTexto],
    aviso: [ui.avisoFundo, ui.avisoTexto],
    info: [ui.infoFundo, ui.infoTexto],
    acao: [ui.acao, ui.acaoTexto],
  }[tipo];
  return (
    <span
      style={{
        display: "inline-block",
        background: cor[0],
        color: cor[1],
        fontSize: tam,
        fontWeight: 500,
        padding: `${tam * 0.36}px ${tam * 0.7}px`,
        borderRadius: tam * 0.5,
        whiteSpace: "nowrap",
      }}
    >
      {texto}
    </span>
  );
};

const Rotulo: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div style={{ fontSize: 21, letterSpacing: "0.1em", textTransform: "uppercase", fontWeight: 500, color: ui.secundario, marginBottom: 22 }}>
    {children}
  </div>
);

export const MockBusca: React.FC<{ p?: number }> = ({ p = 99 }) => (
  <>
    <div style={{ display: "flex", gap: 16, ...aparece(p, 0, 3) }}>
      <div
        style={{ flex: 1, border: `2px solid ${ui.borda}`, borderRadius: 18, padding: "22px 26px", fontSize: 30, color: ui.secundario }}
      >
        CNPJ da empresa
      </div>
      <div style={{ background: ui.acao, color: ui.acaoTexto, borderRadius: 18, padding: "22px 30px", fontSize: 30, fontWeight: 500 }}>
        Descobrir grátis
      </div>
    </div>
    <div style={{ marginTop: 30, background: ui.elevado, borderRadius: 24, padding: 32, ...aparece(p, 1, 3) }}>
      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <Chip texto="Tecnologia" tipo="info" />
        <Chip texto="Produtos" />
        <Chip texto="Na sua região" tipo="sucesso" />
      </div>
      <div style={{ fontSize: 38, fontWeight: 500, lineHeight: 1.2, letterSpacing: "-0.02em" }}>
        Fornecimento de equipamentos de informática
      </div>
      <div style={{ fontSize: 26, color: ui.secundario, marginTop: 10 }}>São José dos Campos · SP</div>
      <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginTop: 26, ...aparece(p, 2, 3) }}>
        <div style={{ fontSize: 68, fontWeight: 600, letterSpacing: "-0.035em" }}>R$ 480.000</div>
        <div style={{ fontSize: 24, color: ui.secundario }}>valor estimado</div>
      </div>
    </div>
  </>
);

export const MockChat: React.FC<{ p?: number }> = ({ p = 99 }) => (
  <>
    <Rotulo>Pergunte ao edital</Rotulo>
    <div style={{ display: "flex", justifyContent: "flex-end", ...aparece(p, 0, 3) }}>
      <div
        style={{ background: ui.acao, color: ui.acaoTexto, borderRadius: "28px 28px 6px 28px", padding: "26px 32px", fontSize: 34, lineHeight: 1.25, maxWidth: "82%" }}
      >
        Quando preciso entregar os equipamentos?
      </div>
    </div>
    <div style={{ marginTop: 22, ...aparece(p, 1, 3) }}>
      <div
        style={{ background: ui.elevado, borderRadius: "28px 28px 28px 6px", padding: "26px 32px", fontSize: 34, lineHeight: 1.25, maxWidth: "86%" }}
      >
        Em até <b style={{ fontWeight: 600 }}>30 dias</b> após a ordem de fornecimento.
      </div>
    </div>
    <div style={{ marginTop: 20, display: "flex", gap: 12, ...aparece(p, 2, 3) }}>
      <Chip texto="▤  Edital · página 25" tipo="aviso" tam={27} />
      <Chip texto="Garantia 12 meses · p. 26" tam={27} />
    </div>
  </>
);

const Marca: React.FC<{ ok: boolean }> = ({ ok }) => (
  <div
    style={{
      width: 44,
      height: 44,
      borderRadius: 22,
      background: ok ? ui.sucessoTexto : "transparent",
      border: ok ? "none" : `3px solid ${ui.avisoTexto}`,
      color: ok ? "#fff" : ui.avisoTexto,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 26,
      fontWeight: 600,
      flexShrink: 0,
    }}
  >
    {ok ? "✓" : "!"}
  </div>
);

export const MockChecklist: React.FC<{ p?: number }> = ({ p = 99 }) => {
  const itens: [string, string, "sucesso" | "aviso" | "neutro", boolean][] = [
    ["Cartão CNPJ", "Já salvo", "sucesso", true],
    ["Certidão FGTS", "Vence em 15 nov", "aviso", false],
    ["Proposta comercial", "Preencher preços", "neutro", false],
  ];
  return (
    <>
      <Rotulo>Documentos e proposta</Rotulo>
      {itens.map(([nome, estado, tipo, ok], i) => (
        <div
          key={nome}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 22,
            padding: "24px 0",
            borderTop: i ? `1px solid ${ui.borda}` : "none",
            ...aparece(p, i, 3),
          }}
        >
          <Marca ok={ok} />
          <div style={{ fontSize: 36, fontWeight: 500, flex: 1, letterSpacing: "-0.01em" }}>{nome}</div>
          <Chip texto={estado} tipo={tipo} tam={26} />
        </div>
      ))}
    </>
  );
};

export const MockTarefas: React.FC<{ p?: number }> = ({ p = 99 }) => {
  const itens: [string, string, string, string, string][] = [
    ["15", "NOV", "Renovar a certidão FGTS", "Ana", "#243D32"],
    ["19", "NOV", "Entregar a proposta até 10:00", "Carlos", "#274F83"],
    ["19", "NOV", "Acompanhar a sessão às 10:15", "Ana", "#243D32"],
  ];
  return (
    <>
      <Rotulo>Tarefas da licitação</Rotulo>
      {itens.map(([d, m, tarefa, quem, cor], i) => (
        <div
          key={tarefa}
          style={{ display: "flex", alignItems: "center", gap: 24, padding: "20px 0", borderTop: i ? `1px solid ${ui.borda}` : "none", ...aparece(p, i, 3) }}
        >
          <div style={{ width: 84, textAlign: "center", background: ui.elevado, borderRadius: 16, padding: "10px 0" }}>
            <div style={{ fontSize: 36, fontWeight: 600, lineHeight: 1 }}>{d}</div>
            <div style={{ fontSize: 17, letterSpacing: "0.1em", color: ui.secundario, marginTop: 4 }}>{m}</div>
          </div>
          <div style={{ fontSize: 33, fontWeight: 500, flex: 1, lineHeight: 1.2, letterSpacing: "-0.01em" }}>{tarefa}</div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div
              style={{ width: 50, height: 50, borderRadius: 25, background: cor, color: "#fff", fontSize: 22, fontWeight: 600, display: "flex", alignItems: "center", justifyContent: "center" }}
            >
              {quem[0]}
            </div>
            <div style={{ fontSize: 25, color: ui.secundario }}>{quem}</div>
          </div>
        </div>
      ))}
    </>
  );
};

export const MockResultado: React.FC<{ p?: number }> = ({ p = 99 }) => (
  <>
    <Rotulo>Resultado publicado no PNCP</Rotulo>
    <div style={{ display: "flex", alignItems: "center", gap: 36 }}>
      <div style={{ ...aparece(p, 0, 3) }}>
        <div style={{ fontSize: 170, fontWeight: 600, letterSpacing: "-0.05em", lineHeight: 0.9, color: ui.acao }}>2º</div>
        <div style={{ fontSize: 26, color: ui.secundario, marginTop: 8 }}>lugar na classificação</div>
      </div>
      <div style={{ flex: 1 }}>
        {(
          [
            ["Valor homologado", "R$ 426.000", 0.86, ui.acao],
            ["Proposta da empresa", "R$ 438.000", 0.9, "#9DB3A4"],
          ] as [string, string, number, string][]
        ).map(([k, v, w, cor], i) => (
          <div key={k} style={{ marginBottom: 22, ...aparece(p, i + 1, 3) }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 25, marginBottom: 8 }}>
              <span style={{ color: ui.secundario }}>{k}</span>
              <span style={{ fontWeight: 600 }}>{v}</span>
            </div>
            <div style={{ height: 20, borderRadius: 10, background: ui.elevado }}>
              <div style={{ height: 20, borderRadius: 10, width: `${w * 100 * Math.max(0, Math.min(1, p - 1 - i * 0.5))}%`, background: cor }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  </>
);

export const MOCKS = { busca: MockBusca, chat: MockChat, checklist: MockChecklist, tarefas: MockTarefas, resultado: MockResultado };
export type NomeMock = keyof typeof MOCKS;
