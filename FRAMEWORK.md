# Profissio Licit Conteúdo Studio: FRAMEWORK

Estúdio de criação, edição e agendamento para as redes da **Profissio Licit**. Infraestrutura e craft herdados dos estúdios irmãos; marca própria.

> **Fonte deste documento**: o Drive da marca, edição 1.1 de 29/09/2026 (Manual de Marca, Diagnóstico e Posicionamento, Comunicação, Uso da Marca, Preparação do Site), lido em 09/nov/2026. O que está marcado **PENDENTE** não está na fonte. Não inferir e não herdar da Profissio.ai nem do Profecia.

## Persona e voz do perfil

- **Produto**: **IA para licitação de Obras** (categoria aprovada). Descrição institucional, literal: "A Profissio Licit reúne documentos da empresa e análises de editais em um ambiente de trabalho para equipes de licitação de obras. Organiza exigências, prazos e referências aos documentos para apoiar a conferência e a preparação de cada participação."
- **Quem fala**: a marca, em voz institucional. Não há rosto, personagem nem agente falando. **PENDENTE**: confirmar se haverá porta-voz humano.
- **Público**: empresa de obras que já licita com estrutura (foco); depois a que licita sem estrutura. O texto serve à liderança que contrata e à equipe que opera. **A equipe nunca é o problema.**
- **Tom**: institucional, preciso, seguro e direto. Referência indicada pelo usuário: a comunicação empresarial da **Enter**.
- **Vocabulário**: edital, requisito, exigência, documento, acervo, revisão, fonte, prazo, participação, conferência.
- **Nome**: Profissio Licit, sem `.ai`. Depois da primeira menção, Licit.
- **CTA**: **PENDENTE**. Não há ação de contato nem destino definidos. Até lá, a peça fecha na categoria.
- **Pronúncia e voz de locução**: **PENDENTES**.
- **Redes**: Instagram `@profissio.licit`, LinkedIn (organização `146949785`), TikTok `@profissio.licit`.

### REGRAS INEGOCIÁVEIS

1. **Só se afirma o que tem evidência.** Nada de garantia de vitória, habilitação automática, conformidade jurídica, eliminação de erros, números de economia ou de produtividade, clientes, depoimentos. Nada de anunciar recurso de roadmap. Lista completa em "Limites de mensagem" no `CLAUDE.md`.
2. **Nenhum argumento de substituição de profissionais.**
3. **Nunca usar travessão em texto público.** Reescrever a frase.
4. **Sem urgência artificial, sem humor de infoproduto, sem promessa de enriquecimento.**
5. **Palavrão bipa, não corta.**
6. **Loudness final: -14 LUFS.**

## Identidade visual (padrão: Design System da Profissio Licit)

Fonte de verdade: o Design System (`https://claude.ai/artifact/1Cew4xmRADNpZi6aRve4MU`, espelho em `design-system/`). Resumo de leitura rápida:

- **Paleta "Floresta Tech"**: floresta `#243D32`, grafite `#101218`, acento `#A8F27A`, superfície `#F4F6F9`, branco, apoio `#59616E`. **Tema padrão escuro.**
- **O acento orienta atenção, não decora.** Uma palavra, um fio, um rótulo. Em fundo claro o destaque é a floresta, porque o acento sobre branco não lê (1,34:1).
- **Sora**: título 500, corpo 400, 600 só em ênfase pontual. Tracking do título -0,035em. Sentence case, alinhado à esquerda. Sem display caps.
- **Assinaturas**: institucional (Profissio Licit com o P) na primeira identificação; estrela + Licit quando o produto aparece sozinho; estrela isolada em avatar e ícone. Nunca P + estrela.
- **Fundos**: plano chapado onde há leitura; geometria discreta (grade técnica, planos, topografia) em área de marca. Sem brilho difuso.
- **Molde das peças sociais** (dos modelos do kit): assinatura no topo, fio + rótulo em caixa alta, título em três ou quatro linhas curtas, linha de apoio, categoria no rodapé. É a composição `CartaoTitulo` do Remotion.

## Pilares de conteúdo (PROPOSTA, a validar com o usuário)

Derivados do que as evidências permitem dizer. Cada pilar parte de um mecanismo observado nas telas, não de promessa.

| Pilar | O que mostra | Limite |
| --- | --- | --- |
| **A. Cada exigência, com sua referência** | A análise estruturada do edital com referência a arquivo e página. É o diferencial mais legível em 3 segundos | Não afirmar completude nem correção da análise |
| **B. A empresa no centro** | Documentos e dados da empresa organizados: categorias, validade, fontes, divergências | Não afirmar alerta automático nem precisão de classificação |
| **C. O trabalho de licitar obras** | Conteúdo de ofício para quem já licita: leitura de edital, habilitação, acervo técnico, prazos. Constrói autoridade sem prometer produto | Conteúdo jurídico exige fonte citada; não é parecer |
| **D. A equipe e a conferência** | O papel de quem confere: a ferramenta organiza, a equipe decide | Nenhuma sugestão de substituição |

