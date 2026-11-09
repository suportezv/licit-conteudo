# Por Dentro da Licitação: instruções para implementar o formato na Licit (profissiolicit.ai)

Documento de transferência, escrito em 09/nov/2026 a partir de tudo que a produção da Porcin.IA aprendeu com 23 peças do formato (Partes 1, 2 e 3 da série "10 milhões" e 20 peças avulsas), do padrão medido do maxagroapp (`PADRAO-MAXAGRO.md`) e do estudo do @desmontandoomundo (`PADRAO-DESMONTANDO.md`). Serve para quem for montar a editoria no estúdio da Licit: uma pessoa ou uma sessão do Claude com este repositório como referência.

Leia nesta ordem: 1 (o que é a editoria), 2 (o produto e as regras), 3 (o formato), 4 (a pauta), 5 (o sistema visual), 6 (a linha de produção), 7 (o roteiro modelo), 8 (QA), 9 (legenda e agendamento), 10 (pendências).

---

## 1. O que é a editoria

**Nome proposto: "Por Dentro da Licitação".** Vídeos verticais de 130 a 160 segundos, animação 3D low-poly gerada por código, narração em off, protagonista "você" dentro da cena, um contador na tela que sobe ou desce, efeitos sonoros a cada poucos segundos, e um fecho que pede comentário. O espectador entra numa licitação por dentro: do edital que ninguém lê até o pagamento que demora.

**Por que esse formato para a Licit.** O produto da Licit é exatamente a sequência que o formato encena: encontrar, analisar, preparar, acompanhar, conferir. Cada vídeo mostra a jornada acontecendo com uma pessoa dentro, e o produto aparece uma vez por ato como a tela que resolve o passo. Não é um canal de conteúdo com anúncio no fim. É uma plataforma mostrando a si mesma dentro de uma história.

**O que não é.** Não é aula de direito administrativo, não é notícia de licitação, não é promessa de contrato. Quem decide participar, o preço e o recurso é a empresa, com a assessoria dela.

---

## 2. O produto, a voz e as regras

### O produto (lido no site em 09/nov/2026)

- **Licit, "Toda a sua operação de licitações". Um produto Profissio.** Site `profissiolicit.ai`, em protótipo público: "Consulta de empresa, oportunidades, autenticação e análise usam cenários de demonstração."
- **Promessa**: "Venda para o governo. Saiba o que fazer em cada etapa." Cinco etapas: **Encontre** (oportunidades do PNCP cruzadas com o CNPJ), **Analise** (requisitos, documentos e prazos; "pergunte ao edital em linguagem simples e confira as referências", com página do edital citada), **Prepare** (certidões reunidas com validade e aviso de renovação; proposta montada a partir das exigências, "você preenche os preços"), **Acompanhe** (tarefas com responsável e prazo, sessão, avisos), **Confira** (resultado e classificação publicados no PNCP junto do histórico).
- **Público**: empresas que fornecem produtos, prestam serviços ou executam obras para órgãos públicos. Dois momentos: **"Vai disputar sua primeira licitação?"** (começa pelo CNPJ, sem dominar o processo) e **"Já tem equipe ou assessoria?"** (operação no mesmo ambiente).
- **CTAs do site** (usar estes): "Descobrir oportunidades grátis", "Consulta grátis pelo CNPJ. Sem criar uma conta.", "Fale com a Licit", "Começar", "Já tem um edital? Comece por ele."
- **Exemplo oficial do site**: "Fornecimento de equipamentos de informática, São José dos Campos, SP, valor estimado R$ 480.000, pregão eletrônico, entrega das propostas 19 nov 10:00, prazo de entrega 30 dias (edital, página 25), garantia 12 meses (p. 26), certidão FGTS vence em 15 nov, resultado: 2º lugar, valor homologado R$ 426.000, proposta da empresa R$ 438.000." É o cenário que o produto já conta; os vídeos podem partir dele.
- **Redes no rodapé do site**: Instagram, LinkedIn, TikTok. Blog "Licitações na prática" com o artigo "Como o governo compra: do planejamento ao pagamento" (já é um roteiro pronto para o formato "como funciona").
- **Identidade visual medida no CSS do site**: verde profundo `#243d32` (cor principal), verde-limão `#a8f27a` (destaque), tinta `#101218`, cinza `#59616e`, fundo claro `#f4f6f9`, verdes claros `#edf2ed` e `#e0ebe1`, verde-musgo `#7b9c81`, dourado `#8a6c27`, aviso `#fff2cc`. Fonte **Sora** (a mesma da Profissio.ai). **O logo oficial e o símbolo precisam vir da equipe como arquivo**; nunca desenhar um wordmark aproximado (a Porcin.IA perdeu uma rodada inteira por isso).

