# Setup do Profissio Licit Conteúdo Studio

Espelho do setup dos estúdios irmãos. No cloud, basta:

```bash
bash scripts/setup.sh
```

```bash
bash scripts/validate.sh
```

O `setup.sh` tem 6 passos (ffmpeg, video-use, hyperframes, Remotion, Python, estúdio) e **sai com código 0 mesmo se um passo avisar**, para a sessão nascer com uma ferramenta faltando em vez de não nascer. Por isso, ler a saída. O `validate.sh` testa comportamento, não presença de arquivo: roda filtros reais no ffmpeg, confere a detecção de orientação com três vídeos sintéticos e renderiza 1 frame de verdade no Remotion.

## Environment (Claude Code cloud)

Configura-se no seletor de nuvem acima da caixa de mensagem em claude.ai/code. Environment deste estúdio: **`licit-conteudo`**.

| Item | Estado em 09/nov/2026 | O que fazer |
|---|---|---|
| Rede | Sem restrição | Nada. Se trocar para Custom, liberar os hosts listados no `CLAUDE.md` |
| Setup script | Gravado em 09/nov/2026 (versão à prova de diretório abaixo) | Conferir `ls /workspace` na primeira sessão nova: ainda não foi provado em boot real |
| Variáveis | Nenhuma | Cadastrar as chaves abaixo |

Setup script (nunca `bash scripts/setup.sh`, que é caminho relativo e falha no boot):

```bash
for p in ./scripts/setup.sh ./*/scripts/setup.sh; do [ -f "$p" ] && exec bash "$p"; done; p=$(find /home /workspace /repo /app /src -maxdepth 4 -type f -path "*/scripts/setup.sh" 2>/dev/null | head -1); [ -n "$p" ] && exec bash "$p"; echo "setup.sh nao encontrado no repo"; exit 0
```

Variáveis de ambiente (cadastrar no environment; nunca no repo, nunca no chat; **valem para sessões novas**):

| Variável | Para quê |
|---|---|
| `ELEVENLABS_API_KEY` | Transcrição (Scribe), locução, SFX e trilha |
| `OPENAI_API_KEY` | Geração de imagem |
| `GEMINI_API_KEY` | Geração de imagem e o skill `/watch` |
| `META_ACCESS_TOKEN` | Opcional: análise de Instagram pela Graph API |

## Conectores (cada um exige ação do usuário)

- **Metricool**: conectado pela conta `suporte@profissio.ai`, mas **sem marca da Profissio Licit**. Criar a marca no painel, conectar as redes e registrar o blog_id no `CLAUDE.md`.
- **Google Drive**: conector oficial + pastas de brutos e de marca com "qualquer pessoa com o link: leitor". Pastas **PENDENTES**.
- **Kairogen** (B-roll por IA): conferir plano e créditos com `get_me_context`.

## Validação final

1. `bash scripts/validate.sh` verde nos itens 1, 2, 4, 5 e 6. O item 3 fica PENDENTE até a `ELEVENLABS_API_KEY` existir.
2. `python3 scripts/gera_imagem.py --listar` responde nas duas chaves.
3. Metricool: `getBrandSettings` lista a marca da Profissio Licit.
4. Memória persistente: `CLAUDE.md` deste repo.

## Pendências de marca (bloqueiam produção de texto público)

Ver "PENDENTES de marca" no `CLAUDE.md` e as seções PENDENTE do `FRAMEWORK.md`.
