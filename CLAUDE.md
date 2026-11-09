# Profissio Licit Conteúdo Studio (memória persistente do projeto)

Este repositório é o **Profissio Licit Conteúdo Studio**: criação, edição e agendamento de conteúdo para as redes da **Profissio Licit**. Estúdio irmão do `profissioai-conteudo` e do `profecia-conteudo` (e do restante da frota: `eita-conteudo`, `ana-conteudo`, `normalyze.conteudo`); infraestrutura idêntica, posicionamento próprio da Profissio Licit.

**Antes de editar qualquer vídeo ou escrever qualquer caption, leia `FRAMEWORK.md`.**

> **O que se sabe da Profissio Licit até aqui** (09/nov/2026): só o nome, dado pelo usuário ao pedir este estúdio, e que é uma marca do ecossistema Profissio. **Nenhuma fonte primária foi lida**: não há site, material de marca, pauta nem conta de rede social apontados ainda, e os repositórios dos estúdios irmãos não citam o produto. Tudo que não está confirmado abaixo é **PENDENTE**: perguntar ou ler na fonte, nunca inventar, e **nunca herdar posicionamento, persona, paleta, CTA ou voz da Profissio.ai, do Profecia ou de outro estúdio** sem confirmação. O nome sugere licitações, mas isso é leitura do nome e não fato: confirmar antes de usar em texto público.

## PENDENTES de marca (bloqueiam produção de texto público)

- **O que é a Profissio Licit**: produto, proposta, público, dores e soluções. Pedir à equipe o site e a base de conhecimento, e ler na fonte.
- **Nome e gênero em texto**: o usuário escreveu "da Profissio Licit" (feminino). Confirmar a grafia oficial (Profissio Licit, Profissio.ai Licit, Licit) e a relação declarada com a Profissio.ai.
- **Identidade visual**: paleta, fontes, logo, fundos. `remotion/src/marca.ts` está com um **provisório neutro em cinza**, de propósito sem cara de marca. Não usar a aurora rosa da Profissio.ai nem o céu dourado do Profecia.
- **Persona e voz do perfil**: quem fala, tom, público, CTAs oficiais.
- **Pilares de conteúdo**: derivar das fontes primárias quando existirem (método no `FRAMEWORK.md`).
- **Pronúncia da marca em TTS**: confirmar com o usuário antes da primeira locução. Regra aprendida no grupo: a Profissio.ai se fala "profício ei ái", e isso só se descobriu perguntando. Como se diz "Licit" (lícit, licít, em inglês)?
- **Voz ElevenLabs**: voice_id, modelo e parâmetros próprios. Não reaproveitar voz de outro estúdio sem confirmação.
- **Redes e Metricool**: a marca **não existe** no Metricool (ver "IDs e contas"). Conectar no painel e registrar aqui o blog_id e os perfis.
- **Ativos de marca e brutos**: pastas no Drive (logo, fontes, fundos, gravações), se existirem.
- **Design system**: não existe. Quando houver identidade, criar e espelhar em `design-system/` (ver `design-system/README.md`).
- **Licença do Remotion**: confirmar o enquadramento da empresa antes de usar em produção (ver gotchas).

## Regras que valem em qualquer resposta pública (herdadas do grupo, confirmadas pelo usuário nos estúdios irmãos)

- Nunca usar travessão em texto público (caption, lettering, legenda): reescrever a frase.
- Palavrão em vídeo **bipa**, não corta.
- Loudness final: **-14 LUFS**.
- **Metricool é só para agendar conteúdo.** Não usar como fonte de análise, leitura de feed, métrica ou concorrente. Análise de Instagram é pela Graph API (`scripts/instagram_analisa.py`).

## Working dirs

- Estúdio: este repo (symlink `~/licit-conteudo` aponta para cá). Projetos em `projects/<nome>/`.
- Ferramentas: `video-use` e `hyperframes` clonados em `/workspace/browser-use/` e `/workspace/heygen-com/` (Linux/cloud) ou `~/video-editor/` (Mac). Skills registradas em `~/.claude/skills/`.
- **Remotion**: composições versionadas em `remotion/` (React/TS); `node_modules` fora do git, instalado pelo `setup.sh`. `npm run studio` abre o editor, `npx remotion render src/index.ts <Composicao> saida.mp4` renderiza. Prontos: `Fundo` (fundo padrão) e `CartaoTitulo`, com `marca.ts` guardando os tokens.
- Ambiente novo (container limpo): `bash scripts/setup.sh` e depois `bash scripts/validate.sh`. **Em sessão nova, conferir `ls /workspace` antes de contar com video-use ou hyperframes**; se estiver vazio, rodar o `setup.sh` à mão.
- **Campo de setup script do environment: nunca caminho relativo.** O comando de boot roda com o diretório de trabalho no **pai** do repo, então `bash scripts/setup.sh` falha com `No such file or directory` (exit 127) e a sessão nasce sem `/workspace` e sem skills. Versão à prova de diretório, a mesma dos estúdios irmãos (aqui terminando em `exit 0`, para um repo sem `setup.sh` não impedir a sessão de nascer):
  ```bash
  for p in ./scripts/setup.sh ./*/scripts/setup.sh; do [ -f "$p" ] && exec bash "$p"; done; p=$(find /home /workspace /repo /app /src -maxdepth 4 -type f -path "*/scripts/setup.sh" 2>/dev/null | head -1); [ -n "$p" ] && exec bash "$p"; echo "setup.sh nao encontrado no repo"; exit 0
  ```