### A voz (herdada do `FRAMEWORK.md` da Profissio.ai, ajustada à Licit)

- Direta, competente e concreta. Nada de hype de IA, nada de "revolucione". Mostrar o trabalho sendo resolvido, com número quando houver.
- Quem fala é a marca, em off. Não há rosto de autoridade nem credencial de criador.
- Tratamento "você" para quem está na empresa. O público é B2B: dono, sócio, gestor de licitações, assessoria.

### Regras inegociáveis

1. **Nunca usar travessão em texto público.** Reescrever a frase.
2. **Loudness final -14 LUFS**, true peak -1 dBTP.
3. **Nenhuma orientação jurídica no vídeo.** O formato mostra a mecânica; quem decide é a empresa com a assessoria. Frase padrão para a legenda: "Cenário ilustrativo. A decisão de participar, o preço e qualquer recurso são da sua empresa, com a sua assessoria."
4. **Nenhuma promessa de resultado.** O produto organiza e orienta; não ganha licitação.
5. **Valores e prazos ilustrativos vão na legenda, não na tela.** Na tela entram números redondos. Dados reais do PNCP (quantidade de licitações, valores em disputa) só com data e fonte na legenda.
6. **Vocabulário técnico só quando o vídeo explica.** Pregão, dispensa, habilitação, empenho, ata de registro de preços, ME e EPP: cada termo entra com a cena que o mostra, nunca solto.
7. **Todo roteiro passa por um especialista antes de gravar.** Na Porcin.IA é a fundadora, veterinária. Na Licit precisa ser alguém que opera licitação (assessoria ou advogado administrativista). Dois vídeos da Porcin.IA foram descartados por erro conceitual depois de prontos; é mais barato validar o roteiro.
8. **O protagonista não tem nome de empresa real nem CNPJ real.** Órgão fictício ou genérico ("a prefeitura", "o órgão") a não ser que o roteiro use um exemplo público com fonte.

---

## 3. O formato, medido e ajustado

### As regras que vieram da referência (maxagroapp, 14 vídeos medidos)

1. **130 a 160 s, 320 a 400 palavras, 146 a 158 palavras por minuto.** Parte 2 fica em 115 a 130 s. Vídeos curtos (45 a 75 s) não são o formato; esse erro já foi cometido e corrigido.
2. **Abre com o sonho e o primeiro número em 12 s.** "Você tem um CNPJ, uma empresa de informática e o sonho de vender pra prefeitura. Só que começa assim: um edital de 80 páginas e 12 dias de prazo."
3. **Um motor na tela, fixo no topo.** Na série "10 milhões" é o saldo que desce. Na Licit o motor é o **PRAZO** (dias e horas até a sessão) e, ao lado, um placar da etapa (**DOCUMENTOS 0/6**, **PROPOSTA R$ ...**, **CLASSIFICAÇÃO 3º**). O motor é falado a cada duas ou três cenas.
4. **Cada passo nasce de uma consequência do anterior.** "Abriu o edital, achou o objeto. Foi ver a habilitação: pede certidão do FGTS. Foi puxar a certidão: venceu semana passada." Nunca lista.
5. **Texto na tela por beat**, troca a cada ~3 s, com uma palavra em destaque. (Ver 5.4 sobre o modo palavra a palavra.)
6. **"Ô, pausa rapidinha. Deixa o like e segue a Licit pra ver se [a tensão do próprio vídeo]. Bora continuar."** Entre 40 % e 55 % do vídeo, tela em preto e branco com ícone de pause, 5 a 7 s. O pedido usa o gancho do vídeo ("pra ver se a proposta entra antes das dez").
7. **SFX a cada 4 a 6 s**: pop quando um objeto entra, carimbo em documento, tique no prazo, registradora em valor, alarme em erro, efeito no último segundo. Todos nivelados (ver 6.5).
8. **Uma virada que custa ativo, não o motor**: a certidão vencida, o anexo que não abriu, a proposta enviada no item errado, a amostra reprovada. A virada tem lição de uma frase e o vídeo continua.
9. **A espera entra como etapa.** Na suinocultura é a ração até a venda; na licitação é **o tempo entre vencer e receber** (empenho, entrega, atesto, pagamento) e o tempo de renovar certidão.
10. **Fecho em fórmula**: "Do CNPJ ao contrato: [lista]. E o prazo? Entrou com 40 minutos de sobra. Mas será que ganhou? Isso fica pra parte dois. Segue a Licit pra não perder." Selo `PARTE 2 EM BREVE`.
11. **A marca não vende no vídeo.** Logo pequeno fixo no canto, nome falado só na pausa e no fecho. A diferença em relação ao maxagroapp: **o produto aparece como tela, uma vez por ato** (regra 12).
12. **O produto é a tela que resolve o passo** (aprendido na Parte 3 da Porcin.IA): um cartão com a interface real da Licit entra uma vez por ato, com o texto exato do produto. Exemplos: o chat "Quando preciso entregar os equipamentos?" respondido com "Em até 30 dias após a ordem de fornecimento. Edital, página 25"; o checklist "Cartão CNPJ: já salvo. Certidão FGTS: vence em 15 nov, renovar antes da entrega."; a tarefa "Renovar a certidão FGTS. Ana, antes da entrega da proposta". Enquanto o cartão está na tela, o logo do rodapé some. Fora do cartão, ninguém fala do produto.

