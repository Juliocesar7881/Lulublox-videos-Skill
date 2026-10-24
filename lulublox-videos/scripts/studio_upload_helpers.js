// YouTube Studio upload helpers (paste once into the Studio tab with javascript_tool; they live on `window`).
// Needs scripts/servidor_envio.py LOTE running (127.0.0.1:8768). Works with the Portuguese and the English UI.
// Flow per video N (tested on 2026-10-16, 28 uploads):
//   1. await __iniciar2('NN')      -> opens Create > Upload, sends the file, fills title/description, kids radio
//      (from the agenda's feito_para_criancas), language English, Category Gaming when needed, focuses the game box.
//   2. type "Roblox" with real keys (computer.type), wait 2 s, find "Roblox 2006 game suggestion option", click it,
//      WAIT 1.5 s (the dropdown takes the focus back), then  await __focar('input[aria-label=Tags]').
//   3. type __meta.tags.join(', ') + ',' with real keys; poll the game box (it reads empty while "Saving...");
//      check __chips() === __meta.tags.length, then  await __passo3()  (Next x3, opens the date picker).
//   4. ctrl+a, type the date in the box's format ("Oct 31, 2026" / "31 de out. de 2026"), Return;
//      await __fusoHora('09:00' | '18:00')  -> check fuso GMT-0300, hora and the date in `resumo`.
//   5. await __programar()  -> {link, quando}; then  lote.py marcar LOTE N agendado --link LINK
//      (copy the link from THIS result, never type it from memory).
window.__criar = () => document.querySelector('ytcp-button#create-icon') || [...document.querySelectorAll('ytcp-button')].find(e => /^(criar|create)$/i.test((e.innerText || '').trim()) && e.offsetParent);
window.__passo1 = async (N) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const clicar = el => (el.querySelector('button') || el).click();
  for (const b of [...document.querySelectorAll('ytcp-button, button')].filter(b => /^(close|fechar)$/i.test((b.innerText || '').trim()) && b.offsetParent)) { clicar(b); await espera(500); }
  clicar(window.__criar()); await espera(1200);
  [...document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu tp-yt-paper-item, [role=menuitem]')].find(i => /upload videos|enviar v.deos/i.test(i.innerText) && i.offsetParent).click(); await espera(2500);
  const m = await (await fetch('http://127.0.0.1:8768/meta/' + N)).json();
  const blob = await (await fetch('http://127.0.0.1:8768/video/' + N)).blob();
  const input = document.querySelector('ytcp-uploads-file-picker input[type=file][name=Filedata]');
  const dt = new DataTransfer(); dt.items.add(new File([blob], m.arquivo, {type: 'video/mp4'}));
  input.files = dt.files; input.dispatchEvent(new Event('change', {bubbles: true}));
  let t0 = Date.now(); while (!document.querySelector('ytcp-uploads-dialog #title-textarea #textbox') && Date.now() - t0 < 30000) await espera(500);
  await espera(6000);
  const d = document.querySelector('ytcp-uploads-dialog');
  const preencher = (sel, texto) => { const c = d.querySelector(sel); c.focus(); document.execCommand('selectAll', false, null); document.execCommand('insertText', false, texto); c.dispatchEvent(new Event('input', {bubbles: true})); return c.innerText; };
  const t = preencher('#title-textarea #textbox', m.titulo); await espera(500);
  const ds = preencher('#description-textarea #textbox', m.descricao); await espera(500);
  const mais = d.querySelector('#toggle-button'); if (mais) { clicar(mais); await espera(1500); }
  const marcados = [];
  const kids = m.feito_para_criancas === false ? 'VIDEO_MADE_FOR_KIDS_NOT_MFK' : 'VIDEO_MADE_FOR_KIDS_MFK';
  for (const nome of [kids, 'VIDEO_PAID_PRODUCT_PLACEMENT_NO', 'VIDEO_HAS_ALTERED_CONTENT_NO']) { const r = d.querySelector('[name=' + nome + ']'); if (r) { r.click(); await espera(400); marcados.push(nome + ':' + (r.checked || r.getAttribute('aria-checked'))); } else marcados.push(nome + ':MISSING'); }
  window.__meta = m;
  return {titulo: t === m.titulo, desc: ds.length, marcados, tags: m.tags.length, arquivo: m.arquivo};
};
window.__escolher = async (rotulo, opcao) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const d = document.querySelector('ytcp-uploads-dialog');
  const sel = [...d.querySelectorAll('ytcp-form-select')].find(x => x.offsetParent && rotulo.test((x.innerText || '').replace(/\s+/g, ' ')));
  if (!sel) return 'no select';
  const trig = sel.querySelector('ytcp-dropdown-trigger, #trigger'); trig.scrollIntoView({block: 'center'}); trig.click(); await espera(900);
  let op = null; for (let k = 0; k < 12 && !op; k++) { op = [...document.querySelectorAll('tp-yt-paper-item, [role=option]')].find(i => i.offsetParent && opcao.test((i.innerText || '').trim())); if (!op) await espera(400); }
  if (!op) return 'no option';
  op.scrollIntoView({block: 'center'}); op.click(); await espera(700);
  return (sel.innerText || '').replace(/\s+/g, ' ').trim();
};
window.__JOGO = 'input[aria-label="Game title (optional)"], input[aria-label="Título do jogo (opcional)"]';
window.__focar = async (sel) => { const espera = ms => new Promise(r => setTimeout(r, ms)); const e = document.querySelector('ytcp-uploads-dialog').querySelector(sel); if (!e) return 'missing'; e.scrollIntoView({block: 'center'}); await espera(500); e.click(); e.focus(); await espera(300); return document.activeElement === e; };
window.__iniciar = async (N) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  for (const b of [...document.querySelectorAll('ytcp-button, button')].filter(b => /^(fechar|close)$/i.test((b.innerText || '').trim()) && b.offsetParent)) { (b.querySelector('button') || b).click(); await espera(600); }
  const r1 = await window.__passo1(N);
  const lang = await window.__escolher(/Idioma do v.deo|Video language/i, /^(Ingl.s|English)$/i);
  const foco = await window.__focar(window.__JOGO);
  return {r1, lang, foco};
};
window.__iniciar2 = async (N) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const r = await window.__iniciar(N);
  const d = document.querySelector('ytcp-uploads-dialog');
  if (!d.querySelector(window.__JOGO)) { r.cat = await window.__escolher(/^(Entertainment|People & Blogs|Category.*|Categoria.*|Entretenimento|Pessoas e blogs)$/i, /^(Gaming|Jogos)$/i); await espera(1200); }
  r.foco = await window.__focar(window.__JOGO);
  return r;
};
window.__chips = () => [...document.querySelectorAll('ytcp-uploads-dialog ytcp-chip, ytcp-uploads-dialog ytcp-free-text-chip')].filter(c => c.offsetParent).length;
window.__jogoOk = async () => { let jogo = ''; for (let k = 0; k < 12 && jogo !== 'Roblox'; k++) { await new Promise(r => setTimeout(r, 700)); const e = document.querySelector('ytcp-uploads-dialog').querySelector(window.__JOGO); jogo = e ? e.value : ''; } return jogo; };
window.__passo3 = async () => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const d = document.querySelector('ytcp-uploads-dialog');
  for (let i = 0; i < 3; i++) { d.querySelector('#next-button').click(); await espera(1600); }
  const trig = () => d.querySelector('#datepicker-trigger');
  if (!(trig() && trig().offsetParent)) { const exp = d.querySelector('#second-container-expand-button'); if (exp) { exp.click(); await espera(1200); } }
  trig().click(); await espera(1200);
  const inp = [...document.querySelectorAll('ytcp-date-picker input, tp-yt-paper-input input, input')].find(i => i.offsetParent && /\d{4}/.test(i.value || ''));
  if (!inp) return 'no date input';
  inp.focus(); inp.select();
  return {valor: inp.value, foco: document.activeElement === inp};
};
window.__fusoHora = async (hora) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const d = document.querySelector('ytcp-uploads-dialog');
  const fusoBtn = [...d.querySelectorAll('ytcp-button, button')].find(b => /fuso hor.rio|time ?zone/i.test((b.innerText || '').trim()) && b.offsetParent);
  let fuso = 'no button';
  if (fusoBtn) {
    (fusoBtn.querySelector('button') || fusoBtn).click(); await espera(1200);
    const op = [...document.querySelectorAll('tp-yt-paper-item, [role=option], ytcp-ve, li')].find(i => i.offsetParent && /GMT-0?3:?00\)?\s*(Hor.rio local|Local time)/i.test((i.innerText || '').replace(/\s+/g, ' ')));
    if (op) { op.scrollIntoView({block: 'center'}); op.click(); await espera(900); fuso = op.innerText.replace(/\s+/g, ' ').trim(); }
    else { fuso = 'option not found: ' + [...document.querySelectorAll('tp-yt-paper-item, [role=option]')].filter(i => i.offsetParent).slice(0, 5).map(i => i.innerText.trim()).join(' | '); }
  }
  const horaInp = [...d.querySelectorAll('input')].find(i => i.offsetParent && /^\d{1,2}:\d{2}(\s?[AP]M)?$/i.test((i.value || '').trim()));
  if (!horaInp) return {fuso, erro: 'no time input'};
  horaInp.click(); horaInp.focus(); await espera(900);
  const [hh, mm] = hora.split(':').map(Number);
  const h12 = ((hh + 11) % 12) + 1, ap = hh < 12 ? 'AM' : 'PM';
  const padroes = [new RegExp('^0?' + hh + ':' + String(mm).padStart(2, '0') + '$'), new RegExp('^0?' + h12 + ':' + String(mm).padStart(2, '0') + '\\s?' + ap + '$', 'i')];
  const opH = [...document.querySelectorAll('tp-yt-paper-item, [role=option]')].find(i => i.offsetParent && padroes.some(p => p.test((i.innerText || '').trim())));
  if (opH) { opH.scrollIntoView({block: 'center'}); opH.click(); await espera(800); }
  const texto = (d.querySelector('#schedule-radio-button, ytcp-visibility-scheduler, #second-container') || d).innerText.replace(/\s+/g, ' ');
  return {fuso, hora: horaInp.value, achouHora: !!opH, resumo: texto.slice(0, 260)};
};
window.__programar = async () => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const d = document.querySelector('ytcp-uploads-dialog');
  const btn = d.querySelector('#done-button');
  (btn.querySelector('button') || btn).click();
  for (let i = 0; i < 50; i++) {
    await espera(700);
    for (const b of [...document.querySelectorAll('ytcp-button, button')].filter(b => /^(ok|entendi|got it)$/i.test((b.innerText || '').trim()) && b.offsetParent)) { (b.querySelector('button') || b).click(); await espera(400); }
    const dlg = [...document.querySelectorAll('ytcp-video-share-dialog, ytcp-dialog, tp-yt-paper-dialog')].find(x => x.offsetParent && /V.deo programado|Video scheduled/i.test(x.innerText || ''));
    if (dlg) {
      const a = [...dlg.querySelectorAll('a')].find(x => /youtube\.com\/shorts\/|youtu\.be\//.test(x.href));
      return {link: a && a.href.replace(/\?.*$/, ''), quando: (dlg.innerText.match(/(?:em|on|for) (.*?\d{1,2}:\d{2}(?:\s?[AP]M)?)/i) || [])[1]};
    }
  }
  return {erro: 'dialog did not appear'};
};
'helpers ok'
