# c31labs

Source for [company31.com](https://company31.com) — the advisory practice of **Manuel Re**. Programme delivery, data & business intelligence, and AI integration, from Sydney.

A hand-authored static site: semantic HTML5, vanilla CSS (logical properties, custom properties, dark mode), and vanilla JavaScript (progressive enhancement). No build step, no framework, no tracking before consent.

## Highlights

- **Nine languages** — English (canonical, `en-AU`), Spanish, Simplified Chinese, Japanese, Arabic (RTL), German, French, Brazilian Portuguese, Korean.
- **Four pages per language** — home, practice, contact, privacy, plus a shared 404.
- **Consent-gated analytics** — GA4 with Consent Mode v2. No events fire until the visitor opts in.
- **Apache-hardened** — HTTPS redirect, CSP, security headers, compression, cache rules, and 404 routing in `.htaccess`.
- **SEO-complete** — canonical + full hreflang reciprocity, JSON-LD (Organization, Person, WebSite), sitemap with 36 URLs.
- **Accessible by default** — theme persistence, reduced-motion respect, keyboard-reachable navigation, RTL mirroring.

## Layout

```
/
├── index.html, practice.html, contact.html, privacy.html, 404.html
├── es/ zh/ ja/ ar/ de/ fr/ pt/ ko/     localised variants
├── css/     base • layout • components • rtl
├── js/      consent • i18n • main
├── assets/  logo, OG image, favicons, touch icons
├── .htaccess, robots.txt, sitemap.xml, humans.txt, security.txt
└── README.md
```

## Running locally

```bash
python3 -m http.server 8080
# or
npx serve .
```

Open <http://localhost:8080/>. Serve over HTTP rather than `file://` so the language switcher, consent banner, and analytics helpers behave as they do in production.

## Deployment target

Apache 2.4+ with `mod_headers`, `mod_rewrite`, `mod_deflate`, `mod_expires`. Upload the tree to the web root; the `.htaccess` does the rest.

Before enabling CSP enforcement, compute the SHA-256 of the inline theme script in every HTML `<head>` and substitute it for the placeholder in `.htaccess`.

## Analytics

GA4 measurement ID is wired into `js/consent.js`. The same property serves all nine language variants, with every event automatically enriched with `page_language` and `page_path`. Events are English `snake_case` regardless of page language:

`cta_book_click`, `engagement_interest`, `language_change`, `theme_change`, `consent_decision`, `cookie_preferences_reopen`, `practice_section_view`, `scroll_depth`.

## Credits

Manuel Re, Sydney. Built with restraint. Hosted in Australia.