### Os ajustes que a Porcin.IA fez e que valem desde o primeiro vídeo da Licit

Cada item abaixo custou uma recusa do usuário, uma correção da fundadora ou um render perdido. Entram como regra, não como sugestão.

1. **Logo oficial, legível sobre fundo escuro.** A primeira versão da Parte 1 foi recusada por usar um logo de traço fino que não lia. Versão recortada com alfa, testada em frame escuro, antes de qualquer render.
2. **Efeitos nivelados antes de montar.** SFX gerados por IA saem entre -5 e -38 LUFS no mesmo lote; uma buzina a -5 contra a voz a -20 assusta e cobre a narração. Regra: narração a **-19 LUFS**, efeito de um tiro a **-28 LUFS**, cama a 0,07 de volume, e os impactos (buzina, alarme, thud, sting) com 3 dB a menos ainda. Master final por loudnorm em duas passagens mais limiter: **-14,2 LUFS, -1 dBTP**.
3. **Pronúncia do nome decidida antes de gravar.** "Porcin.IA" virou "Porcínia" por decisão do usuário. Para a Licit: decidir se o TTS fala "Licít" ou "Lí-cit" e **validar com o Scribe** (se a transcrição devolver o nome certo, a tônica está certa). Escrever no texto do TTS com acento se precisar.
4. **Câmera em perspectiva, por cenários, dentro da cena.** O usuário recusou a vista aérea isométrica monótona ("maquetes grosseiras, só imagens aéreas indo de lá pra cá"). Regra de enquadramento em retrato: o campo horizontal é só 56 % do vertical, então plano geral a 30 a 40 m com fov 48 a 50, plano médio a 6 a 10 m, close a 3 a 5 m; câmera de interior fica **dentro** do ambiente. Corte seco entre cenários, deriva lenta dentro do plano.
5. **Personagem do gestor em cena**, fazendo coisas (no celular, apontando, andando), com funcionários e visitantes. Na Licit: a pessoa da empresa, a sócia, o atendente do órgão, a equipe.
6. **Interiores e zoom.** Dentro do galpão, dentro do escritório, close no objeto. Nada de contar a história só de cima.
7. **O que a narração cita tem que estar na tela.** A fundadora pegou "a linha pontilhada mostra onde estaria" sem linha nenhuma; entrou um gráfico de linhas com a pontilhada. Todo número e todo objeto citado aparece.
8. **Número na tela e número falado fecham a conta.** Os anos arredondados na tela somavam 800 mil, o imposto era 700 mil, e a narração dizia "sobraram 70 mil" (a conta exata). A fundadora somou na planilha e não fechou. Regra: **o que é falado é a conta dos números mostrados**, e a Parte 3 carrega os mesmos valores da Parte 2.
9. **Conceito técnico validado.** "Via de entrada" (o caminhão) estava errado; o caminhão é via de transmissão, porta de entrada é no animal. Na Licit os equivalentes são: inabilitação não é desclassificação, dispensa não é inexigibilidade, empenho não é pagamento, ata de registro de preços não é contrato. Cada um desses só entra com o especialista de acordo.
10. **Piso de leitura.** Toda frase na tela fica 0,5 s mais 0,3 s por palavra (uma resposta de 12 palavras precisa de 4,1 s). Nada parado mais de 3 s sem um movimento começar. O `hyperframes check` mede os dois.
11. **Legenda com mais de 32 caracteres cai para 40 px**: encurtar a frase, não o corpo. Piso tipográfico de 28 px no lado curto de 1080 (rótulo de HUD a 24 px é reprovado).
12. **Bolinhas de progresso e contadores são 1-based** e precisam ser conferidos no frame final: a Parte 3 saiu com a primeira bolinha apagada e a quinta nunca acesa por um `n - 1`.
13. **Âncoras de palavra curta contam todas as ocorrências, sem diferenciar maiúscula**: "E" cai em "e meio". Ancorar na palavra seguinte ou contar as ocorrências antes.
14. **Conferir no render final, não só no snapshot.** O contato de frames do MP4 entregue é a última etapa, e foi ele que confirmou cada correção.

