# Estreia do perfil, 10/nov/2026

Framework: **Remotion** (ver `FRAMEWORK.md`). Textos em `pecas.json`, render por `python3 projects/01-estreia/gera.py`, saída em `out/` (fora do git).

**Situação: carrosséis aprovados pelo usuário em 10/nov. Vídeo na versão 3, aguardando aprovação. Nada agendado.**

Confirmado pelo usuário em 10/nov: a condição vale até **19 de dezembro**; o trial é **sem cartão** e, depois dos 30 dias, a contratação é pedida quando o usuário voltar a usar; o cadastro está funcionando.

| # | Peça | Arquivos | Formato | Canais |
|---|---|---|---|---|
| 1 | Chegou a Licit | `anuncio-chegou-a-licit.mp4` | Vídeo 9:16, 30 s, trilha e efeitos, sem narração | Instagram (Reel), TikTok, LinkedIn |
| 2 | Seu próximo contrato pode estar numa licitação que você não viu (as cinco etapas) | `etapas-01.png` a `etapas-07.png` | Carrossel 4:5, 7 telas | Instagram, LinkedIn |
| 3 | 30 dias para usar a Licit (fixar) | `oferta-01.png` a `oferta-04.png` | Carrossel 4:5, 4 telas | Instagram, LinkedIn; TikTok como carrossel de fotos |

## O que mudou da versão 1 para a 2

A versão 1 foi recusada pelo usuário: "muito clean, isso em rede social vai virar paisagem, ou panfleto", "institucional e formal demais". A versão 2 troca o molde:

- **Gancho na capa**, não título descritivo: "Seu próximo contrato pode estar numa licitação que você não viu" (frase do site).
- **Tela do produto como elemento visual** em toda etapa: cartão branco inclinado com busca por CNPJ, pergunta ao edital, checklist de certidões, tarefas e resultado.
- **Numeral gigante** (01 a 05, e o 30 da oferta) e **palavra-chave em pílula** de cor.
- **Bloco de cor cheio**: a oferta vai em verde-limão de ponta a ponta. Fundos alternam grafite e floresta.
- **Títulos em tom de conversa**: pergunta, frase curta, sem rótulo institucional.
- **Vídeo com cenas que se sobrepõem**, a estrela girando na abertura, as telas se montando, o 30 contando e efeitos sonoros a cada entrada.

O exemplo das telas (equipamentos de informática, São José dos Campos, R$ 480.000, 2º lugar) é o cenário ilustrativo do próprio site.

## Vídeo, versão 3 (ajustes pedidos em 10/nov)

O usuário pediu: tirar a travada por volta de 2 s, chegar a 30 s para dar tempo de ler, dar mais profundidade à virada dos cartões e sincronizar o surgimento dos elementos com os efeitos sonoros.

- **Travada**: a abertura terminava de animar em 1,3 s e ficava parada até 2,4 s. Agora tudo tem movimento contínuo (a estrela segue girando, o título e as telas flutuam). Conferido quadro a quadro: nenhum trecho parado acima de 0,5 s.
- **Tempo de leitura**: abertura 3,2 s, gancho 5,3 s (3 s parado depois da última linha), cada etapa 3,3 s, oferta 5 s.
- **Profundidade**: a cena nova sobe por cima da anterior, como na versão 2, agora em camadas: a que sai recua (diminui, escurece e desfoca), a que entra sobe com sombra e cantos que se abrem, e o conteúdo chega um pouco depois do fundo. A tela do produto chega de longe, inclinada. Uma tentativa intermediária com cenas girando como faces de um cubo foi recusada pelo usuário: "não queria uma forma geométrica 3D girando".
- **Sincronia**: uma linha do tempo única (`TL` em `remotion/src/Anuncio.tsx`) dispara o elemento e o som. Os efeitos foram aparados para soar no instante 0. Medido sem trilha: todo efeito começa a menos de um quadro (33 ms) do elemento, do início ao fim.
- **Tique das linhas**: o da biblioteca sumia por baixo da trilha (25 dB abaixo); trocado por um tique de 1,85 kHz gerado para o filme (`remotion/public/sfx/tique.mp3`).

## Legendas

### 1. Chegou a Licit

```
Seu próximo contrato pode estar numa licitação que você ainda não viu.

Chegou a Licit: você encontra oportunidades pelo CNPJ, pergunta ao edital, organiza certidões e proposta, distribui as tarefas e confere o resultado. Tudo na mesma licitação.

Serve para quem vai disputar a primeira e para quem já tem equipe ou assessoria.

No lançamento: 30 dias para usar, sem cartão. Vale para quem começa até 19 de dezembro. Link na bio.

A sua empresa já vendeu para o governo?

#licitacoes #licitacao #pregaoeletronico #PNCP #vendaparaogoverno #comprasgovernamentais #Licit
```

Título no TikTok: `Seu próximo contrato pode estar numa licitação que você não viu`

### 2. As cinco etapas

```
Licitação não é um documento. É uma sequência, e cada etapa tem a sua armadilha.

Achar o edital que vale o seu tempo. Descobrir o que ele pede sem ler tudo três vezes. Não ser pego por certidão vencida. Saber quem cuida do quê. E guardar o que aconteceu para a próxima.

Arrasta para ver as cinco etapas na Licit.

No lançamento: 30 dias para usar, sem cartão. Vale para quem começa até 19 de dezembro. Link na bio.

Em qual etapa a sua empresa mais perde tempo?

#licitacoes #licitacao #edital #certidoes #PNCP #vendaparaogoverno #Licit
```

### 3. 30 dias para usar a Licit

```
30 dias para usar a Licit. Sem cartão.

Você começa pelo CNPJ, escolhe uma licitação e segue com a análise do edital, os documentos e a proposta.

Depois dos 30 dias, a contratação só aparece se você voltar a usar.

Vale para quem começa até 19 de dezembro. Link na bio.

#licitacoes #licitacao #pregaoeletronico #vendaparaogoverno #comprasgovernamentais #Licit
```

## Conferência

- Sem travessão em nenhum texto público.
- Nenhuma promessa de vitória, número de clientes ou dado do cenário de demonstração do topo do site.
- "A certidão vence antes da proposta? Você fica sabendo." descreve o aviso de validade que o site declara; não afirma efeito jurídico da certidão vencida.
- Assinatura: institucional (Profissio Licit) nas capas e nos blocos de oferta, estrela + Licit nas telas internas.
- Vídeo: 1080x1920, 30 fps, 30 s, master entre -14 e -16 LUFS.
- O bloco verde cheio e as pílulas vão além do manual de marca, que pede o acento "contido". Decisão do usuário, registrada no `CLAUDE.md`.
