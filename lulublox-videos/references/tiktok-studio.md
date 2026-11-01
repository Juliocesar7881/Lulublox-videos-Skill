# Posting on TikTok (@lulublox.yt)

Every LuluBlox YT video also goes to the TikTok profile **@lulublox.yt**, at the same date and time as on YouTube, with
the same title, description and tags (user's decision, 2026-11-01). The user is already signed in to TikTok Studio in
their Chrome (Claude in Chrome). Never type passwords and never post to another profile. Check that TikTok Studio
shows `lulublox.yt` before the first upload.

## What differs from YouTube

| Topic | TikTok |
|---|---|
| Text | One box, 4000 characters. No title or tags fields: `lote.py pacote` joins title + description and turns every hashtag and tag into a hashtag. |
| Scheduling | Web only, from TikTok Studio. On 2026-11-01 the calendar allowed **30 days** ahead (Nov 1 to Dec 1, `tiktok.dias_agendamento` in `config.json`). Videos further out wait for the next round. |
| Time | 24 h, whole minutes in steps of 5. The post list shows `GMT-3 Sao Paulo`. |
| File | TikTok's CSP blocks `servidor_envio.py` (`connect-src`). Upload with the `file_upload` browser tool, limited to 10 MB. `lote.py pacote` makes the copy in `final-tiktok/` (30 fps, under 9.7 MB). |
| Audience | There is no "made for kids" option. Who can see: **Everyone**. Comments and reuse stay on, as the form opens. |
| Thumbnail | The form's default cover. Change it only if the user asks. |

## Steps

1. `python scripts/lote.py tiktok` lists what fits the window, across all batches. Phonkfox batches are skipped.
2. `python scripts/lote.py pacote LOTE N` makes the MP4 and prints the caption (`texto`, `hashtags`).
3. Open `https://www.tiktok.com/tiktokstudio/upload` and run `scripts/tiktok_helpers.js` once with `javascript_tool`.
   The app is a single page: `window.__tt` survives while you only click inside it, so go back to the upload page with
   the sidebar **Upload** button (real click), press `Escape` to close its menu, and do not use `navigate`.
4. Use `find` to get the ref of the file input and send the MP4 with `file_upload`. The ref changes on every page.
   Never click the input or the "Select video" button: that opens the native file picker.
5. Wait about 6 s for `Uploaded`. Dismiss tips with **Got it**. On **Turn on automatic content checks?** click
   **Cancel**: it is a setting and the user did not ask for it.
6. Click the caption box, real keys `ctrl+a` and `Delete` to clear the file name.
7. `await __tt(TEXTO, HASHTAGS, 'HH:MM', 'YYYY-MM-DD', true)`. It pastes the text, adds each hashtag and picks it from
   the suggestion list, selects Schedule, sets the time and the date, checks them and clicks **Schedule**. With `false`
   it fills the form and stops. It returns `hora`, `data`, `tags` (linked hashtags), `cont` and `ok`; `fim` is
   `/tiktokstudio/content` when it scheduled. If `ok` is false it did not schedule: look at the page.
8. `python scripts/lote.py marcar LOTE N agendado --tiktok`. There is no public link before the post goes live. At the
   end, check `https://www.tiktok.com/tiktokstudio/content`: each row shows the date and `GMT-3 Sao Paulo`.

`file_upload` works inside `browser_batch`, but the 10 MB limit counts the whole batch: one video per batch.

For many videos, keep the captions out of the conversation: write the queue as a JSON file, create a temporary
`<input type=file>` in the page, send the JSON with `file_upload`, read it with `files[0].text()` and call `__tt` by index.

## Consent dialog

The first click on **Schedule** on an account opens **Allow your video to be saved for scheduled posting?**. It is a
consent on the user's account: click **Allow** only after the user says so in chat, otherwise click **Cancel** and
stop. The user approved it for @lulublox.yt on 2026-11-01 and it did not come back.

## Traps

- **Scheduling limit.** On 2026-11-01 the 52nd scheduled post (50 still pending) was refused with a toast, "You can
  only schedule up to 30 posts.", on any date. The form stays open, nothing changes on screen and the toast is gone
  in seconds: `fim` staying `/tiktokstudio/upload` after `ok: true` means it did **not** schedule. 42 and then 9 more
  had passed on the same day, so the exact rule is unknown. Never click again in a loop or look for a way around it:
  discard the upload and tell the user.
- **Never use `document.execCommand` in the caption box.** The text appears on screen but the editor state does not
  get it (wrong counter), and the next `Delete` crashes the page with "Something went wrong" (2026-11-01). A synthetic
  `paste` event works, and so does a synthetic `keydown` Enter with `keyCode` 13 to pick a suggestion.
- Hashtags typed or pasted in one go stay plain text (0 linked). Each one must be picked from the suggestion list. A
  tag with no suggestion stays plain text: that is normal, so `tags` is usually 9 to 16 of about 18.
- After a crash, **Retry** does not recover the page, and leaving it opens a "Leave site?" dialog that blocks `navigate`
  and `tabs_close_mcp`. Open a new tab and upload again. Nothing is posted.
- The page scrolls by itself after the upload. Coordinates from an old screenshot can miss the Schedule radio, so
  `__tt` does it from JavaScript.
- `.day.valid` can show the same number twice (Nov 1 and Dec 1): `__tt` opens the right month first.
- To drop an upload: `[data-e2e="discard_post_button"]`, then **Discard** in the dialog.
- Test the form without pressing the post button: **Post** with "Now" selected publishes at once.
- The Location row suggests places near the user. Leave it empty.
- Do not turn on **AI-generated content** or **Disclose post content** on your own. If TikTok asks for a label, stop
  and ask the user.
