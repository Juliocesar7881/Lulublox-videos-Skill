# Posting on YouTube (LuluBlox YT)

Lulu videos go **only** to the **LuluBlox YT** channel (`UCuSjAXe84Yzfi8BqN5SBQdw`, see `config.json`). Never post
them on another channel. The user is already signed in to YouTube Studio in their Chrome (Claude in Chrome); never
type passwords, never change account or channel settings.

## Settings for every Lulu video (decided with the user on 2026-10-15)

| Field | Value |
|---|---|
| Schedule | **09:00 and 18:00 of the same day**, time zone `(GMT-0300) Local time` (America/Sao_Paulo). `lote.py agenda` fills the slots. |
| Audience | Channel default (`config.json`): **made for kids** (`VIDEO_MADE_FOR_KIDS_MFK`). A batch can override it in `lote.json` / `roteiro.json` (`"feito_para_criancas": false`, e.g. the 2026-10-23 engagement test) and then uses `VIDEO_MADE_FOR_KIDS_NOT_MFK`; `lote.py metadados/agenda` carry the choice to `publicacao.json` and `agenda.json`. |
| Paid promotion | No (`VIDEO_PAID_PRODUCT_PLACEMENT_NO`) |
| Altered content | No (`VIDEO_HAS_ALTERED_CONTENT_NO`) |
| Video language | English |
| Category | Gaming, with the game title **Roblox** (pick the `Roblox` / `Roblox 2006` suggestion). Gaming + the Roblox game card got the most reach for Roblox Shorts. |
| Title / description / tags | from `publicacao.json` (`lote.py metadados`): English, SEO for kids' Roblox searches, `#shorts #roblox` in the title, tags ≤ 500 characters. |
| Thumbnail | the user makes it; leave the default. |

## How the upload is automated

The Studio UI of this account is in **Portuguese** (Criar, Enviar vídeos, Mostrar mais, Próxima, Programar,
Entendi, Horário local). The snippets below accept the Portuguese and English labels.

1. `python scripts/servidor_envio.py LOTE` serves `GET /meta/NN` (title, description, tags, file name) and
   `GET /video/NN` (the final MP4) on 127.0.0.1:8768 only.
2. In the Studio tab (channel content page), run with `javascript_tool`:

```js
const espera = ms => new Promise(r => setTimeout(r, ms)); const N = '01';
const clicar = el => (el.querySelector('button') || el).click();
for (const b of [...document.querySelectorAll('ytcp-button, button')].filter(b => /^(close|fechar)$/i.test((b.innerText || '').trim()) && b.offsetParent)) { clicar(b); await espera(500); }
// the Create button lost its id in Oct 2026: find it by its label
clicar(document.querySelector('ytcp-button#create-icon') || [...document.querySelectorAll('ytcp-button')].find(e => /^(criar|create)$/i.test((e.innerText || '').trim()) && e.offsetParent)); await espera(1200);
[...document.querySelectorAll('tp-yt-paper-item')].find(i => /upload videos|enviar v.deos/i.test(i.innerText) && i.offsetParent).click(); await espera(2500);
const m = await (await fetch('http://127.0.0.1:8768/meta/' + N)).json();
const blob = await (await fetch('http://127.0.0.1:8768/video/' + N)).blob();
const input = document.querySelector('ytcp-uploads-file-picker input[type=file][name=Filedata]');
const dt = new DataTransfer(); dt.items.add(new File([blob], m.arquivo, {type: 'video/mp4'}));
input.files = dt.files; input.dispatchEvent(new Event('change', {bubbles: true}));
let t0 = Date.now(); while (!document.querySelector('ytcp-uploads-dialog #title-textarea #textbox') && Date.now() - t0 < 30000) await espera(500);
await espera(6000);
const d = document.querySelector('ytcp-uploads-dialog');
const preencher = (sel, texto) => { const c = d.querySelector(sel); c.focus(); document.execCommand('selectAll', false, null); document.execCommand('insertText', false, texto); c.dispatchEvent(new Event('input', {bubbles: true})); return c.innerText; };
preencher('#title-textarea #textbox', m.titulo); await espera(500);
preencher('#description-textarea #textbox', m.descricao); await espera(500);
const mais = d.querySelector('#toggle-button'); if (mais) { clicar(mais); await espera(1500); }
for (const nome of [m.feito_para_criancas === false ? 'VIDEO_MADE_FOR_KIDS_NOT_MFK' : 'VIDEO_MADE_FOR_KIDS_MFK', 'VIDEO_PAID_PRODUCT_PLACEMENT_NO', 'VIDEO_HAS_ALTERED_CONTENT_NO']) { const r = d.querySelector('[name=' + nome + ']'); if (r) { r.click(); await espera(400); } }
```

3. Language: a dropdown helper (`ytcp-form-select` whose text matches the label), then pick `Inglês`/`English`:

```js
window.__escolher = async (rotulo, opcao) => {
  const espera = ms => new Promise(r => setTimeout(r, ms));
  const d = document.querySelector('ytcp-uploads-dialog');
  const sel = [...d.querySelectorAll('ytcp-form-select')].find(x => x.offsetParent && rotulo.test((x.innerText || '').replace(/\s+/g, ' ')));
  const trig = sel.querySelector('ytcp-dropdown-trigger, #trigger'); trig.scrollIntoView({block: 'center'}); trig.click(); await espera(900);
  const op = [...document.querySelectorAll('tp-yt-paper-item, [role=option]')].find(i => i.offsetParent && opcao.test((i.innerText || '').trim()));
  op.scrollIntoView({block: 'center'}); op.click(); await espera(700);
  return (sel.innerText || '').replace(/\s+/g, ' ').trim();
};
await window.__escolher(/Idioma do v.deo|Video language/i, /^(Ingl.s|English)$/i);
```

   The language list renders a moment after it opens: wait for the `Inglês` option (retry ~5 s) before clicking.

4. Category stays **Jogos/Gaming** (the account default). Focus the game title box from JS (`scrollIntoView`,
   `click()`, `focus()`; a coordinate click can land on another field after the dialog scrolls), or click the game title box (`input[aria-label="Título do jogo
   (opcional)"]`), type `Roblox` with real key presses (`computer` → `type`) and click the `Roblox 2006` suggestion.
5. Tags: click `input[aria-label=Tags]`, type `m.tags.join(', ') + ','` with real key presses and check that the
   number of chips (`ytcp-chip, ytcp-free-text-chip`) equals the number of tags.
6. Next ×3 (`#next-button`), open scheduling (`#second-container-expand-button`), open the date picker
   (`#datepicker-trigger`), select the date input and type the date in the UI format (`17 de out. de 2026`) + Enter.
   Time zone button → `(GMT-0300) Horário local`. Click the time input and pick the `09:00` or `18:00` option.
   Before `#done-button` (**Programar**), check the date, the time and `GMT-0300` in the dialog.
7. Close the "Entendi/Got it" notice; the share dialog shows "Vídeo programado … DATE às HH:MM" and the Shorts
   link. Save it with `python scripts/lote.py marcar LOTE N agendado --link URL`.

Uploads in a row: YouTube may limit the daily uploads of a new channel. If the dialog shows a limit, stop and tell
the user which videos are left; never try another channel.

Checks that saved time in the 2026-10-23 batch: verify `chips === tags.length` and the title before Next; verify the
date text, `HH:MM` and `GMT-0300` in one call and only then click Programar; read the link from the dialog that says
"Vídeo programado" (the upload dialog also shows a link before scheduling). In the content list, a not-made-for-kids
Short shows comments on; a made-for-kids one shows "Comentários desativados".
