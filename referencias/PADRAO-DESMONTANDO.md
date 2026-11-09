# O padrão do @desmontandoomundo (estudo de 09/nov/2026)

Referência maior de estética e de conteúdo para o formato "Por Dentro da Granja" (Porcin.IA) e para a editoria da Licit (`PORTAR-LICIT.md`). Pedido do usuário em 09/nov/2026: estudar o perfil minuciosamente.

## O que foi lido e o que ficou de fora

**Lido daqui** (hosts liberados no environment em 09/nov/2026: `desmontandoomundo.com.br`, `youtube.com`, `i.ytimg.com`):

- A página do curso "Desmontando o Vídeo" (`www.desmontandoomundo.com.br`): números do canal, o processo em seis passos, o que o criador diz que faz um vídeo prender.
- A página "Sobre" do canal no YouTube (`@DesmontandoOMundo`): descrição, inscritos, visualizações, data de criação.
- A aba Shorts do canal: os 22 vídeos com título e visualizações, e a capa de 20 deles (contato em `referencias-desmontando/contato_capas.png`, fora do git).

**Fora do alcance** (e por quê):

- **Os vídeos em si.** O YouTube devolve a página de verificação anti-robô (`google.com/sorry`) para qualquer `watch?v=`, então nem a descrição nem a legenda automática saíram. O Instagram exige login para perfil e mídia. Não se contorna nenhum dos dois (regra do `CLAUDE.md`).
- **Consequência:** duração, palavras por minuto, estrutura do roteiro, densidade de SFX, voz e o jeito de encenar a "revelação do mecanismo" **ainda não foram medidos**. A rota validada é a mesma do maxagroapp: o usuário sobe 8 a 10 reels na pasta pública do Drive e `scripts/analisa_reel.py` faz transcrição com tempo por palavra, grade de frames e picos de SFX. A seção "Para medir" lista o que falta.

## O canal em números (09/nov/2026)

| Fonte | Dado |
|---|---|
| Página do curso | 707 mil no Instagram, 445 mil no YouTube, 57 mil no Facebook, 65 mil no TikTok; "mais de 180 milhões de visualizações com 21 vídeos"; "mais de 1 milhão de seguidores em 12 dias" (autopromoção, sem verificação independente) |
| YouTube, Sobre | 460 mil inscritos, 75.424.615 visualizações, 25 vídeos, canal criado em **5 de julho de 2026** |
| YouTube, Sobre | "Criado por Felipe Brandt. Estrelado por Zé Parafuso." O criador também fez o GeoAnalyst |

Quatro meses de canal. A média por vídeo no YouTube passa de 3 milhões. O maior (estádio) tem 8,5 milhões só lá.

## Os 22 Shorts, por visualizações

| Views | Título |
|---|---|
| 8,5 mi | Como se constrói um estádio de futebol? |
| 6,5 mi | Como uma ponte sustenta tanto peso sem cair? |
| 6,3 mi | Como construir um MURO DE ARRIMO? |
| 5,5 mi | Como se constrói um arranha-céu? A engenharia por trás dos gigantes |
| 4,5 mi | Como o elevador funciona? Cabos, contrapeso e freios |
| 4,4 mi | Como um avião tão pesado consegue voar? |
| 4,1 mi | Como uma rua é construída? Muito além do asfalto |
| 4,1 mi | Como um telhado funciona? A engenharia por trás das telhas |
| 3,9 mi | Como uma casa fica de pé? Da fundação ao telhado |
| 3,3 mi | Como uma barragem segura tanta água sem cair? |
| 3,2 mi | Como um paraquedas freia uma queda? O poder do ar |
| 2,7 mi | Como é feito o metrô? |
| 2,7 mi | Como um para-raios protege uma casa? |
| 2,4 mi | Como a fechadura reconhece a chave certa? |
| 2,3 mi | Por que a geladeira esfria por dentro e esquenta por fora? |
| 2,1 mi | Como o bungee jump freia a queda e faz você subir de novo? |
| 2,1 mi | Como o micro-ondas aquece a comida? Não é de dentro para fora! |
| 2 mi | Como uma lâmpada funciona? Do filamento ao LED |
| 1,9 mi | Como o motor do carro transforma gasolina em movimento? |
| 1,8 mi | Como o cinto de segurança trava na hora certa? |
| 1,7 mi | Como o ar-condicionado funciona? Ele não fabrica frio! |
| 592 mil | Como uma sacada fica de pé sem coluna embaixo? (o mais recente) |