### O que o @desmontandoomundo acrescenta (ver `PADRAO-DESMONTANDO.md`)

- **Tema como pergunta universal com surpresa**: "Como o governo compra? Não é quem dá o menor preço." "Por que a certidão vencida derruba a proposta inteira?" "Como funciona um pregão eletrônico por dentro?"
- **Protagonista com rosto e emoção**, em plano próximo nos beats de tensão (susto no prazo, dúvida no edital, alívio no resultado).
- **Corte e raio-x do objeto**: o edital aberto como um prédio de seções (objeto, habilitação, proposta, prazos, anexos), a certidão como cartão com validade, o PNCP como painel da cidade, a sessão do pregão como placar.
- **Setas e etiquetas sobre o objeto**, chips com bolinha colorida ("VENCIDA", "FALTA ANEXO", "3º LUGAR"), X vermelho no erro, contorno pontilhado onde a coisa deveria estar, ▶▶ nos saltos de tempo.
- **Legenda palavra a palavra com a chave em cor** como variante a testar (a infraestrutura de tempo por palavra já existe).
- **Luz de dia claro** e ação física (o caminhão chega, a tela trava, o relógio vira).

---

## 4. A pauta: séries e primeiras 12 peças

Alternar as séries na publicação, duas por semana, para a editoria não virar um curso de 10 semanas.

### Série A: "A primeira licitação" (o "10 milhões" da Licit)

| # | Peça | Motor | Virada | Produto na tela |
|---|---|---|---|---|
| A1 | **"Você tem um CNPJ e vai disputar sua primeira licitação"**: do edital achado no PNCP até a proposta enviada, contra o prazo | `PRAZO 12 dias` descendo até `0h40`; `DOCUMENTOS 0/6` subindo | certidão do FGTS vencida descoberta no dia 9 | chat ao edital (prazo de entrega, p. 25); checklist de documentos |
| A2 | **"Parte 2: a sessão"**: o pregão eletrônico ao vivo, lances, empate ficto de ME, habilitação do primeiro colocado, recurso | `CLASSIFICAÇÃO` e `SEU LANCE R$ ...` | o primeiro colocado inabilitado por atestado; a empresa sobe | tarefa "Acompanhar a sessão, Ana, 19 nov 10:15"; resultado publicado no PNCP |
| A3 | **"Parte 3: venceu. E o dinheiro?"**: empenho, ordem de fornecimento, entrega, atesto, pagamento, e a próxima licitação começando pela base já pronta | `A RECEBER R$ 426 mil` e `DIAS` até o pagamento | a nota fiscal devolvida por divergência | histórico da participação; certidões reutilizadas na próxima |

A3 fecha com a mensagem da Licit: "A próxima licitação não precisa começar do zero."

### Série B: "Como funciona" (a fórmula do @desmontandoomundo)

| # | Peça | Objeto aberto por dentro |
|---|---|---|
| B1 | **Como o governo compra: do planejamento ao pagamento** (já existe como artigo no blog da Licit) | o ciclo inteiro como uma linha de montagem |
| B2 | **Por dentro de um edital: o que as 80 páginas escondem** | o edital como prédio: objeto, habilitação, proposta, julgamento, prazos, anexos |
| B3 | **Como funciona um pregão eletrônico? Não é quem dá o menor preço** | a sessão como placar: lances, empate ficto, habilitação, recurso |
| B4 | **Como uma certidão vencida derruba a proposta inteira** | a certidão como cartão com validade; o calendário |
| B5 | **O que é o PNCP e como as oportunidades chegam até você** | o painel da cidade; o CNPJ como chave |
| B6 | **Dispensa eletrônica: a licitação pequena que quase ninguém disputa** | a prateleira de compras pequenas |

### Série C: "O dia a dia" (o gestor de licitações)