## Cinto de ferramentas (portado dos estúdios irmãos em 09/nov/2026)

Ferramenta é genérica, marca não é. Os scripts vieram do `profecia-conteudo` (a versão mais nova do cinto, que por sua vez nasceu do `profissioai-conteudo`) com zero referências de marca, conferido por varredura. Só `setup.sh`, `validate.sh`, `remotion/src/marca.ts`, `remotion/src/Root.tsx` e `remotion/package.json` carregam nome de estúdio. O guia de porte é o `PORTAR.md` do `profissioai-conteudo`.

| Arquivo | O que faz |
|---|---|
| `scripts/decupar.py` | Decupa vídeo por **âncoras de texto** ("de tal frase até tal frase", `edl.json`) casadas contra transcrição com timestamp por palavra. Junta trechos, gira, aplica LUT, normaliza áudio |
| `scripts/relatorio_decupagem.py` | Retranscreve as peças finais e monta o relatório do que ficou e do que caiu |
| `scripts/gera_lut_slog2.py` | Gera LUT 3D de S-Log2/S-Gamut para Rec.709 com a `colour-science` |
| `scripts/zip_index_remoto.py` | Lista e extrai arquivos de um ZIP gigante no Drive por *range request*, sem baixar o ZIP |
| `scripts/gera_imagem.py` | Gera imagem pela OpenAI ou pelo Gemini, mesma interface; aceita anexos de referência (`--ref`, só OpenAI). Chaves **só** por variável de ambiente (recusa chave por argumento) |
| `scripts/sobe_para_drive.py` | Sobe arquivos para uma pasta do Drive com token de acesso |
| `scripts/instagram_analisa.py` | Lê conta Business/Criador ou hashtag do Instagram pela Graph API da Meta (`business_discovery`). Token **só** por `META_ACCESS_TOKEN` |
| `remotion/` | Composições React (`CartaoTituloVertical`, `CartaoTituloQuadrado`). Tokens em `src/marca.ts`, fundo em `src/Fundo.tsx`, texto de exemplo em `src/Root.tsx` |
| `.claude/skills/watch/` | Skill `/watch`: o agente assiste um vídeo inteiro, com som (ver seção abaixo) |
| `assets/sfx/` | Biblioteca de sons de UI do grupo (15 arquivos, brand-neutral, custo zero). Trilha musical é própria por peça |

**Não portado, de propósito**: `instagram_navega.py` (o próprio cabeçalho declara que não funciona no ambiente e depende de cookie de sessão), `patches/` (o patch do video-use foi aposentado em 18/set/2026), `projects/`, `design-system/` e `assets/` de marca dos irmãos.

**Diferença em relação aos irmãos**: o caminho do `headless_shell` do Remotion é **resolvido em tempo de execução**, não fixado. Os irmãos fixam `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`; a imagem do container de 09/nov/2026 mudou o número **e o layout** (`chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`), e o caminho fixo aponta para um arquivo que não existe mais. Aqui `remotion/remotion.config.ts` e `scripts/validate.sh` pegam a maior versão instalada, nos dois layouts. Validado no mesmo dia: `validate.sh` verde no item 5 e frame 1080x1920 renderizado. **Vale levar essa correção para os irmãos**, que devem estar com o render do Remotion quebrado em container novo.

## Skill `/watch`: dar vídeo de entrada ao agente

Vive em `.claude/skills/watch/`, copiado sem edição do `bradautomates/claude-video` v0.3.2 (MIT), pela cópia já revisada do `profecia-conteudo`. Procedência, revisão de segurança e como atualizar: `.claude/skills/watch/PROCEDENCIA.md` (os testes de ambiente citados lá foram feitos no environment do Profecia).