## A fórmula de tema

1. **Uma pergunta que todo mundo já se fez e nunca respondeu.** "Como X funciona?", "Como se constrói X?", "Como X segura / sustenta / freia / fica de pé?". O objeto é do cotidiano (elevador, geladeira, telhado, cinto) ou do imaginário coletivo (estádio, ponte, arranha-céu). Nunca um assunto que exige contexto prévio.
2. **O subtítulo derruba uma crença.** "Ele não fabrica frio!", "Não é de dentro para fora!", "Muito além do asfalto", "sem coluna embaixo". O gancho é a surpresa, não a utilidade.
3. **O prêmio é ver por dentro.** O nome do canal é o formato: a câmera abre o objeto (corte, raio-x, explosão de peças) e mostra o mecanismo invisível. O vídeo entrega algo que o olho não alcança na vida real.
4. **Nicho com identidade, cotidiano para alcance.** Onze dos 22 são construção civil e engenharia (fundação, pilar, laje, arrimo, barragem, ponte). O resto são objetos domésticos e veículos. O nicho dá a cara do canal; o cotidiano puxa o público geral.
5. **Um objeto por vídeo.** Nunca lista, nunca "5 coisas". Um mecanismo, do começo ao fim.

## A gramática visual (lida nas 20 capas)

- **Protagonista com rosto e emoção.** Zé Parafuso: boneco low-poly de camisa amarela e calça azul, capacete ou boné, rosto simples que **expressa** (medo no elevador, enjoo, susto, dúvida com interrogações, sorriso). Ele é o "você" do vídeo e aparece em **plano próximo** (meio corpo, rosto) na maioria das capas. Em várias cenas há outras pessoas (torcida, passageiros, operários).
- **Câmera dentro da cena, perspectiva, baixa.** Nada de vista aérea isométrica fixa. A câmera está no elevador, no avião, na calçada olhando o telhado, dentro da sala. Objeto grande no quadro.
- **Corte e raio-x como recurso central.** Fundação vista sob o solo, treliça do telhado sem telha, serpentina da geladeira exposta, prédio em obra com pilares e tijolo, fios de látex em explosão. O vídeo mostra o interior sem explicar que está mostrando.
- **Setas de força e etiquetas.** Setas vermelhas ("3 TONELADAS" sobre o telhado, "A FORÇA SE JUNTA NOS CANTOS" na janela do avião), chips flutuantes com bolinha colorida ("SEM PILARES", "ENJOADO"), rótulos em caixa alta amarela sobre o objeto ("FUNDAÇÃO", "PILARES", "FIOS DE LÁTEX").
- **HUD quando há número.** Paraquedas: `ALTURA 3.860 metros` e `DESCIDA 190 km/h` em cantos opostos.
- **Controle de tempo na tela.** Ícones de avanço rápido (▶▶) e retrocesso (◀◀) quando o vídeo acelera ou volta a cena.
- **Certo e errado desenhados.** X vermelho sobre o que não serve, contorno pontilhado mostrando onde a coisa deveria estar, interrogações sobre a cabeça.
- **Legenda palavra a palavra.** Uma palavra por vez, branca, bold, grande, centralizada no terço inferior, com a palavra-chave em amarelo. Não é a frase de duas linhas que usamos hoje.
- **Luz e cor de dia claro.** Paleta saturada e alegre (verde grama, azul céu, amarelo), sombras suaves, nuvens low-poly. Mesmo o tema sério (barragem, enchente) tem a mesma luz.
- **Ação, não diagrama.** Carro bate no muro, pessoa cai de paraquedas, elevador cheio, fogo no arranha-céu. A física acontece com personagem dentro.

## O processo deles (página do curso)

Seis passos: **Preparação** (configurar o Claude e o kit), **Escolha da ideia**, **Roteiro** ("gancho, ritmo e fechamento: as regras que eu uso para o roteiro prender do início ao fim"), **Produção** ("o Claude no trabalho pesado"), **Refinamento** ("o que ajustar, o que cortar"), **Publicação**. Frases que importam:

