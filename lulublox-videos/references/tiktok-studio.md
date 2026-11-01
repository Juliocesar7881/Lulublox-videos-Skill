# Posting on TikTok (@lulublox.yt)

Every LuluBlox YT video also goes to the TikTok profile **@lulublox.yt**, at the same date and time as on YouTube, with
the same title, description and tags (user's decision, 2026-11-01). The user is already signed in to TikTok Studio in
their Chrome (Claude in Chrome). Never type passwords and never post to another profile. Check that TikTok Studio
shows `lulublox.yt` before the first upload.

## What differs from YouTube

| Topic | TikTok |
|---|---|
| Text | One box, 4000 characters. No title or tags fields: `lote.py pacote` joins title + description and turns every hashtag and tag into a hashtag. |
| Scheduling | Web only, from TikTok Studio. Guides say 15 minutes to about 10 days ahead (`config.json` → `tiktok.dias_agendamento`). Videos further out wait for the next round. |
| File | TikTok's CSP blocks `servidor_envio.py` (`connect-src`). Upload with the `file_upload` browser tool, limited to 10 MB. `lote.py pacote` makes the copy in `final-tiktok/`. |
| Audience | There is no "made for kids" option. Who can see: **Everyone**. Comments and reuse stay on, as the form opens. |
| Thumbnail | The form's default cover. Change it only if the user asks. |

## Steps

1. `python scripts/lote.py tiktok` lists what fits the window, across all batches. Phonkfox batches are skipped.
2. `python scripts/lote.py pacote LOTE N` prints the MP4 path and the caption (`texto`, `hashtags`).
3. Open `https://www.tiktok.com/tiktokstudio/upload`. Use `find` to get the ref of the file input and send the MP4 with
   `file_upload`. Never click the input or the "Select video" button: that opens the native file picker.
4. Wait for `Uploaded`. Dismiss the tips with **Got it**.
   On **Turn on automatic content checks?** click **Cancel**. That is a setting and the user did not ask for it.
5. Caption, in this order:
   - Click the box, then real keys `ctrl+a` and `Delete` to clear the file name.
   - Paste `texto` with a synthetic paste event:

   ```js
   const e = document.querySelector('.public-DraftEditor-content'); e.focus();
   const dt = new DataTransfer(); dt.setData('text/plain', TEXTO);
   e.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
   ```

   - Real key `ctrl+End`. For each hashtag: `computer` → `type` the hashtag, wait 2 s for the suggestion list, press
     `Return`. The tag turns into a `mention` span and a space is added by itself. Pasted hashtags stay plain text.
   - Check the counter `N/4000`.
6. Click the **Schedule** radio (`input[name=postSchedule][value=schedule]`).
7. Pick the date and time of `quando` (the same as YouTube, GMT-0300). **NOT VERIFIED YET:** on 2026-11-01 the user had
   not accepted the consent below, so the date picker was never seen. Fill in the selectors and the real day limit on
   the first real run, and update `tiktok.dias_agendamento`.
8. Check the date, the time and the caption, then click the button `[data-e2e="post_video_button"]`.
9. Find the post in `https://www.tiktok.com/tiktokstudio/content` and record it:
   `python scripts/lote.py marcar LOTE N agendado --tiktok --link URL`.

## Consent dialog

The first click on **Schedule** opens **Allow your video to be saved for scheduled posting?**. It is a consent on the
user's account: click **Allow** only after the user says so in chat, otherwise click **Cancel** and stop.

## Traps

- **Never use `document.execCommand` in the caption box.** The text appears on screen but the editor state does not
  get it (wrong counter), and the next `Delete` crashes the page with "Something went wrong" (2026-11-01).
- After that crash, **Retry** does not recover it and leaving the page opens a "Leave site?" dialog that blocks
  `navigate`. Open a new tab and upload again. Nothing is posted.
- To drop an upload: `[data-e2e="discard_post_button"]`, then **Discard** in the dialog.
- Test the form without pressing the post button: **Post** on a video with "Now" selected publishes it at once.
- The Location row suggests places near the user. Leave it empty.
- Do not turn on **AI-generated content** or **Disclose post content** on your own. If TikTok asks for a label, stop
  and ask the user.