| # | Peça | Motor |
|---|---|---|
| C1 | **Seis da manhã, três editais vencendo hoje e a assessoria de férias** | relógio do dia e pendências |
| C2 | **Venceu a licitação e perdeu dinheiro: onde foram parar os R$ 40 mil?** | prejuízo devolvido por item (preço abaixo do custo, frete, prazo de pagamento, multa) |
| C3 | **Duas empresas, mesmo edital. Uma classificada, outra inabilitada. A diferença foi um anexo** | comparativo com dois placares |

**Validar com o especialista antes de roteirizar** (lista aberta): modalidades e quando cada uma se aplica (pregão, concorrência, dispensa eletrônica, inexigibilidade), o que é habilitação jurídica, fiscal, técnica e econômica, quais certidões são exigidas na prática e as validades, o empate ficto de ME e EPP e o percentual, prazos de recurso, ordem das fases no pregão (proposta, lances, julgamento, habilitação, recurso, adjudicação, homologação), empenho e prazo de pagamento, ata de registro de preços, SICAF, e a lei em vigor (14.133/2021) sem citar artigo na tela.

---

## 5. O sistema visual

### 5.1 Mundo

Um conjunto de cenários a 120 unidades um do outro na mesma cena 3D (padrão da Parte 3): **escritório da empresa** (mesa, computador com a tela da Licit, janela, quadro de prazos), **prédio do órgão** (fachada pública, balcão, mural de avisos), **cidade** (rua, prédios, o painel do PNCP como outdoor), **sessão** (a tela do pregão em primeiro plano, placar de lances), **galpão e entrega** (caminhão, caixas, conferência), **casa** (o fim do dia). Câmera em perspectiva com chaves por cenário, corte seco entre eles, deriva lenta dentro do plano.

### 5.2 Paleta

Da Licit, não da Profissio.ai: verde profundo `#243d32` como cor estrutural (HUD, cartões, texto de apoio), verde-limão `#a8f27a` como destaque (palavra-chave, acerto, delta positivo), tinta `#101218`, fundo da cena em dia claro (céu azul suave, grama e concreto claros), dourado `#8a6c27` para "dinheiro" e aviso `#fff2cc` para prazo apertado. Erro e perda em vermelho-coral (definir um hex com a equipe; o site não tem). Fonte Sora em tudo.

### 5.3 Kit de modelos (começar pelo `lib/kit3d.js` da Porcin.IA)

Já existe e se reaproveita: pessoa blocada com boné ou jaleco e celular, animações (parado, celular, andando, apontando), caminhão, galpão, cerca, árvore, grama, casa com varanda, carro, caixa d'água, portaria. **Trocar**: as pessoas ganham roupa social e camisa polo; **criar**: prédio do órgão com colunas e bandeira, mesa de escritório com monitor, documento 3D (o edital) que abre em seções, cartão de certidão com faixa de validade, calendário de parede com dias caindo, placar de lances, caixa e nota fiscal, carimbo, relógio de parede. **Adicionar ao kit, por causa do @desmontandoomundo**: rosto com cinco expressões na pessoa, setas de força, chip com bolinha, X vermelho, contorno pontilhado, ícone ▶▶.

### 5.4 Texto na tela

- Padrão atual: **duas linhas, até 32 caracteres cada**, branca com a segunda linha ou a palavra-chave em verde-limão, no topo abaixo do HUD (`top + 212`), troca por beat.
- Variante a testar na peça B1: **uma palavra por vez**, a partir do tempo por palavra do Scribe, palavra-chave em verde-limão. Medir retenção contra o padrão antes de adotar.
- Cartões: pílulas (lado a lado), tag flutuante, medidor, barras, gráfico de linhas (com pontilhada), conversa. **Novo para a Licit**: o cartão de interface do produto (ver 3.12), feito com os textos exatos do site e as cores da Licit, em cima de uma captura real da tela quando houver.

### 5.5 HUD

Pílula no topo (`top 196`), rótulo a 28 px, valor grande, bolinhas de progresso quando há etapas (1-based), delta a 38 px em `top + 140`, segundo HUD à direita quando há duas grandezas (prazo e documentos; classificação e lance).

---

## 6. A linha de produção (portar de `projects/trend-granja-10-milhoes/lib/`)

### 6.1 Ambiente

