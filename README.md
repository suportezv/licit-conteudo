# Profissio Licit Conteúdo Studio

Estúdio de criação, edição e agendamento de conteúdo para as redes da **Profissio Licit**. Mesma infraestrutura dos estúdios irmãos ([`profissioai-conteudo`](https://github.com/suportezv/profissioai-conteudo), repositório de referência técnica do grupo, e [`profecia-conteudo`](https://github.com/suportezv/profecia-conteudo)); posicionamento próprio: **IA para licitação de Obras**.

- **`FRAMEWORK.md`**: persona, regras, pilares, assinaturas e fluxo por peça.
- **`CLAUDE.md`**: memória persistente (IDs, contas, gotchas, PENDENTES de marca).
- **`SETUP.md`**: environment, chaves, conectores e validação.
- **`projects/`**: um subdiretório por peça (briefing, roteiro, scripts de edição, caption).
- **`scripts/`**: setup, validação e o cinto de ferramentas do grupo (decupagem por âncora de texto, LUT S-Log2, ZIP remoto do Drive, geração de imagem, upload para o Drive, análise de Instagram pela Graph API).
- **`remotion/`**: composições React; paleta só em `src/marca.ts`.
- **`assets/sfx/`**: biblioteca de sons do grupo. **`assets/marca/`** e **`assets/fonts/`**: logos, fundos, favicon e a Sora, vindos do Drive da marca.
- **`design-system/`**: espelho do Design System da marca ([artifact](https://claude.ai/artifact/1Cew4xmRADNpZi6aRve4MU)) e os documentos de origem.
- **`.claude/skills/watch/`**: skill `/watch`, para o agente assistir um vídeo inteiro com som.

## Primeiro uso (cloud)

```bash
bash scripts/setup.sh
```

```bash
bash scripts/validate.sh
```

Depois: aponte as fontes da marca (site, material, pastas do Drive), escreva o briefing em `projects/<nome>/` e peça a peça.

## Estado

Infraestrutura pronta. Marca registrada a partir do Drive de identidade (edição 1.1), com Design System publicado e Remotion na identidade real. Em aberto: CTA e destino, voz e pronúncia de locução, pilares a validar. Lista em "PENDENTES" no `CLAUDE.md`.

> Este repositório é **privado**. A mídia para o Metricool vai por URL direta do Drive, não por `raw.githubusercontent.com`. Nunca commitar chaves.