- **Para que serve**: conferir peça renderizada antes de agendar. Um frame extraído com ffmpeg não pega erro de digitação no meio do card, corte torto nem áudio ausente; o `/watch` assiste o vídeo inteiro com som.
- **Motor padrão: gemini**, fixado em `~/.config/watch/.env` pelo `setup.sh`. Precisa da `GEMINI_API_KEY` no environment (**PENDENTE**).
- **O motor gemini manda o vídeo para o Google.** Bruto de cliente e peça não publicada só sobem com o usuário autorizando na hora. Material sensível: `--engine local`.
- **Decupagem continua no `decupar.py`** com o Scribe da ElevenLabs, que dá timestamp por palavra.
- `.claude/settings.json` libera `setup.py` e `watch.py` de prompt de permissão.

## IDs e contas (verificado em 09/nov/2026)

- **Metricool**: conta `suporte@profissio.ai`. O `getBrandSettings` devolve **só duas marcas**: "Profissio.ai" (blog_id 6736175) e "Profec.ia" (blog_id 7027080). **Não há marca da Profissio Licit: PENDENTE criar/conectar no painel** e registrar aqui o blog_id, o timezone e os perfis. **Nunca agendar peça do Licit nos blog_ids acima.**
- **Chaves de API: nenhuma cadastrada.** O environment `licit-conteudo` nasceu sem variáveis (`printenv | grep -c API_KEY` devolve 0). Cadastrar **nas variáveis do environment**, nunca em arquivo do repo e nunca no chat:
  - `ELEVENLABS_API_KEY` (`sk_...`, 51 caracteres): TTS, STT (Scribe), `sound-generation` e Eleven Music (`POST /v1/music`, até 600s, para trilhas; `sound-generation` fica para SFX).
  - `OPENAI_API_KEY` e `GEMINI_API_KEY`: geração de imagem (`scripts/gera_imagem.py`); a do Gemini também move o `/watch`.
  - `META_ACCESS_TOKEN` (opcional): Graph API da Meta para o `instagram_analisa.py`. Expira; `code 190` quer dizer renovar.
  - Variável nova só aparece em **sessão nova**. Chave válida não significa quota: no Gemini, `429` com `quotaId: ...-FreeTier` quer dizer que o projeto da chave não está no faturamento (ler o campo `details` do erro).
- **Kairogen** (B-roll por IA): nos irmãos a conta `suporte@profissio.ai` está no plano FREE com 0 créditos. Conferir com `get_me_context` antes de planejar B-roll.
- **Google Drive**: pasta de brutos e pasta de marca da Profissio Licit **PENDENTES**.

## Rede do environment (verificado em 09/nov/2026)

Environment **`licit-conteudo`**, network **sem restrição** (diferente dos irmãos, que usam Custom com allowlist). Sem variáveis e, na criação do estúdio, sem setup script. Consequências:

- O `apt` pode funcionar aqui; o `setup.sh` tenta o apt e cai para o ffmpeg estático do GitHub Releases se precisar.
- Os gotchas de allowlist abaixo **só passam a valer se a rede for trocada para Custom**. Ficam registrados porque é o padrão do grupo. Hosts que o cinto exige nesse caso (a allowlist é literal por subdomínio; `*.dominio.com` para site inteiro): `api.elevenlabs.io`, `api.openai.com`, `generativelanguage.googleapis.com`, `www.googleapis.com`, `drive.google.com`, `drive.usercontent.google.com`, `graph.facebook.com`, `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`, `api.github.com` + GitHub Releases.
- Diagnóstico de host em um comando: `curl -sv https://host/ 2>&1 | grep CONNECT`. `403` no CONNECT é allowlist; qualquer outra resposta é chave, quota ou rota.

## Gotchas essenciais (herdados e validados nos estúdios irmãos)

Referência técnica completa do grupo: `CLAUDE.md` do `suportezv/profissioai-conteudo` (seções "Rede do environment" e "Gotchas essenciais") e do `suportezv/profecia-conteudo`. O que mais custa tempo:

**Ambiente**
- Network Custom: `pypi`/`npm` vêm em `no_proxy` e falham com 403 mesmo na allowlist; rotear pelo agent proxy (o `setup.sh` já faz quando existe `HTTPS_PROXY`). WebFetch tem rota de egresso própria: usar `curl` do container. Chromium não contorna allowlist.
- **Allowlist pega na hora; variável de ambiente, não.** Host liberado passa a responder na mesma sessão; variável nova só em sessão nova.
- **A URL do ffmpeg estático difere por uma palavra.** `releases/download/latest/…` (tag rolante do BtbN) serve o arquivo; `releases/latest/download/…` devolve 404. O `setup.sh` tenta as duas e confere a assinatura XZ antes de extrair.
- **Processo em background com `nohup`/`setsid` é recolhido quando a tool call retorna.** Usar `run_in_background: true` da ferramenta Bash. Em lote longo, `flock` evita dois loops escrevendo o mesmo arquivo.
- **Skills do hyperframes sem rede**: se `npx hyperframes skills update` falhar, o `setup.sh` registra as skills a partir do clone local.

