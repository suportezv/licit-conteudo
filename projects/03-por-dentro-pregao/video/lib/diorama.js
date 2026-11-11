// Diorama isometrico low-poly da granja. Tudo e funcao do tempo t (segundos):
// renderAt(t) reconstrui a cena do zero a cada seek, sem estado acumulado.
import * as THREE from "./vendor/three.module.js";

// Fabrica: uma cena por canvas. Modo simples (um canvas) ou dual (duas granjas, dois canvases empilhados).
function criarDiorama(cfg) {
const EV = cfg.events; const CAMK = cfg.cam; const G = cfg.generico || {}; const P2 = !!(cfg.parte2 || G.pronta);
const W = cfg.w || 1080, H = cfg.h || 1920;
const C = { creme: 0xF4F0E6, navy: 0x141B3F, azul: 0x2F4DB8, lav: 0xB48CE4, mag: 0xF55CEB, ciano: 0x5BC6EE,
            grama: 0x52B585, gramaClara: 0x86D6A0, solo: 0x6B4F3A, soloClaro: 0x8C6A4E, amarelo: 0xF2C94C,
            rosa: 0xF2A6C4, pele: 0xF1C7A5, metal: 0xC9CDD6, escuro: 0x22284F, agua: 0x2C6E8F, lagoa: 0x1F5F58 };

// ---------- utilidades deterministicas
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const clamp01 = (x) => Math.max(0, Math.min(1, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const backOut = (p) => { const s = 1.70158; p = clamp01(p) - 1; return 1 + (s + 1) * p * p * p + s * p * p; };
const pop = (t, t0, d = 0.55) => (t < t0 ? 0 : backOut((t - t0) / d));       // 0 -> ~1 com overshoot
const lin = (t, t0, t1) => clamp01((t - t0) / Math.max(1e-6, t1 - t0));
const lerp = (a, b, k) => a + (b - a) * k;

// ---------- cena
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById(cfg.canvas || "dio-canvas"), antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene();
const ASPECT = W / H; const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 400);
const LUZ = { key: 2.4, hemi: 1.25, rim: 0.7 };
const hemi = new THREE.HemisphereLight(0xE8E2FF, 0x3A4A8A, LUZ.hemi); scene.add(hemi);
scene.add(new THREE.AmbientLight(0xFFFFFF, 0.35));
const key = new THREE.DirectionalLight(0xFFF1DC, LUZ.key); key.position.set(10, 18, 8); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); key.shadow.camera.left = -18; key.shadow.camera.right = 18; key.shadow.camera.top = 18; key.shadow.camera.bottom = -18; key.shadow.camera.near = 1; key.shadow.camera.far = 60; key.shadow.bias = -0.0008;
scene.add(key);
const rim = new THREE.DirectionalLight(0x5BC6EE, LUZ.rim); rim.position.set(-10, 9, -8); scene.add(rim);

const mats = {};
function mat(color, extra = {}) { const k = color + JSON.stringify(extra); if (!mats[k]) mats[k] = new THREE.MeshStandardMaterial({ color, roughness: 0.85, metalness: 0.02, flatShading: true, ...extra }); return mats[k]; }
function box(w, h, d, color, x = 0, y = 0, z = 0, extra = {}) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat(color, extra)); m.position.set(x, y + h / 2, z); m.castShadow = true; m.receiveShadow = true; return m; }
function cyl(r, h, color, x = 0, y = 0, z = 0, seg = 10, rt) { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt ?? r, r, h, seg), mat(color)); m.position.set(x, y + h / 2, z); m.castShadow = true; m.receiveShadow = true; return m; }
function cone(r, h, color, x, y, z, seg = 6) { return cyl(r, h, color, x, y, z, seg, 0.001); }
function grp(x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); scene.add(g); return g; }