- "Criar um vídeo nunca foi tão rápido: com o Claude, o trabalho pesado sai em horas. Mas a IA não sabe sozinha o que faz alguém assistir até o fim."
- "Você pode fazer com um computador de entrada, e nem precisa de placa de vídeo, já que o Claude faz a renderização dos vídeos na nuvem."
- "Funciona para qualquer nicho, desde que o vídeo seja uma animação."
- Na descrição do canal: "Criação de vídeos como a nossa envolve horas de trabalho HUMANO. Existe uso de ferramentas de IA para a edição, mas a maior parte desse curso é voltada para o criador: roteiro, ganchos, decisões artísticas."

Leitura: o pipeline deles é da mesma família do nosso (animação gerada por código a partir do roteiro, render em nuvem). A diferença não está na ferramenta. Está em três coisas: **a escolha do tema** (pergunta universal com surpresa), **a encenação** (personagem com rosto dentro da cena, corte e raio-x, ação física) e **o ritmo** (que ainda precisamos medir nos vídeos).

## Onde a Porcin.IA está e o que muda

| Elemento | Porcin.IA hoje (Parte 3, 05/nov) | Desmontando | Decisão |
|---|---|---|---|
| Câmera | perspectiva, por cenários, plano geral a 30 m e médio a 6 m | sempre próxima, meio corpo, dentro | aproximar mais: close no personagem em cada beat emocional |
| Protagonista | gestor blocado, sem rosto | rosto com emoção | **dar rosto e 5 expressões ao `pessoa` do `kit3d.js`** (neutro, susto, dúvida, alívio, sorriso) |
| Interior | galpão por dentro, baias, porcos animados | corte e raio-x do objeto | adicionar corte: galpão em seção, intestino, úbere, silo, caixa d'água |
| Texto | frase de 2 linhas a cada ~3 s | 1 palavra por vez, chave em amarelo | **testar legenda palavra a palavra** (o `palavras.json` já tem o tempo de cada palavra) em uma peça e comparar retenção |
| Números | HUD de saldo/resultado, chips, delta | HUD só quando há número; setas de força | manter HUD; **adicionar setas e rótulos sobre o objeto** |
| Tempo | "bora acelerar cinco anos" só na fala | ▶▶ e ◀◀ na tela | adicionar ícone de avanço nos saltos de tempo |
| Erro e acerto | legenda | X vermelho e contorno pontilhado | adicionar ao kit |
| Produto | conversa no WhatsApp uma vez por ano narrado | sem produto (canal de mídia) | manter: a Porcin.IA é produto, a conversa fica |
| Tema | "10 milhões", dia do gestor, manejo | "Como X funciona?" | abrir a série **"Por dentro"** com a fórmula deles: "Como o leitão ganha peso?", "Por que a maternidade a 23 graus é fria?", "Como um caminhão leva doença pra granja?" (os roteiros 13, 11 e 16 já são isso) |
| Luz | dia claro com noite quando a cena pede | sempre dia claro | ok |

O que não muda: o porco da marca não entra na cena (não tem mãos), o veterinário decide, valores ilustrativos na legenda, -14 LUFS, pronúncia "Porcínia".

**Reprocessar as 20 peças no padrão novo é decisão do usuário**: cada render leva 20 a 55 minutos, e as 13 agendadas já estão aprovadas pela fundadora como estão.

## Para medir (assim que os vídeos chegarem no Drive)

1. Duração e palavras por minuto dos 8 a 10 reels mais vistos.
2. Gancho: o que é dito e mostrado nos primeiros 3 s; se há SFX antes da primeira palavra.
3. Estrutura: há "pausa rapidinha"? Em que ponto? Quantos atos até a revelação?
4. Voz: humana ou TTS, ritmo, se há mudança de tom na surpresa.
5. Cortes por minuto e duração média de cada plano.
6. SFX por minuto e tipos (whoosh, impacto, tique, risada?).
7. Legenda: palavra a palavra em todo o vídeo ou só nos picos; tamanho; cor da chave.
8. Fecho: pergunta, CTA de seguir, gancho do próximo.
9. Uso de música de fundo e nível relativo.
10. Quantos personagens por cena e se o protagonista fala (boca animada?).

Rodar `python3 -I scripts/analisa_reel.py <pasta>` e registrar aqui, com a mesma tabela do `PADRAO-MAXAGRO.md`.
