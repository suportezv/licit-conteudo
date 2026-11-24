const { chromium } = require('playwright'); const fs=require('fs');
const D = JSON.parse(process.argv[2]);
const html = d => `<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box} body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#c9ccd1;color:#1b1f24}
.win{width:800px;height:600px;display:flex;flex-direction:column;background:#fff}
.tb{height:30px;background:linear-gradient(#2a5caa,#1c468c);color:#fff;font-size:13px;display:flex;align-items:center;padding:0 10px;justify-content:space-between}
.tb b{font-weight:600}.tb span{letter-spacing:6px;font-size:12px}
.nav{height:38px;background:#e9ebee;border-bottom:1px solid #b9bdc4;display:flex;align-items:center;gap:8px;padding:0 10px;font-size:13px;color:#555}
.url{flex:1;background:#fff;border:1px solid #aeb3bb;border-radius:3px;height:24px;line-height:22px;padding:0 8px;color:#222;font-size:13px}
.hd{background:#0c326f;color:#fff;padding:12px 22px;display:flex;justify-content:space-between;align-items:center}
.hd .t{font-size:19px;font-weight:700}.hd .s{font-size:12px;opacity:.85}
.bc{font-size:12px;color:#1351b4;padding:9px 22px;border-bottom:1px solid #e3e5e8}
.ct{padding:14px 22px;flex:1}
h1{font-size:21px;margin:0 0 3px} .sub{font-size:13px;color:#555;margin-bottom:12px}
.st{display:inline-block;background:#e3f5e1;color:#168821;border:1px solid #168821;font-size:12px;font-weight:700;padding:3px 9px;border-radius:3px;margin-left:8px;vertical-align:middle}
table{width:100%;border-collapse:collapse;font-size:14px} td{padding:8px 10px;border-bottom:1px solid #e3e5e8;vertical-align:top}
td:first-child{width:250px;color:#555;background:#f8f8f8;font-weight:700;font-size:13px}
.v{font-size:22px;font-weight:700;color:#0c326f}
.it{margin-top:12px;font-size:13px} .it th{text-align:left;background:#f0f0f0;padding:6px 10px;font-size:12px;border-bottom:2px solid #ccc} .it td{font-weight:400;background:#fff;color:#1b1f24;width:auto;font-size:13px}
.ft{font-size:11px;color:#777;padding:6px 22px;border-top:1px solid #e3e5e8;display:flex;justify-content:space-between}
</style></head><body><div class="win">
<div class="tb"><b>Editais e Avisos de Contratações - Navegador</b><span>_ □ ×</span></div>
<div class="nav">◀ ▶ ⟳ <div class="url">https://pncp.gov.br/app/editais/${d.id}</div></div>
<div class="hd"><div><div class="t">Portal Nacional de Contratações Públicas</div><div class="s">Editais e avisos de contratações</div></div><div class="s">Acesso público</div></div>
<div class="bc">Início › Editais › ${d.orgao}</div>
<div class="ct"><h1>Edital nº ${d.num}<span class="st">Recebendo propostas</span></h1><div class="sub">${d.orgao} · ${d.cidade}</div>
<table>
<tr><td>Modalidade da contratação</td><td>${d.mod||"Pregão eletrônico"}</td></tr>
<tr><td>Objeto</td><td>${d.objeto}</td></tr>
<tr><td>Valor total estimado</td><td class="v">${d.valor}</td></tr>
<tr><td>Fim do recebimento de propostas</td><td><b>${d.fim}</b></td></tr>
<tr><td>Id da contratação no PNCP</td><td>${d.pncp}</td></tr>
<tr><td>Situação</td><td>Divulgada no PNCP</td></tr>
</table></div>
<div class="ft"><span>Lei nº 14.133/2021</span><span>Consulta pública</span></div>
</div></body></html>`;
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:800,height:600},deviceScaleFactor:1.28});
 for(const d of D){ await p.setContent(html(d)); await p.screenshot({path:d.out}); console.log(d.out); } await b.close(); })();