function setScale(g, s) { g.visible = s > 0.001; const k = Math.max(0.001, s); g.scale.set(k, k, k); }
// generico: listas de keyframes [[t, valor], ...] e intervalos [[t0, t1], ...] vindas do gera.py
function kf(list, t, dflt, ramp = 0.8) { if (!list || !list.length) return dflt; let v = dflt; for (const [tk, vk] of list) { if (t >= tk) v = lerp(v, vk, smooth(lin(t, tk, tk + ramp))); } return v; }
function inRanges(list, t, ramp = 1.0) { if (!list) return 0; let k = 0; for (const [a, b] of list) { if (t >= a) k = Math.max(k, smooth(lin(t, a, a + ramp)) * (1 - smooth(lin(t, b - ramp, b)))); } return k; }
const TRUCKS = G.trucks || (P2 && EV.y1 !== undefined ? [EV.y1, EV.y2, EV.y3, EV.y4, EV.y5] : []);
function sackLevel(t) {
  if (!P2) return t < EV.sacks_start ? 0 : (t < EV.sacks_end ? lin(t, EV.sacks_start, EV.sacks_end) : 1);
  if (G.sacks) return kf(G.sacks, t, G.sacks_inicial ?? 0.65, 2.0);
  let s = 0.65;
  if (EV.sacks_up !== undefined && t >= EV.sacks_up) s = lerp(0.65, 1.0, smooth(lin(t, EV.sacks_up, EV.sacks_up + 2.0)));
  if (EV.conv !== undefined && t >= EV.conv + 0.3) s = lerp(1.0, 0.5, smooth(lin(t, EV.conv + 0.3, EV.conv + 2.2)));
  return s; }
function grassBad(t) { if (!P2) return 0; if (G.grass_bad) return inRanges(G.grass_bad, t, 1.5); if (EV.y1 === undefined) return 0; let k = 0; for (const y of [EV.y1, EV.y3]) { if (t >= y) k = Math.max(k, smooth(lin(t, y, y + 1.5)) * (1 - smooth(lin(t, y + 5.0, y + 6.5)))); } return k; }
function truckOut(t) { let o = 0; for (const y of TRUCKS) { if (t >= y && t < y + 2.6) o = smooth(lin(t, y, y + 2.4)); } return o; }
function confettiT(t) { const L = G.confetti || [EV.confetti]; let best = Infinity; for (const c of L) { if (t >= c && t - c < best) best = t - c; } return best; }

// ---------- camera: keyframes + deriva
const lerpAng = (a, b, s) => a + (((b - a + 540) % 360) - 180) * s;
function camAt(t) { let az = CAMK[0][1], el = CAMK[0][2], hw = CAMK[0][3], tx = CAMK[0][4], tz = CAMK[0][5];
  for (let i = 1; i < CAMK.length; i++) { const k = CAMK[i]; if (t < k[0]) break; const s = smooth((t - k[0]) / 1.8); az = lerpAng(az, k[1], s); el = lerp(el, k[2], s); hw = lerp(hw, k[3], s); tx = lerp(tx, k[4], s); tz = lerp(tz, k[5], s); }
  az += t * 1.2; if (t > EV.orbit) az += (t - EV.orbit) * 14; // deriva continua + orbita final
  const a = az * Math.PI / 180, e = el * Math.PI / 180, dist = 120;
  const hh = hw / ASPECT, off = hh * 0.10; // cena um pouco abaixo do centro: HUD e legendas ficam em cima
  camera.left = -hw; camera.right = hw; camera.top = hh + off; camera.bottom = -hh + off; camera.updateProjectionMatrix();
  camera.position.set(tx + dist * Math.cos(e) * Math.sin(a), dist * Math.sin(e) + 0.8, tz + dist * Math.cos(e) * Math.cos(a));
  camera.lookAt(tx, 0.9, tz); }

