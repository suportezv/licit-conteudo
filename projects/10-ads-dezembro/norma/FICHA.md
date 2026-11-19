# Dona Norma: ficha visual

Norma Seabra, 52, pregoeira há dezenove anos numa prefeitura de cidade média do interior.

## Imagens de referência

| Arquivo | Uso |
|---|---|
| `norma_master.png` | Imagem-mestra. Vai como primeiro anexo em toda geração nova |
| `norma_angulos.png` | Frente, três quartos, perfil e costas |
| `norma_expressoes.png` | Seca, cansada, sem jeito, lendo, meio sorriso, sorriso aberto |
| `norma_cena_carimbo.png` | Quadro de teste do roteiro 2 (o carimbo que hesita) |
| `norma_sala.png` | A sala vazia, para ancorar o cenário em todo plano |

## O que não muda (trava de identidade)

- **Rosto:** pele morena clara com textura real, rugas de riso, duas linhas entre as sobrancelhas, sobrancelha reta e forte, olho castanho-escuro de pálpebra pesada, pinta na bochecha esquerda.
- **Cabelo:** grisalho cacheado, mais branco nas têmporas, coque baixo frouxo **preso com uma caneta azul**, fios soltos.
- **Óculos:** de leitura, tartaruga, pendurados num cordão de contas. Só vão ao rosto quando ela lê.
- **Roupa:** cardigã de tricô verde-musgo com bolinhas em relevo, blusa creme de folhinhas verdes.
- **Detalhes:** brinco de bolinha dourado, aliança, relógio de pulseira de couro marrom, unha curta sem esmalte.
- **Corpo e postura:** estatura média, corpo cheio, coluna reta, mãos cruzadas sobre os processos quando escuta.

O verde do cardigã conversa com a Floresta da marca sem ser uniforme. O verde-limão fica só na legenda e na tela do produto.

## A sala

Mesa de madeira, monitor antigo, pilhas de processo com clipes coloridos, garrafa térmica e copinho de café, a jiboia no vaso preto, arquivos de aço bege com etiqueta, relógio redondo de parede, ar-condicionado de janela velho, persiana com luz do dia vindo da esquerda. Sem brasão, sem nome de prefeitura, sem logo.

## Expressão por momento do roteiro

| Momento | Expressão |
|---|---|
| Gancho ("Vieram duas", "inabilitei o menor preço") | Seca, sobrancelha levantada |
| "Eu não gosto de fazer isso" | Sem jeito, lábio apertado, olha para baixo |
| "Eu não posso te ligar" | Cansada, óculos na mão |
| Conferindo a tela | Óculos no rosto, concentrada |
| "Não garanto que você ganha..." | Meio sorriso |
| "Eu prefiro mil vezes habilitar" | Sorriso aberto, o único da peça |

## Ângulos de câmera (mínimo de quatro por peça)

1. Close frontal, olho na lente (gancho e fecho).
2. Plano médio na mesa, com a térmica e os processos.
3. Perfil ou três quartos junto da janela (a virada).
4. Por cima do ombro, para a tela.
5. Detalhe: mão com o carimbo, óculos sendo postos, café sendo servido.

## Prompt base (colar em toda geração, com `norma_master.png` como anexo 1)

```
Attachment 1 is the reference of the character Dona Norma. Keep EXACTLY the same woman: same face, age, skin, mole on the left cheek, salt-and-pepper hair in a loose low bun held by a blue ballpoint pen, tortoiseshell glasses on a beaded cord, moss-green knitted cardigan, cream blouse with small green leaf print, gold stud earrings, wedding band, brown leather watch. A 52-year-old Brazilian municipal procurement officer, dry, tired but warm, a real person, no caricature.
Setting: a real Brazilian city hall office, beige metal filing cabinets, stacks of procurement files with colored clips, steel thermos of coffee, pothos plant, round wall clock, old wall air conditioner, window blinds with soft daylight from the left.
Style: photorealistic cinematic still, 35mm lens look, shallow depth of field, muted greens, creams, wood and paper, fine film grain. No text, no logos.
```

Gerado com `gpt-image-2`, 1024x1536, qualidade alta (`scripts/gera_imagem.py openai ... --ref norma_master.png`).

## Voz (para quando formos gravar)

Mulher de 50 e poucos, grave médio, interior de São Paulo ou Minas sem sotaque carregado, ritmo calmo, frase curta, ironia leve. Nunca estridente, nunca locutora.
