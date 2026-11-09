# Profissio Licit Conteúdo Studio: FRAMEWORK

Estúdio de criação, edição e agendamento para as redes da **Profissio Licit**. Infraestrutura e craft herdados dos estúdios irmãos (`profissioai-conteudo`, `profecia-conteudo`); posicionamento próprio, ainda por definir.

> **Seções marcadas PENDENTE não foram definidas.** Não preencher por inferência e não herdar posicionamento da Profissio.ai, do Profecia nem de outro estúdio. Perguntar antes de produzir qualquer texto público. O que está aqui sem a marca PENDENTE é craft do grupo, válido para qualquer marca.

## Persona e voz do perfil

- **Produto**: PENDENTE. Só o nome é conhecido. Ler o site e a base de conhecimento quando forem apontados e confirmar com a equipe.
- **Quem fala, tom, público**: PENDENTE.
- **CTAs oficiais**: PENDENTE (extrair da fonte, não inventar).
- **Vocabulário do produto**: PENDENTE (extrair os termos literais do site e da ajuda, e usar com consistência).
- **Pronúncia da marca**: PENDENTE (confirmar antes da primeira locução).
- **Referência de estilo**: PENDENTE. Os irmãos usam `@elevenlabsio` como referência de formato e ritmo; confirmar se vale aqui.

### REGRAS INEGOCIÁVEIS (herdadas do grupo)

1. **Nunca usar travessão em texto público.** Reescrever a frase.
2. **Palavrão bipa, não corta** (sine 1000 Hz curto, voz mutada no trecho).
3. **Loudness final: -14 LUFS.**

## Identidade visual

PENDENTE: paleta, tipografia, logo, fundos e motion de marca. Enquanto não houver, `remotion/src/marca.ts` carrega um provisório neutro em cinza que **não é identidade de ninguém** e não deve sair em peça pública. Quando a identidade chegar:

1. Registrar os tokens em `design-system/` (fonte de verdade).
2. Espelhar em `remotion/src/marca.ts` (único arquivo com paleta no Remotion).
3. Colocar logo em `assets/marca/` e fontes em `assets/fonts/`.
4. Escrever aqui o resumo de leitura rápida.

## Pilares de conteúdo

PENDENTE: derivar das fontes primárias quando lidas. Método validado nos estúdios irmãos: ler site e base de conhecimento do produto, extrair dores e soluções **literais**, e escolher as features que sejam (1) diferenciadas, (2) legíveis em 3 segundos e (3) nativamente visuais. Validar desempenho antes de fixar proporção entre pilares.

## Assinaturas de motion (craft do grupo, validado contra 4 vídeos reais do @elevenlabsio)

- **Peça contínua, sem cortes secos**: estados se transformam um no outro; cada estado segura 2 a 3 segundos.
- **Muito espaço negativo** no fundo. **Fundo e paleta: PENDENTES.**
- **Tipografia contida**: sentence case, 1 linha curta por vez, revelação palavra a palavra ou máquina de escrever com cursor. Sem display caps gigante em motion.
- **UI real do produto como card flutuante** com sombra suave; cursor navega; transições por escala. Qual é a UI do Licit: PENDENTE.
- **Grafo de nós** (chips + linhas de 1px + pontinhos viajando) para critérios, canais e orquestração.
- **CTA discreto**: texto + URL digitada com cursor piscando. Sem botão chamativo.
- Trilha via **Eleven Music**, comedida, com ducking pela locução; SFX da biblioteca `assets/sfx`.
- Área segura 9:16: 220px no topo, 420px na base. Duração alvo: 20 a 60s. Master **-14 LUFS**.

As assinaturas de vídeo filmado (mais abaixo) valem para gravações reais, não para motion.

## Escolha do framework de motion: HyperFrames ou Remotion

O estúdio mantém os dois, e a escolha **não é preferência do momento**: cada peça declara o seu no `BRIEFING.md`, na primeira linha. Sem isso, quem pegar o projeto depois não sabe onde mexer.

