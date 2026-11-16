// Kit de modelos low-poly (v2, nivel das referencias): silo nervurado, galpao com interior, caminhao de suinos com
// rodas, porco com pernas, pessoa com bone e celular, cerca, arvore, caixa d'agua, cancela, lavador, casa, grama.
// Classic script: window.__KIT(THREE) devolve os construtores. Escala: 1 unidade = 1 m. Tudo com sombra.
window.__KIT = function (THREE) {
  const PAL = { creme: 0xF4F0E6, branco: 0xFBFAF6, navy: 0x141B3F, azul: 0x2F4DB8, azulClaro: 0x5B74C9, lav: 0xB48CE4, mag: 0xF55CEB,
    verde: 0x5CE0A6, grama: 0x74C078, grama2: 0x5EA862, grama3: 0x8ACB84, terra: 0xB58B5A, madeira: 0x9C6B3C, metal: 0xCDD3DA, metalEsc: 0x8A939E,
    rosa: 0xF2A6C4, rosaEsc: 0xD98BA8, borracha: 0x2B2F38, vidro: 0xA9D8EC, concreto: 0xD9D6CC, amarelo: 0xF2C94C, laranja: 0xF08A4B,
    telha: 0xC8714D, pele: 0xE8B89A, jeans: 0x2F3E6B, camisa: 0xF4F0E6, jaleco: 0xFBFAF6, macacao: 0x3B6FB6, ciano: 0x5BC6EE, lama: 0x6B4A2B, milho: 0xF2C94C };
  const mats = {};
  function mat(c, extra = {}) { const k = c + JSON.stringify(extra); if (!mats[k]) mats[k] = new THREE.MeshStandardMaterial({ color: c, roughness: 0.85, metalness: 0.0, flatShading: true, ...extra }); return mats[k]; }
  function mesh(geo, c, x = 0, y = 0, z = 0, extra) { const m = new THREE.Mesh(geo, mat(c, extra)); m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true; return m; }
  function box(w, h, d, c, x, y, z, extra) { return mesh(new THREE.BoxGeometry(w, h, d), c, x, y, z, extra); }
  function cyl(rt, rb, h, c, x, y, z, seg = 12, extra) { return mesh(new THREE.CylinderGeometry(rt, rb, h, seg), c, x, y, z, extra); }
  function sph(r, c, x, y, z, seg = 8, extra) { return mesh(new THREE.SphereGeometry(r, seg, Math.max(5, seg - 2)), c, x, y, z, extra); }
  function cone(r, h, c, x, y, z, seg = 10) { return mesh(new THREE.ConeGeometry(r, h, seg), c, x, y, z); }
  function grp(x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); return g; }
  const RND0 = (function () { let a = 4242; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; })();   // fase deterministica (o lint reprova aleatorio nativo e dois workers divergiriam)
  function rnd(seed) { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

  // ---------- chao ----------
  function chao(w, d, c = PAL.grama, x = 0, z = 0) { const m = box(w, 0.4, d, c, x, -0.2, z); m.castShadow = false; return m; }
  function grama(n, w, d, x = 0, z = 0, seed = 1) {
    const r = rnd(seed); const geo = new THREE.ConeGeometry(0.07, 0.32, 4); const im = new THREE.InstancedMesh(geo, new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9, flatShading: true }), n);
    const d3 = new THREE.Object3D(); const cores = [new THREE.Color(PAL.grama2), new THREE.Color(PAL.grama3), new THREE.Color(0x9ED98E)];
    for (let i = 0; i < n; i++) { d3.position.set(x + (r() - 0.5) * w, 0.14, z + (r() - 0.5) * d); d3.rotation.set((r() - 0.5) * 0.4, r() * 6.28, (r() - 0.5) * 0.4); const s = 0.7 + r() * 0.8; d3.scale.set(s, s, s); d3.updateMatrix(); im.setMatrixAt(i, d3.matrix); im.setColorAt(i, cores[i % 3]); }
    im.castShadow = true; im.receiveShadow = true; return im;
  }
  function estrada(len, w, x, z, rotY = 0) { const g = grp(x, 0, z); g.rotation.y = rotY; const s = box(len, 0.06, w, 0xB9B4AA, 0, 0.03, 0); s.castShadow = false; g.add(s); for (let i = -len / 2 + 1; i < len / 2; i += 2.5) g.add(box(1.2, 0.07, 0.12, PAL.creme, i, 0.04, 0)); return g; }
  function arvore(h = 3, seed = 1) { const r = rnd(seed); const g = grp(); g.add(cyl(0.12, 0.18, h * 0.45, PAL.madeira, 0, h * 0.22, 0, 6)); const cores = [0x5EA862, 0x74C078, 0x4F9F58]; for (let i = 0; i < 3; i++) { const s = h * (0.28 + r() * 0.12); const m = mesh(new THREE.IcosahedronGeometry(s, 0), cores[i % 3], (r() - 0.5) * h * 0.3, h * 0.55 + i * h * 0.16, (r() - 0.5) * h * 0.3); m.rotation.set(r() * 3, r() * 3, 0); g.add(m); } return g; }
  function arbusto(s = 0.6, seed = 2) { const r = rnd(seed); const g = grp(); for (let i = 0; i < 3; i++) g.add(mesh(new THREE.IcosahedronGeometry(s * (0.6 + r() * 0.5), 0), i ? 0x74C078 : 0x5EA862, (r() - 0.5) * s, s * 0.5, (r() - 0.5) * s)); return g; }

  // ---------- cerca ----------
  function cerca(len, x, z, rotY = 0, altura = 1.1) { const g = grp(x, 0, z); g.rotation.y = rotY; const n = Math.max(2, Math.round(len / 2.2)); const step = len / (n - 1);
    for (let i = 0; i < n; i++) g.add(box(0.12, altura, 0.12, PAL.madeira, -len / 2 + i * step, altura / 2, 0));
    for (const y of [altura * 0.35, altura * 0.65, altura * 0.92]) { const w = cyl(0.015, 0.015, len, PAL.metalEsc, 0, y, 0, 5); w.rotation.z = Math.PI / 2; w.castShadow = false; g.add(w); } return g; }
  function cercaPainel(len, x, z, rotY = 0) { const g = grp(x, 0, z); g.rotation.y = rotY; for (let i = 0; i <= len; i += 1.5) g.add(cyl(0.04, 0.04, 1.0, PAL.metal, -len / 2 + i, 0.5, 0, 6)); for (const y of [0.3, 0.6, 0.9]) { const b = box(len, 0.05, 0.05, PAL.metal, 0, y, 0); g.add(b); } return g; }

  // ---------- silo ----------
  function silo(h = 6, r = 1.4) { const g = grp(); g.add(cyl(r, r, h, PAL.metal, 0, h / 2, 0, 18));
    for (let y = 0.5; y < h; y += 0.5) { const an = mesh(new THREE.TorusGeometry(r + 0.02, 0.035, 5, 24), PAL.metalEsc, 0, y, 0); an.rotation.x = Math.PI / 2; an.castShadow = false; g.add(an); }
    g.add(cone(r + 0.05, 1.3, PAL.metalEsc, 0, h + 0.65, 0, 18)); g.add(cyl(0.18, 0.18, 0.5, PAL.metalEsc, 0, h + 1.45, 0, 8));
    for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2 + Math.PI / 4; g.add(cyl(0.08, 0.08, 1.2, PAL.metalEsc, Math.cos(a) * (r - 0.3), -0.0, Math.sin(a) * (r - 0.3), 6)); }
    const esc = grp(r + 0.12, 0, 0); for (const dz of [-0.2, 0.2]) esc.add(cyl(0.025, 0.025, h, PAL.metalEsc, 0, h / 2, dz, 5)); for (let y = 0.4; y < h; y += 0.4) { const d = cyl(0.02, 0.02, 0.4, PAL.metalEsc, 0, y, 0, 5); d.rotation.x = Math.PI / 2; esc.add(d); } g.add(esc);
    const tubo = cyl(0.12, 0.12, 4, PAL.metalEsc, -r - 1.2, 1.0, 0, 8); tubo.rotation.z = Math.PI / 2 + 0.45; g.add(tubo); return g; }

  // ---------- galpao ----------
  function galpao(L = 16, W = 7, opts = {}) {
    const g = grp(); const H = 2.6, pitch = 0.42, ridge = H + Math.tan(pitch) * W / 2; const o = Object.assign({ interior: true, baias: 6, porcos: 7, cortina: true }, opts);
    const piso = box(L + 0.6, 0.2, W + 0.6, PAL.concreto, 0, 0.1, 0); piso.castShadow = false; g.add(piso);
    for (let i = 0; i <= 6; i++) { const x = -L / 2 + i * L / 6; for (const sz of [-1, 1]) g.add(box(0.22, H, 0.22, PAL.creme, x, H / 2 + 0.2, sz * W / 2)); }
    const viga = box(L + 0.3, 0.25, 0.25, PAL.azul, 0, H + 0.2, 0); g.add(viga);
    for (const sz of [-1, 1]) { const b = box(L + 0.3, 0.18, 0.18, PAL.creme, 0, H + 0.1, sz * W / 2); g.add(b); }
    const slope = Math.sqrt((W / 2) ** 2 + (ridge - H) ** 2) + 0.5;
    for (const sz of [-1, 1]) { const t = box(L + 1.0, 0.12, slope, 0xEDE8DA, 0, (H + ridge) / 2 + 0.26, sz * W / 4); t.rotation.x = -sz * pitch; g.add(t);
      for (let i = -L / 2; i <= L / 2; i += 2) { const n = box(0.08, 0.04, slope - 0.2, 0xD9D2C0, i, (H + ridge) / 2 + 0.34, sz * W / 4); n.rotation.x = -sz * pitch; n.castShadow = false; g.add(n); } }
    g.add(box(L + 1.1, 0.16, 0.3, PAL.azulClaro, 0, ridge + 0.3, 0));
    for (const sx of [-1, 1]) { const sh = new THREE.Shape(); sh.moveTo(-W / 2, 0); sh.lineTo(W / 2, 0); sh.lineTo(0, ridge - H); sh.lineTo(-W / 2, 0); const geo = new THREE.ExtrudeGeometry(sh, { depth: 0.12, bevelEnabled: false }); const m = mesh(geo, PAL.creme, sx * (L / 2 + (sx > 0 ? 0 : 0.12)), H + 0.2, 0); m.rotation.y = Math.PI / 2; g.add(m);
      for (let k = -1; k <= 1; k++) { const fan = grp(sx * (L / 2 + 0.2), H + 0.2 + 0.9, k * 1.6); fan.rotation.y = Math.PI / 2; fan.add(mesh(new THREE.TorusGeometry(0.55, 0.06, 6, 16), PAL.metalEsc, 0, 0, 0)); const pas = grp(); for (let p = 0; p < 4; p++) { const pa = box(0.14, 0.95, 0.03, PAL.metal, 0, 0, 0); pa.rotation.z = p * Math.PI / 4; pas.add(pa); } fan.add(pas); fan.userData.pas = pas; g.add(fan); g.userData.fans = (g.userData.fans || []).concat([fan]); } }
    for (const sz of [-1, 1]) g.add(box(L + 0.3, 0.9, 0.12, PAL.creme, 0, 0.65, sz * (W / 2 + 0.1)));   // muretas
    g.userData.cortinas = [];
    if (o.cortina) for (const sz of [-1, 1]) { const c = box(L, H * 0.55, 0.06, 0xE6ECF6, 0, H * 0.72 + 0.2, sz * (W / 2 + 0.16), { transparent: true, opacity: 0.55 }); c.castShadow = false; g.add(c); g.userData.cortinas.push(c); }
    g.userData.lampadas = []; for (let i = -L / 2 + 2; i < L / 2; i += 4) { const l = sph(0.16, 0xFFE2A8, i, H - 0.3, 0, 6, { emissive: 0xFFC46A, emissiveIntensity: 0 }); l.castShadow = false; g.add(l); g.userData.lampadas.push(l); }
    g.userData.baias = [];
    if (o.interior) { const corredor = 1.6, prof = (W - corredor) / 2 - 0.3, nb = o.baias, bl = (L - 1.0) / nb;
      for (const sz of [-1, 1]) { const zc = sz * (corredor / 2 + prof / 2);
        for (let i = 0; i < nb; i++) { const xc = -L / 2 + 0.5 + bl * (i + 0.5); const b = grp(xc, 0.2, zc);
          b.add(box(bl - 0.1, 0.9, 0.05, PAL.metal, 0, 0.45, -sz * prof / 2)); for (const dx of [-1, 1]) b.add(box(0.05, 0.9, prof, PAL.metal, dx * (bl / 2 - 0.05), 0.45, 0));
          const com = box(bl - 0.5, 0.35, 0.42, PAL.concreto, 0, 0.18, -sz * (prof / 2 - 0.25)); b.add(com); b.add(box(bl - 0.5, 0.06, 0.08, PAL.metalEsc, 0, 0.38, -sz * (prof / 2 - 0.05)));
          const bb = cyl(0.03, 0.03, 0.5, PAL.metalEsc, bl / 2 - 0.4, 0.5, sz * (prof / 2 - 0.2), 5); b.add(bb); const nip = cyl(0.025, 0.025, 0.25, PAL.ciano, bl / 2 - 0.4, 0.42, sz * (prof / 2 - 0.35), 5); nip.rotation.x = Math.PI / 2; b.add(nip);
          g.add(b); g.userData.baias.push({ g: b, w: bl - 0.3, d: prof - 0.5, sz, xc, zc }); } } }
    g.userData.H = H; g.userData.ridge = ridge; g.userData.L = L; g.userData.W = W; return g; }

  // ---------- porco ----------
  function porco(s = 1, cor = PAL.rosa) { const g = grp(); g.scale.set(s, s, s);
    const corpo = mesh(new THREE.CapsuleGeometry(0.3, 0.55, 3, 8), cor, 0, 0.5, 0); corpo.rotation.z = Math.PI / 2; g.add(corpo);
    const cab = grp(0.58, 0.52, 0); cab.add(sph(0.24, cor, 0, 0, 0, 8)); const fo = cyl(0.1, 0.12, 0.14, PAL.rosaEsc, 0.26, -0.04, 0, 8); fo.rotation.z = Math.PI / 2; cab.add(fo);
    for (const dz of [-1, 1]) { const or = cone(0.06, 0.15, PAL.rosaEsc, 0.02, 0.2, dz * 0.14, 5); or.rotation.x = dz * 0.5; or.rotation.z = -0.3; cab.add(or); const olho = sph(0.03, PAL.navy, 0.18, 0.06, dz * 0.12, 5); olho.castShadow = false; cab.add(olho); }
    g.add(cab); const pernas = []; for (const dx of [-0.28, 0.28]) for (const dz of [-0.15, 0.15]) { const p = grp(dx, 0.3, dz); p.add(cyl(0.06, 0.07, 0.3, cor, 0, -0.15, 0, 6)); p.add(cyl(0.07, 0.07, 0.05, PAL.rosaEsc, 0, -0.3, 0, 6)); g.add(p); pernas.push(p); }
    const rabo = mesh(new THREE.TorusGeometry(0.08, 0.022, 5, 8, Math.PI * 1.4), PAL.rosaEsc, -0.6, 0.62, 0); rabo.rotation.y = Math.PI / 2; g.add(rabo);
    g.userData = { cab, pernas, ph: RND0() * 6.28 }; return g; }
  function animaPorco(p, t, modo = "parado", vel = 1) { const u = p.userData; const ph = u.ph;
    if (modo === "andando") { u.pernas.forEach((pe, i) => { pe.rotation.z = Math.sin(t * 7 * vel + ph + (i % 2) * Math.PI) * 0.45; }); u.cab.rotation.z = Math.sin(t * 3 + ph) * 0.06; p.position.y = Math.abs(Math.sin(t * 7 * vel + ph)) * 0.03; }
    else if (modo === "comendo") { u.pernas.forEach(pe => pe.rotation.z = 0); u.cab.rotation.z = -0.55 + Math.sin(t * 6 + ph) * 0.08; u.cab.position.y = 0.4; }
    else { u.pernas.forEach(pe => pe.rotation.z = 0); u.cab.rotation.z = Math.sin(t * 1.2 + ph) * 0.08; u.cab.rotation.y = Math.sin(t * 0.7 + ph) * 0.3; u.cab.position.y = 0.52; } }

  // ---------- pessoa ----------
  function pessoa(o = {}) { const o2 = Object.assign({ roupa: PAL.camisa, calca: PAL.jeans, pele: PAL.pele, bone: PAL.azul, chapeu: false, jaleco: false, celular: true }, o); const g = grp();
    const pernas = []; for (const dx of [-0.11, 0.11]) { const p = grp(dx, 0.85, 0); p.add(box(0.17, 0.85, 0.2, o2.calca, 0, -0.42, 0)); p.add(box(0.19, 0.1, 0.28, PAL.navy, 0, -0.86, 0.03)); g.add(p); pernas.push(p); }
    g.add(box(0.46, 0.62, 0.27, o2.jaleco ? PAL.jaleco : o2.roupa, 0, 1.18, 0)); if (o2.jaleco) g.add(box(0.5, 0.75, 0.3, PAL.jaleco, 0, 1.12, 0));
    const bracos = []; for (const dx of [-1, 1]) { const b = grp(dx * 0.31, 1.45, 0); b.add(box(0.13, 0.6, 0.13, o2.jaleco ? PAL.jaleco : o2.roupa, 0, -0.3, 0)); b.add(box(0.12, 0.14, 0.12, o2.pele, 0, -0.64, 0)); g.add(b); bracos.push(b); }
    const cab = grp(0, 1.72, 0); cab.add(mesh(new THREE.BoxGeometry(0.34, 0.36, 0.32), o2.pele, 0, 0, 0)); for (const dz of [-0.08, 0.08]) { const ol = box(0.03, 0.05, 0.05, PAL.navy, 0.17, 0.02, dz); ol.castShadow = false; cab.add(ol); }
    if (o2.chapeu) { cab.add(cyl(0.42, 0.42, 0.04, PAL.madeira, 0, 0.19, 0, 12)); cab.add(cyl(0.2, 0.22, 0.2, PAL.madeira, 0, 0.3, 0, 10)); }
    else if (o2.bone) { cab.add(cyl(0.19, 0.19, 0.14, o2.bone, 0, 0.2, 0, 10)); cab.add(box(0.2, 0.03, 0.16, o2.bone, 0.2, 0.15, 0)); }
    else { cab.add(box(0.36, 0.1, 0.34, 0x3B2A1F, 0, 0.19, 0)); }
    g.add(cab); let tel = null; if (o2.celular) { tel = grp(0, -0.66, 0.1); tel.add(box(0.12, 0.22, 0.014, PAL.navy, 0, 0, 0)); const tela = box(0.1, 0.195, 0.005, 0xCFE9FF, 0, 0, 0.009, { emissive: 0x9FD8FF, emissiveIntensity: 0.6 }); tela.castShadow = false; tel.add(tela); bracos[1].add(tel); }
    g.userData = { pernas, bracos, cab, tel, ph: RND0() * 6.28 }; return g; }
  function animaPessoa(p, t, modo = "parado") { const u = p.userData;
    if (modo === "andando") { u.pernas.forEach((pe, i) => pe.rotation.x = Math.sin(t * 6 + (i ? Math.PI : 0)) * 0.5); u.bracos.forEach((b, i) => b.rotation.x = Math.sin(t * 6 + (i ? 0 : Math.PI)) * 0.4); p.position.y = Math.abs(Math.sin(t * 6)) * 0.03; u.cab.rotation.y = 0; }
    else if (modo === "celular") { u.pernas.forEach(pe => pe.rotation.x = 0); u.bracos[1].rotation.x = -1.9; u.bracos[1].rotation.z = -0.35; u.bracos[0].rotation.x = -0.2; u.cab.rotation.x = 0.35; u.cab.rotation.y = Math.sin(t * 0.8) * 0.05; }
    else if (modo === "apontando") { u.pernas.forEach(pe => pe.rotation.x = 0); u.bracos[1].rotation.x = -1.3; u.bracos[1].rotation.z = -0.5; u.bracos[0].rotation.x = 0; u.cab.rotation.x = 0.1; u.cab.rotation.y = -0.4; }
    else { u.pernas.forEach(pe => pe.rotation.x = 0); u.bracos.forEach(b => { b.rotation.x = Math.sin(t * 1.5 + u.ph) * 0.05; b.rotation.z = 0; }); u.cab.rotation.x = 0; u.cab.rotation.y = Math.sin(t * 0.6 + u.ph) * 0.25; } }

  // ---------- caminhao de suinos ----------
  function caminhao(o = {}) { const o2 = Object.assign({ cor: PAL.creme, cab: PAL.azul, sujo: false, gaiola: true, carga: null }, o); const g = grp();
    g.add(box(7.2, 0.3, 2.2, PAL.metalEsc, 0, 0.75, 0)); const cab = grp(2.6, 0, 0); cab.add(box(2.0, 1.9, 2.3, o2.cab, 0, 1.85, 0)); cab.add(box(1.2, 0.8, 2.0, o2.cab, 1.4, 1.3, 0));
    const pb = box(0.08, 0.9, 2.0, PAL.vidro, 0.98, 2.1, 0, { emissive: 0x6FB3D6, emissiveIntensity: 0.15 }); pb.castShadow = false; cab.add(pb); for (const dz of [-1, 1]) { const j = box(1.0, 0.7, 0.06, PAL.vidro, 0.2, 2.1, dz * 1.18); j.castShadow = false; cab.add(j); cab.add(box(0.08, 0.3, 0.3, PAL.metalEsc, 0.9, 2.3, dz * 1.35)); }
    cab.add(cyl(0.07, 0.07, 1.6, PAL.metal, -0.9, 2.6, -1.1, 8)); for (const dz of [-0.6, 0.6]) { const f = sph(0.12, 0xFFF1C9, 2.0, 1.1, dz, 6, { emissive: 0xFFE9A8, emissiveIntensity: 0.5 }); f.castShadow = false; cab.add(f); } g.add(cab);
    const corpo = grp(-1.4, 0, 0); corpo.add(box(4.6, 0.16, 2.3, PAL.metal, 0, 0.98, 0)); corpo.add(box(4.6, 0.12, 2.3, PAL.metal, 0, 3.0, 0));
    if (o2.gaiola) { for (const dz of [-1, 1]) { for (let i = -2.2; i <= 2.2; i += 0.42) corpo.add(box(0.06, 1.95, 0.06, o2.cor, i, 2.0, dz * 1.13)); for (const y of [1.3, 2.0, 2.7]) corpo.add(box(4.6, 0.06, 0.06, o2.cor, 0, y, dz * 1.16)); } for (let i = -2.2; i <= 2.2; i += 0.42) corpo.add(box(0.06, 1.95, 0.06, o2.cor, i, 2.0, 0)); corpo.add(box(0.1, 1.95, 2.3, o2.cor, -2.3, 2.0, 0)); corpo.add(box(0.1, 1.95, 2.3, o2.cor, 2.3, 2.0, 0)); }
    else corpo.add(box(4.6, 1.9, 2.3, o2.cor, 0, 2.0, 0));
    g.add(corpo); const rodas = []; for (const [x, dz] of [[2.6, -1], [2.6, 1], [-0.6, -1], [-0.6, 1], [-1.9, -1], [-1.9, 1]]) { const r = grp(x, 0.55, dz * 1.05); const pn = cyl(0.55, 0.55, 0.42, PAL.borracha, 0, 0, 0, 14); pn.rotation.x = Math.PI / 2; r.add(pn); const cubo = cyl(0.3, 0.3, 0.46, PAL.metal, 0, 0, 0, 10); cubo.rotation.x = Math.PI / 2; r.add(cubo); for (let k = 0; k < 5; k++) { const par = box(0.08, 0.4, 0.05, PAL.metalEsc, 0, 0, dz * 0.24); par.rotation.z = k * Math.PI * 2 / 5; r.add(par); } g.add(r); rodas.push(r); }
    g.add(box(0.3, 0.3, 2.2, PAL.metalEsc, -3.6, 0.75, 0));
    if (o2.sujo) { const r = rnd(9); for (let i = 0; i < 8; i++) { const f = sph(0.14 + r() * 0.16, PAL.lama, 4.2 + (i % 2) * 0.1, 0.9 + r() * 1.6, (r() - 0.5) * 2.0, 5); f.scale.x = 0.25; f.castShadow = false; g.add(f); } for (let i = 0; i < 26; i++) { const s = sph(0.12 + r() * 0.2, PAL.lama, -3.5 + r() * 7, 0.5 + r() * 1.3, (r() > 0.5 ? 1 : -1) * 1.18, 5); s.scale.z = 0.25; s.castShadow = false; g.add(s); } }
    g.userData = { rodas, cab, corpo }; return g; }
  function animaCaminhao(c, dist) { c.userData.rodas.forEach(r => r.rotation.z = -dist / 0.55); }

  // ---------- outros ----------
  function caixaDagua() { const g = grp(); for (const [dx, dz] of [[-0.8, -0.8], [0.8, -0.8], [-0.8, 0.8], [0.8, 0.8]]) g.add(cyl(0.08, 0.1, 4.2, PAL.metalEsc, dx, 2.1, dz, 6)); g.add(box(2.3, 0.15, 2.3, PAL.metalEsc, 0, 4.2, 0)); g.add(cyl(1.25, 1.25, 1.5, PAL.creme, 0, 5.0, 0, 16)); g.add(cone(1.3, 0.5, PAL.ciano, 0, 6.0, 0, 16)); g.add(cyl(0.06, 0.06, 4.2, PAL.ciano, 1.1, 2.1, 1.1, 6)); return g; }
  function cancela() { const g = grp(); g.add(box(0.35, 1.1, 0.35, PAL.creme, 0, 0.55, 0)); const barra = grp(0, 1.0, 0); const b = box(4.2, 0.12, 0.12, PAL.creme, 2.0, 0, 0); barra.add(b); for (let i = 0.4; i < 4; i += 0.8) barra.add(box(0.4, 0.13, 0.13, PAL.mag, i, 0, 0)); g.add(barra); g.userData.barra = barra; return g; }
  function guarita() { const g = grp(); g.add(box(2.6, 0.2, 2.6, PAL.concreto, 0, 0.1, 0)); g.add(box(2.2, 2.4, 2.2, PAL.creme, 0, 1.4, 0)); for (const dz of [-1, 1]) { const j = box(1.2, 0.8, 0.06, PAL.vidro, 0, 1.7, dz * 1.12); j.castShadow = false; g.add(j); } const j2 = box(0.06, 0.8, 1.2, PAL.vidro, 1.12, 1.7, 0); j2.castShadow = false; g.add(j2); g.add(box(2.8, 0.14, 2.8, PAL.azul, 0, 2.7, 0)); g.add(box(0.9, 1.0, 0.05, PAL.creme, -0.5, 0.6, 1.13)); return g; }
  function lavador() { const g = grp(); for (const dz of [-2.0, 2.0]) g.add(box(0.2, 4.2, 0.2, PAL.metalEsc, 0, 2.1, dz)); g.add(box(0.25, 0.25, 4.4, PAL.metalEsc, 0, 4.2, 0)); g.userData.bicos = []; for (let dz = -1.5; dz <= 1.5; dz += 1.0) { g.add(cyl(0.05, 0.08, 0.2, PAL.ciano, 0, 4.0, dz, 6)); g.userData.bicos.push([0, 3.9, dz]); } for (const dz of [-1.7, 1.7]) for (const y of [1.0, 2.2]) { g.add(cyl(0.05, 0.08, 0.2, PAL.ciano, 0, y, dz, 6)); g.userData.bicos.push([0, y, dz]); } const p = box(7, 0.08, 4.6, 0x9FA9B5, 0, 0.04, 0); p.castShadow = false; g.add(p); return g; }
  function casa() { const g = grp(); g.add(box(7.2, 0.3, 6.2, PAL.concreto, 0, 0.15, 0)); g.add(box(6.4, 2.8, 5.0, PAL.creme, 0, 1.7, -0.4)); const H = 3.1;
    for (const sz of [-1, 1]) { const t = box(7.6, 0.14, 3.6, PAL.telha, 0, H + 0.75, -0.4 + sz * 1.45); t.rotation.x = -sz * 0.5; g.add(t); } g.add(box(7.8, 0.16, 0.3, PAL.telha, 0, H + 1.55, -0.4));
    for (const dx of [-2.2, 0, 2.2]) g.add(box(0.18, 2.6, 0.18, PAL.madeira, dx, 1.6, 2.8)); const vp = box(7.0, 0.12, 2.2, PAL.telha, 0, 2.95, 2.3); vp.rotation.x = 0.18; g.add(vp);
    g.add(box(0.9, 1.9, 0.08, PAL.madeira, 0.9, 1.25, 2.12)); for (const dx of [-1.8, 2.4]) { const j = box(1.0, 0.9, 0.08, PAL.vidro, dx, 1.8, 2.12); j.castShadow = false; g.add(j); g.add(box(1.1, 0.08, 0.2, PAL.madeira, dx, 1.3, 2.18)); }
    g.add(box(0.5, 1.2, 0.5, PAL.telha, 2.2, H + 1.4, -1.4)); g.add(box(2.2, 0.9, 0.9, PAL.madeira, -1.9, 0.75, 2.4)); g.add(box(2.0, 0.12, 0.6, PAL.madeira, -1.9, 1.25, 2.4)); return g; }
  function sacos(n, x, z, seed = 3) { const r = rnd(seed); const g = grp(x, 0, z); let i = 0; for (let y = 0; i < n; y++) { const per = Math.max(1, 5 - y); for (let k = 0; k < per && i < n; k++, i++) { const s = box(0.9, 0.42, 0.55, PAL.creme, (k - (per - 1) / 2) * 0.95 + (r() - 0.5) * 0.08, 0.21 + y * 0.42, (r() - 0.5) * 0.1); s.rotation.y = (r() - 0.5) * 0.15; g.add(s); } } return g; }
  function pilhaMilho(x, z, s = 1) { const g = grp(x, 0, z); const m = cone(1.6 * s, 1.1 * s, PAL.milho, 0, 0.55 * s, 0, 12); g.add(m); return g; }
  function cocho(len) { const g = grp(); g.add(box(len, 0.4, 0.6, PAL.concreto, 0, 0.2, 0)); g.add(box(len - 0.2, 0.1, 0.4, PAL.milho, 0, 0.36, 0)); return g; }
  function poste(h = 5) { const g = grp(); g.add(cyl(0.08, 0.1, h, PAL.concreto, 0, h / 2, 0, 6)); g.add(box(0.8, 0.08, 0.08, PAL.madeira, 0, h - 0.3, 0)); return g; }
  function moeda() { const m = cyl(0.3, 0.3, 0.06, PAL.amarelo, 0, 0, 0, 12); return m; }
  function balanca() { const g = grp(); g.add(box(2.4, 0.15, 1.6, PAL.metalEsc, 0, 0.08, 0)); g.add(box(0.12, 1.6, 0.12, PAL.metalEsc, -1.1, 0.8, -0.7)); g.add(box(0.7, 0.5, 0.2, PAL.creme, -1.1, 1.6, -0.7)); return g; }
  function rampa(len = 4) { const g = grp(); const r = box(len, 0.12, 1.4, PAL.madeira, 0, 0, 0); r.rotation.z = Math.atan2(1.0, len); r.position.set(0, 0.55, 0); g.add(r); for (const dz of [-0.7, 0.7]) { const l = box(len, 0.6, 0.05, PAL.metal, 0, 0, dz); l.rotation.z = Math.atan2(1.0, len); l.position.set(0, 0.95, dz); g.add(l); } return g; }
  function veterinarioCarro() { const g = grp(); g.add(box(3.8, 0.9, 1.8, PAL.branco, 0, 0.8, 0)); g.add(box(2.0, 0.8, 1.7, PAL.branco, -0.2, 1.6, 0)); const v = box(1.6, 0.6, 1.72, PAL.vidro, -0.2, 1.65, 0); v.castShadow = false; g.add(v); for (const [x, dz] of [[1.2, -1], [1.2, 1], [-1.2, -1], [-1.2, 1]]) { const w = cyl(0.38, 0.38, 0.3, PAL.borracha, x, 0.4, dz * 0.85, 12); w.rotation.x = Math.PI / 2; g.add(w); } g.add(box(0.5, 0.5, 0.1, PAL.mag, 0.6, 1.0, 0.92)); g.add(box(0.14, 0.5, 0.1, PAL.branco, 0.6, 1.0, 0.95)); g.add(box(0.5, 0.14, 0.1, PAL.branco, 0.6, 1.0, 0.95)); return g; }
  return { PAL, mat, mesh, box, cyl, sph, cone, grp, rnd, chao, grama, estrada, arvore, arbusto, cerca, cercaPainel, silo, galpao, porco, animaPorco, pessoa, animaPessoa, caminhao, animaCaminhao, caixaDagua, cancela, guarita, lavador, casa, sacos, pilhaMilho, cocho, poste, moeda, balanca, rampa, veterinarioCarro };
};