function cenaGranja() {
// chao
const plataforma = grp();
const topo = box(22, 0.3, 22, C.grama, 0, -0.3, 0); topo.receiveShadow = true; plataforma.add(topo); topo.material = topo.material.clone();
const corGrama = new THREE.Color(C.grama), corSeca = new THREE.Color(0x9CB36A);
plataforma.add(box(22, 1.1, 22, C.solo, 0, -1.4, 0));
plataforma.add(box(22.6, 0.25, 22.6, C.escuro, 0, -1.65, 0));
// capim (some com a terraplanagem, varrido em x)
const rnd = mulberry32(7); const capins = [];
for (let i = 0; i < 140; i++) { const x = (rnd() - 0.5) * 20, z = (rnd() - 0.5) * 20; const c = cone(0.22 + rnd() * 0.15, 0.55 + rnd() * 0.5, rnd() > 0.5 ? C.gramaClara : C.grama, x, 0, z, 5); c.userData.x = x; plataforma.add(c); capins.push(c); }
// barranco (fundo), achata com a terraplanagem
const barranco = box(22, 1.7, 3.0, C.soloClaro, 0, 0, -9.4); plataforma.add(barranco);
// grade de lotes
const lotes = grp(); for (let i = -2; i <= 2; i++) { lotes.add(box(0.07, 0.06, 20, C.creme, i * 4.4, 0.02, 0)); lotes.add(box(20, 0.06, 0.07, C.creme, 0, 0.02, i * 4.4)); }
// carimbo
const papel = grp(0, 2.6, 2); papel.add(box(3.2, 0.06, 2.2, C.creme)); const selo = cyl(0.45, 0.9, C.mag, 0, 0.2, 0, 16); papel.add(selo);
// trator de esteira
const dozer = grp(-12, 0, -7); dozer.add(box(1.7, 0.75, 1.1, C.amarelo)); dozer.add(box(0.8, 0.65, 0.85, C.creme, -0.2, 0.75, 0)); dozer.add(box(0.12, 0.9, 1.7, C.escuro, 1.05, 0, 0)); dozer.add(box(1.9, 0.3, 0.35, C.escuro, 0, -0.1, 0.62)); dozer.add(box(1.9, 0.3, 0.35, C.escuro, 0, -0.1, -0.62));
// galpoes
function galpao(z) { const g = grp(-1, 0, z); g.add(box(9, 1.55, 2.7, C.creme)); const r1 = box(9.5, 0.14, 1.75, C.azul, 0, 1.55 + 0.42, 0.72); r1.rotation.x = 0.5; g.add(r1); const r2 = box(9.5, 0.14, 1.75, C.azul, 0, 1.55 + 0.42, -0.72); r2.rotation.x = -0.5; g.add(r2); g.add(box(9.6, 0.1, 0.22, C.navy, 0, 2.3, 0));
  // portas e janelas (textura simples)
  for (let i = -3; i <= 3; i++) g.add(box(0.5, 0.42, 0.05, C.navy, i * 1.25, 0.8, 1.36));
  return g; }
const galpoes = [galpao(-5.2), galpao(0), galpao(5.2)];
// equipamento: silos, linha de racao, ventiladores
const equip = grp(); const ventiladores = [];
galpoes.forEach((g, i) => { const z = g.position.z; equip.add(cyl(0.62, 2.1, C.creme, 5.2, 0, z - 0.8, 12)); equip.add(cone(0.64, 0.6, C.metal, 5.2, 2.1, z - 0.8, 12)); equip.add(cyl(0.62, 2.1, C.creme, 5.2, 0, z + 0.8, 12)); equip.add(cone(0.64, 0.6, C.metal, 5.2, 2.1, z + 0.8, 12));
  equip.add(box(0.14, 0.14, 1.6, C.metal, 4.4, 1.9, z)); // linha
  for (let k = -1; k <= 1; k += 2) { const f = grp(-5.55, 0.8, z + k * 0.7); const h = box(0.1, 0.62, 0.62, C.escuro); f.add(h); const b1 = box(0.04, 0.5, 0.1, C.creme, -0.07, 0.06, 0); const b2 = box(0.04, 0.1, 0.5, C.creme, -0.07, 0.26, 0); b1.position.y = 0.31; b2.position.y = 0.31; const blades = new THREE.Group(); blades.position.set(-0.07, 0.31, 0); blades.add(box(0.04, 0.5, 0.1, C.creme, 0, -0.25, 0)); blades.add(box(0.04, 0.1, 0.5, C.creme, 0, -0.05, 0)); f.add(blades); ventiladores.push(blades); equip.add(f); } });
// comedouros dentro (linhas) nao visiveis; bebedouro seco: tubo na ponta
const canoSeco = box(0.12, 0.12, 2.4, C.ciano, 8.2, 0.6, -7.2);
// caixa d'agua e rede
const torre = grp(8.3, 0, -8.3); for (const [dx, dz] of [[-0.6, -0.6], [0.6, -0.6], [-0.6, 0.6], [0.6, 0.6]]) torre.add(cyl(0.08, 3.2, C.metal, dx, 0, dz, 6)); torre.add(cyl(1.0, 1.3, C.creme, 0, 3.2, 0, 14)); torre.add(cyl(1.02, 0.25, C.ciano, 0, 3.7, 0, 14)); torre.add(cone(1.05, 0.5, C.metal, 0, 4.5, 0, 14));
const rede = grp(); rede.add(box(0.14, 0.14, 15, C.ciano, 7.4, 0.25, 0)); for (const g of galpoes) rede.add(box(3.2, 0.14, 0.14, C.ciano, 5.9, 0.25, g.position.z));
// postes, fios, gerador
const postes = grp(); for (let i = 0; i < 4; i++) { postes.add(cyl(0.09, 3.0, C.soloClaro, -10 + i * 2.6, 0, 9.6, 6)); postes.add(box(0.7, 0.08, 0.08, C.soloClaro, -10 + i * 2.6, 2.8, 9.6)); if (i < 3) { const w = box(2.6, 0.03, 0.03, C.escuro, -10 + i * 2.6 + 1.3, 2.82, 9.6); postes.add(w); } }
const gerador = grp(-8.6, 0, 7.2); gerador.add(box(1.3, 0.95, 0.85, C.navy)); gerador.add(box(1.32, 0.16, 0.87, C.mag, 0, 0.5, 0)); const genLuz = box(0.18, 0.18, 0.05, C.escuro, 0.45, 0.65, 0.44, { emissive: 0x000000 }); gerador.add(genLuz);
// dejetos
const canal = grp(); for (const g of galpoes) canal.add(box(3.4, 0.1, 0.22, C.escuro, -7.2, 0.0, g.position.z)); canal.add(box(0.22, 0.1, 11.6, C.escuro, -8.8, 0.0, 0));
const lagoa = grp(-7.6, 0, -8.2); lagoa.add(cyl(2.3, 0.22, C.lagoa, 0, -0.02, 0, 18)); lagoa.add(cyl(2.55, 0.14, C.solo, 0, -0.1, 0, 18));
const bio = grp(-8.2, 0, -3.6); const dome = new THREE.Mesh(new THREE.SphereGeometry(1.25, 14, 10, 0, Math.PI * 2, 0, Math.PI / 2), mat(C.escuro)); dome.castShadow = true; bio.add(dome); bio.add(cyl(1.3, 0.3, C.creme, 0, 0, 0, 14));
// cerca, portaria, embarcadouro, composteira
const cerca = grp(); const postesCerca = [];
{ const P = []; const n = 17; for (let i = 0; i < n; i++) { const u = -10.2 + i * (20.4 / (n - 1)); P.push([u, -10.2]); P.push([u, 10.2]); P.push([-10.2, u]); P.push([10.2, u]); }
  for (const [x, z] of P) { if (Math.abs(x) < 1.6 && z > 9) continue; const p = cyl(0.07, 0.95, C.soloClaro, x, 0, z, 6); cerca.add(p); postesCerca.push(p); }
  const rails = [box(20.4, 0.05, 0.05, C.creme, 0, 0.55, -10.2), box(8.6, 0.05, 0.05, C.creme, -5.9, 0.55, 10.2), box(8.6, 0.05, 0.05, C.creme, 5.9, 0.55, 10.2), box(0.05, 0.05, 20.4, C.creme, -10.2, 0.55, 0), box(0.05, 0.05, 20.4, C.creme, 10.2, 0.55, 0)]; rails.forEach(r => { r.userData.rail = true; cerca.add(r); }); }
const portaria = grp(0, 0, 10.6); portaria.add(box(1.9, 1.25, 1.6, C.creme)); portaria.add(box(2.2, 0.12, 1.9, C.azul, 0, 1.25, 0)); portaria.add(box(0.1, 0.6, 0.1, C.ciano, 0.7, 1.37, 0)); portaria.add(box(0.4, 0.06, 0.4, C.ciano, 0.7, 1.95, 0));
const embarc = grp(6.2, 0, 10.2); const rampa = box(2.4, 0.3, 1.2, C.creme, 0, 0.5, 0); rampa.rotation.z = -0.32; embarc.add(rampa); embarc.add(box(1.2, 0.9, 1.3, C.creme, 1.4, 0, 0));
const compost = grp(-9.2, 0, 9.0); compost.add(box(1.7, 0.75, 1.3, C.solo)); compost.add(box(1.8, 0.1, 1.4, C.soloClaro, 0, 0.75, 0));
// caminhoes
function caminhao(cor) { const g = grp(); g.add(box(1.25, 1.15, 1.35, C.creme, -1.7, 0.5, 0)); g.add(box(1.0, 0.5, 1.2, C.navy, -1.75, 1.0, 0)); g.add(box(2.9, 1.25, 1.45, cor, 0.5, 0.55, 0)); for (let i = -1; i <= 1; i++) g.add(box(2.9, 0.08, 1.5, C.escuro, 0.5, 0.7 + i * 0.35, 0)); for (const [x, z] of [[-1.7, 0.75], [-1.7, -0.75], [0.0, 0.75], [0.0, -0.75], [1.4, 0.75], [1.4, -0.75]]) { const w = cyl(0.36, 0.3, C.escuro, x, 0.0, z, 10); w.rotation.x = Math.PI / 2; w.position.y = 0.36; g.add(w); } return g; }
const truck1 = caminhao(C.rosa); const truck2 = caminhao(C.lav);
// piquetes (cercados baixos) entre os galpoes e na frente: e onde os porcos ficam visiveis
const PENS = [-2.6, 2.6, 7.9]; const PEN_X0 = -5.4, PEN_X1 = 3.4, PEN_D = 1.9;
const cercados = grp();
for (const z of PENS) { for (let x = PEN_X0; x <= PEN_X1 + 0.01; x += 1.1) { cercados.add(cyl(0.05, 0.42, C.soloClaro, x, 0, z - PEN_D / 2, 5)); cercados.add(cyl(0.05, 0.42, C.soloClaro, x, 0, z + PEN_D / 2, 5)); }
  for (const dz of [-PEN_D / 2, PEN_D / 2]) cercados.add(box(PEN_X1 - PEN_X0, 0.04, 0.04, C.creme, (PEN_X0 + PEN_X1) / 2, 0.3, z + dz));
  for (const x of [PEN_X0, PEN_X1]) cercados.add(box(0.04, 0.04, PEN_D, C.creme, x, 0.3, z));
  cercados.add(box(PEN_X1 - PEN_X0, 0.03, PEN_D, C.soloClaro, (PEN_X0 + PEN_X1) / 2, 0.0, z)); }
const nPigs = 480; const pigs = new THREE.InstancedMesh(new THREE.BoxGeometry(0.3, 0.22, 0.44), mat(C.rosa), nPigs); pigs.castShadow = true; scene.add(pigs);
const pigHeads = new THREE.InstancedMesh(new THREE.BoxGeometry(0.22, 0.18, 0.2), mat(0xE88FB0), nPigs); scene.add(pigHeads);
const pigPos = []; { const r = mulberry32(99); for (let i = 0; i < nPigs; i++) { const z0 = PENS[i % 3]; const x = PEN_X0 + 0.25 + r() * (PEN_X1 - PEN_X0 - 0.5); const z = z0 + (r() - 0.5) * (PEN_D - 0.5); pigPos.push([x, z, r() * Math.PI * 2, r() * 6.28]); } }
const headOff = new THREE.Vector3();
// sacos de racao (instancias) numa pilha ao lado dos silos
const nSacks = 180; const sacks = new THREE.InstancedMesh(new THREE.BoxGeometry(0.55, 0.3, 0.38), mat(0xE7D9B8), nSacks); sacks.castShadow = true; scene.add(sacks);
const sackPos = []; { let i = 0; for (let layer = 0; i < nSacks; layer++) { const a0 = Math.max(4, 8 - layer), b0 = Math.max(3, 6 - layer); for (let a = 0; a < a0 && i < nSacks; a++) for (let b = 0; b < b0 && i < nSacks; b++) { sackPos.push([8.6 + (a - a0 / 2 + 0.5) * 0.57, layer * 0.3, 0.6 + (b - b0 / 2 + 0.5) * 0.4, layer]); i++; } } }
// pessoas
function pessoa(x, z, corRoupa, chapeu) { const g = grp(x, 0, z); g.add(cyl(0.24, 0.72, corRoupa, 0, 0, 0, 8)); const head = new THREE.Mesh(new THREE.SphereGeometry(0.21, 10, 8), mat(C.pele)); head.position.y = 0.98; head.castShadow = true; g.add(head); if (chapeu) { g.add(cyl(0.34, 0.05, chapeu, 0, 1.08, 0, 10)); g.add(cyl(0.18, 0.18, chapeu, 0, 1.12, 0, 10)); } return g; }
const tratador = pessoa(-6.6, 8.2, C.navy, C.mag);
const workers = [pessoa(-6.6, -2.6, C.azul, C.creme), pessoa(4.6, 2.6, C.azul, C.creme), pessoa(-2.0, -7.6, C.azul, C.creme), pessoa(4.6, -6.6, C.lav, C.creme)];
const visitante = pessoa(0, 13.2, C.soloClaro, C.solo);
// fantasma da granja pronta (sonho)
const ghost = grp(); { const gm = new THREE.MeshStandardMaterial({ color: C.creme, transparent: true, opacity: 0.22, roughness: 1 }); for (const z of [-5.2, 0, 5.2]) { const b = new THREE.Mesh(new THREE.BoxGeometry(9, 1.6, 2.7), gm); b.position.set(-1, 0.8, z); ghost.add(b); const r = new THREE.Mesh(new THREE.BoxGeometry(9.5, 0.9, 3.2), gm); r.position.set(-1, 2.0, z); ghost.add(r); } const s = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 4.6, 12), gm); s.position.set(8.3, 2.3, -8.3); ghost.add(s); }
// confete
const nConf = 160; const confetti = new THREE.InstancedMesh(new THREE.BoxGeometry(0.18, 0.04, 0.26), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 }), nConf); scene.add(confetti);
const confPos = []; { const r = mulberry32(3); const cols = [new THREE.Color(C.mag), new THREE.Color(C.ciano), new THREE.Color(C.lav), new THREE.Color(C.creme)]; for (let i = 0; i < nConf; i++) { confPos.push([(r() - 0.5) * 16, (r() - 0.5) * 16, r() * 6, r() * 6.28, 0.8 + r() * 0.6]); confetti.setColorAt(i, cols[i % 4]); } confetti.instanceColor.needsUpdate = true; }
const dummy = new THREE.Object3D(); const hidden = new THREE.Matrix4().makeScale(0, 0, 0);

