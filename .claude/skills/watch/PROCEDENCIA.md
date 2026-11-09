# Procedência deste skill

Não é código deste estúdio. Copiado sem edição de:

- Repo: https://github.com/bradautomates/claude-video
- Skill: `skills/watch/`
- Versão: **0.3.2**, commit `03ceb42` (tag `v0.3.2`)
- Licença: MIT, Copyright (c) 2026 Bradley Bonanno (ver `LICENSE`)
- Copiado em: 02/out/2026

Mudanças feitas na cópia: nenhuma no código. Acrescentados só `LICENSE` e este arquivo.

## Para atualizar

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/bradautomates/claude-video /tmp/cv
rm -rf .claude/skills/watch && cp -r /tmp/cv/skills/watch .claude/skills/watch
cp /tmp/cv/LICENSE .claude/skills/watch/LICENSE
find .claude/skills/watch -name __pycache__ -type d -exec rm -rf {} +
# recriar este arquivo com a versão e o commit novos
```

## Por que vive aqui e não em `/plugin install`

O container da sessão é efêmero: plugin instalado em `~/.claude` morre quando a
sessão é reciclada. Dentro de `.claude/skills/` do repo, o skill nasce com toda
sessão nova, como os outros.

## O que roda neste ambiente

- **Motor gemini: funciona.** `generativelanguage.googleapis.com` está na
  allowlist e a `GEMINI_API_KEY` vem do environment. Preflight em 02/out/2026:
  `status: ready`, `engine: gemini`, `can_proceed: true`.
- **URL do YouTube: funciona no motor gemini**, que manda a URL para o Google
  em vez de baixar. Sem precisar de `yt-dlp`.
- **Motor local: parcial.** `ffmpeg`/`ffprobe` existem, `yt-dlp` não (só é
  preciso para baixar URL; arquivo local dispensa). Transcrição por
  `--whisper openai` funciona (`api.openai.com` está na allowlist); `groq` não
  (`api.groq.com` fora da allowlist) e o WhisperX local não instala
  (`astral.sh` e `download.pytorch.org` fora da allowlist).
- O autor documenta que ambiente de nuvem não é suportado, pelos motivos de que
  a chave do Gemini não persiste e o yt-dlp é bloqueado. Nenhum dos dois vale
  aqui: a chave está no environment e o caminho que usamos não baixa nada.

## Privacidade

O motor gemini **envia o vídeo para o Google**. Bruto de cliente e peça não
publicada não sobem sem o usuário autorizar na hora. Para material sensível,
usar `--engine local`, que não manda nada para fora.

## Revisão de segurança (02/out/2026, 2.789 linhas, 9 arquivos)

Leitura de primeira mão antes de commitar, porque isto roda em toda sessão deste
repo com acesso às chaves do environment.

**Nada de ofuscação ou execução dinâmica**: zero `eval`, `exec`, `compile`,
`__import__`, `pickle`, `marshal`, `base64`.

**Nenhum shell**: zero `shell=True`, `os.system`, `os.popen`. Todo processo
externo sai por `subprocess.run`/`Popen` com lista de argumentos
(`runtime.py:run_text`), então URL do usuário não vira injeção de comando.

**Três hosts, todos literais no código**, nenhum montado em tempo de execução:
`generativelanguage.googleapis.com` (gemini.py), `api.groq.com` e
`api.openai.com` (whisper.py).

**Chaves**: lidas de variável de ambiente, depois `~/.config/watch/.env`, depois
`.env` do diretório atual. Viajam só em cabeçalho de autenticação
(`x-goog-api-key`, `Authorization`). O `gemini.py:_fail` troca a chave por
`[redacted]` em toda mensagem de erro. Nenhum `print` de chave em nenhum arquivo.

**Escrita de config** (`config.py:write_settings`): atômica, por
`mkstemp` + `os.replace`; valida o nome da chave por regex, recusa `\r\n` no
valor e preserva as linhas que não está mudando.

**Apagar arquivo**: só dentro do que ele mesmo criou. Os `work dir` são
`tempfile.mkdtemp`; o `rmtree` do `watch.py:64` cai nesse diretório. Os `unlink`
do `frames.py` apagam frames que ele gerou. O `rmtree` do `setup.py:287` só
toca `~/.cache/watch/whisperx-venv`, com guarda contra symlink.
**O vídeo de origem nunca é modificado nem apagado.**

**Upload para o Google** (`gemini.py:upload_file`): streaming por blocos, nunca
inteiro em memória; o arquivo remoto é apagado em bloco `finally`, e se a
exclusão falhar o relatório avisa que expira em 48h.

**Cookies do navegador**: estritamente opcional. Sem `--cookies` ou
`--cookies-from-browser` ele passa `--no-cookies`/`--no-cookies-from-browser`
explícitos ao yt-dlp. Não há default que leia o navegador.

**Nenhuma leitura** de `~/.ssh`, `~/.aws`, `.netrc`, keychain ou `.git/config`.

**O único caminho que baixa script remoto** é o instalador do WhisperX
(`setup.py:_ensure_uv`, `install_whisperx`): pega o `uv` em `astral.sh` e o
PyTorch em `download.pytorch.org`, com versões fixadas, e baixa o script antes
de rodar em vez de canalizar `curl | sh`. **Inalcançável aqui**: os dois hosts
estão fora da allowlist e o `setup.sh` fixa `WATCH_WHISPER_BACKEND=none`. Só é
atingido por `--install-whisperx` ou `--backend whisperx`.

Conclusão: código cuidadoso, sem comportamento oculto. O risco que resta não é
de código, é de produto: **o motor gemini envia o vídeo para o Google**, por
desenho e documentado em letra clara pelo próprio autor.
