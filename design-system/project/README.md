# Profissio Licit

**IA para licitação de Obras.**

A Profissio Licit reúne documentos da empresa e análises de editais em um ambiente de trabalho para equipes de licitação de obras. Organiza exigências, prazos e referências aos documentos para apoiar a conferência e a preparação de cada participação.

Este sistema consolida a identidade da edição 1.1 (29/09/2026): o Manual de Marca, as diretrizes de uso e de comunicação, os tokens e a especificação de UX que estão no Drive da marca. A paleta, os letterings e a arquitetura de assinaturas são aprovados. Os tokens e componentes de interface são especificação de implementação.

## Como usar este sistema

1. Escolha a assinatura pelo papel (seção Assinaturas) e pegue o SVG no grupo **Logos**. Nunca redigite o nome.
2. Escolha o tema. **O padrão é o escuro.** O claro existe para leitura longa e documentos.
3. Use os tokens `licit-*` pelo nome. Não decida cor por peça.
4. Antes de escrever qualquer texto, leia **Voz e limites de mensagem**.

## Princípios

- **Institucional, concreta, conferível.** A marca descreve o trabalho apoiado pela plataforma e preserva o papel da equipe.
- **A superfície sustenta o conteúdo.** Planos simples onde há dado; textura só em área de marca.
- **Contraste é regra de composição**, não ajuste final.
- **Uma família, um produto reconhecível.** A proximidade com a Profissio é estrutural (o P, a Sora, a qualidade de execução). A Licit se identifica pelo nome, pela paleta e pela estrela.

## Cor: Floresta Tech

| Cor | Token | Valor | Papel |
| --- | --- | --- | --- |
| Floresta | `licit-forest` | #243D32 | Estrutura e identidade |
| Grafite | `licit-ink` | #101218 | Estrutura, fundo escuro, tinta no claro |
| Acento Tech | `licit-accent` | #A8F27A | Pequenos pontos de atenção |
| Superfície | `licit-surface` | #F4F6F9 | Áreas de leitura |
| Branco | `licit-white` | #FFFFFF | Painéis claros |
| Apoio | `licit-muted` | #59616E | Texto secundário em fundo claro |

Floresta e grafite dão estrutura. Branco e superfície criam alternância e áreas de leitura. **O acento orienta a atenção: é contido, nunca decorativo.** O azul da Profissio pertence à marca mãe e não entra aqui. As cores funcionais (sucesso, atenção, erro, informação) existem só na interface e não ampliam a paleta institucional.

### Pares de contraste

| Combinação | Contraste | Uso |
| --- | --- | --- |
| Branco sobre floresta | 11,74:1 | Texto |
| Branco sobre grafite | 18,72:1 | Texto |
| Grafite sobre superfície | 17,29:1 | Texto |
| Apoio sobre branco | 6,25:1 | Texto |
| Acento sobre grafite | 13,95:1 | Texto e destaque |
| Acento sobre floresta | 8,75:1 | Texto e destaque |
| Acento sobre branco | 1,34:1 | **Evitar como texto** |
| Floresta sobre grafite | 1,59:1 | **Evitar como texto** |

Consequência prática: **em fundo claro, o destaque é a floresta; em fundo escuro, é o acento.** Estado nunca depende só de cor.

O degradê (de #000000 no canto inferior esquerdo a #243D32 no superior direito) é **exclusivo da estrela**. Letterings e o P ficam em cor sólida. Não há equivalência CMYK homologada: impressão pede prova física.

## Tipografia

**Sora** (SIL Open Font License 1.1) é a fonte de comunicação e de interface. Títulos em **500**, corpo em **400**, **600** só para ênfase pontual (prazo, origem, pendência). Tracking do título em -0,035em. Frases diretas e espaço entre blocos.

O lettering das marcas é desenho em curvas, não Sora digitada. A licença acompanha o arquivo em `fonts/Sora-OFL.txt` e deve ser preservada ao redistribuir.

## Assinaturas

| Contexto | Assinatura | Arquivo |
| --- | --- | --- |
| Institucional, primeira identificação, relação com a marca mãe | **Profissio Licit** com o P oficial, sem estrela | `profissio-licit-*` |
| Ambiente e comunicação próprios do produto | **Estrela + Licit** | `licit-estrela-*` |
| Ícone da plataforma, avatar, favicon | **Estrela isolada** | `estrela-licit-*` |

Profissio identifica a origem. A estrela identifica o produto. Não acrescentar estrela à assinatura completa nem usar o P isolado como ícone da Licit.

O nome editorial é **Profissio Licit**, sem `.ai`, sem "by" e sem slogan. Depois da identificação inicial, "Licit" pode ser usado sozinho.

A estrela tem quatro braços arredondados, laterais côncavas, dois vazados que definem um círculo interno com margem e uma faixa curva ascendente. Relaciona-se com IA e com a origem brasileira. **Não é selo oficial, certificação, vínculo com governo nem garantia de habilitação**, e nunca serve de estado de sucesso.

Área livre: um quarto da altura visível. Larguras de partida: institucional 240 px, produto 160 px, estrela 32 px.

## Fundos e superfícies

Em tabelas, documentos e leituras longas, superfície plana. Os dez fundos geométricos (grupo **Fundos**) ficam para entradas institucionais e comunicação, sempre subordinados à leitura. Evitar brilho difuso, textura atrás de dado e reflexo.

## Iconografia

Ícones funcionais de linha simples (grupo **Icones**: grade de 24, traço 1,7, terminais arredondados), sempre com rótulo ou nome acessível. Descrevem ações e conteúdos reais: documento, referência, conferência. Não competem com a estrela e não usam o P.

## Geometria e movimento

Raios de 4, 8, 12 e 16 px. Borda de 1 px. Foco de 2 px com afastamento de 3 px. Espaçamento na escala de 2 a 64 px.

Movimento sóbrio: 120 ms (rápido), 180 ms (base) e 240 ms (painel), com a curva `cubic-bezier(0.2, 0, 0, 1)`. Nada de movimento atrás de dado que precisa ser conferido.

## Fontes

Drive da marca, pasta "01_Profissio_Licit_Identidade_Atual": `07_Relatorios` (Manual de Marca, Diagnóstico e Posicionamento), `05_Diretrizes` (uso, comunicação, tokens), `11_UX_Design` (manual, componentes, contraste), `01_Logos`, `02_Fontes`, `04_Social`, `06_Fundos`.
