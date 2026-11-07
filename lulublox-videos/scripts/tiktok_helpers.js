// Run once in the TikTok Studio tab (javascript_tool). Then, on an upload page with the caption box empty:
//   await __tt(TEXTO, HASHTAGS, 'HH:MM', 'YYYY-MM-DD', false)   fills the form and returns what it would schedule
//   await __tt(TEXTO, HASHTAGS, 'HH:MM', 'YYYY-MM-DD', true)    same, and clicks Schedule if everything matches
// TEXTO and HASHTAGS come from `lote.py pacote`. Never use execCommand in this box: it corrupts the editor.
// 2026-11-07: TikTok replaced the date/time inputs with pickers (.scheduled-picker .Picker__trigger: [0] date,
// [1] time; .TimePicker__column hours/minutes; .DatePicker__panel button.DatePicker__day with a Portuguese
// aria-label such as "sábado, 14 de novembro de 2026"). The timezone select reads "(GMT-3) Local Time".
// After Schedule, `fim` is /tiktokstudio/content when it worked; `toast` holds "You can only schedule up to 30
// posts." when TikTok refused it (then discard the upload and stop).
window.__ttHora = async (HORA) => {
  const esp = ms => new Promise(r => setTimeout(r, ms));
  const [HH, MM] = HORA.split(':');
  document.body.click(); await esp(300);
  document.querySelectorAll('.scheduled-picker .Picker__trigger')[1].click(); await esp(700);
  let cols = [...document.querySelectorAll('.TimePicker__column')].filter(x => x.offsetParent);
  [...cols[0].children].find(x => x.innerText.trim() === HH).click(); await esp(400);
  cols = [...document.querySelectorAll('.TimePicker__column')].filter(x => x.offsetParent);
  if (cols[1]) { [...cols[1].children].find(x => x.innerText.trim() === MM).click(); await esp(400); }
  document.body.click(); await esp(300);
  return document.querySelectorAll('.scheduled-picker .Picker__value')[1].innerText;
};
window.__ttData = async (DATA) => {
  const esp = ms => new Promise(r => setTimeout(r, ms));
  const MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
  const [a, m, d] = DATA.split('-').map(Number);
  const rot = d + ' de ' + MESES[m - 1] + ' de ' + a;
  if (!document.querySelector('.DatePicker__panel')) { document.querySelectorAll('.scheduled-picker .Picker__trigger')[0].click(); await esp(700); }
  for (let k = 0; k < 3; k++) {
    const b = [...document.querySelectorAll('.DatePicker__panel button.DatePicker__day')].find(x => (x.getAttribute('aria-label') || '').endsWith(rot) && !x.disabled);
    if (b) { b.click(); await esp(500); return true; }
    const nav = document.querySelectorAll('.DatePicker__nav button, .DatePicker__nav [role=button], .DatePicker__nav > *');
    nav[nav.length - 1].click(); await esp(500);
  }
  return false;
};
window.__tt = async (TEXTO, TAGS, HORA, DATA, agendar) => {
  const esp = ms => new Promise(r => setTimeout(r, ms));
  const e = document.querySelector('.public-DraftEditor-content');
  const col = s => { const dt = new DataTransfer(); dt.setData('text/plain', s); e.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true})); };
  const ent = () => { const k = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', bubbles: true, cancelable: true}); Object.defineProperty(k, 'keyCode', {get: () => 13}); Object.defineProperty(k, 'which', {get: () => 13}); e.dispatchEvent(k); };
  e.focus(); col(TEXTO); await esp(600);
  for (const h of TAGS) {
    col(h);
    const lista = new RegExp(h + '\\n[\\d.,]+[KMB]? posts', 'i');
    let sug = false;
    for (let i = 0; i < 10 && !sug; i++) { await esp(250); sug = lista.test(document.body.innerText); }
    if (sug) { ent(); await esp(250); } else col(' ');
  }
  const r = document.querySelector('input[name=postSchedule][value=schedule]');
  r.click(); await esp(1300);
  if (!r.checked) return JSON.stringify({erro: 'Schedule did not turn on (consent dialog?)'});
  await window.__ttHora(HORA);
  const dOk = await window.__ttData(DATA);
  document.body.click(); await esp(400);
  const vals = [...document.querySelectorAll('.scheduled-picker .Picker__value')].map(x => x.innerText);
  const MES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const [a, m, d] = DATA.split('-').map(Number);
  const tz = [...document.querySelectorAll('input.Select__searchInput')].map(i => i.value).join('');
  const b = document.querySelector('[data-e2e=post_video_button]');
  const res = {hora: vals[1], data: vals[0], tags: e.querySelectorAll('.mention').length, cont: (document.body.innerText.match(/\d+\/4000/) || [])[0]};
  res.ok = vals[1] === HORA && vals[0] === MES[m - 1] + ' ' + d + ', ' + a && dOk && r.checked && /GMT-3/.test(tz) && b.innerText.trim() === 'Schedule' && res.tags >= 5;
  if (agendar && res.ok) {
    b.click(); let toast = null;
    for (let i = 0; i < 10; i++) { await esp(500); toast = toast || (document.body.innerText.match(/You can only schedule[^\n]*/) || [])[0]; }
    res.fim = location.pathname; res.toast = toast;
  }
  return JSON.stringify(res);
};
// Queue mode: window.__fila = [{texto, hashtags, hora, data, ...}] loaded from a JSON via a temporary file input.
window.__ttN = async (k) => { const q = window.__fila[k]; return await window.__tt(q.texto, q.hashtags, q.hora, q.data, true); };
'tiktok helpers ok'