Mesmo setup do estúdio Porcin.IA, que já é o do estúdio Profissio.ai: `scripts/setup.sh` (ffmpeg estático, video-use, hyperframes com 20 skills, Remotion opcional), `scripts/validate.sh`, `scripts/hf_vendor.sh` (vendoriza assets de CDN porque o navegador do render não confia no CA do proxy), variáveis `HYPERFRAMES_BROWSER_PATH`, `HYPERFRAMES_SKIP_SKILLS=1`, `NODE_USE_ENV_PROXY=1` no `.claude/settings.json`. **Fixar `npx --yes hyperframes@0.9.14`** (o `latest` quebrou no meio de uma fila). Fontes embutidas em `assets/fonts/` (Google Fonts está fora do render). Allowlist mínima: `drive.google.com`, `drive.usercontent.google.com`, `api.elevenlabs.io`, registries, `raw.githubusercontent.com`, `cdn.jsdelivr.net`, mais `profissiolicit.ai` e `www.profissiolicit.ai`.

### 6.2 O que copiar (e renomear)

| Arquivo da Porcin.IA | Papel | O que muda na Licit |
|---|---|---|
| `lib/hf_peca.py` | gerador de qualquer peça: segmentos, âncoras por palavra, legendas, SFX, câmera, HUDs, cartões, pausa, endcard | paleta (constantes `MAG`, `LAV`, `CIANO`, `VERDE` viram os tokens da Licit), fonte Sora, logo do rodapé, texto da pausa ("segue a Licit"), endcard ("Descubra oportunidades grátis pelo CNPJ: link na bio") |
| `lib/kit3d.js` | fábrica de modelos | ver 5.3 |
| `lib/diorama.js` | fábrica de cenas, despacha `cfg.cena` | sem mudança |
| `lib/cena_parte3.js` | cena por cenários em perspectiva | base da `cena_licit.js` |
| `lib/nova_peca.sh` | cria a pasta da peça e copia as libs | sem mudança |
| `narra.py`, `normaliza_audio.py`, `palavras.py` | TTS por segmento com texto anterior e seguinte, nivelamento, tempo por palavra | voice_id da Licit |
| `lib/fila_runner.sh`, `lib/FILA_RENDER.txt`, `lib/finaliza.sh` | fila de render, loudnorm e limiter, tira de frames | sem mudança |
| `scripts/analisa_reel.py` | decupar referência | sem mudança |

### 6.3 Sequência de uma peça

1. `bash lib/nova_peca.sh video-A1-primeira-licitacao`.
2. Escrever `ROTEIRO.md` (segmentos numerados, conta ilustrativa, lista "validar com o especialista") e mandar para validação **antes** de gravar.
3. Escrever `gera.py`: `SEG` com a narração por segmento; `Peca(SEG, pausa_seg="07")`; tudo por âncora de palavra (`at("03", "certidão")`): `cap`, `sfx`, `shot`, `hud_set`, `val`, `delta`, `dot`, cartões, `conversa` ou o cartão de interface, eventos da cena.
4. `python3 narra.py` (ElevenLabs, com `previous_text` e `next_text`, validação por Scribe), `python3 normaliza_audio.py`, `python3 -I palavras.py`, `python3 gera.py`.
5. `npx --yes hyperframes@0.9.14 snapshot --at <tempos-chave> --no-end -o renders/snap --json` e **ler o contato** (foi o snapshot que pegou câmera colada, cena escura, personagem escondido, corte dentro da cortina).
6. `check --json` em background (4 min por 170 s de vídeo) até `ok: true`, sem erro de lint, layout, contraste ou áudio; ler os avisos de craft (`line_unread`, `dead_stretch`).
7. `render . --quality looks --workers 2 --keep-segments --resume -o renders/raw.mp4` com `HF_SEGMENTED_CAPTURE=true` (o container pode reiniciar no meio; `--resume` reaproveita). 110 s rendem em ~28 min; 157 s em ~45 a 55 min.
8. `bash lib/finaliza.sh <pasta> <nome>` (loudnorm, limiter, -14,2 LUFS, tira de frames) e conferir os frames dos momentos corrigidos **no MP4 final**.
9. Entregar, registrar em `FILA.md`, commitar fontes (mp3 de narração e logos com `git add -f`, MP4 fora do git).

### 6.4 Fila

`bash lib/fila_runner.sh` em background lê `FILA_RENDER.txt`, pula quem já tem `raw.mp4`, roda check e render um por vez. O harness mata processo em background depois de 2 h e leva o render junto: relançar o runner **a cada entrega**, entre renders.

### 6.5 Áudio