**O que decide**: a ponte entre os dois só existe num sentido. Há a skill `remotion-to-hyperframes`; **não existe o inverso**. Então peça feita em HyperFrames é definitiva, e peça feita em Remotion ainda pode migrar. Na dúvida, Remotion é a aposta reversível.

| Use **HyperFrames** quando | Use **Remotion** quando |
|---|---|
| É peça da série recorrente, na gramática já documentada | A peça é exceção, fora do padrão da série |
| Você quer o fluxo pronto: brief, storyboard, registry de ~400 blocos, legendas, áudio, render em nuvem | A composição precisa de lógica de programação, dados ou parametrização |
| O visual pedido já existe no registry (scanlines, glitch, gráfico, janela de terminal) | Você vai gerar **N variações** da mesma peça mudando nome, cupom, idioma ou número |
| Ninguém vai reprocessar a peça em outro framework | Há chance real de a peça mudar de destino depois |

**Padrão declarado: HyperFrames**, herdado do grupo enquanto a Profissio Licit não tem série própria; é o que está integrado ao fluxo e tem as skills. O Remotion entra por decisão consciente. Revisar o padrão quando a primeira série existir.

**Custo de manter os dois, para vigiar**: dois `node_modules`, dois caminhos de render e dois lugares onde a paleta pode divergir. Os tokens do Remotion vivem em `remotion/src/marca.ts`: se a paleta mudar, atualizar os dois lados.

## Assinaturas de edição (vídeo filmado)

Craft técnico validado nos estúdios irmãos, aplicável a qualquer marca:

- Hook verbal ou visual + título na tela nos **2 primeiros segundos**.
- Lettering condensado caps branco com sombra dura (Helvetica Neue Condensed Black no Mac; Liberation Sans Bold como fallback Linux). **Cor de acento nas ênfases: PENDENTE.**
- Legendas frase a frase em branco (não karaokê), terço inferior, **SEMPRE por último no filter chain**.
- Cortes secos; punch-ins de zoom 1.10 a 1.22x; freeze frames P&B com card para punchlines; cutaways como payoff.
- Palavrão não corta: **bipa**.
- Trilha discreta (vol ~0.12 a 0.15); SFX sincronizados aos cortes.
- Duração alvo: **20 a 60s**. Loudness final: **-14 LUFS**.

## Fórmula da caption

Estrutura do grupo; o conteúdo de cada bloco depende do posicionamento **PENDENTE**:

1. Hook em 1 linha (dor ou cena concreta, sem travessão)
2. 2 a 3 parágrafos curtos, no vocabulário do produto
3. CTA oficial (PENDENTE)
4. Pergunta de engajamento
5. Hashtags: PENDENTE (definir o conjunto da marca)

## Fluxo por peça

1. Briefing + fontes (pilar, mensagem central, duração, data). **Se for motion, declarar HyperFrames ou Remotion já aqui.** Se for vídeo filmado, bruto no Drive ou anexo na conversa.
2. Roteiro em cenas (`BRIEFING.md` + `CENAS.md`) ou, em vídeo filmado, proxy SDR (se HLG) + transcrição Scribe e decupagem por âncora de texto.
3. Cor (vídeo filmado) ou composição (motion).
4. Lettering/motion.
5. **Legendas por último.**
6. Locução (voz PENDENTE; validar pronúncia por STT) + SFX da biblioteca + trilha Eleven Music; mix com ducking, master **-14 LUFS**.
7. Conferir a peça inteira com o `/watch` (com autorização do usuário para subir o vídeo ao Google) ou por frames.
8. **Preview na conversa para aprovação** (não agendar antes da aprovação).
9. Caption.
10. Agendamento no Metricool (marca da Profissio Licit, blog_id **PENDENTE**; mídia por URL direta do Drive; tirar do rascunho na mesma sessão e confirmar com `getScheduledPosts`).
11. Registrar aprendizados no `POS.md` do projeto e atualizar o `CLAUDE.md`.

## Gotchas técnicos

Ver a seção "Gotchas essenciais" do `CLAUDE.md` deste repo.