// ---------- parte 2: anos, grama, sacos
// ---------- estado por tempo
function renderAt(t) {
  // compra a compra: pop-in
  const dz = lin(t, EV.dozer, EV.dozer_end);
  capins.forEach(c => { const corte = c.userData.x < -11 + dz * 24 ? 1 : 0; const s = t < EV.dozer ? 1 : (1 - corte); setScale(c, s); c.visible = t < EV.dozer_end + 0.1 ? c.visible : false; c.rotation.z = Math.sin(t * 1.7 + c.userData.x * 1.3) * 0.07; });
  barranco.scale.y = t < EV.dozer ? 1 : Math.max(0.02, 1 - dz); barranco.position.y = barranco.scale.y * 0.85; barranco.visible = dz < 0.98;
  dozer.visible = t >= EV.dozer && t < EV.dozer_end; dozer.position.x = -12 + dz * 24;
  setScale(lotes, t < EV.lots ? 0 : (t < EV.dozer ? pop(t, EV.lots) : 0)); lotes.position.y = 0;
  const sp = t >= EV.stamp && t < EV.stamp + 2.6; papel.visible = sp; if (sp) { const k = lin(t, EV.stamp, EV.stamp + 0.5); papel.position.y = 2.6 - k * 1.2; selo.position.y = 2.2 - backOut(lin(t, EV.stamp + 0.15, EV.stamp + 0.55)) * 2.0 + 0.2; }
  galpoes.forEach((g, i) => setScale(g, pop(t, EV["shed" + (i + 1)], 0.7)));
  setScale(equip, pop(t, EV.equip, 0.6)); canoSeco.visible = t >= EV.equip + 1.0 && t < EV.tower;
  setScale(torre, pop(t, EV.tower, 0.7)); setScale(rede, pop(t, EV.tower + 0.5, 0.6));
  setScale(postes, pop(t, EV.poles, 0.6)); setScale(gerador, pop(t, EV.poles + 0.4, 0.6));
  setScale(canal, pop(t, EV.canal, 0.6)); setScale(lagoa, pop(t, EV.lagoon, 0.7)); if (P2) { const ls = kf(G.lagoa, t, 1.0, 1.5); lagoa.scale.set(ls, 1, ls); } setScale(bio, pop(t, EV.lagoon + 0.4, 0.7));
  const fp = lin(t, EV.fence, EV.fence + 2.4); postesCerca.forEach((p, i) => setScale(p, i / postesCerca.length < fp ? 1 : 0)); cerca.children.forEach(c => { if (c.userData.rail) c.visible = fp >= 0.999; });
  setScale(portaria, pop(t, EV.portaria, 0.6)); setScale(embarc, pop(t, EV.embarc, 0.6)); setScale(compost, pop(t, EV.compost, 0.6));
  visitante.visible = t >= EV.visitor && t < EV.visitor + 2.2;
  // caminhao 1 entra, para na portaria, sai
  const in1 = lin(t, EV.truck1_in, EV.truck1_in + 2.4), out1 = lin(t, EV.truck1_out, EV.truck1_out + 2.0);
  truck1.visible = t >= EV.truck1_in && t < EV.truck1_out + 2.0; truck1.position.set(-2.6, 0, 16.5 - smooth(in1) * 4.2 + smooth(out1) * 5.0); truck1.rotation.y = Math.PI / 2;
  truck2.visible = t >= EV.truck2; truck2.position.set(3.4, 0, 12.6 + (1 - smooth(lin(t, EV.truck2, EV.truck2 + 1.4))) * 4 + (P2 ? truckOut(t) * 8.0 : 0)); truck2.rotation.y = Math.PI / 2;
  topo.material.color.lerpColors(corGrama, corSeca, grassBad(t));
  // porcos chegam
  setScale(cercados, pop(t, EV.pigs - 0.4, 0.5));
  const pk = P2 ? kf(G.pigs, t, 1.0, 1.2) : lin(t, EV.pigs, EV.pigs + 3.0); for (let i = 0; i < nPigs; i++) { const vis = (i / nPigs) < pk; if (vis) { const [x, z, r, ph] = pigPos[i]; const ry = r + Math.sin(t * 2.3 + ph) * 0.14; const hop = Math.max(0, Math.sin(t * 4.1 + ph * 2)) * 0.03; dummy.position.set(x, 0.11 + hop, z); dummy.rotation.set(0, ry, 0); dummy.scale.set(1, 1, 1); dummy.updateMatrix(); pigs.setMatrixAt(i, dummy.matrix); headOff.set(0, 0.03, 0.28).applyAxisAngle(new THREE.Vector3(0, 1, 0), ry); dummy.position.add(headOff); dummy.updateMatrix(); pigHeads.setMatrixAt(i, dummy.matrix); } else { pigs.setMatrixAt(i, hidden); pigHeads.setMatrixAt(i, hidden); } } pigs.instanceMatrix.needsUpdate = true; pigHeads.instanceMatrix.needsUpdate = true;
  // sacos se multiplicam
  const sk = sackLevel(t); for (let i = 0; i < nSacks; i++) { if ((i / nSacks) < sk) { const [x, y, z] = sackPos[i]; dummy.position.set(x, y + 0.15, z); dummy.rotation.set(0, (i % 3) * 0.08, 0); dummy.scale.set(1, 1, 1); dummy.updateMatrix(); sacks.setMatrixAt(i, dummy.matrix); } else sacks.setMatrixAt(i, hidden); } sacks.instanceMatrix.needsUpdate = true;
  const nW = Math.round(kf(G.workers, t, 4, 0.3)); workers.forEach((w, i) => setScale(w, i < nW ? pop(t, EV.workers + i * 0.18, 0.5) : 0));
  tratador.visible = true;
  // sonho fantasma
  const gh = t < EV.ghost_on ? 0 : (t < EV.ghost_off ? lin(t, EV.ghost_on, EV.ghost_on + 0.6) : 0); ghost.visible = gh > 0; ghost.children.forEach(m => m.material.opacity = 0.22 * gh);
  // confete
  const ct = confettiT(t); confetti.visible = ct >= 0 && ct < 5.0; if (confetti.visible) for (let i = 0; i < nConf; i++) { const [x, z, ph, rot, sp] = confPos[i]; dummy.position.set(x + Math.sin(ct * 2 + ph) * 0.6, 13 - ct * (2.2 + sp) - ph * 0.3, z); dummy.rotation.set(ct * 3 + rot, rot, ct * 2); dummy.scale.set(1, 1, 1); dummy.updateMatrix(); confetti.setMatrixAt(i, dummy.matrix); } confetti.instanceMatrix.needsUpdate = true;
  // ventiladores: giram apos a energia, param no apagao, voltam com o gerador
  const rodando = t >= EV.fans_on && !(t >= EV.blackout && t < EV.gen_on); let ang = 0; if (t >= EV.fans_on) { const tFim = Math.min(t, EV.blackout); ang = (tFim - EV.fans_on) * 14; if (t >= EV.gen_on) ang += (t - EV.gen_on) * 14; } ventiladores.forEach(v => v.rotation.x = ang);
  // apagao: luz cai, galpoes avermelham; gerador acende
  const black = t >= EV.blackout && t < EV.gen_on; key.intensity = black ? 0.7 : LUZ.key; hemi.intensity = black ? 0.45 : LUZ.hemi; rim.intensity = black ? 0.25 : LUZ.rim;
  genLuz.material = mat(t >= EV.gen_on ? C.ciano : C.escuro, { emissive: t >= EV.gen_on ? 0x5BC6EE : 0x000000, emissiveIntensity: 1.5 });
  // pausa em preto e branco
  const dio = document.getElementById("dio"); dio.classList.toggle("gray", t >= EV.pause_start && t < EV.pause_end); dio.classList.toggle("worn", (P2 && EV.desgaste !== undefined && t >= EV.desgaste && t < EV.conv) || inRanges(G.worn, t) > 0.5); dio.classList.toggle("noite", inRanges(G.noite, t) > 0.5);
  camAt(t); renderer.render(scene, camera);
}
return { renderAt };
}
const ctx = { THREE, scene, camera, renderer, mat, box, cyl, cone, grp, C, EV, G, P2, lin, smooth, pop, lerp, kf, inRanges, camAt, setScale, W, H, mulberry32, backOut, clamp01, hemi, key, rim, LUZ, cfg };
if (cfg.cena && cfg.cena !== "granja") { if (!window.__CENAS || !window.__CENAS[cfg.cena]) throw new Error("cena nao registrada: " + cfg.cena); return window.__CENAS[cfg.cena](ctx); }
return cenaGranja();
}
const D = window.__DIO;
const cenas = D.cenas
  ? D.cenas.map(c => criarDiorama({ events: c.events || D.events, cam: c.cam || D.cam, generico: c.generico || D.generico, parte2: D.parte2, canvas: c.canvas, w: c.w, h: c.h, cena: c.cena || D.cena }))
  : [criarDiorama({ events: D.events, cam: D.cam, generico: D.generico, parte2: D.parte2, canvas: "dio-canvas", cena: D.cena })];
window.addEventListener("hf-seek", (e) => cenas.forEach(c => c.renderAt(e.detail.time)));
cenas.forEach(c => c.renderAt(0)); window.__dioReady && window.__dioReady();