- Voz: ElevenLabs `eleven_multilingual_v2`, settings de partida stability 0,45, similarity 0,8, style 0,35 (a voz provisória da Porcin.IA é `YU8EsJtXFMyKMxYtheDk`; **a Licit escolhe a dela**). Um mp3 por segmento, `data-duration` explícita em todo `<audio>`.
- SFX: ElevenLabs `sound-generation` (0,5 a 22 s; `duration_seconds` abaixo de 0,5 devolve JSON de erro gravado como mp3 de 188 bytes, conferir com `ffprobe`). Tique curto por ffmpeg (`sine` + `afade`). Quatro faixas rotativas.
- Níveis: narração -19 LUFS, SFX -28 LUFS, cama 0,07, impactos com -3 dB extras; `ebur128` por arquivo em todo lote.
- Master: -14,2 LUFS, -1 dBTP.

---

## 7. Roteiro modelo: A1, "Você tem um CNPJ e vai disputar sua primeira licitação"

Ilustrativo, 12 segmentos, ~380 palavras, 140 a 150 s. Os números são redondos e **todos precisam do aval do especialista** (lista no fim). Motor: `PRAZO` (dias, depois horas) no HUD da esquerda, `DOCUMENTOS 0/6` com seis bolinhas à direita.

| Seg | Narração | Tela e cena |
|---|---|---|
| 01 | Você tem um CNPJ, uma empresa de informática e um sonho: vender pra prefeitura. Só que começa assim: um edital de oitenta páginas e doze dias de prazo. Bora disputar a sua primeira licitação. | Plano geral do escritório, o protagonista na mesa; HUD `PRAZO 12 dias`, `DOCUMENTOS 0/6`; chord de abertura; legenda "Sua primeira licitação" / "12 dias de prazo." |
| 02 | Dia um. A oportunidade apareceu no PNCP: fornecimento de computadores, quatrocentos e oitenta mil reais, pregão eletrônico, entrega em trinta dias. Na região da empresa. Vale avaliar. | Corte para a cidade: o painel do PNCP como outdoor; chip `R$ 480 mil`; registradora; cartão de interface: a oportunidade como aparece na Licit |
| 03 | Dia dois. Abrir o edital. Objeto, habilitação, proposta, julgamento, prazos, anexos. Oitenta páginas que decidem se a sua empresa entra ou fica de fora. | Close no edital 3D abrindo em seções com rótulos; setas; "Onde está o que importa?" |
| 04 | Dia três. A pergunta que trava todo mundo: quando preciso entregar? A resposta está na página vinte e cinco: até trinta dias depois da ordem de fornecimento. Dá. | Cartão de interface: chat "Quando preciso entregar os equipamentos?" e resposta com "Edital, página 25"; pop |
| 05 | Dia cinco. A habilitação pede seis documentos. Cartão CNPJ, já tem. Contrato social, já tem. Certidão federal, estadual, municipal: puxou os três. Cinco de seis. | Bolinhas acendendo uma a uma com carimbo; `DOCUMENTOS 5/6` |
| 06 | Dia nove. A certidão do FGTS. Venceu semana passada. E sem ela, não adianta o preço, não adianta o produto: a proposta nem é lida. | **Virada**: close no cartão da certidão com faixa `VENCIDA` em vermelho e X; alarme; o protagonista com susto; HUD `PRAZO 3 dias` em amarelo de aviso |
| 07 | Ô, pausa rapidinha. Deixa o like e segue a Licit pra ver se essa certidão sai antes do prazo. Bora continuar. | Tela em preto e branco, ícone de pause, 6 s |
| 08 | Renovar a certidão leva um dia quando está tudo em ordem. Estava. Seis de seis. Agora a proposta: os itens do edital, as condições, e o preço, que quem decide é você. | Bolinha 6 acende; cartão de interface da proposta: dados da empresa, itens e condições, "Preços: você preenche" |
| 09 | Dia onze. Quatrocentos e trinta e oito mil. Abaixo do valor estimado, acima do seu custo. Proposta enviada às nove e vinte da manhã. Sessão amanhã às dez. | `PROPOSTA R$ 438 mil`; `PRAZO 24 h`; tique; cartão de tarefa "Entregar a proposta. Carlos, até 10:00" |
| 10 | Dia doze. Nove e quarenta. A sessão abre em vinte minutos, a certidão está válida, a proposta está no sistema, e a empresa está dentro. Pela primeira vez. | Plano próximo do protagonista aliviado; `PRAZO 0h20`; relógio; pop de alívio |
| 11 | Do CNPJ à proposta enviada: um edital de oitenta páginas, seis documentos, uma certidão vencida e doze dias. Mas será que ganhou? Isso fica pra parte dois. | Plano geral do escritório com tudo que entrou; selo `PARTE 2 EM BREVE`; sting curto |
| 12 | E aí, a sua empresa já disputou uma licitação? Comenta aqui. E segue a Licit. | Endcard: logo, "Descubra oportunidades grátis pelo CNPJ: link na bio" |