**Vídeo filmado**
- Brutos de iPhone são HLG 10-bit: gerar proxy SDR antes de editar (`colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`).
- **Brutos de Sony em S-Log2: converter, não "filtrar".** O XML lateral do clipe declara `CaptureGammaEquation`/`CaptureColorPrimaries`; quando diz `s-log2`/`s-gamut`, gerar a LUT com `scripts/gera_lut_slog2.py` (exposição −0,5 stop e joelho em 0,65, senão o branco estoura) e conferir que o ffmpeg aplica a `lut3d` em RGB (`-v verbose`). Saída com `out_range=tv` e `-color_range tv`.
- **Câmera pode gravar na vertical sem gravar a flag de rotação.** Checar um frame de qualquer lote novo; corrigir com `transpose=1` antes de escalar.
- **Decupagem por âncora de texto, não por timecode** (`scripts/decupar.py` + `edl.json`). O campo `apos` empurra o cursor quando a mesma frase aparece antes.
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG; zoom animado com `zoompan`, não `crop`.
- **Ler o índice de um ZIP gigante no Drive sem baixar**: `scripts/zip_index_remoto.py`. Download direto de arquivo público: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`. Pasta compartilhada por link não lista pelo conector: `curl` na página pública e parsear `window['_DRIVE_ivd']`.

**Motion**
- **Remotion renderiza com o `headless_shell`, não com o Chromium do Playwright** ("Old Headless mode has been removed"). Aqui o caminho é achado em tempo de execução (ver "Cinto de ferramentas").
- **Licença do Remotion não é MIT**: grátis para indivíduo e empresa de até 3 funcionários; acima disso, Company License. Confirmar antes de produção.
- **Sem rede de fontes no render** quando a rede é Custom: fonte de marca entra como asset local ou por pacote `@fontsource/*` do npm.
- Remotion e HyperFrames resolvem o mesmo problema; a regra de escolha está no `FRAMEWORK.md`.

**Áudio e locução**
- **TTS: validar pronúncia por STT antes de mixar.** "mas" e "mais" se confundem em português e invertem o sentido; evitar as duas perto uma da outra. Frases curtas de fecho com `previous_text`.
- **Ritmo de locução é medido, não estimado**: nos irmãos o medido ficou entre 1,9 e 2,3 palavras por segundo conforme a voz. Medir a voz do Licit antes de fechar duração de roteiro.
- Testar escopo de chave da ElevenLabs sem gastar crédito: chamar o endpoint com parâmetro inválido. `401 missing_permissions` = escopo ausente; `400`/`404` = presente.

**Metricool e redes**
- MCP sem delete (cancelar = update `draft:true`); **update devolve id novo**. O servidor MCP cai no meio de lote: recarregar a tool pelo ToolSearch e seguir.
- **Rascunho com data vencida não publica e não avisa.** Quem agenda tira do rascunho na mesma sessão e confirma com `getScheduledPosts`.
- **Mídia por URL**: o Metricool aceita vídeo do Drive por URL direta (`https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download`) e re-hospeda no CDN dele. É a rota preferida aqui, porque **este repo é privado** e o truque do commit temporário servido por `raw.githubusercontent.com` só funciona em repo público.
- **TikTok exige `tiktokData.title`.** Um post pode ir para Instagram, Facebook e TikTok de uma vez com `providers` + `instagramData {type: REEL, showReelOnFeed: true}` + `facebookData {type: REEL}` + `tiktokData {title}`.
- **Instagram pela web não dá nada sem login**, mesmo com a rede liberada. Análise de feed: Graph API (`instagram_analisa.py`), exportação oficial da conta ou prints do usuário. Nunca pedir senha nem cookie de sessão.

## Histórico de decisões

- **09/nov/2026**: estúdio criado a pedido do usuário, "com as mesmas especificações" do `profissioai-conteudo` e do `profecia-conteudo`. Infra, cinto de ferramentas, biblioteca de SFX, skill `/watch` e gotchas herdados; **marca 100% PENDENTE**, sem herdar nada dos irmãos, como manda o `PORTAR.md`. Base do porte: a branch de trabalho do Profecia (a mais nova do grupo), não a `main` dele, que está parada em 18/set. Remotion entra com tokens neutros provisórios e nomes de token sem cor de marca (`acento`, `mancha1..4`, `fundo`, `tinta`). Caminho do `headless_shell` passou a ser resolvido em tempo de execução. `setup.sh` rodou os 6 passos com código 0 e o `validate.sh` ficou verde em tudo, menos na chave da ElevenLabs, que ainda não existe. Conferido no mesmo dia: Metricool sem marca do Licit, environment sem chaves e sem setup script.
