# St Paul Baptist Church — Website

A static website for St Paul Baptist Church, 2917 W Cleveland St, Elloree, SC 29047.

## Structure
- `index.html` — the full single-page site (Home, About, Worship, Ministries, Cemetery & Memorials, Our Legacy, Visit & Contact)
- `css/styles.css` — all styling
- `js/main.js` — mobile nav toggle + footer year
- `assets/` — put a logo, photos, and any gallery images here, then reference them from `index.html`

## Running locally
No build step required. Open `index.html` directly in a browser, or serve the folder:

```
cd church-website
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deploying
Any static host works (GitHub Pages, Netlify, Vercel, or plain shared hosting). For GitHub Pages, point Pages at this folder (or copy its contents to the repo root / a `docs/` folder) and enable Pages in the repository settings.

## Placeholders to confirm with the church before publishing
- **Service times** — currently listed as Sunday School 9:30 AM and Sunday Morning Worship 11:00 AM; confirm the actual schedule.
- **Photos** — the site currently uses no photos (color/typography only), including a monogram placeholder ("JH") in place of a real photo of Reverend Joseph Hamm. Add a church exterior photo, a pastor photo, and choir/congregation photos to `assets/` for a more personal feel.
- **Email address**, if the church has one, for a contact form or mailto link.
