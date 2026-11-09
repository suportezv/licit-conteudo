# Contraste da proposta de interface Licit

29/09/2026 · Cálculo de tokens propostos, sem auditoria do produto em execução.

Os pares abaixo foram calculados em sRGB pela luminância relativa e razão de contraste. A decisão usa o valor completo; a tabela mostra duas casas decimais. Texto comum usa a meta de 4,5:1. Contornos essenciais e indicadores usam 3:1. Estes critérios vêm da [W3C, contraste de texto](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) e da [W3C, contraste não textual](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html).

A paleta da marca está aprovada. Tons auxiliares, cores de estado e mapeamento de temas são propostas funcionais para esta interface. As razões calculadas não certificam acessibilidade do aplicativo: foco, semântica, teclado, zoom, comportamento e todos os estados precisam de teste na implementação.

| Tema | Uso | Frente | Fundo | Razão | Meta | Resultado |
| --- | --- | --- | --- | ---: | ---: | --- |
| dark | Texto principal | `#F4F6F9` | `#171C20` | 15.85:1 | 4.5:1 | Atende ao par calculado |
| dark | Texto secundário | `#B8C5BC` | `#171C20` | 9.61:1 | 4.5:1 | Atende ao par calculado |
| dark | Legenda e metadado | `#95A49C` | `#171C20` | 6.59:1 | 4.5:1 | Atende ao par calculado |
| dark | Texto em seleção | `#F4F6F9` | `#243D32` | 10.84:1 | 4.5:1 | Atende ao par calculado |
| dark | Botão principal | `#101218` | `#A8F27A` | 13.95:1 | 4.5:1 | Atende ao par calculado |
| dark | Botão em hover | `#101218` | `#BBF697` | 14.93:1 | 4.5:1 | Atende ao par calculado |
| dark | Botão pressionado | `#101218` | `#91DD60` | 11.34:1 | 4.5:1 | Atende ao par calculado |
| dark | Link | `#A8F27A` | `#171C20` | 12.79:1 | 4.5:1 | Atende ao par calculado |
| dark | Contorno de controle | `#728178` | `#171C20` | 4.19:1 | 3:1 | Atende ao par calculado |
| dark | Contorno sobre canvas | `#728178` | `#101218` | 4.57:1 | 3:1 | Atende ao par calculado |
| dark | Foco sobre painel | `#A8F27A` | `#171C20` | 12.79:1 | 3:1 | Atende ao par calculado |
| dark | Foco sobre canvas | `#A8F27A` | `#101218` | 13.95:1 | 3:1 | Atende ao par calculado |
| dark | Estado success | `#B4E5C2` | `#193B2A` | 8.78:1 | 4.5:1 | Atende ao par calculado |
| dark | Estado warning | `#F4C76D` | `#372B15` | 8.72:1 | 4.5:1 | Atende ao par calculado |
| dark | Estado danger | `#FFB4AC` | `#3B1D1E` | 8.97:1 | 4.5:1 | Atende ao par calculado |
| dark | Estado info | `#B4CEFF` | `#1E2E48` | 8.58:1 | 4.5:1 | Atende ao par calculado |
| light | Texto principal | `#101218` | `#FFFFFF` | 18.72:1 | 4.5:1 | Atende ao par calculado |
| light | Texto secundário | `#59616E` | `#FFFFFF` | 6.25:1 | 4.5:1 | Atende ao par calculado |
| light | Legenda e metadado | `#59616E` | `#FFFFFF` | 6.25:1 | 4.5:1 | Atende ao par calculado |
| light | Texto em seleção | `#101218` | `#E1F4D4` | 16.13:1 | 4.5:1 | Atende ao par calculado |
| light | Botão principal | `#FFFFFF` | `#243D32` | 11.74:1 | 4.5:1 | Atende ao par calculado |
| light | Botão em hover | `#FFFFFF` | `#183125` | 13.95:1 | 4.5:1 | Atende ao par calculado |
| light | Botão pressionado | `#FFFFFF` | `#0F251B` | 16.14:1 | 4.5:1 | Atende ao par calculado |
| light | Link | `#243D32` | `#FFFFFF` | 11.74:1 | 4.5:1 | Atende ao par calculado |
| light | Contorno de controle | `#748279` | `#FFFFFF` | 4.03:1 | 3:1 | Atende ao par calculado |
| light | Contorno sobre canvas | `#748279` | `#F4F6F9` | 3.72:1 | 3:1 | Atende ao par calculado |
| light | Foco sobre painel | `#243D32` | `#FFFFFF` | 11.74:1 | 3:1 | Atende ao par calculado |
| light | Foco sobre canvas | `#243D32` | `#F4F6F9` | 10.84:1 | 3:1 | Atende ao par calculado |
| light | Estado success | `#205B37` | `#E3F3E8` | 6.98:1 | 4.5:1 | Atende ao par calculado |
| light | Estado warning | `#76500B` | `#FFF2CC` | 6.44:1 | 4.5:1 | Atende ao par calculado |
| light | Estado danger | `#992B28` | `#FBE9E7` | 6.56:1 | 4.5:1 | Atende ao par calculado |
| light | Estado info | `#274F83` | `#E7EFFB` | 7.16:1 | 4.5:1 | Atende ao par calculado |

## Combinações restritas

| Combinação | Frente | Fundo | Razão | Orientação |
| --- | --- | --- | ---: | --- |
| Acento claro em branco | `#A8F27A` | `#FFFFFF` | 1.34:1 | Não usar em texto nem como único contorno essencial. |
| Floresta no grafite | `#243D32` | `#101218` | 1.59:1 | Usar como superfície, acompanhado de texto claro e indicador visível; não como texto. |
| Apoio original no grafite | `#59616E` | `#101218` | 3.00:1 | Substituir por text-secondary ou text-muted do tema escuro para texto. |
| Borda sutil escura | `#35413C` | `#171C20` | 1.61:1 | Apenas separação decorativa. Controles usam border-control. |
| Borda sutil clara | `#D8E0D9` | `#FFFFFF` | 1.35:1 | Apenas separação decorativa. Controles usam border-control. |

## Uso na implementação

Os nomes de tokens por par estão em `CONTRASTE_CALCULADO.json`. Os valores fonte estão em `TOKENS_UX_PROPOSTOS.json`. Acrescentar fundo e cor explicitamente ao componente, sem reduzir a opacidade do texto. Não reutilizar a borda sutil como única indicação de um campo, checkbox ou foco. Um estado desabilitado não deve esconder instruções necessárias em texto ilegível.

O anel de foco deve aparecer sobre o fundo externo do componente, com afastamento de 3 px; quando esse fundo for outro botão ou cor não prevista, usar uma camada de separação na cor do painel e recalcular o par final. Em fotos, documentos e gráficos, preferir foco com anel externo e base opaca.

O cálculo é reprodutível por `gerar_tokens_contraste.py`. Se qualquer cor, opacidade ou superfície for alterada, repetir os pares afetados. Não arredondar uma razão abaixo do limiar para declará-la aprovada.
