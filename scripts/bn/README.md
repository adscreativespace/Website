# Bengali pages (`/bn/`)

The Bengali site is generated from the English pages, so layout, images, prices and links stay identical.

- `strings/src_<page>.json` — the English text found on each page
- `strings/tr_<page>.json` — the Bengali for each line (same order)
- `build.py` — writes `bn/<page>.html` from `<page>.html` + the translations

**After editing an English page:** run `python3 scripts/bn/build.py`.
It lists any English text that has no Bengali yet ("missing"). Add the Bengali for those lines
(or ask Claude to), then run it again and commit both the English page and `bn/`.

Project write-ups (`projects/*.md`) are shown in English on the Bengali project pages.
For Terms and Privacy, the English version is the binding one (the Bengali pages say so).