Fora dos pilares até haver evidência: resultado de cliente, comparação com concorrente, preço, demonstração de recurso de roadmap.

**Referência `@licitacertabr`** (indicada pelo usuário como SaaS mais simples com bom MRR, de proposta mais amadora): **ainda não lida**, o Instagram exige login. Quando houver prints, gravação ou token da Meta, analisar o que funciona em formato, gancho e frequência e trazer só o que cabe na voz institucional: clareza de gancho e utilidade prática entram; urgência, promessa de ganho e tom de infoproduto não.

## Assinaturas de motion (craft do grupo, ajustado à marca)

- **Peça contínua, sem cortes secos**: estados se transformam; cada estado segura 2 a 3 segundos.
- **Movimento sóbrio**, com a curva do sistema `cubic-bezier(0.2, 0, 0, 1)`. Nada de glitch, brilho ou mola.
- **Tipografia contida**: 1 ideia por vez, revelação linha a linha.
- **UI do produto como card flutuante** só com captura atual e legenda que descreva o que se vê. Sem captura, usar os componentes do Design System (`Requisito`, `Selo`) com dados claramente ilustrativos.
- **Nada de movimento ou textura atrás de dado.**
- Trilha via Eleven Music, comedida, com ducking pela locução; SFX da biblioteca `assets/sfx`.
- Área segura 9:16: 220px no topo, 420px na base. Duração alvo: 20 a 60s. Master **-14 LUFS**.

## Escolha do framework de motion: HyperFrames ou Remotion

Cada peça declara o seu no `BRIEFING.md`, na primeira linha.

**O que decide**: a ponte só existe num sentido (`remotion-to-hyperframes`). Peça em HyperFrames é definitiva; peça em Remotion ainda pode migrar.

| Use **HyperFrames** quando | Use **Remotion** quando |
|---|---|
| É peça da série recorrente, na gramática já documentada | A peça é exceção, fora do padrão da série |
| Você quer o fluxo pronto: brief, storyboard, registry de blocos, legendas, áudio | A composição precisa de lógica, dados ou parametrização |
| O visual pedido já existe no registry | Você vai gerar **N variações** da mesma peça mudando texto, tema ou formato |
| Ninguém vai reprocessar a peça em outro framework | Há chance real de a peça mudar de destino |

**Padrão declarado: Remotion para cartões e posts estáticos** (o molde da marca já está pronto em `CartaoTitulo`, em três formatos e três temas) **e HyperFrames para vídeo de motion com vários estados.** Revisar quando a primeira série existir.

## Assinaturas de edição (vídeo filmado)

Craft do grupo, com a tinta da marca:

- Hook verbal ou visual + título na tela nos **2 primeiros segundos**.
- Lettering em **Sora 500**, sentence case, branco sobre o vídeo; ênfase em acento `#A8F27A` só sobre área escura.
- Legendas frase a frase em branco, terço inferior, **SEMPRE por último no filter chain**.
- Cortes limpos; punch-ins discretos (1.08 a 1.15x). Sem freeze frame de piada, sem scratch, sem whoosh de infoproduto.
- Duração alvo: **20 a 60s**. Loudness final: **-14 LUFS**.

## Fórmula da caption

1. Abertura em 1 linha: uma situação concreta do trabalho de licitar (uma exigência, um prazo, um documento), sem travessão e sem alarme.
2. 1 a 2 parágrafos curtos, no vocabulário do trabalho, dizendo o que se organiza e o que a equipe confere.
3. Fecho na categoria: "Profissio Licit. IA para licitação de Obras." **CTA: PENDENTE.**
4. Hashtags: **PENDENTE**.

A legenda complementa a peça; não repete o texto do card.

## Fluxo por peça

1. Briefing + fontes (pilar, mensagem central, formato, data). **Declarar HyperFrames ou Remotion.**
2. **Conferir a mensagem contra os limites** (`CLAUDE.md`, "Limites de mensagem") antes de produzir.
3. Roteiro (`BRIEFING.md` + `CENAS.md`) ou, em vídeo filmado, proxy SDR + transcrição Scribe e decupagem por âncora de texto.
4. Composição ou cor.
5. Lettering/motion. **Legendas por último.**
6. Locução (voz PENDENTE; validar pronúncia por STT) + SFX + trilha; master **-14 LUFS**.
7. Conferir a peça inteira (`/watch`, com autorização para subir o vídeo ao Google, ou por frames).
8. **Preview na conversa para aprovação.**
9. Caption.
10. Agendamento no Metricool (marca Profissio Licit, **blog_id 7994045**; mídia por URL direta do Drive; tirar do rascunho na mesma sessão e confirmar com `getScheduledPosts`).
11. Registrar aprendizados no `POS.md` do projeto e atualizar o `CLAUDE.md`.

## Gotchas técnicos

Ver "Gotchas essenciais" no `CLAUDE.md`.