**Validar com o especialista antes de gravar**: os seis documentos de habilitação usados como exemplo e se "certidão do FGTS" é a forma correta de nomear o CRF; a validade típica; se uma certidão vencida leva à inabilitação ou se há diligência ou prazo de regularização para ME e EPP; o que acontece com a proposta de quem não é habilitado (é "não lida" ou é julgada e depois inabilitada); se a sessão de pregão tem horário fixo e se a proposta precisa estar no sistema antes; o fluxo "ordem de fornecimento, trinta dias" como prazo de entrega; se a frase "abaixo do valor estimado" faz sentido como regra de proposta.

---

## 8. QA antes de entregar

1. `check --json` com `ok: true`, zero erros em lint, runtime, layout, contraste e áudio; nenhum `GSAP target ... not found` no runtime (foi o sintoma do contador errado).
2. Craft: nenhum `line_unread`; `dead_stretch` só na pausa e no endcard.
3. Snapshot nos momentos-chave e contato lido: câmera dentro do ambiente, personagem visível, nada cortado, nada escuro, cartão sem colidir com HUD e legenda.
4. Números: o que a narração fala é a conta do que a tela mostra; a parte seguinte da série usa os mesmos valores.
5. Áudio: `ebur128` por arquivo; nenhum SFX acima da voz; master -14,2 LUFS.
6. Logo legível no frame mais escuro.
7. Pronúncia do nome e dos termos técnicos conferida na transcrição do Scribe.
8. Conceitos validados pelo especialista, por escrito, antes do TTS.
9. Frames do MP4 final nos momentos corrigidos.
10. Legenda do post sem travessão, com o aviso de cenário ilustrativo e a frase de decisão da empresa.

---

## 9. Legenda do post e agendamento

### Legenda

Gancho em uma linha; dois ou três parágrafos curtos com o que acontece; a linha de cenário ilustrativo com a frase de decisão; a linha do produto com o CTA do site ("Descubra oportunidades grátis pelo CNPJ. Link na bio."); a pergunta de engajamento ("Comenta aqui."); bloco de hashtags (`#licitacoes #licitacao #pregaoeletronico #PNCP #vendaparaogoverno #comprasgovernamentais #gestaodelicitacoes #Licit`, ajustar com a equipe). Sem emoji por padrão até a marca definir um (a Porcin.IA usa 🐷 porque a marca é um porco; a Licit não tem equivalente).

### Agendamento (Metricool, regra da agência)

- Criar a marca Licit no Metricool e conectar **todos** os canais que a Licit tiver (Instagram, Facebook se houver página, LinkedIn, TikTok). Regra: todo post vai para todos os canais conectados, exceto YouTube horizontal. Instagram REEL, Facebook REEL (aceitou 170 s na Porcin.IA, apesar da documentação dizer 90 s), TikTok e LinkedIn com `networkData` padrão.
- Mídia por URL pública do Drive (`drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`, pasta "qualquer pessoa com o link: leitor"); o Metricool copia para o CDN dele na criação. Não depender de commit no repositório.
- Medir `getBestTimeToPostByNetwork` antes do primeiro agendamento; na Porcin.IA os melhores slots livres foram segunda e quinta às 10h. Duas peças por semana, séries alternadas, partes de uma série com 3 a 5 dias entre elas.
- Conferir `providers` no retorno de cada post e nunca deixar rascunho com data vencida.
- Depois de cada publicação, ler comentários: a peça "reação aos comentários" (formato do maxagroapp) é a mais barata de produzir e a que mais converte seguidor em comentário.

---

## 10. Pendências que travam o primeiro vídeo (decisões da equipe Licit)

1. Nome da editoria (proposta: "Por Dentro da Licitação").
2. Logo e símbolo oficiais em arquivo, com versão sobre fundo escuro.
3. Voz da narração (voice_id, modelo, settings) e a pronúncia de "Licit", validada com o Scribe.
4. Quem valida os roteiros (assessoria ou advogado), com prazo de resposta por roteiro.
5. Cor de erro e perda (o site não tem vermelho definido).
6. Marca no Metricool, canais conectados e pasta pública no Drive.
7. Hashtags e CTA padrão da legenda.
8. Se a Licit quer o personagem com rosto desde o primeiro vídeo (recomendado) ou o boneco sem rosto da Parte 3.
9. Os 8 a 10 reels do @desmontandoomundo no Drive para a medição de ritmo que falta (`PADRAO-DESMONTANDO.md`, seção "Para medir").
