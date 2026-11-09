#!/usr/bin/env python3
"""Lê contas e hashtags públicas do Instagram pela Graph API da Meta.

Serve para analisar perfil de terceiro (Business ou Criador) sem login:
seguidores, e de cada post a legenda, curtidas, comentários, data e link.

O token vem SÓ da variável de ambiente META_ACCESS_TOKEN. Passar token por
argumento é recusado de propósito: argumento vaza no histórico do shell e na
lista de processos.

Uso:
    export META_ACCESS_TOKEN=...            # cadastrado no environment
    python3 scripts/instagram_analisa.py --contas
    python3 scripts/instagram_analisa.py --perfil nome_do_perfil --posts 25
    python3 scripts/instagram_analisa.py --hashtag licitacao --top
    python3 scripts/instagram_analisa.py --perfil alguem --json > saida.json

Precisa de `graph.facebook.com` na allowlist do environment.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request

API = 'https://graph.facebook.com/v21.0'

CAMPOS_MIDIA = 'caption,like_count,comments_count,timestamp,permalink,media_type,media_product_type'

DICAS = {
    190: 'token inválido ou expirado; gere outro em developers.facebook.com',
    200: 'faltam permissões no token (instagram_basic, pages_show_list, '
         'pages_read_engagement, instagram_manage_insights)',
    100: 'a conta alvo pode não ser Business/Criador, ou não existe. '
         'A Graph API não enxerga perfil pessoal',
    4: 'limite de requisições da Meta atingido; espere e tente de novo',
    2500: 'o token não identifica um usuário; confira se é token de usuário '
          'ou de página com as permissões certas',
}


def token() -> str:
    for proibido in sys.argv[1:]:
        if proibido.startswith('EAA') or '--token' in proibido:
            sys.exit('Recusado: nao passe token por argumento. Use META_ACCESS_TOKEN.')
    t = os.environ.get('META_ACCESS_TOKEN', '').strip()
    if not t:
        sys.exit('META_ACCESS_TOKEN ausente no ambiente. Cadastre no environment '
                 '(variavel nova so aparece em sessao nova).')
    return t


def chamar(caminho: str, params: dict) -> dict:
    tok = token()
    params = {**params, 'access_token': tok}
    url = f'{API}/{caminho.lstrip("/")}?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        bruto = e.read().decode('utf-8', 'replace').replace(tok, '[redacted]')
        try:
            err = json.loads(bruto)['error']
            cod = err.get('code')
            dica = DICAS.get(cod, '')
            sys.exit(f'Meta API {e.code} (code {cod}): {err.get("message")}'
                     + (f'\n  -> {dica}' if dica else ''))
        except (ValueError, KeyError):
            sys.exit(f'Meta API {e.code}: {bruto[:400]}')
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        sys.exit(f'Nao alcancou graph.facebook.com ({type(e).__name__}: {e}). '
                 'Confira se o host esta na allowlist do environment.')


def minhas_contas() -> list[dict]:
    """Contas Instagram Business que o token enxerga, via paginas do Facebook."""
    d = chamar('me/accounts', {'fields': 'id,name,instagram_business_account{id,username}'})
    saida = []
    for p in d.get('data', []):
        iba = p.get('instagram_business_account')
        if iba:
            saida.append({'pagina': p.get('name'), 'pagina_id': p.get('id'),
                          'ig_id': iba.get('id'), 'ig_username': iba.get('username')})
    return saida


def ig_user_id(preferido: str | None = None) -> str:
    """A Business Discovery exige um IG user id proprio como ponto de partida."""
    if os.environ.get('IG_USER_ID'):
        return os.environ['IG_USER_ID'].strip()
    contas = minhas_contas()
    if not contas:
        sys.exit('O token nao enxerga nenhuma conta Instagram Business. '
                 'Vincule a conta a uma pagina do Facebook e conceda as permissoes.')
    if preferido:
        for c in contas:
            if c['ig_username'] == preferido.lstrip('@'):
                return c['ig_id']
    return contas[0]['ig_id']


def perfil(alvo: str, limite: int) -> dict:
    alvo = alvo.lstrip('@')
    campos = (f'business_discovery.username({alvo})'
              f'{{followers_count,media_count,username,'
              f'media.limit({limite}){{{CAMPOS_MIDIA}}}}}')
    d = chamar(ig_user_id(), {'fields': campos})
    return d.get('business_discovery', {})


def hashtag(nome: str, top: bool, limite: int) -> list[dict]:
    uid = ig_user_id()
    nome = nome.lstrip('#')
    busca = chamar('ig_hashtag_search', {'user_id': uid, 'q': nome})
    dados = busca.get('data') or []
    if not dados:
        sys.exit(f'Hashtag #{nome} nao encontrada.')
    hid = dados[0]['id']
    borda = 'top_media' if top else 'recent_media'
    d = chamar(f'{hid}/{borda}', {'user_id': uid, 'fields': CAMPOS_MIDIA,
                                  'limit': limite})
    return d.get('data', [])


def mostra_posts(posts: list[dict]) -> None:
    for m in posts:
        data = (m.get('timestamp') or '')[:10]
        tipo = m.get('media_product_type') or m.get('media_type') or '?'
        print(f'\n{data}  {tipo}  {m.get("like_count", "?")} curtidas, '
              f'{m.get("comments_count", "?")} comentarios')
        print(f'  {m.get("permalink", "")}')
        leg = (m.get('caption') or '').strip()
        if leg:
            for ln in textwrap.wrap(leg, 92)[:8]:
                print(f'  | {ln}')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--contas', action='store_true',
                   help='lista as contas Instagram que o token enxerga')
    g.add_argument('--perfil', metavar='@CONTA',
                   help='analisa uma conta Business/Criador publica')
    g.add_argument('--hashtag', metavar='TAG', help='posts de uma hashtag')
    ap.add_argument('--posts', type=int, default=25, help='quantos posts (padrao 25)')
    ap.add_argument('--top', action='store_true',
                    help='com --hashtag: posts de maior alcance em vez dos recentes')
    ap.add_argument('--json', action='store_true', help='saida crua em JSON')
    a = ap.parse_args()

    if a.contas:
        c = minhas_contas()
        print(json.dumps(c, ensure_ascii=False, indent=1) if a.json else
              '\n'.join(f'{x["ig_username"]:24s} ig_id={x["ig_id"]}  pagina={x["pagina"]}'
                        for x in c) or '(nenhuma)')
        return

    if a.perfil:
        p = perfil(a.perfil, a.posts)
        if a.json:
            print(json.dumps(p, ensure_ascii=False, indent=1)); return
        print(f'@{p.get("username")}  {p.get("followers_count"):,} seguidores, '
              f'{p.get("media_count"):,} posts'.replace(',', '.'))
        mostra_posts((p.get('media') or {}).get('data', []))
        return

    posts = hashtag(a.hashtag, a.top, a.posts)
    if a.json:
        print(json.dumps(posts, ensure_ascii=False, indent=1)); return
    print(f'#{a.hashtag.lstrip("#")}  {len(posts)} posts '
          f'({"maior alcance" if a.top else "recentes"})')
    mostra_posts(posts)


if __name__ == '__main__':
    main()
