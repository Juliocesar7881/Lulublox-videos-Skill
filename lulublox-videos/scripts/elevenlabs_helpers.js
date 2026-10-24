// ElevenLabs Text to Speech helpers (paste once into the elevenlabs.io tab with javascript_tool; they live on
// `window`). Voice: Jessica (My voices), model Eleven v4. NEVER use execCommand in the editor (it froze the tab):
// type the lines with real keys. Flow per video (tested 2026-10-16, 14 videos in ~15 browser steps):
//   1. click the editor text line, ctrl+a, type all lines of the video separated by "\n" (one paragraph per line)
//   2. click "Generate speech", wait ~9 s
//   3. await __finaliza('<unique words of line 1>', 'E07')  -> plays the history items of that text, captures the
//      audio, keeps the take whose model_id is eleven_v4 (not eleven_v4_exp) and posts it to the receiver window
//      as E07-todas.mp3 (scripts/receptor_falas.py PASTA must be running and the receiver window open: inject
//      __botaoEnviar() once and click the button with a REAL click - window.open needs a user gesture).
//   4. python scripts/dividir_falas.py PROJECT PASTA/E07-todas.mp3, then alinhar_falas.py roteiro.json falas
// JS calls must finish in under ~45 s.
window.__capt = window.__capt || [];
if (!window.__hookA) {
  const of = window.fetch.bind(window);
  window.fetch = async function (...a) {
    const r = await of(...a);
    try {
      const u = String(a[0] && a[0].url || a[0]);
      const m = u.match(/history\/([^/?]+)\/audio/);
      if (m) { r.clone().blob().then(b => window.__capt.push({id: m[1], blob: b})); }
      else if (/history/.test(u)) { r.clone().json().then(j => { window.__hist = window.__hist || []; window.__hist.push(j); }).catch(() => {}); }
    } catch (e) {}
    return r;
  };
  window.__hookA = true;
}
window.__N = s => s.normalize('NFC').replace(/\s+/g, ' ').trim();
window.__tk = window.__tk || {};
window.__itensT = (trecho) => [...document.querySelectorAll('button, [role=button]')].filter(b => /play|pause|reproduzir/i.test(b.getAttribute('aria-label') || '')).map(b => { let el = b; for (let k = 0; k < 6 && el; k++) { el = el.parentElement; if (el && el.innerText && el.innerText.length > 15) break; } return {b, t: el ? window.__N(el.innerText) : ''}; }).filter(x => x.t.includes('Jessica') && x.t.length < 400 && x.t.includes(trecho));
window.__modeloDe = (id) => { for (const j of (window.__hist || []).slice().reverse()) { const arr = j.history || j.items || (Array.isArray(j) ? j : [j]); for (const h of arr) { if (h && (h.history_item_id === id || h.id === id)) return h.model_id; } } return null; };
window.__pegaTodos = async (trecho, prefixo) => { const its = window.__itensT(trecho); const out = []; for (let i = 0; i < its.length; i++) { const n0 = window.__capt.length; its[i].b.click(); for (let k = 0; k < 50 && window.__capt.length === n0; k++) await new Promise(r => setTimeout(r, 150)); document.querySelectorAll('audio').forEach(a => a.pause()); if (window.__capt.length > n0) { const c = window.__capt[window.__capt.length - 1]; out.push([i, c.id, c.blob.size, window.__modeloDe(c.id)]); window.__tk[prefixo + '-' + i] = c; } await new Promise(r => setTimeout(r, 300)); } return out; };
window.__mandar = (obj) => { for (const [nome, blob] of Object.entries(obj)) window.__receptor.postMessage({nome, blob}, 'http://127.0.0.1:8766'); return Object.keys(obj); };
window.__finaliza = async (trecho, nome) => {
  let its = [];
  for (let k = 0; k < 60; k++) { its = window.__itensT(trecho); if (its.length >= 2) break; await new Promise(r => setTimeout(r, 300)); }
  if (its.length < 2) return [nome, 'still generating', its.length];
  const r = await window.__pegaTodos(trecho, nome);
  const v4 = Object.entries(window.__tk).filter(([k]) => k.startsWith(nome + '-')).map(([k, c]) => [k, c, window.__modeloDe(c.id)]).find(x => x[2] === 'eleven_v4');
  if (!v4) return [nome, 'no v4 take', r.map(x => [x[2], x[3]])];
  window.__mandar({[nome + '-todas.mp3']: v4[1].blob});
  const cred = (document.body.innerText.match(/([\d.,]+)\s*(credits remaining|cr[eé]ditos restantes)/i) || [])[1];
  return [nome, v4[1].blob.size, r.map(x => [x[2], x[3]]), cred];
};
window.__salvos = window.__salvos || [];
if (!window.__msgOk) {
  window.addEventListener('message', ev => { if (ev.origin !== 'http://127.0.0.1:8766') return; if (ev.data && ev.data.salvo) window.__salvos.push(ev.data.salvo); });
  window.__msgOk = true;
}
window.__botaoEnviar = () => {
  let b = document.getElementById('__baixarFalas');
  if (!b) { b = document.createElement('button'); b.id = '__baixarFalas'; document.body.appendChild(b); }
  b.textContent = 'ENVIAR FALAS';
  b.style.cssText = 'position:fixed;left:20px;top:20px;z-index:999999;padding:20px 30px;font-size:22px;background:#f0c;color:#fff;border:0;border-radius:10px';
  b.onclick = e => { e.preventDefault(); window.__receptor = window.open('http://127.0.0.1:8766/receber.html', 'receptorFalas', 'width=500,height=400'); };
  return 'button ready';
};
'eleven helpers ok'
