// Cena "pregao": Por Dentro da Licitacao #1. Sete cenarios na mesma cena 3D, camera em perspectiva com cortes:
// cidade (prefeitura), predio (sete empresas em corte), escritorio (o protagonista), arena (a sala do pregao com placar
// e relogio), podio (classificacao), raiox (o computador da proposta aberto) e habil (a pasta de habilitacao).
// Tudo e funcao de t (seek deterministico). Usa lib/kit3d.js (window.__KIT) so para utilitarios e arvores.
// Listas genericas (G) vindas do gera.py: ver gera.py, funcao diorama(...).
window.__CENAS = window.__CENAS || {};
window.__CENAS.habil = function (ctx) {
  const { THREE, scene, renderer, EV, G, hemi, key, rim, lin, smooth, lerp, kf, inRanges, clamp01, mulberry32 } = ctx;
  const K = window.__KIT(THREE); const { box, cyl, sph, grp, mesh } = K;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  key.shadow.camera.left = -22; key.shadow.camera.right = 22; key.shadow.camera.top = 22; key.shadow.camera.bottom = -22; key.shadow.camera.far = 90; key.shadow.bias = -0.0005; key.shadow.normalBias = 0.03; key.shadow.camera.updateProjectionMatrix(); scene.add(key.target);
  hemi.color.setHex(0xF2FAFF); hemi.groundColor.setHex(0x6E8F7A); rim.color.setHex(0xC8F7A8);

  // ---------- paleta da Licit + cena de dia
  const P = { flo: 0x243D32, flo2: 0x2F5242, gra: 0x101218, gra2: 0x1B2026, lim: 0xA8F27A, sup: 0xF4F6F9, bra: 0xFFFFFF, apo: 0x59616E,
    creme: 0xF3EEE3, pedra: 0xE4DED2, grama: 0x7DC47A, grama2: 0x5FAE66, asfalto: 0x7A7F86, madeira: 0xB98A5A, madeiraEsc: 0x8A6440,
    pele: [0xE8B89A, 0xC98E6B, 0x9C6A4C, 0xF1CBB0], cabelo: [0x2B211B, 0x5A3A22, 0x111111, 0x8A5A2B], erro: 0xFF6B5B, ouro: 0xF2C94C,
    ceuA: "#9FD6F0", ceuB: "#E9F6FB", parede: 0xEFE7DA, parede2: 0xDCE8DF, tela: 0x0E1A14 };
  const FONT = "Sora, sans-serif";
  function mat(c, extra) { return K.mat(c, extra); }
  function basic(c, extra = {}) { return new THREE.MeshBasicMaterial({ color: c, ...extra }); }

  // ---------- texturas de texto (canvas)
  function tex(w, h, draw) { const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); draw(g, w, h); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData = { c, g }; return t; }
  function retex(t, draw) { const { c, g } = t.userData; g.clearRect(0, 0, c.width, c.height); draw(g, c.width, c.height); t.needsUpdate = true; }
  function placa(w, h, t, extra = {}) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, toneMapped: false, ...extra })); m.castShadow = false; m.receiveShadow = false; return m; }
  function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
  function txt(g, s, x, y, size, cor, peso = 600, al = "center") { g.font = `${peso} ${size}px ${FONT}`; g.fillStyle = cor; g.textAlign = al; g.textBaseline = "middle"; g.fillText(s, x, y); }
  const hex = (n) => "#" + n.toString(16).padStart(6, "0");

  // ---------- fundos por cenario (gradiente de ceu ou de sala)
  function grad(a, b) { return tex(4, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, a); gr.addColorStop(1, b); g.fillStyle = gr; g.fillRect(0, 0, w, h); }); }
  const BG = { ceu: grad(P.ceuA, P.ceuB), arena: grad("#0B0E12", "#1C3329"), sala: grad("#CFE8F2", "#F4F6F9") };

  // ---------- personagem com rosto e expressao (frente = +z)
  function gente(o = {}) {
    const o2 = Object.assign({ camisa: P.bra, calca: P.gra2, pele: P.pele[0], cabelo: P.cabelo[0], gravata: null, longo: false, oculos: false, sem_rosto: false, cor_rosto: null }, o);
    const g = grp(); const pernas = [], bracos = [];
    for (const dx of [-0.12, 0.12]) { const p = grp(dx, 0.88, 0); p.add(box(0.18, 0.88, 0.2, o2.calca, 0, -0.44, 0)); p.add(box(0.2, 0.1, 0.3, 0x2A2420, 0, -0.83, 0.04)); g.add(p); pernas.push(p); }
    g.add(box(0.5, 0.66, 0.28, o2.camisa, 0, 1.22, 0));
    if (o2.gravata) { g.add(box(0.08, 0.42, 0.02, o2.gravata, 0, 1.28, 0.15)); }
    for (const dx of [-1, 1]) { const b = grp(dx * 0.33, 1.5, 0); b.add(box(0.14, 0.62, 0.14, o2.camisa, 0, -0.31, 0)); b.add(box(0.13, 0.14, 0.13, o2.pele, 0, -0.66, 0)); g.add(b); bracos.push(b); }
    const cab = grp(0, 1.82, 0); g.add(cab);
    const rosto = box(0.4, 0.42, 0.36, o2.cor_rosto ?? o2.pele, 0, 0, 0); cab.add(rosto);
    cab.add(box(0.43, 0.12, 0.405, o2.cabelo, 0, 0.225, -0.0075)); cab.add(box(0.415, 0.24, 0.085, o2.cabelo, 0, 0.1, -0.1625));
    if (o2.longo) { cab.add(box(0.445, 0.42, 0.1, o2.cabelo, 0, -0.08, -0.185)); for (const dx of [-0.21, 0.21]) cab.add(box(0.05, 0.36, 0.3, o2.cabelo, dx, -0.04, -0.03)); }
    const olhos = [], sobr = []; let boca = null;
    if (!o2.sem_rosto) {
      for (const dx of [-0.09, 0.09]) { const e = grp(dx, 0.03, 0.181); e.add(box(0.075, 0.075, 0.01, 0xFFFFFF, 0, 0, 0)); const pu = box(0.042, 0.05, 0.012, 0x1A1410, 0, 0, 0.004); e.add(pu); e.userData.pu = pu; cab.add(e); olhos.push(e);
        const s = box(0.1, 0.022, 0.012, o2.cabelo, dx, 0.11, 0.182); cab.add(s); sobr.push(s); }
      boca = box(0.12, 0.03, 0.012, 0x7A2E2E, 0, -0.1, 0.182); cab.add(boca);
      if (o2.oculos) { for (const dx of [-0.09, 0.09]) { const a = new THREE.Mesh(new THREE.TorusGeometry(0.055, 0.009, 6, 14), mat(0x1A1A1A)); a.position.set(dx, 0.03, 0.19); cab.add(a); } cab.add(box(0.06, 0.012, 0.01, 0x1A1A1A, 0, 0.04, 0.19)); }
    }
    g.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
    g.userData = { pernas, bracos, cab, olhos, sobr, boca, ph: 0 }; return g;
  }
  // expressoes: neutro, tenso, susto, alivio, duvida, foco
  const EXP = { neutro: [0, 0, 1, 1, 0.12, 0.03], tenso: [-0.28, 0.28, 1, 0.9, 0.09, 0.025], susto: [0.25, -0.25, 1.35, 1.35, 0.08, 0.08], alivio: [0.18, -0.18, 1, 1, 0.16, 0.05], duvida: [0.32, 0.0, 1.1, 1.0, 0.09, 0.03], foco: [-0.12, 0.12, 0.85, 0.85, 0.1, 0.025] };
  function exprAt(p, lista, t) {
    const u = p.userData; if (!u.boca) return; let cur = EXP.neutro.slice();
    for (const [tk, nome] of (lista || [])) { if (t < tk) break; const alvo = EXP[nome] || EXP.neutro; const s = smooth(lin(t, tk, tk + 0.35)); cur = cur.map((v, i) => lerp(v, alvo[i], s)); }
    u.sobr[0].rotation.z = cur[0]; u.sobr[1].rotation.z = cur[1]; u.sobr[0].position.y = 0.11 + Math.abs(cur[0]) * 0.03 * (cur[0] > 0 ? 1 : -0.5); u.sobr[1].position.y = u.sobr[0].position.y;
    const pisca = ((t * 0.37 + u.ph) % 1) > 0.965 ? 0.12 : 1;
    u.olhos.forEach(o => o.scale.set(cur[2], cur[3] * pisca, 1));
    u.boca.scale.set(cur[4] / 0.12, cur[5] / 0.03, 1);
  }
  function anima(p, t, modo = "parado") { const u = p.userData; const ph = u.ph; p.userData.salto = 0;
    u.pernas.forEach(pe => pe.rotation.x = 0); u.bracos.forEach(b => { b.rotation.set(0, 0, 0); }); u.cab.rotation.set(0, 0, 0); if (p.userData.y0 !== undefined) p.position.y = p.userData.y0;
    if (modo === "andando") { u.pernas.forEach((pe, i) => pe.rotation.x = Math.sin(t * 7 + (i ? Math.PI : 0)) * 0.5); u.bracos.forEach((b, i) => b.rotation.x = Math.sin(t * 7 + (i ? 0 : Math.PI)) * 0.4); p.position.y = (p.userData.y0 || 0) + Math.abs(Math.sin(t * 7)) * 0.03; }
    else if (modo === "digitando") { u.bracos.forEach((b, i) => { b.rotation.x = -1.15 + Math.sin(t * 14 + i * 2) * 0.06; b.rotation.z = (i ? -1 : 1) * 0.12; }); u.cab.rotation.x = 0.12; }
    else if (modo === "apontando") { u.bracos[1].rotation.x = -1.4; u.bracos[1].rotation.z = -0.35; u.cab.rotation.y = -0.2; }
    else if (modo === "comemora") { u.bracos.forEach((b, i) => { b.rotation.z = (i ? 1 : -1) * (2.5 + Math.sin(t * 8) * 0.15); }); p.userData.salto = Math.abs(Math.sin(t * 6)) * 0.06; }
    else if (modo === "maos_cabeca") { u.bracos.forEach((b, i) => { b.rotation.x = -2.6; b.rotation.z = (i ? -1 : 1) * 0.55; }); }
    else if (modo === "fala") { u.bracos[1].rotation.x = -1.5 + Math.sin(t * 3) * 0.12; u.bracos[1].rotation.z = -0.25; u.cab.rotation.y = Math.sin(t * 1.4) * 0.12; }
    else { u.bracos.forEach((b, i) => b.rotation.x = Math.sin(t * 1.5 + ph + i) * 0.05); u.cab.rotation.y = Math.sin(t * 0.6 + ph) * 0.12; }
  }
  const rnd = mulberry32(31);
  function figurante(i) { return gente({ camisa: [0xDCE3EA, 0xF4D6C4, 0xCFE1D6, 0xE9E2F2, 0xF1E6C8, 0xD5E4F1, 0xE2D4C8][i % 7], calca: [P.gra2, 0x34405A, 0x4A3B30][i % 3], pele: P.pele[i % 4], cabelo: P.cabelo[(i + 1) % 4], longo: i % 3 === 1, gravata: i % 4 === 2 ? 0x34405A : null }); }

  // ---------- objetos de cena
  function mesa(w = 2.2, d = 1.0, cor = P.madeira) { const g = grp(); g.add(box(w, 0.08, d, cor, 0, 0.76, 0)); for (const [x, z] of [[-w / 2 + 0.08, -d / 2 + 0.08], [w / 2 - 0.08, -d / 2 + 0.08], [-w / 2 + 0.08, d / 2 - 0.08], [w / 2 - 0.08, d / 2 - 0.08]]) g.add(box(0.06, 0.76, 0.06, P.madeiraEsc, x, 0.38, z)); g.add(box(w - 0.2, 0.6, 0.04, cor, 0, 0.42, -d / 2 + 0.06)); return g; }
  function monitor(t) { const g = grp(); g.add(box(0.08, 0.32, 0.08, P.gra2, 0, 0.98, 0)); g.add(box(0.36, 0.03, 0.22, P.gra2, 0, 0.815, 0)); g.add(box(0.98, 0.6, 0.05, P.gra, 0, 1.38, 0)); const s = placa(0.92, 0.54, t); s.position.set(0, 1.38, 0.04); g.add(s); g.userData.tela = s; return g; }
  function cadeira(cor = P.gra2) { const g = grp(); g.add(box(0.5, 0.08, 0.5, cor, 0, 0.48, 0)); g.add(box(0.5, 0.55, 0.07, cor, 0, 0.8, -0.24)); g.add(cyl(0.04, 0.04, 0.45, 0x444444, 0, 0.24, 0, 6)); return g; }
  function planta(s = 1) { const g = grp(); g.add(cyl(0.16 * s, 0.12 * s, 0.3 * s, 0xC9734A, 0, 0.15 * s, 0, 10)); for (let i = 0; i < 5; i++) { const f = mesh(new THREE.IcosahedronGeometry(0.17 * s, 0), [0x5FAE66, 0x7DC47A, 0x4C9A57][i % 3], Math.cos(i * 1.3) * 0.12 * s, 0.42 * s + i * 0.06 * s, Math.sin(i * 1.3) * 0.12 * s); g.add(f); } return g; }
  function caixaPC(t) { const g = grp(); g.add(box(0.9, 0.6, 0.7, 0xC9A27A, 0, 0.3, 0)); const lado = placa(0.62, 0.42, t); lado.position.set(0, 0.32, 0.352); g.add(lado); g.add(box(0.92, 0.04, 0.12, 0xD8B48A, 0, 0.6, 0)); return g; }
  function lampada(y) { const g = grp(0, y, 0); g.add(cyl(0.02, 0.02, 0.5, 0x333333, 0, 0.25, 0, 5)); g.add(cyl(0.12, 0.28, 0.18, 0x2F3A33, 0, -0.08, 0, 10)); g.add(sph(0.08, 0xFFF4D6, 0, -0.16, 0, 8, { emissive: 0xFFE7A8, emissiveIntensity: 1.5 })); return g; }

  // ---------- os cenarios
  const SETS = { cidade: [0, 0, 0], predio: [150, 0, 0], escritorio: [300, 0, 0], arena: [450, 0, 0], podio: [600, 0, 0], raiox: [750, 0, 0], habil: [900, 0, 0], torre: [1050, 0, 0], linha: [1200, 0, 0] };
  const BGSET = { cidade: "ceu", predio: "ceu", escritorio: "sala", arena: "arena", podio: "arena", raiox: "arena", habil: "sala", torre: "arena", linha: "arena" };
  const R = {}; for (const n in SETS) { R[n] = grp(...SETS[n]); scene.add(R[n]); }
  const TX = {};

  // ===== A: cidade (prefeitura) =====
  { const A = R.cidade; A.add(K.chao(120, 90, P.grama)); A.add(K.grama(1400, 110, 30, 0, 26, 3));
    A.add(box(120, 0.05, 8, P.asfalto, 0, 0.02, 14)); for (let x = -56; x < 56; x += 4) A.add(box(2, 0.06, 0.18, P.sup, x, 0.04, 14));
    A.add(box(40, 0.12, 6, P.pedra, 0, 0.06, 8)); // praca
    const pref = grp(0, 0, -2); A.add(pref);
    for (let i = 0; i < 4; i++) pref.add(box(16 - i * 0.6, 0.22, 3.6 - i * 0.5, P.pedra, 0, 0.11 + i * 0.22, 4.4 - i * 0.25)); // escadaria
    pref.add(box(15, 6.2, 6, P.creme, 0, 3.1 + 0.9, 0)); pref.add(box(15.6, 0.5, 6.6, P.sup, 0, 7.25, 0));
    for (let i = 0; i < 6; i++) { const c = cyl(0.36, 0.42, 5.4, P.sup, -5.5 + i * 2.2, 3.6, 3.4, 14); pref.add(c); }
    pref.add(box(13.6, 0.5, 1.2, P.sup, 0, 6.55, 3.4));
    const fr = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.2, 1.2, 3, 1), mat(P.sup)); fr.rotation.set(Math.PI / 2, 0, Math.PI / 2); fr.scale.set(1, 1, 0.45); fr.position.set(0, 8.4, 3.0); pref.add(fr);
    for (let r = 0; r < 2; r++) for (let i = 0; i < 6; i++) pref.add(box(0.9, 1.3, 0.06, 0x6E8FA0, -5.5 + i * 2.2, 2.4 + r * 2.4, 3.03, { emissive: 0x2A4A5A, emissiveIntensity: 0.25 }));
    pref.add(box(2.0, 2.4, 0.06, 0x5A3E2A, 0, 2.1, 3.04));
    TX.pref = tex(1024, 160, (g, w, h) => { txt(g, "PREFEITURA MUNICIPAL", w / 2, h / 2, 74, "#243D32", 700); });
    const nome = placa(9, 1.4, TX.pref); nome.position.set(0, 6.55, 4.02); pref.add(nome);
    const mastro = cyl(0.06, 0.06, 9, 0xBFC5CC, 9.5, 4.5, 4.5, 8); pref.add(mastro);
    const band = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.5, 12, 4), new THREE.MeshStandardMaterial({ color: P.flo, side: THREE.DoubleSide, flatShading: true, roughness: 0.8 })); band.position.set(10.75, 8.1, 4.5); band.castShadow = true; pref.add(band); A.userData.band = band;
    band.userData.base = band.geometry.attributes.position.array.slice();
    const listra = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 0.3, 12, 1), new THREE.MeshStandardMaterial({ color: P.lim, side: THREE.DoubleSide, flatShading: true })); listra.position.set(0, 0, 0.01); band.add(listra);
    // caixas de computador na calcada: o que a prefeitura vai comprar
    TX.cx = tex(512, 340, (g, w, h) => { g.fillStyle = "#C9A27A"; g.fillRect(0, 0, w, h); g.strokeStyle = "#5A3E2A"; g.lineWidth = 14; rr(g, 150, 60, 212, 150, 14); g.stroke(); g.fillStyle = "#5A3E2A"; g.fillRect(236, 210, 40, 40); g.fillRect(190, 250, 132, 16); txt(g, "COMPUTADOR", w / 2, 305, 44, "#5A3E2A", 700); });
    const pilha = grp(-6.5, 0, 7.6); A.add(pilha); A.userData.caixas = [];
    for (let i = 0; i < 12; i++) { const c = caixaPC(TX.cx); const col = i % 4, lin_ = Math.floor(i / 4); c.position.set(col * 0.95 - 1.4, lin_ * 0.62, (i % 2) * 0.05); c.rotation.y = (i % 3 - 1) * 0.06; pilha.add(c); A.userData.caixas.push(c); }
    for (const [x, z, h] of [[-14, 6, 4.4], [14, 6, 4.0], [-20, -4, 5], [20, -6, 4.6], [-26, 10, 3.8], [26, 9, 4.2], [-11, -10, 4], [12, -11, 4.5]]) { const a = K.arvore(h, Math.round(x * 3 + z)); a.position.set(x, 0, z); A.add(a); }
    for (const x of [-18, -9, 9, 18]) { const p = K.poste(4.5); p.position.set(x, 0, 10.6); A.add(p); }
    A.userData.pedestres = []; for (let i = 0; i < 5; i++) { const pp = figurante(i + 2); pp.userData.ph = i; A.add(pp); A.userData.pedestres.push(pp); }
  }

  // ===== B: predio em corte (sete empresas) =====
  const salas = [];
  { const B = R.predio; B.add(K.chao(80, 60, P.grama)); B.add(K.grama(800, 70, 20, 0, 14, 5)); B.add(box(80, 0.05, 6, P.asfalto, 0, 0.02, 9));
    const W_ = 3.4, H_ = 3.0, D_ = 3.2; const pos = [[-1.5, 0], [-0.5, 0], [0.5, 0], [1.5, 0], [-1, 1], [0, 1], [1, 1]];
    const fr = grp(0, 0, 0); B.add(fr);
    fr.add(box(4 * W_ + 0.6, 0.3, D_ + 0.4, P.sup, 0, 0, 0)); fr.add(box(4 * W_ + 0.6, 0.3, D_ + 0.4, P.sup, 0, H_ + 0.15, 0)); fr.add(box(3 * W_ + 0.6, 0.3, D_ + 0.4, P.sup, 0, 2 * H_ + 0.3, 0));
    for (const x of [-2, -1, 0, 1, 2]) fr.add(box(0.22, H_, D_ + 0.4, P.sup, x * W_, 0.15 + H_ / 2, 0)); for (const x of [-1.5, -0.5, 0.5, 1.5]) fr.add(box(0.22, H_, D_ + 0.4, P.sup, x * W_, H_ + 0.3 + H_ / 2, 0));
    fr.add(box(4 * W_ + 0.6, 2 * H_ + 0.6, 0.2, P.parede2, 0, H_ + 0.3, -D_ / 2 - 0.1)); // fundo
    // borda de corte em verde-limao (o raio-x)
    for (const [x, y, w, h] of [[0, 0.3, 4 * W_ + 0.7, 0.06], [0, H_ + 0.45, 4 * W_ + 0.7, 0.06], [0, 2 * H_ + 0.6, 3 * W_ + 0.7, 0.06]]) fr.add(box(w, h, 0.06, P.lim, x, y, D_ / 2 + 0.22, { emissive: P.lim, emissiveIntensity: 0.6 }));
    pos.forEach(([cx, fl], i) => { const s = grp(cx * W_, fl * (H_ + 0.15) + 0.15, 0); fr.add(s);
      s.add(box(W_ - 0.24, 0.05, D_, i === 6 ? 0xCFE3D2 : 0xE8DCCB, 0, 0.0, 0)); s.add(box(W_ - 0.24, H_ - 0.2, 0.06, [0xF2E6D8, 0xE3EEF2, 0xF0E9DA, 0xE7F0E3, 0xF3E3E3, 0xE6E9F5, 0xE4F2DA][i], 0, (H_ - 0.2) / 2 + 0.03, -D_ / 2 + 0.06));
      const m = mesa(1.6, 0.7); m.position.set(0, 0, 0.1); s.add(m);
      const tt = tex(512, 300, (g, w, h) => { g.fillStyle = "#0E1A14"; g.fillRect(0, 0, w, h); }); const mo = monitor(tt); mo.position.set(0, 0, -0.05); mo.scale.set(0.9, 0.9, 0.9); s.add(mo);
      const p = i === 6 ? gente({ camisa: P.flo, calca: P.gra2, pele: P.pele[1], cabelo: P.cabelo[0], oculos: true }) : figurante(i); p.position.set(0, 0, -0.75); p.rotation.y = 0; p.userData.ph = i * 0.9; s.add(p);
      const l = lampada(H_ - 0.35); s.add(l);
      const qt = tex(256, 256, (g, w, h) => { g.fillStyle = "rgba(16,18,24,0.85)"; g.beginPath(); g.arc(w / 2, h / 2, 110, 0, Math.PI * 2); g.fill(); txt(g, "?", w / 2, h / 2 + 6, 170, "#A8F27A", 700); });
      const q = placa(0.7, 0.7, qt); q.position.set(0, 2.55, 0.6); q.visible = false; s.add(q);
      salas.push({ s, tt, mo, p, q, i }); });
    for (const [x, z, h] of [[-12, 4, 4], [12, 3, 4.4], [-16, -5, 5], [16, -4, 4.8]]) { const a = K.arvore(h, Math.round(x * 5 + z)); a.position.set(x, 0, z); B.add(a); }
  }
  function telaNumero(sala, n, cor = "#A8F27A") { retex(sala.tt, (g, w, h) => { g.fillStyle = "#0E1A14"; g.fillRect(0, 0, w, h); txt(g, "EMPRESA", w / 2, 80, 46, "#B8C5BC", 600); txt(g, String(n).padStart(2, "0"), w / 2, 190, 140, cor, 700); }); }

  // ===== C: escritorio do protagonista =====
  const prot = gente({ camisa: P.flo, calca: P.gra2, pele: P.pele[1], cabelo: P.cabelo[0], oculos: true }); prot.userData.ph = 0.4;
  const docs = []; let envelope, calTex, telaEsc;
  { const C = R.escritorio; C.add(box(14, 0.2, 12, 0xC9A57E, 0, -0.1, 0)); for (let x = -7; x < 7; x += 0.7) C.add(box(0.02, 0.2, 12, 0xB58F67, x, -0.09, 0));
    C.add(box(14, 6, 0.3, P.parede, 0, 3, -4)); C.add(box(0.3, 6, 12, 0xE6DCCD, -7, 3, 2));
    // janela com a cidade
    C.add(box(3.6, 2.4, 0.32, P.sup, 3.6, 3.0, -4)); const vt = tex(512, 340, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#9FD6F0"); gr.addColorStop(1, "#E9F6FB"); g.fillStyle = gr; g.fillRect(0, 0, w, h); g.fillStyle = "#C9D6DC"; for (let i = 0; i < 8; i++) { const bw = 40 + (i * 37) % 50, bh = 80 + (i * 53) % 140; g.fillRect(i * 66, h - bh, bw, bh); } g.fillStyle = "#7DC47A"; g.fillRect(0, h - 26, w, 26); });
    const jan = placa(3.3, 2.1, vt); jan.position.set(3.6, 3.0, -3.83); C.add(jan); C.add(box(0.08, 2.1, 0.05, P.sup, 3.6, 3.0, -3.8)); C.add(box(3.3, 0.08, 0.05, P.sup, 3.6, 3.0, -3.8));
    // calendario
    calTex = tex(512, 560, (g, w, h) => {});
    const cal = placa(1.2, 1.32, calTex); cal.position.set(-2.3, 2.55, -3.83); C.add(cal);
    // estante e planta
    C.add(box(2.2, 2.6, 0.5, P.madeiraEsc, -4.8, 1.3, -3.6)); for (let i = 0; i < 4; i++) C.add(box(2.1, 0.06, 0.48, P.madeira, -4.8, 0.4 + i * 0.65, -3.55)); for (let i = 0; i < 9; i++) C.add(box(0.18, 0.5, 0.36, [P.flo, 0xC9734A, 0x34405A, P.lim, 0xE4DED2][i % 5], -5.7 + i * 0.22, 1.32 + Math.floor(i / 5) * 0.65, -3.5));
    const pl = planta(1.6); pl.position.set(-3, 0, -3.2); C.add(pl);
    const m = mesa(2.6, 1.2); m.position.set(0, 0, -1.2); C.add(m);
    telaEsc = tex(1024, 600, (g, w, h) => {}); const mo = monitor(telaEsc); mo.position.set(0.2, 0, -1.55); mo.scale.set(1.25, 1.25, 1.25); C.add(mo);
    C.add(box(0.7, 0.03, 0.24, 0x2A2F35, 0.2, 0.81, -0.95)); C.add(box(0.12, 0.03, 0.18, 0x2A2F35, 0.85, 0.81, -0.95));
    const xc = cyl(0.07, 0.06, 0.14, P.sup, -0.9, 0.87, -1.0, 10); C.add(xc);
    const ch = cadeira(); ch.position.set(0.2, 0, 0.35); ch.rotation.y = Math.PI; C.add(ch);
    prot.position.set(0.2, 0, -0.35); prot.rotation.y = Math.PI; C.add(prot);
    // o edital: pilha que se abre em secoes (raio-x)
    const nomes = ["OBJETO", "ESPECIFICAÇÃO", "HABILITAÇÃO", "PRAZOS"];
    nomes.forEach((n, i) => { const t = tex(640, 400, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#243D32"; g.fillRect(0, 0, w, 86); txt(g, n, w / 2, 46, 52, "#FFFFFF", 700); g.fillStyle = "#C9D1CC"; for (let k = 0; k < 7; k++) g.fillRect(48, 120 + k * 36, (k % 3 === 2 ? 360 : 540), 14); g.fillStyle = "#A8F27A"; g.fillRect(48, 120 + (i + 1) * 36, 300, 14); });
      const d = grp(); const fl = box(1.6, 0.03, 1.0, 0xFFFFFF, 0, 0, 0); d.add(fl); const top_ = placa(1.6, 1.0, t); top_.rotation.x = -Math.PI / 2; top_.position.y = 0.03; d.add(top_); d.position.set(-0.9, 0.82 + i * 0.035, -1.05); C.add(d); docs.push(d); });
    // envelope da proposta
    envelope = grp(); { const ev = box(0.9, 0.04, 0.6, P.sup, 0, 0, 0); envelope.add(ev); const ab = box(0.9, 0.02, 0.34, 0xE4DED2, 0, 0.03, -0.13); ab.rotation.x = 0.3; envelope.add(ab); const sl = cyl(0.08, 0.08, 0.02, P.lim, 0, 0.05, 0.05, 12, { emissive: P.lim, emissiveIntensity: 0.6 }); envelope.add(sl); }
    envelope.visible = false; C.add(envelope);
    const luz = new THREE.PointLight(0xFFE7B8, 6, 12, 1.5); luz.position.set(0, 4.6, 0.5); C.add(luz);
  }
  function desenhaCal(dias) { const n = Math.round(dias); if (calTex.userData.n === n) return; calTex.userData.n = n; retex(calTex, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#243D32"; g.fillRect(0, 0, w, 110); if (n < 1) { txt(g, "NOVEMBRO", w / 2, 58, 46, "#FFFFFF", 700); g.fillStyle = "#D8E0D9"; for (let r = 0; r < 5; r++) for (let c = 0; c < 6; c++) g.fillRect(40 + c * 76, 150 + r * 76, 56, 56); return; } txt(g, "EDITAL NO AR", w / 2, 58, 46, "#FFFFFF", 700); txt(g, String(n), w / 2, 300, 230, "#243D32", 700); txt(g, "dias úteis", w / 2, 470, 54, "#59616E", 600); }); }
  function desenhaTelaEsc(modo) { retex(telaEsc, (g, w, h) => { g.fillStyle = "#F4F6F9"; g.fillRect(0, 0, w, h); g.fillStyle = "#243D32"; g.fillRect(0, 0, w, 80); txt(g, modo === "proposta" ? "Proposta enviada" : "Edital: aquisição de computadores", 40, 42, 36, "#FFFFFF", 600, "left");
    if (modo === "proposta") { g.fillStyle = "#E1F4D4"; rr(g, 60, 140, w - 120, 300, 26); g.fill(); txt(g, "R$ 438.000,00", w / 2, 260, 96, "#243D32", 700); txt(g, "Registrada no sistema", w / 2, 360, 40, "#59616E", 500); }
    else { for (let k = 0; k < 8; k++) { g.fillStyle = k === 2 ? "#A8F27A" : "#D8E0D9"; g.fillRect(60, 130 + k * 52, k === 2 ? 520 : (k % 2 ? 760 : 880), 22); } } }); }

  // ===== D: arena (a sala do pregao) =====
  const pulpitos = []; let placarTex, pregoeiro, feixes = [];
  { const D = R.arena; const piso = new THREE.Mesh(new THREE.CylinderGeometry(16, 16, 0.3, 64), mat(0x16201B)); piso.position.y = -0.15; piso.receiveShadow = true; D.add(piso);
    for (const r of [4, 7.5, 11, 14.5]) { const an = new THREE.Mesh(new THREE.RingGeometry(r - 0.04, r + 0.04, 96), basic(P.lim, { transparent: true, opacity: 0.35, side: THREE.DoubleSide })); an.rotation.x = -Math.PI / 2; an.position.y = 0.02; D.add(an); }
    for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2; const l = box(0.04, 0.01, 12, P.lim, 0, 0.02, 0, { emissive: P.lim, emissiveIntensity: 0.4, transparent: true, opacity: 0.18 }); l.rotation.y = a; l.position.set(Math.sin(a) * 9, 0.02, Math.cos(a) * 9); D.add(l); }
    // placar holografico ao fundo
    placarTex = tex(1024, 1024, (g, w, h) => {});
    const pl = placa(7.2, 7.2, placarTex); pl.position.set(0, 4.7, -9.5); D.add(pl);
    const mold = new THREE.Mesh(new THREE.BoxGeometry(7.6, 7.6, 0.2), mat(P.gra, { emissive: 0x0B1410 })); mold.position.set(0, 4.7, -9.65); D.add(mold);
    for (const x of [-3.9, 3.9]) D.add(box(0.14, 7.6, 0.14, P.lim, x, 2.6, -9.45, { emissive: P.lim, emissiveIntensity: 0.9 }));
    // pregoeiro na mesa central, de frente para os pulpitos
    const mp = grp(0, 0, -6.2); D.add(mp); mp.add(box(3.2, 1.05, 1.0, P.flo, 0, 0.52, 0)); mp.add(box(3.3, 0.06, 1.1, P.lim, 0, 1.06, 0, { emissive: P.lim, emissiveIntensity: 0.5 }));
    const tp = tex(512, 128, (g, w, h) => { txt(g, "PREGOEIRO", w / 2, h / 2, 64, "#A8F27A", 700); }); const pt = placa(2.4, 0.6, tp); pt.position.set(0, 0.55, 0.51); mp.add(pt);
    pregoeiro = gente({ camisa: 0x2D3640, calca: P.gra2, pele: P.pele[2], cabelo: P.cabelo[2], gravata: P.lim, oculos: false }); pregoeiro.position.set(0, 0, -1.2); pregoeiro.userData.ph = 2; mp.add(pregoeiro);
    // sete pulpitos em arco
    for (let i = 0; i < 7; i++) { const a = (-60 + i * 20) * Math.PI / 180; const g = grp(Math.sin(a) * 9.5, 0, Math.cos(a) * 9.5 - 3.2); g.rotation.y = a + Math.PI; D.add(g);
      g.add(box(1.5, 1.15, 0.8, P.gra2, 0, 0.58, 0)); const borda = box(1.56, 0.06, 0.86, P.flo2, 0, 1.17, 0); g.add(borda);
      const nt = tex(256, 160, (gg, w, h) => { gg.fillStyle = "#0E1A14"; gg.fillRect(0, 0, w, h); txt(gg, String(i + 1).padStart(2, "0"), w / 2, h / 2 + 4, 110, i === 2 ? "#A8F27A" : "#F4F6F9", 700); });
      const np = placa(1.0, 0.62, nt); np.position.set(0, 0.62, 0.41); g.add(np); np.rotation.y = Math.PI * 0; // frente do pulpito para o centro
      const pess = i === 2 ? gente({ camisa: P.flo, calca: P.gra2, pele: P.pele[1], cabelo: P.cabelo[0], oculos: true }) : gente({ camisa: 0x8A939E, calca: 0x59616E, cor_rosto: 0x9AA3AD, cabelo: 0x59616E, sem_rosto: true });
      pess.position.set(0, 0, -0.75); g.add(pess);
      const mk = tex(256, 256, (gg, w, h) => { gg.fillStyle = "#0E1A14"; gg.beginPath(); gg.arc(w / 2, h / 2, 118, 0, 6.3); gg.fill(); gg.strokeStyle = i === 2 ? "#A8F27A" : "#59616E"; gg.lineWidth = 12; gg.stroke(); txt(gg, String(i + 1).padStart(2, "0"), w / 2, h / 2 + 4, 120, i === 2 ? "#A8F27A" : "#F4F6F9", 700); });
      const masc = placa(0.62, 0.62, mk); masc.position.set(i === 2 ? -0.8 : 0, i === 2 ? 2.15 : 1.85, -0.5); masc.userData.y0 = masc.position.y; g.add(masc);
      const anel = new THREE.Mesh(new THREE.RingGeometry(1.05, 1.18, 48), basic(i === 2 ? P.lim : 0x59616E, { transparent: true, opacity: i === 2 ? 0.9 : 0.4, side: THREE.DoubleSide })); anel.rotation.x = -Math.PI / 2; anel.position.y = 0.03; g.add(anel);
      const luz = box(1.5, 0.05, 0.05, P.lim, 0, 1.2, 0.43, { emissive: P.lim, emissiveIntensity: 0 }); g.add(luz);
      const check = tex(128, 128, (gg, w, h) => { gg.fillStyle = "#A8F27A"; gg.beginPath(); gg.arc(64, 64, 58, 0, 6.3); gg.fill(); gg.strokeStyle = "#101218"; gg.lineWidth = 14; gg.beginPath(); gg.moveTo(34, 66); gg.lineTo(56, 88); gg.lineTo(96, 42); gg.stroke(); });
      const ck = placa(0.5, 0.5, check); ck.position.set(0.55, 1.6, 0.42); ck.visible = false; g.add(ck);
      pulpitos.push({ g, pess, masc, luz, ck, i, a }); }
    // feixes de lance: do pulpito ao placar
    for (let k = 0; k < 6; k++) { const f = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1, 6), basic(P.lim, { transparent: true, opacity: 0.9 })); f.visible = false; D.add(f); feixes.push(f); }
    const amb = new THREE.PointLight(0xA8F27A, 18, 30, 1.6); amb.position.set(0, 7, -6); D.add(amb);
  }
  const brl = (v) => "R$ " + Math.round(v).toLocaleString("pt-BR");
  function desenhaPlacar(t) {
    const L = G.lances || []; let melhor = null, ultimo = null; for (const [tk, idx, v] of L) { if (t >= tk) { melhor = v; ultimo = [tk, idx]; } }
    const modo = Math.round(kf(G.placar_modo, t, 0, 0.01));
    // relogio: interpolacao linear entre chaves [t, segundos]
    const RK = G.relogio || []; let seg = RK.length ? RK[0][1] : 0; for (let i = 0; i < RK.length; i++) { const [tk, s] = RK[i]; if (t < tk) break; const nx = RK[i + 1]; seg = nx && t < nx[0] ? lerp(s, nx[1], (t - tk) / (nx[0] - tk)) : s; }
    seg = Math.max(0, seg);
    const flash = ultimo ? clamp01(1 - (t - ultimo[0]) / 0.6) : 0;
    retex(placarTex, (g, w, h) => {
      g.fillStyle = "rgba(14,26,20,0.92)"; g.fillRect(0, 0, w, h);
      g.strokeStyle = "rgba(168,242,122,0.35)"; g.lineWidth = 4; for (let y = 0; y < h; y += 64) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
      if (modo === 0) { txt(g, "SESSÃO PÚBLICA", w / 2, 300, 70, "#B8C5BC", 600); txt(g, "10:00", w / 2, 520, 260, "#F4F6F9", 700); txt(g, "Pregão eletrônico", w / 2, 740, 64, "#A8F27A", 600); return; }
      if (modo >= 5) { const M = { 5: ["HABILITAÇÃO", "EMPRESA 02", "INABILITADA", "#FF6B5B"], 6: ["HABILITAÇÃO", "EMPRESA 03", "EM ANÁLISE", "#F2C94C"], 7: ["DILIGÊNCIA", "CERTIDÃO FGTS", "ATUALIZADA", "#A8F27A"], 8: ["HABILITADA", "EMPRESA 03", "R$ 438.000", "#A8F27A"] }[modo];
        txt(g, M[0], w / 2, 250, 72, "#B8C5BC", 600); txt(g, M[1], w / 2, 410, 96, "#F4F6F9", 700); txt(g, M[2], w / 2, 610, 120, M[3], 700); return; }
      if (modo === 4) { txt(g, "EM NEGOCIAÇÃO", w / 2, 250, 72, "#F2C94C", 600); txt(g, "EMPRESA 02", w / 2, 400, 90, "#A8F27A", 700); txt(g, "R$ 426.000", w / 2, 620, 150, "#F4F6F9", 700); txt(g, "01 desclassificada", w / 2, 800, 54, "#FF6B5B", 600); return; }
      if (modo === 3) { txt(g, "PROPOSTA ACEITA", w / 2, 250, 72, "#B8C5BC", 600); txt(g, "EMPRESA 02", w / 2, 400, 90, "#A8F27A", 700); txt(g, "R$ 426.000", w / 2, 620, 150, "#F4F6F9", 700); return; }
      txt(g, modo === 2 ? "DISPUTA ENCERRADA" : "MELHOR LANCE", w / 2, 150, 66, modo === 2 ? "#FF6B5B" : "#B8C5BC", 600);
      g.save(); g.globalAlpha = 1; txt(g, melhor ? brl(melhor) : "R$ 480.000", w / 2, 330, 150, flash > 0.3 ? "#A8F27A" : "#F4F6F9", 700); g.restore();
      txt(g, "de quem? ninguém sabe", w / 2, 450, 46, "#59616E", 500);
      // relogio circular
      const cx = w / 2, cy = 740, r = 190; g.lineWidth = 26; g.strokeStyle = "rgba(168,242,122,0.18)"; g.beginPath(); g.arc(cx, cy, r, 0, 6.2832); g.stroke();
      const frac = clamp01(seg / 120); g.strokeStyle = seg < 30 ? "#FF6B5B" : "#A8F27A"; g.beginPath(); g.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + frac * 6.2832); g.stroke();
      const mm = Math.floor(seg / 60), ss = Math.floor(seg % 60); txt(g, `${String(mm).padStart(2, "0")}:${String(ss).padStart(2, "0")}`, cx, cy, 120, seg < 30 ? "#FF6B5B" : "#F4F6F9", 700);
    });
  }

  // ===== E: podio =====
  const podio = {}; { const E = R.podio; const piso = new THREE.Mesh(new THREE.CylinderGeometry(14, 14, 0.3, 48), mat(0x16201B)); piso.position.y = -0.15; E.add(piso);
    for (const r of [5, 9]) { const an = new THREE.Mesh(new THREE.RingGeometry(r - 0.04, r + 0.04, 96), basic(P.lim, { transparent: true, opacity: 0.3, side: THREE.DoubleSide })); an.rotation.x = -Math.PI / 2; an.position.y = 0.02; E.add(an); }
    const defs = [{ k: 1, x: 0, h: 2.6, v: "R$ 399 mil", c: P.flo }, { k: 2, x: -2.7, h: 1.8, v: "R$ 426 mil", c: P.flo2 }, { k: 3, x: 2.7, h: 1.5, v: "R$ 438 mil", c: 0x3B4A42 }];
    for (const d of defs) { const g = grp(d.x, 0.012, 0); E.add(g); g.add(box(2.4, d.h, 2.0, d.c, 0, d.h / 2, 0)); g.add(box(2.46, 0.07, 2.06, P.lim, 0, d.h, 0, { emissive: P.lim, emissiveIntensity: 0.5 }));
      const pinta = (k, v) => (gg, w, h) => { txt(gg, k + "º", w / 2, 120, 150, "#A8F27A", 700); txt(gg, v, w / 2, 300, 84, "#F4F6F9", 700); };
      const t = tex(512, 400, pinta(d.k, d.v)); t.userData.pinta = pinta; const pw = Math.min(2.2, (d.h - 0.12) * 1.28); const f = placa(pw, pw / 1.28, t); f.position.set(0, d.h / 2 - 0.02, 1.01); g.add(f); podio[d.k] = { g, h: d.h, x: d.x, t, v: d.v }; }
    // figuras: 01 e 02 sem rosto, voce com rosto
    podio.f1 = gente({ camisa: 0x8A939E, calca: 0x59616E, cor_rosto: 0x9AA3AD, cabelo: 0x59616E, sem_rosto: true }); podio.f2 = gente({ camisa: 0x8A939E, calca: 0x59616E, cor_rosto: 0x9AA3AD, cabelo: 0x59616E, sem_rosto: true });
    podio.fv = gente({ camisa: P.flo, calca: P.gra2, pele: P.pele[1], cabelo: P.cabelo[0], oculos: true }); podio.fv.userData.ph = 1;
    for (const f of [podio.f1, podio.f2, podio.fv]) E.add(f);
    const nm = (n) => tex(256, 256, (gg, w, h) => { gg.fillStyle = "#0E1A14"; gg.beginPath(); gg.arc(w / 2, h / 2, 118, 0, 6.3); gg.fill(); gg.strokeStyle = "#59616E"; gg.lineWidth = 12; gg.stroke(); txt(gg, n, w / 2, h / 2 + 4, 120, "#F4F6F9", 700); });
    podio.m1 = placa(0.62, 0.62, nm("01")); podio.m2 = placa(0.62, 0.62, nm("02")); E.add(podio.m1); E.add(podio.m2);
    // faixa de 5% (empate ficto): lamina translucida sobre o 1o e o 2o lugares
    podio.faixa = new THREE.Mesh(new THREE.BoxGeometry(5.6, 0.5, 2.3), new THREE.MeshBasicMaterial({ color: P.lim, transparent: true, opacity: 0.0 })); podio.faixa.position.set(0, 2.65, 0); E.add(podio.faixa);
    // X vermelho
    podio.x = grp(0, 4.6, 1.2); for (const r of [0.78, -0.78]) { const b = box(2.4, 0.34, 0.2, P.erro, 0, 0, 0, { emissive: P.erro, emissiveIntensity: 0.6 }); b.rotation.z = r; podio.x.add(b); } podio.x.visible = false; E.add(podio.x);
    const luz = new THREE.PointLight(0xA8F27A, 14, 24, 1.6); luz.position.set(0, 7, 4); E.add(luz);
  }

  // ===== F: raio-x do computador =====
  const rx = {}; { const F = R.raiox; const piso = box(30, 0.3, 24, 0x16201B, 0, -0.15, 0); F.add(piso);
    for (let x = -14; x <= 14; x += 1.5) F.add(box(0.03, 0.01, 24, P.lim, x, 0.01, 0, { transparent: true, opacity: 0.2 })); for (let z = -12; z <= 12; z += 1.5) F.add(box(30, 0.01, 0.03, P.lim, 0, 0.01, z, { transparent: true, opacity: 0.2 }));
    const bancada = box(9, 0.2, 3.4, 0x2A3530, 0, 1.0, 0); F.add(bancada); F.add(box(8.6, 1.0, 3.0, 0x1E2723, 0, 0.5, 0));
    function gabinete(x, fantasma) { const g = grp(x, 1.1, -0.2); g.rotation.y = -Math.PI / 2; g.scale.setScalar(0.85); F.add(g); const cor = fantasma ? P.lim : 0x2B3138;
      const eM = fantasma ? { transparent: true, opacity: 0.12, emissive: P.lim, emissiveIntensity: 0.3 } : {};
      g.add(box(1.4, 2.8, 2.6, cor, 0, 1.4, 0, eM));
      const pl = box(1.15, 2.4, 2.3, 0x2E7A52, 0.05, 1.4, 0, fantasma ? { transparent: true, opacity: 0.3 } : { emissive: 0x1F5F3F, emissiveIntensity: 0.4 }); g.add(pl);
      const lado = grp(0.72, 0, 1.3); const lp = box(0.05, 2.8, 2.6, fantasma ? P.lim : 0x3A424B, 0, 1.4, -1.3, fantasma ? { transparent: true, opacity: 0.15 } : {}); lado.add(lp); g.add(lado);
      const slots = []; for (let i = 0; i < 2; i++) { const sl = box(0.06, 1.2, 0.08, 0x111111, 0.62, 1.8, -0.3 + i * 0.32); g.add(sl); slots.push(sl); }
      const bord = []; for (let i = 0; i < 2; i++) bord.push(box(0.16, 1.3, 0.18, P.erro, 0.62, 1.8, -0.3 + i * 0.32, { transparent: true, opacity: 0.0, emissive: P.erro, emissiveIntensity: 0.8 }));
      bord.forEach(b => g.add(b));
      const rams = []; for (let i = 0; i < 2; i++) { const r = box(0.14, 1.15, 0.12, P.lim, 0.68, 1.8, -0.3 + i * 0.32, { emissive: P.lim, emissiveIntensity: 1.2 }); g.add(r); rams.push(r); }
      return { g, lado, rams, bord }; }
    rx.ed = gabinete(-1.55, true); rx.pr = gabinete(1.55, false); rx.pr.rams[1].visible = false;
    const et = (a, b, cor) => tex(640, 260, (g, w, h) => { g.fillStyle = "rgba(16,18,24,0.88)"; rr(g, 10, 10, w - 20, h - 20, 40); g.fill(); g.strokeStyle = cor; g.lineWidth = 8; rr(g, 10, 10, w - 20, h - 20, 40); g.stroke(); txt(g, a, w / 2, 90, 58, "#B8C5BC", 600); txt(g, b, w / 2, 180, 92, cor, 700); });
    rx.eE = placa(1.9, 0.77, et("EDITAL PEDE", "16 GB", "#A8F27A")); rx.eE.position.set(-1.6, 4.25, 0.8); F.add(rx.eE);
    rx.eP = placa(1.9, 0.77, et("PROPOSTA 01", "8 GB", "#FF6B5B")); rx.eP.position.set(1.6, 4.25, 0.8); F.add(rx.eP);
    rx.x = grp(1.55, 2.4, 1.6); for (const r of [0.78, -0.78]) { const b = box(2.2, 0.3, 0.16, P.erro, 0, 0, 0, { emissive: P.erro, emissiveIntensity: 0.7 }); b.rotation.z = r; rx.x.add(b); } rx.x.visible = false; F.add(rx.x);
    rx.dt = placa(2.7, 0.75, tex(720, 200, (g, w, h) => { g.fillStyle = "#FF6B5B"; rr(g, 10, 10, w - 20, h - 20, 90); g.fill(); txt(g, "DESCLASSIFICADA", w / 2, h / 2 + 4, 62, "#101218", 700); })); rx.dt.position.set(0, 0.55, 2.2); rx.dt.visible = false; F.add(rx.dt);
    const luz = new THREE.PointLight(0xA8F27A, 12, 20, 1.6); luz.position.set(0, 6, 5); F.add(luz);
  }

  // ===== G: habilitacao =====
  const hb = {}; { const H = R.habil; H.add(box(16, 0.2, 12, 0xC9A57E, 0, -0.1, 0)); H.add(box(16, 6, 0.3, P.parede2, 0, 3, -4));
    const m = mesa(4.2, 2.2, P.madeira); m.position.set(0, 0, 0); H.add(m);
    const pasta = grp(0, 0.82, 0.1); H.add(pasta); pasta.add(box(3.0, 0.04, 2.0, 0x2F5242, -0.05, 0, 0)); const capa = box(1.5, 0.04, 2.0, P.flo, 0.75, 0.02, 0); pasta.add(capa);
    const ttl = tex(512, 160, (g, w, h) => { txt(g, "HABILITAÇÃO", w / 2, h / 2, 70, "#A8F27A", 700); }); const tp = placa(1.4, 0.44, ttl); tp.rotation.x = -Math.PI / 2; tp.position.set(-0.8, 0.03, -0.75); pasta.add(tp);
    hb.docs = []; const nomes = [["HABILITAÇÃO", "JURÍDICA"], ["HABILITAÇÃO", "TÉCNICA"], ["FISCAL E", "TRABALHISTA"], ["ECONÔMICO-", "FINANCEIRA"]];
    nomes.forEach((n, i) => { const t = tex(512, 660, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#243D32"; g.fillRect(0, 0, w, 150); txt(g, n[0], w / 2, 58, 56, "#FFFFFF", 700); txt(g, n[1], w / 2, 116, 40, "#A8F27A", 600); g.fillStyle = "#C9D1CC"; for (let k = 0; k < 9; k++) g.fillRect(50, 210 + k * 44, k % 3 === 2 ? 260 : 412, 16); });
      const d = grp(); d.add(box(1.25, 0.02, 1.6, 0xFFFFFF, 0, 0, 0)); const tp2 = placa(1.25, 1.6, t); tp2.rotation.x = -Math.PI / 2; tp2.position.y = 0.025; d.add(tp2); d.visible = false; H.add(d); hb.docs.push(d); });
    // carimbo
    hb.car = grp(); hb.car.add(cyl(0.45, 0.5, 0.25, P.flo, 0, 0.12, 0, 18)); hb.car.add(cyl(0.12, 0.14, 0.7, P.madeiraEsc, 0, 0.6, 0, 10)); hb.car.add(sph(0.22, P.madeiraEsc, 0, 1.0, 0, 10)); H.add(hb.car); hb.car.visible = false;
    hb.tinta = placa(1.3, 0.5, tex(520, 200, (g, w, h) => { g.strokeStyle = "#2F7A3F"; g.lineWidth = 12; rr(g, 12, 12, w - 24, h - 24, 30); g.stroke(); txt(g, "HABILITADA", w / 2, h / 2 + 4, 84, "#2F7A3F", 700); })); hb.tinta.rotation.x = -Math.PI / 2; hb.tinta.rotation.z = 0.12; H.add(hb.tinta); hb.tinta.visible = false;
    const pl = planta(1.5); pl.position.set(-5, 0, -3); H.add(pl); const luz = new THREE.PointLight(0xFFE7B8, 8, 12, 1.5); luz.position.set(0, 4.4, 1.5); H.add(luz);
  }

  // ---------- homologacao: documento grande e carimbo na praca da prefeitura
  const hm = {}; { const A = R.cidade; hm.doc = grp(0, 0.2, 6.3); A.add(hm.doc); hm.doc.add(box(4.4, 0.08, 5.6, 0xFFFFFF, 0, 0, 0));
    const t = tex(640, 820, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#243D32"; g.fillRect(0, 0, w, 130); txt(g, "RESULTADO", w / 2, 66, 64, "#FFFFFF", 700); g.fillStyle = "#C9D1CC"; for (let k = 0; k < 7; k++) g.fillRect(60, 190 + k * 50, k % 3 === 2 ? 300 : 520, 18); });
    const p = placa(4.4, 5.6, t); p.rotation.x = -Math.PI / 2; p.position.y = 0.05; hm.doc.add(p); hm.doc.visible = false;
    hm.tinta = placa(4.0, 2.0, tex(800, 400, (g, w, h) => { g.strokeStyle = "#2F7A3F"; g.lineWidth = 18; rr(g, 16, 16, w - 32, h - 32, 50); g.stroke(); txt(g, "HOMOLOGADO", w / 2, 150, 104, "#2F7A3F", 700); txt(g, "R$ 426.000", w / 2, 290, 96, "#2F7A3F", 700); })); hm.tinta.rotation.x = -Math.PI / 2; hm.tinta.rotation.z = -0.08; hm.tinta.position.set(0, 0.32, 6.2); A.add(hm.tinta); hm.tinta.visible = false;
    hm.car = grp(); hm.car.add(cyl(1.4, 1.5, 0.6, P.flo, 0, 0.3, 0, 22)); hm.car.add(cyl(0.3, 0.35, 2.0, P.madeiraEsc, 0, 1.6, 0, 12)); hm.car.add(sph(0.6, P.madeiraEsc, 0, 2.8, 0, 12)); A.add(hm.car); hm.car.visible = false;
  }

  // ===== #2: documento inabilitado na mesa do pregoeiro e certidao FGTS flutuando na arena =====
  const ar2 = {}; { const D = R.arena;
    ar2.doc = grp(0, 1.12, -5.95); D.add(ar2.doc); ar2.doc.add(box(1.2, 0.02, 0.85, 0xFFFFFF, 0, 0, 0));
    const dt = tex(480, 340, (g, w, h) => { g.fillStyle = "#FFFFFF"; g.fillRect(0, 0, w, h); g.fillStyle = "#C9D1CC"; for (let k = 0; k < 6; k++) g.fillRect(40, 40 + k * 44, k % 3 === 2 ? 220 : 400, 16); });
    const dp = placa(1.2, 0.85, dt); dp.rotation.x = -Math.PI / 2; dp.position.y = 0.02; ar2.doc.add(dp);
    ar2.selo = placa(1.0, 0.36, tex(520, 180, (g, w, h) => { g.strokeStyle = "#E0453A"; g.lineWidth = 14; rr(g, 10, 10, w - 20, h - 20, 26); g.stroke(); txt(g, "INABILITADA", w / 2, h / 2 + 4, 62, "#E0453A", 700); }));
    ar2.selo.rotation.x = -Math.PI / 2; ar2.selo.rotation.z = 0.12; ar2.selo.position.y = 0.035; ar2.doc.add(ar2.selo); ar2.doc.visible = false;
    ar2.fgtsTex = tex(600, 760, () => {}); ar2.fgts = placa(1.6, 2.03, ar2.fgtsTex); ar2.fgts.position.set(0, 2.9, -3.6); D.add(ar2.fgts); ar2.fgts.visible = false; }
  function pintaCertidao(t_, nome, nivel, estado) { retex(t_, (g, w, h) => { g.fillStyle = "#FFFFFF"; rr(g, 6, 6, w - 12, h - 12, 36); g.fill(); g.fillStyle = "#243D32"; rr(g, 6, 6, w - 12, 150, 36); g.fill(); g.fillRect(6, 100, w - 12, 56);
      txt(g, "CERTIDÃO", w / 2, 58, 40, "#B8C5BC", 600); txt(g, nome, w / 2, 112, nome.length > 9 ? 50 : 62, "#FFFFFF", 700);
      const cor = estado === "vencida" ? "#E0453A" : (nivel < 0.2 ? "#E0A33A" : "#3E8E4F"); const bx = w * 0.3, bw = w * 0.4, by = 210, bh = h - 400;
      g.fillStyle = "#D8E0D9"; rr(g, bx + bw * 0.3, by - 22, bw * 0.4, 30, 8); g.fill(); g.strokeStyle = "#59616E"; g.lineWidth = 10; rr(g, bx, by, bw, bh, 22); g.stroke();
      const fh = Math.max(0, Math.min(1, nivel)) * (bh - 24); g.fillStyle = cor; rr(g, bx + 12, by + bh - 12 - fh, bw - 24, Math.max(fh, 1), 12); g.fill();
      txt(g, estado === "vencida" ? "VENCIDA" : (estado === "ok" ? "VÁLIDA" : (estado === "atual" ? "ATUALIZADA" : "")), w / 2, h - 120, 52, cor, 700); }); }

  // ===== #2: a torre da habilitacao (quatro andares em corte) =====
  const tr = { andares: [], certs: [] }; { const T = R.torre; const FH = 3.3, LW = 8.4, LD = 4.6;
    const piso = box(30, 0.3, 24, 0x16201B, 0, -0.15, 0); T.add(piso);
    for (let x = -14; x <= 14; x += 1.5) T.add(box(0.03, 0.01, 24, P.lim, x, 0.006, 0, { transparent: true, opacity: 0.18 }));
    const nomes = ["JURÍDICA", "TÉCNICA", "FISCAL E TRABALHISTA", "ECONÔMICO-FINANCEIRA"], pergs = ["Existe e pode fazer isso?", "Já fez isso antes?", "Está em dia?", "Aguenta o contrato?"];
    for (let i = 0; i < 4; i++) { const y = i * FH; const g = grp(0, y, 0); T.add(g);
      g.add(box(LW, 0.24, LD, 0x2A3530, 0, -0.12, 0)); // laje (topo em y)
      g.add(box(LW, FH - 0.02, 0.2, [0x1E2A24, 0x22302A, 0x1E2A24, 0x22302A][i], 0, FH / 2, -LD / 2 + 0.1)); // fundo
      for (const sx of [-1, 1]) g.add(box(0.2, FH - 0.02, LD, 0x26332D, sx * (LW / 2 - 0.1), FH / 2, 0));
      const fita = box(LW + 0.02, 0.07, 0.07, P.lim, 0, -0.12, LD / 2 + 0.03, { emissive: P.lim, emissiveIntensity: 0.15 }); g.add(fita);
      const rot = placa(4.6, 0.9, tex(920, 180, (gg, w, h) => { gg.fillStyle = "rgba(16,18,24,0.0)"; gg.fillRect(0, 0, w, h); txt(gg, String(i + 1), 70, 92, 110, "#A8F27A", 700); txt(gg, nomes[i], 150, 64, nomes[i].length > 16 ? 50 : 62, "#F4F6F9", 700, "left"); txt(gg, pergs[i], 150, 138, 44, "#B8C5BC", 500, "left"); }));
      rot.position.set(-1.6, FH - 0.62, -LD / 2 + 0.215); g.add(rot);
      const luz = new THREE.PointLight(0xC8F7A8, 0, 7, 1.6); luz.position.set(0, FH - 0.5, 0.8); g.add(luz);
      const veu = new THREE.Mesh(new THREE.PlaneGeometry(LW - 0.4, FH - 0.3), basic(0x0B0F0D, { transparent: true, opacity: 0 })); veu.position.set(0, FH / 2, LD / 2 + 0.12); g.add(veu);
      tr.andares.push({ g, fita, luz, y, veu }); }
    T.add(box(LW, 0.24, LD, 0x2A3530, 0, 4 * FH - 0.12, 0));
    // andar 1: contrato social x edital
    { const g = tr.andares[0].g; const card = (titulo, linha, x, rot) => { const c = placa(2.3, 1.6, tex(690, 480, (gg, w, h) => { gg.fillStyle = "#FFFFFF"; rr(gg, 4, 4, w - 8, h - 8, 26); gg.fill(); gg.fillStyle = "#243D32"; rr(gg, 4, 4, w - 8, 96, 26); gg.fill(); gg.fillRect(4, 60, w - 8, 40); txt(gg, titulo, w / 2, 54, 46, "#FFFFFF", 700); gg.fillStyle = "#D8E0D9"; for (let k = 0; k < 3; k++) gg.fillRect(40, 140 + k * 40, k === 2 ? 300 : 600, 16); gg.fillStyle = "#E1F4D4"; rr(gg, 30, 290, w - 60, 140, 18); gg.fill(); txt(gg, "OBJETO", 60, 326, 30, "#243D32", 700, "left"); txt(gg, linha, 60, 386, 34, "#101218", 600, "left"); })); c.position.set(x, 1.5, 0.2); c.rotation.y = rot; g.add(c); return c; };
      tr.jc = card("CONTRATO SOCIAL", "Comércio de equipamentos de informática", -1.85, 0.12); tr.je = card("EDITAL", "Fornecimento de computadores", 1.85, -0.12);
      tr.jlink = box(1.2, 0.08, 0.08, P.lim, 0, 1.25, 0.4, { emissive: P.lim, emissiveIntensity: 1.0 }); g.add(tr.jlink);
      tr.jok = placa(0.62, 0.62, tex(160, 160, (gg) => { gg.fillStyle = "#A8F27A"; gg.beginPath(); gg.arc(80, 80, 74, 0, 6.3); gg.fill(); gg.strokeStyle = "#101218"; gg.lineWidth = 16; gg.beginPath(); gg.moveTo(44, 84); gg.lineTo(70, 110); gg.lineTo(118, 52); gg.stroke(); })); tr.jok.position.set(0, 1.78, 0.45); g.add(tr.jok); }
    // andar 2: atestados e a barra dos 50%
    { const g = tr.andares[1].g; tr.at = []; for (let k = 0; k < 3; k++) { const a = grp(-2.45, 0.9 + k * 0.03, 0.6); a.add(box(1.1, 0.02, 1.4, 0xFFFFFF, 0, 0, 0)); const ap = placa(1.1, 1.4, tex(330, 420, (gg, w, h) => { gg.fillStyle = "#FFFFFF"; gg.fillRect(0, 0, w, h); gg.fillStyle = "#243D32"; gg.fillRect(0, 0, w, 70); txt(gg, "ATESTADO", w / 2, 38, 36, "#FFFFFF", 700); gg.fillStyle = "#C9D1CC"; for (let j = 0; j < 6; j++) gg.fillRect(28, 100 + j * 40, j % 3 === 2 ? 140 : 270, 14); })); ap.rotation.x = -Math.PI / 2; ap.position.y = 0.02; a.add(ap); a.rotation.y = (k - 1) * 0.12; g.add(a); tr.at.push(a); }
      g.add(box(1.4, 0.06, 1.7, P.madeira, -2.45, 0.86, 0.6)); for (const [x, z] of [[-3.05, 0.0], [-1.85, 0.0], [-3.05, 1.2], [-1.85, 1.2]]) g.add(box(0.08, 0.83, 0.08, P.madeiraEsc, x, 0.415, z));
      g.add(box(4.2, 0.42, 0.22, 0x101218, 0.9, 1.6, -0.6)); tr.bar = box(4.0, 0.3, 0.08, P.lim, 0.9, 1.6, -0.46, { emissive: P.lim, emissiveIntensity: 0.6 }); tr.bar.geometry.translate(2.0, 0, 0); tr.bar.position.x = -1.1; g.add(tr.bar);
      g.add(box(0.05, 0.9, 0.3, 0xF4F6F9, 0.9, 1.6, -0.45, { emissive: 0xF4F6F9, emissiveIntensity: 0.4 }));
      const lm = placa(2.4, 0.5, tex(480, 100, (gg, w, h) => { txt(gg, "EXIGÊNCIA ATÉ 50%", w / 2, h / 2, 44, "#F4F6F9", 700); })); lm.position.set(0.9, 2.3, -0.44); g.add(lm);
      const lq = placa(3.6, 0.42, tex(720, 84, (gg, w, h) => { txt(gg, "QUANTIDADE JÁ FORNECIDA", w / 2, h / 2, 40, "#B8C5BC", 600); })); lq.position.set(0.9, 1.05, -0.44); g.add(lq); }
    // andar 3: certidoes como baterias
    { const g = tr.andares[2].g; const C = [["CNPJ", 1.0, "ok"], ["FEDERAL", 0.8, "ok"], ["ESTADUAL", 0.62, "ok"], ["MUNICIPAL", 0.7, "ok"], ["FGTS", 0.08, "ok"], ["TRABALHISTA", 0.88, "ok"]];
      C.forEach(([n, lv, e], k) => { const t_ = tex(400, 620, () => {}); pintaCertidao(t_, n, lv, e); const p = placa(1.08, 1.67, t_); p.position.set(-2.75 + k * 1.1, 1.35, 0.3 - Math.abs(k - 2.5) * 0.12); p.rotation.y = (2.5 - k) * 0.06; g.add(p); tr.certs.push({ p, t_, n, lv, e }); }); }
    // andar 4: balanca
    { const g = tr.andares[3].g; g.add(box(1.4, 0.16, 1.0, 0x3A4048, 0, 0.08, 0.2)); g.add(cyl(0.08, 0.1, 2.0, 0xC9CDD6, 0, 1.08, 0.2, 10)); tr.viga = grp(0, 2.1, 0.2); g.add(tr.viga); tr.viga.add(box(4.6, 0.12, 0.14, 0xC9CDD6, 0, 0, 0));
      tr.pratos = []; for (const sx of [-1, 1]) { const pg = grp(sx * 2.1, 0, 0); tr.viga.add(pg); pg.add(cyl(0.015, 0.015, 0.75, 0x8A939E, 0, -0.37, 0, 6)); const pr = grp(0, -0.8, 0); pg.add(pr); pr.add(cyl(0.7, 0.6, 0.08, 0xC9CDD6, 0, 0, 0, 18));
        const bl = box(1.0, 0.7, 0.7, sx < 0 ? P.flo : 0x3E8E4F, 0, 0.39, 0); pr.add(bl); const lb = placa(0.98, 0.6, tex(300, 180, (gg, w, h) => { txt(gg, sx < 0 ? "CONTRATO" : "PATRIMÔNIO", w / 2, 60, 40, "#F4F6F9", 700); txt(gg, sx < 0 ? "R$ 480 mil" : "da empresa", w / 2, 128, sx < 0 ? 48 : 36, "#A8F27A", 700); })); lb.position.set(0, 0.39, 0.36); pr.add(lb); tr.pratos.push({ pg, pr }); }
      const mn = placa(3.6, 0.6, tex(720, 120, (gg, w, h) => { txt(gg, "MÍNIMO, SE PEDIDO: 10% = R$ 48 mil", w / 2, h / 2, 40, "#F4F6F9", 700); })); mn.position.set(0, 0.36, 1.75); g.add(mn); }
    tr.selo = placa(4.2, 1.3, tex(840, 260, (g, w, h) => { g.fillStyle = "rgba(16,18,24,0.9)"; rr(g, 6, 6, w - 12, h - 12, 50); g.fill(); g.strokeStyle = "#A8F27A"; g.lineWidth = 14; rr(g, 12, 12, w - 24, h - 24, 46); g.stroke(); txt(g, "HABILITADA", w / 2, h / 2 + 6, 120, "#A8F27A", 700); }));
    tr.selo.position.set(0, 6.6, 3.2); tr.selo.visible = false; T.add(tr.selo);
    const amb = new THREE.PointLight(0xA8F27A, 10, 30, 1.6); amb.position.set(0, 8, 8); T.add(amb); }

  // ===== #2: linha do tempo da diligencia e calendario da ME e EPP =====
  const ln = {}; { const L = R.linha; L.add(box(34, 0.3, 30, 0x16201B, 0, -0.15, 0));
    for (let x = -16; x <= 16; x += 1.5) L.add(box(0.03, 0.01, 30, P.lim, x, 0.006, 0, { transparent: true, opacity: 0.16 }));
    L.add(box(11, 0.12, 0.3, 0x59616E, 0, 0.06, 0));
    const marco = (x, a, b, cor) => { L.add(box(0.12, 1.2, 0.12, cor, x, 0.6, 0, { emissive: cor, emissiveIntensity: 0.5 })); L.add(sph(0.22, cor, x, 0.15, 0, 10, { emissive: cor, emissiveIntensity: 0.6 }));
      const p = placa(2.4, 0.8, tex(480, 160, (g, w, h) => { txt(g, a, w / 2, 56, 46, "#F4F6F9", 700); txt(g, b, w / 2, 118, 40, "#B8C5BC", 500); })); p.position.set(x, 1.65, 0.05); L.add(p); };
    marco(-2.2, "PROPOSTAS", "entregues em 10/11", 0xF4F6F9); marco(1.0, "FGTS VENCEU", "em 12/11", 0xFF6B5B);
    ln.certTex = tex(400, 620, () => {}); ln.cert = placa(1.3, 2.0, ln.certTex); ln.cert.position.set(1.0, 3.4, 0.1); L.add(ln.cert);
    ln.seta = grp(2.9, 3.4, 0.1); { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.4, 10), basic(P.lim)); c.rotation.z = Math.PI / 2; ln.seta.add(c); const cn = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.4, 12), basic(P.lim)); cn.rotation.z = Math.PI / 2; cn.position.x = -0.85; ln.seta.add(cn); }
    ln.setaTxt = placa(2.2, 0.5, tex(440, 100, (g, w, h) => { txt(g, "DILIGÊNCIA", w / 2, h / 2, 50, "#A8F27A", 700); })); ln.setaTxt.position.set(3.05, 3.95, 0.1); L.add(ln.seta); L.add(ln.setaTxt);
    // documento novo: contorno pontilhado e X
    ln.novo = grp(4.6, 2.3, 0.1); L.add(ln.novo); { const pts = []; const w = 1.2, h = 1.6; for (const [x, y] of [[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2], [-w / 2, -h / 2]]) pts.push(new THREE.Vector3(x, y, 0)); const lg = new THREE.BufferGeometry().setFromPoints(pts); const ll = new THREE.Line(lg, new THREE.LineDashedMaterial({ color: 0xF4F6F9, dashSize: 0.12, gapSize: 0.08 })); ll.computeLineDistances(); ln.novo.add(ll);
      const nt = placa(1.6, 0.5, tex(400, 120, (g, W, H) => { txt(g, "DOCUMENTO", W / 2, 40, 40, "#B8C5BC", 700); txt(g, "NOVO", W / 2, 92, 40, "#B8C5BC", 700); })); nt.position.set(0, -1.15, 0); ln.novo.add(nt); }
    ln.x = grp(4.6, 2.3, 0.2); for (const r of [0.78, -0.78]) { const b = box(1.6, 0.22, 0.1, P.erro, 0, 0, 0, { emissive: P.erro, emissiveIntensity: 0.7 }); b.rotation.z = r; ln.x.add(b); } ln.x.visible = false; L.add(ln.x);
    // calendario (atras, em z -14)
    const cal = grp(0, 0, -14); L.add(cal); ln.dias = [];
    for (let r = 0; r < 2; r++) for (let c = 0; c < 5; c++) { const d = box(1.05, 0.12, 1.05, 0x26332D, -2.4 + c * 1.2, 0.06, -0.7 + r * 1.3); cal.add(d); const n = placa(0.8, 0.8, tex(160, 160, (g) => { txt(g, String(r * 5 + c + 1), 80, 84, 96, "#F4F6F9", 700); })); n.rotation.x = -Math.PI / 2; n.position.set(-2.4 + c * 1.2, 0.135, -0.7 + r * 1.3); cal.add(n); ln.dias.push(d); }
    ln.calRot = placa(4.8, 0.9, tex(960, 180, (g, w, h) => { txt(g, "5 dias úteis", w * 0.28, h / 2, 70, "#A8F27A", 700); txt(g, "+ 5", w * 0.78, h / 2, 70, "#F2C94C", 700); })); ln.calRot.position.set(0, 1.4, -1.8); ln.calRot.rotation.x = -0.4; cal.add(ln.calRot);
    ln.badge = placa(1.8, 0.8, tex(360, 160, (g, w, h) => { g.fillStyle = "#A8F27A"; rr(g, 4, 4, w - 8, h - 8, 70); g.fill(); txt(g, "ME / EPP", w / 2, h / 2 + 4, 66, "#101218", 700); })); ln.badge.position.set(0, 0.45, 2.7); ln.badge.rotation.x = -0.9; ln.cal = cal; cal.add(ln.badge);
    const amb = new THREE.PointLight(0xA8F27A, 10, 30, 1.6); amb.position.set(0, 7, 6); L.add(amb); const amb2 = new THREE.PointLight(0xA8F27A, 8, 20, 1.6); amb2.position.set(0, 6, -10); L.add(amb2); }

  // ---------- particulas (confete limao e branco) e moedas de lance
  const conf = new THREE.InstancedMesh(new THREE.BoxGeometry(0.22, 0.05, 0.14), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.6 }), 160); scene.add(conf); conf.frustumCulled = false;
  { const cores = [new THREE.Color(P.lim), new THREE.Color(P.sup), new THREE.Color(P.flo2), new THREE.Color(P.ouro)]; for (let i = 0; i < 160; i++) conf.setColorAt(i, cores[i % 4]); }
  const dummy = new THREE.Object3D(); const hidden = new THREE.Matrix4().makeScale(0, 0, 0); const CR = []; { const rc = mulberry32(9); for (let k = 0; k < 160; k++) CR.push([rc(), rc(), rc()]); }

  // ---------- camera (mesmo formato do cena_parte3: [t, set, px,py,pz, lx,ly,lz, fov, cut, mvx,mvy,mvz, dur])
  const cam = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.3, 400);
  const CAMK = (G.cam3 || [[0, "cidade", 0, 5, 30, 0, 4, 0, 45, 1]]).map(k => ({ t: k[0], set: k[1], p: new THREE.Vector3(k[2], k[3], k[4]), l: new THREE.Vector3(k[5], k[6], k[7]), fov: k[8], cut: !!k[9], mv: new THREE.Vector3(k[10] || 0, k[11] || 0, k[12] || 0), dur: k[13] || 1.6 }));
  const off = (s) => new THREE.Vector3(...SETS[s]);
  function camAt3(t) { let st = CAMK[0], pos = st.p.clone().add(off(st.set)), look = st.l.clone().add(off(st.set)), fov = st.fov, tk = st.t, mv = st.mv, setA = st.set;
    for (let i = 1; i < CAMK.length; i++) { const k = CAMK[i]; if (t < k.t) break; const p2 = k.p.clone().add(off(k.set)), l2 = k.l.clone().add(off(k.set));
      if (k.cut) { pos = p2; look = l2; fov = k.fov; } else { const s = smooth((t - k.t) / k.dur); pos.lerp(p2, s); look.lerp(l2, s); fov = lerp(fov, k.fov, s); } tk = k.t; mv = k.mv; setA = k.set; }
    const dt = t - tk; pos = pos.clone().add(mv.clone().multiplyScalar(dt)); look = look.clone().add(mv.clone().multiplyScalar(dt * 0.6));
    pos.x += Math.sin(t * 0.9) * 0.02; pos.y += Math.sin(t * 1.3 + 1) * 0.015;
    cam.position.copy(pos); cam.lookAt(look); cam.fov = fov; cam.updateProjectionMatrix();
    const o = off(setA); key.position.set(o.x + 12, o.y + 22, o.z + 16); key.target.position.copy(look); key.target.updateMatrixWorld(); return setA; }

  const pop = (t, t0, d = 0.5) => { if (t < t0) return 0; const p = clamp01((t - t0) / d) - 1; const s = 1.7; return 1 + (s + 1) * p * p * p + s * p * p; };
  const ev = (n) => (EV[n] === undefined ? 1e9 : EV[n]);

  function renderAt(t) {
    const setA = camAt3(t); scene.background = BG[BGSET[setA]];
    const arenaLike = BGSET[setA] === "arena";
    key.intensity = arenaLike ? 1.3 : 2.5; hemi.intensity = arenaLike ? 0.55 : 1.25; rim.intensity = arenaLike ? 1.2 : 0.6; renderer.toneMappingExposure = arenaLike ? 1.15 : 1.05;

    // --- cidade: bandeira, pedestres, caixas
    { const A = R.cidade; const b = A.userData.band, pa = b.geometry.attributes.position, base = b.userData.base; for (let i = 0; i < pa.count; i++) { const x = base[i * 3]; pa.array[i * 3 + 2] = Math.sin(x * 2.4 - t * 5) * 0.12 * (x + 1.2); } pa.needsUpdate = true; b.geometry.computeVertexNormals();
      A.userData.pedestres.forEach((p, i) => { p.visible = t < 30; const u = ((t * 0.04 + i * 0.21) % 1); const dir = i % 2 ? 1 : -1; p.position.set(-24 + u * 48 * (dir > 0 ? 1 : -1) + (dir < 0 ? 48 : 0), 0, 10.2 + (i % 3) * 0.5); p.rotation.y = dir > 0 ? Math.PI / 2 : -Math.PI / 2; anima(p, t + i, "andando"); });
      A.userData.caixas.forEach((c, i) => { const k = pop(t, ev("caixas") + i * 0.07, 0.4); c.scale.setScalar(Math.max(0.001, k)); c.visible = k > 0.01; });
      const h0 = ev("homolog"); hm.doc.visible = t >= h0 - 0.6; hm.doc.position.y = 0.2 + (1 - smooth(lin(t, h0 - 0.6, h0 - 0.1))) * 3;
      hm.car.visible = t >= h0 - 0.5 && t < h0 + 2.2; { const d = t - h0; const y = d < 0 ? lerp(8, 0.1, smooth(lin(t, h0 - 0.5, h0))) : (d < 0.25 ? 0.1 : lerp(0.1, 8, smooth(lin(t, h0 + 0.6, h0 + 1.6)))); hm.car.position.set(0, y + 0.2, 6.2); }
      hm.tinta.visible = t >= h0; }

    // --- predio: telas com numero, interrogacoes, figurantes
    salas.forEach((s, i) => { const tn = ev("numeros") + i * 0.18; if (s.tt.userData.n !== (t >= tn)) { s.tt.userData.n = (t >= tn); if (t >= tn) telaNumero(s, i + 1, i === 6 ? "#A8F27A" : "#F4F6F9"); else retex(s.tt, (g, w, h) => { g.fillStyle = "#0E1A14"; g.fillRect(0, 0, w, h); txt(g, "edital", w / 2, h / 2, 60, "#59616E", 500); }); }
      const qk = pop(t, ev("interroga") + i * 0.12, 0.4); s.q.visible = qk > 0.01 && t < ev("interroga") + 6; s.q.scale.setScalar(Math.max(0.001, qk)); s.q.position.y = 2.55 + Math.sin(t * 2 + i) * 0.06;
      anima(s.p, t + i, "digitando"); exprAt(s.p, i === 6 ? [[0, "foco"]] : [[0, "neutro"]], t); });

    // --- escritorio
    { exprAt(prot, G.expr, t); anima(prot, t, kf(G.prot_modo, t, 0, 0.01) > 0.5 ? "fala" : "digitando");
      const ab = smooth(lin(t, ev("edital_abre"), ev("edital_abre") + 1.0)); const fecha = smooth(lin(t, ev("edital_fecha"), ev("edital_fecha") + 0.8));
      docs.forEach((d, i) => { const k = smooth(lin(ab * (1 - fecha), i * 0.12, i * 0.12 + 0.64)); const col = i % 2, row = Math.floor(i / 2);
        d.position.set(lerp(-0.9, -2.0 + col * 1.2, k), lerp(0.82 + i * 0.035, 3.05 - row * 0.95, k), lerp(-1.05, -1.6, k)); d.rotation.x = lerp(0, Math.PI / 2, k); d.rotation.y = lerp(0, (col ? -1 : 1) * 0.12, k); d.scale.setScalar(lerp(1, 0.72, k)); });
      const dias = kf(G.cal, t, 0, 0.9); desenhaCal(dias);
      if (telaEsc.userData.m !== (t >= ev("tela_proposta"))) { telaEsc.userData.m = (t >= ev("tela_proposta")); desenhaTelaEsc(t >= ev("tela_proposta") ? "proposta" : "edital"); }
      const e0 = ev("envelope"); envelope.visible = t >= e0 && t < e0 + 2.4; if (envelope.visible) { const u = smooth(lin(t, e0, e0 + 2.2)); envelope.position.set(lerp(0.9, 3.6, u), 0.86 + Math.sin(u * Math.PI) * 2.2 + u * 1.6, lerp(-0.9, -3.6, u)); envelope.rotation.set(u * 0.6, u * 3.0, u * 0.4); envelope.scale.setScalar(1 - u * 0.6); } }

    // --- arena: placar, pulpitos, lances, pregoeiro
    { if (setA === "arena" || Math.abs(t - (placarTex.userData.t || -9)) > 0.5) { desenhaPlacar(t); placarTex.userData.t = t; }
      anima(pregoeiro, t, kf(G.preg_modo, t, 0, 0.01) > 0.5 ? "fala" : "parado"); exprAt(pregoeiro, [[0, "foco"]], t);
      const L = G.lances || []; pulpitos.forEach(pu => { let k = 0; for (const [tk, idx] of L) if (idx === pu.i + 1 && t >= tk) k = Math.max(k, clamp01(1 - (t - tk) / 0.7)); pu.luz.material.emissiveIntensity = 0.2 + 2.5 * k; pu.g.position.y = k * 0.08;
        pu.ck.visible = t >= ev("confere") + pu.i * 0.15 && t < ev("confere") + 3.5; pu.ck.scale.setScalar(Math.max(0.001, pop(t, ev("confere") + pu.i * 0.15, 0.35)));
        if (pu.i === 2) { exprAt(pu.pess, G.expr, t); anima(pu.pess, t, "parado"); } else anima(pu.pess, t + pu.i, "parado");
        const des = pu.i === 0 && t >= ev("arena_fora"); pu.g.visible = !des; pu.masc.position.y = pu.masc.userData.y0 + Math.sin(t * 1.8 + pu.i) * 0.05; });
      let fi = 0; for (const [tk, idx] of L) { const d = t - tk; if (d < 0 || d > 0.55 || fi >= feixes.length) continue; const pu = pulpitos[idx - 1]; const a = new THREE.Vector3(); pu.g.getWorldPosition(a); a.y += 1.3; const b = new THREE.Vector3(450, 4.7, -9.4); const u = smooth(d / 0.45); const p = a.clone().lerp(b, u); const f = feixes[fi++]; f.visible = true; const tail = a.clone().lerp(b, Math.max(0, u - 0.35)); const mid = p.clone().add(tail).multiplyScalar(0.5); f.position.copy(mid).sub(off("arena")); const len = p.distanceTo(tail); f.scale.set(1, Math.max(0.01, len), 1); f.lookAt(p); f.rotateX(Math.PI / 2); f.position.copy(mid).sub(off("arena")); f.material.opacity = 0.95 * (1 - smooth(lin(d, 0.4, 0.55))); }
      for (; fi < feixes.length; fi++) feixes[fi].visible = false; }

    // --- podio
    if (G.podio2) { anima(podio.f2, t + 1, "parado"); podio.fv.userData.salto = 0; anima(podio.fv, t + 2, t >= ev("fv_festa") && t < ev("fv_festa") + 3.5 ? "comemora" : "parado"); podio.f1.visible = false; podio.m1.visible = false; podio[3].g.visible = false; podio.faixa.material.opacity = 0;
      for (const k of [1, 2]) { podio[k].g.scale.set(1, 1, 1); podio[k].g.visible = true; podio[k].g.position.y = 0.012; podio[k].g.rotation.z = 0; }
      if (podio[1].t.userData.p2 !== (t >= ev("p2_sobe"))) { const nv = t >= ev("p2_sobe"); podio[1].t.userData.p2 = nv; retex(podio[1].t, podio[1].t.userData.pinta(1, nv ? "R$ 438 mil" : "R$ 426 mil")); retex(podio[2].t, podio[2].t.userData.pinta(2, nv ? "" : "R$ 438 mil")); }
      const cai = smooth(lin(t, ev("p2_cai"), ev("p2_cai") + 1.0)); podio.f2.position.set(0, podio[1].h + Math.sin(cai * Math.PI) * 0.6 - cai * 3.2, -cai * 1.6); podio.f2.rotation.x = -cai * 0.9; podio.f2.visible = cai < 0.97;
      podio.m2.position.set(podio.f2.position.x, podio.f2.position.y + 2.45, 0.3); podio.m2.visible = podio.f2.visible;
      const sb = smooth(lin(t, ev("p2_sobe"), ev("p2_sobe") + 1.4)); podio.fv.position.set(lerp(-2.7, 0, sb), lerp(podio[2].h, podio[1].h, sb) + Math.sin(sb * Math.PI) * 1.4 + (podio.fv.userData.salto || 0), 0); exprAt(podio.fv, G.expr, t);
      podio.x.visible = inRanges(G.podio_x, t, 0.05) > 0.5; podio.x.position.set(0, 4.4, 1.2); podio.x.scale.setScalar(Math.max(0.001, pop(t, (G.podio_x || [[1e9]])[0][0], 0.35))); }
    else { anima(podio.f1, t, "parado"); anima(podio.f2, t + 1, smooth(lin(t, ev("troca"), ev("troca") + 1.4)) > 0.99 ? "comemora" : "parado"); anima(podio.fv, t + 2, kf(G.fv_modo, t, 0, 0.01) > 1.5 ? "comemora" : (kf(G.fv_modo, t, 0, 0.01) > 0.5 ? "maos_cabeca" : "parado"));
      const sobe = smooth(lin(t, ev("podio"), ev("podio") + 1.2)); for (const k of [1, 2, 3]) { const p = podio[k]; const atraso = (3 - k) * 0.25; const s = smooth(lin(t, ev("podio") + atraso, ev("podio") + atraso + 0.9)); p.g.scale.set(1, Math.max(0.001, s), 1); p.g.visible = s > 0.03; }
      const cai = smooth(lin(t, ev("cai"), ev("cai") + 1.0)); podio[1].g.position.y = -cai * 3.0; podio[1].g.rotation.z = cai * 0.18;
      const troca = smooth(lin(t, ev("troca"), ev("troca") + 1.4));
      const top = (k) => podio[k].h * smooth(lin(t, ev("podio") + (3 - k) * 0.25, ev("podio") + (3 - k) * 0.25 + 0.9));
      // f1 no 1o (cai junto), f2 do 2o para o 1o, voce do 3o para o 2o
      podio.f1.position.set(0, top(1) - cai * 3.0, 0); podio.f1.visible = cai < 0.95; podio.f1.rotation.z = cai * 0.3;
      const p2a = new THREE.Vector3(-2.7, top(2), 0), p2b = new THREE.Vector3(0, podio[1].h, 0); const arco = Math.sin(troca * Math.PI) * 1.4;
      podio.f2.position.set(lerp(p2a.x, p2b.x, troca), lerp(p2a.y, p2b.y, troca) + arco, 0);
      podio.fv.position.set(lerp(2.7, -2.7, troca), lerp(top(3), podio[2].h, troca) + arco, 0);
      podio.m1.position.set(podio.f1.position.x, podio.f1.position.y + 2.45, 0.3); podio.m1.visible = podio.f1.visible; podio.m2.position.set(podio.f2.position.x, podio.f2.position.y + 2.45, 0.3);
      if (troca > 0.99) { podio[1].g.position.y = -3 + 3 * smooth(lin(t, ev("troca") + 1.4, ev("troca") + 2.2)); podio[1].g.rotation.z = 0; }
      { const novo = troca > 0.99; if (podio[1].t.userData.novo !== novo) { podio[1].t.userData.novo = novo;
          retex(podio[1].t, podio[1].t.userData.pinta(1, novo ? "R$ 426 mil" : "R$ 399 mil")); retex(podio[2].t, podio[2].t.userData.pinta(2, novo ? "R$ 438 mil" : "R$ 426 mil")); }
        podio[3].g.visible = !novo || t < ev("troca") + 1.0; if (novo) podio[3].g.scale.y = Math.max(0.001, 1 - smooth(lin(t, ev("troca") + 1.4, ev("troca") + 2.0))); }
      for (const f of [podio.f1, podio.f2, podio.fv]) f.position.y += f.userData.salto || 0; exprAt(podio.fv, G.expr, t);
      const fx = inRanges(G.faixa, t, 0.4); podio.faixa.material.opacity = 0.32 * fx; podio.faixa.scale.y = 0.2 + fx;
      podio.x.visible = inRanges(G.podio_x, t, 0.05) > 0.5; podio.x.scale.setScalar(Math.max(0.001, pop(t, (G.podio_x || [[1e9]])[0][0], 0.35))); }

    // --- raio-x
    { const ab = smooth(lin(t, ev("rx_abre"), ev("rx_abre") + 1.0)); rx.ed.lado.rotation.y = -ab * 1.9; rx.pr.lado.rotation.y = -ab * 1.9;
      const so = smooth(lin(t, ev("rx_sobe"), ev("rx_sobe") + 0.8)); rx.eE.scale.setScalar(Math.max(0.001, pop(t, ev("rx_ed"), 0.4))); rx.eP.scale.setScalar(Math.max(0.001, pop(t, ev("rx_pr"), 0.4)));
      rx.ed.rams.forEach(r => r.position.x = 0.66 + so * 0.0); rx.pr.bord[1].material.opacity = 0.9 * smooth(lin(t, ev("rx_pr"), ev("rx_pr") + 0.3)) * (0.6 + 0.4 * Math.sin(t * 10));
      rx.x.visible = t >= ev("rx_x"); rx.x.scale.setScalar(Math.max(0.001, pop(t, ev("rx_x"), 0.35))); rx.dt.visible = t >= ev("rx_x") + 0.4; rx.dt.scale.setScalar(Math.max(0.001, pop(t, ev("rx_x") + 0.4, 0.35))); }

    // --- habilitacao
    { hb.docs.forEach((d, i) => { const t0 = (G.docs || [])[i] ?? 1e9; d.visible = t >= t0; const u = smooth(lin(t, t0, t0 + 0.6)); d.position.set(lerp(-3 + i * 3, 0.05 + i * 0.12, u), lerp(5.5, 0.86 + i * 0.03, u) + Math.sin(u * Math.PI) * 0.4, lerp(-2.5, 0.1 - i * 0.08, u)); d.rotation.y = lerp(1.2, (i - 1) * 0.08, u); d.rotation.x = 0; });
      const c0 = ev("carimbo"); hb.car.visible = t >= c0 - 0.5 && t < c0 + 1.6; { const d = t - c0; const y = d < 0 ? lerp(3.5, 0.92, smooth(lin(t, c0 - 0.5, c0))) : (d < 0.25 ? 0.92 : lerp(0.92, 3.5, smooth(lin(t, c0 + 0.5, c0 + 1.3)))); hb.car.position.set(0.25, y, 0.2); }
      hb.tinta.visible = t >= c0; hb.tinta.position.set(0.25, 0.97, 0.2); }

    // --- #2: arena (documento inabilitado, certidao FGTS)
    { const i0 = ev("inab"); ar2.doc.visible = t >= i0 - 0.6 && t < ev("inab_fim"); ar2.doc.position.y = 1.12 + (1 - smooth(lin(t, i0 - 0.6, i0 - 0.1))) * 2.5; ar2.selo.visible = t >= i0; ar2.selo.scale.setScalar(Math.max(0.001, pop(t, i0, 0.3)));
      const f0 = ev("fgts_abre"); ar2.fgts.visible = t >= f0 && t < ev("fgts_fecha"); ar2.fgts.scale.setScalar(Math.max(0.001, pop(t, f0, 0.45))); ar2.fgts.position.y = 2.9 + Math.sin(t * 1.4) * 0.05;
      const vencA = t >= ev("fgts_venc"); if (ar2.fgtsTex.userData.v !== vencA) { ar2.fgtsTex.userData.v = vencA; pintaCertidao(ar2.fgtsTex, "FGTS", vencA ? 0.02 : 0.08, vencA ? "vencida" : "ok"); } }
    // --- #2: torre
    { const okT = [ev("t_jur"), ev("t_tec"), ev("t_fis"), ev("t_eco")]; const tudo = ev("torre_ok");
      tr.andares.forEach((a, i) => { const k = Math.max(smooth(lin(t, okT[i], okT[i] + 0.5)), smooth(lin(t, tudo + i * 0.15, tudo + i * 0.15 + 0.4))); const alerta = i === 2 && t >= ev("fgts_pisca") && t < tudo ? 0.5 + 0.5 * Math.sin(t * 9) : 0;
        const foco = Math.round(kf(G.torre_foco, t, -1, 0.01)); a.veu.material.opacity = foco >= 0 && foco !== i ? 0.78 : 0; a.veu.visible = a.veu.material.opacity > 0; a.fita.material.emissiveIntensity = 0.15 + 1.6 * k; a.luz.intensity = 6 * k + (foco === i ? 3 : 0); if (alerta) { a.fita.material.emissive.setHex(0xFF6B5B); a.fita.material.emissiveIntensity = 0.4 + 1.6 * alerta; } else a.fita.material.emissive.setHex(P.lim); });
      const j = smooth(lin(t, ev("jur_ok"), ev("jur_ok") + 0.6)); tr.jlink.scale.x = Math.max(0.001, j); tr.jok.visible = t >= ev("jur_ok") + 0.5; tr.jok.scale.setScalar(Math.max(0.001, pop(t, ev("jur_ok") + 0.5, 0.35)));
      tr.at.forEach((a, k) => { const t0 = ev("at") + k * 0.35; a.visible = t >= t0; a.position.y = 0.9 + k * 0.03 + (1 - smooth(lin(t, t0, t0 + 0.35))) * 1.6; });
      tr.bar.scale.x = Math.max(0.001, 0.62 * smooth(lin(t, ev("barra"), ev("barra") + 1.6)));
      tr.certs.forEach((c, k) => { let lv = c.lv, e = c.e; if (c.n === "FGTS") { if (t >= ev("fgts_recarga")) { lv = 0.08 + 0.9 * smooth(lin(t, ev("fgts_recarga"), ev("fgts_recarga") + 1.0)); e = lv > 0.9 ? "atual" : "ok"; } else if (t >= ev("fgts_venc")) { lv = 0.02; e = "vencida"; } }
        const key = Math.round(lv * 40) + e; if (c.t_.userData.k !== key) { c.t_.userData.k = key; pintaCertidao(c.t_, c.n, lv, e); }
        const t0 = ev("certs") + k * 0.18; c.p.visible = t >= t0; c.p.scale.setScalar(Math.max(0.001, pop(t, t0, 0.4))); if (c.n === "FGTS" && t >= ev("fgts_pisca") && t < ev("fgts_recarga")) c.p.position.y = 1.35 + Math.sin(t * 18) * 0.015; });
      const eq = smooth(lin(t, ev("eco_ok"), ev("eco_ok") + 1.4)); const ang = t < ev("eco_ok") ? 0.22 : 0.22 * (1 - eq) + Math.sin(t * 2) * 0.01 * eq; tr.viga.rotation.z = ang; tr.pratos.forEach(p => p.pg.rotation.z = -ang);
      tr.selo.visible = t >= tudo + 0.7; tr.selo.scale.setScalar(Math.max(0.001, pop(t, tudo + 0.7, 0.45))); }
    // --- #2: linha do tempo e calendario
    { const dil = t >= ev("dil"); const key = dil ? "a" : "v"; if (ln.certTex.userData.k !== key) { ln.certTex.userData.k = key; pintaCertidao(ln.certTex, "FGTS", dil ? 0.98 : 0.02, dil ? "atual" : "vencida"); }
      const s = smooth(lin(t, ev("seta"), ev("seta") + 0.5)); ln.seta.scale.setScalar(Math.max(0.001, s)); ln.setaTxt.visible = s > 0.5; ln.seta.position.x = 2.9 + Math.sin(t * 4) * 0.08 * s;
      ln.x.visible = t >= ev("doc_novo"); ln.x.scale.setScalar(Math.max(0.001, pop(t, ev("doc_novo"), 0.35)));
      ln.dias.forEach((d, k) => { const t0 = (k < 5 ? ev("cal1") : ev("cal2")) + (k % 5) * 0.16; const on = t >= t0; d.material = mat(on ? (k < 5 ? P.lim : 0xF2C94C) : 0x26332D, on ? { emissive: k < 5 ? P.lim : 0xF2C94C, emissiveIntensity: 0.5 } : {}); d.position.y = 0.06 + (on ? Math.max(0, 0.25 * (1 - (t - t0) / 0.3)) : 0); });
      ln.cal.visible = t >= ev("cal_on"); ln.badge.visible = t >= ev("cal_badge"); ln.badge.scale.setScalar(Math.max(0.001, pop(t, ev("cal_badge"), 0.4))); }

    // --- confete (homologacao e habilitada)
    let ci = 0; (G.confete || []).forEach(([t0, set, cx, cy, cz]) => { const dt = t - t0; if (dt < 0 || dt > 3.0) return; const o = off(set); for (let k = 0; k < 80 && ci < 160; k++, ci++) { const [r1, r2, r3] = CR[k]; const y = cy + 5 - dt * (2.0 + r1 * 1.4); if (y < 0.05) { conf.setMatrixAt(ci, hidden); continue; } dummy.position.set(o.x + cx + (r1 - 0.5) * 10 + Math.sin(dt * 3 + k) * 0.4, y, o.z + cz + (r2 - 0.5) * 6); dummy.rotation.set(dt * 4 + k, dt * 3 * r3, k); dummy.scale.set(1, 1, 1); dummy.updateMatrix(); conf.setMatrixAt(ci, dummy.matrix); } });
    for (; ci < 160; ci++) conf.setMatrixAt(ci, hidden); conf.instanceMatrix.needsUpdate = true; if (conf.instanceColor) conf.instanceColor.needsUpdate = true;

    const dio = document.getElementById("dio"); if (dio) dio.classList.toggle("gray", t >= EV.pause_start && t < EV.pause_end);
    renderer.render(scene, cam);
  }
  return { renderAt };
};
