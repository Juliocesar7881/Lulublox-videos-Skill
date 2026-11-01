// Run once in the TikTok Studio tab (javascript_tool). Then, on an upload page with the caption box empty:
//   await __tt(TEXTO, HASHTAGS, 'HH:MM', 'YYYY-MM-DD', false)   fills the form and returns what it would schedule
//   await __tt(TEXTO, HASHTAGS, 'HH:MM', 'YYYY-MM-DD', true)    same, and clicks Schedule if everything matches
// TEXTO and HASHTAGS come from `lote.py pacote`. Never use execCommand in this box: it corrupts the editor.
window.__tt = async (TEXTO, TAGS, HORA, DATA, agendar) => {
  const [HH, MM = '00'] = HORA.split(':');
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
  const [ih, id] = document.querySelectorAll('input.TUXTextInputCore-input');
  ih.click(); await esp(500);
  [...document.querySelectorAll('.tiktok-timepicker-left')].find(x => x.innerText.trim() === HH)?.click(); await esp(300);
  if (ih.value.slice(3) !== MM) { [...document.querySelectorAll('.tiktok-timepicker-right')].find(x => x.innerText.trim() === MM)?.click(); await esp(300); }
  document.body.click(); await esp(300);
  id.click(); await esp(500);
  const c = document.querySelector('.calendar-wrapper');
  const [ano, mes, dia] = DATA.split('-').map(Number);
  const nome = new Date(ano, mes - 1, 1).toLocaleString('en', {month: 'long'});
  if (c.querySelector('.month-title').innerText.trim() !== nome) { c.querySelectorAll('.arrow')[1].click(); await esp(400); }
  const ds = [...c.querySelectorAll('.day.valid')].filter(x => x.innerText.trim() === String(dia));
  (dia > 15 ? ds.at(-1) : ds[0])?.click(); await esp(500);
  const res = {hora: ih.value, data: id.value, tags: e.querySelectorAll('.mention').length, cont: (document.body.innerText.match(/\d+\/4000/) || [])[0]};
  const b = document.querySelector('[data-e2e=post_video_button]');
  res.ok = ih.value === HH + ':' + MM && id.value === DATA && r.checked && b.innerText.trim() === 'Schedule' && res.tags >= 5;
  if (agendar && res.ok) { b.click(); await esp(3500); res.fim = location.pathname; }
  return JSON.stringify(res);
};
