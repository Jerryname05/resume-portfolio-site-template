---
name: resume-portfolio-site-template
description: Create an anonymous, responsive static resume/portfolio website template from a resume, candidate profile, target JD, photos, and contact assets. Use when the user wants a GitHub Pages, Netlify, or Vercel-ready personal job-search portfolio without leaking private details in the reusable skill/template.
metadata:
  short-description: Build an anonymous resume portfolio template
---

# Resume Portfolio Site Template

Use this skill to create a polished static portfolio website from a candidate resume and optional target job description. The bundled template is intentionally anonymous: it must not contain the original creator's name, school, phone, email, QR code, social links, private photos, or real company/school logos.

## Workflow

1. Read the candidate's resume, target roles, preferred tone, and supplied assets.
2. Create or update a profile JSON using `assets/example-profile.json` as the shape.
3. Run `scripts/generate_site.py` to copy the bundled template and apply replacements.
4. Edit the generated site directly when the resume needs richer layout changes than simple text replacement.
5. Verify the output in a browser at desktop and mobile widths.
6. Run a privacy scan before sharing or publishing the skill/template.
7. Package or publish the generated output as a static site. GitHub Pages, Netlify, and Vercel all work.

## Generator

From the skill folder:

```bash
python3 scripts/generate_site.py \
  --profile assets/example-profile.json \
  --output ./dist/demo-site
```

The generator:

- Copies `assets/site-template/` into the output folder.
- Applies literal text replacements across `.html`, `.css`, `.js`, `.json`, `.toml`, `.md`, and `.txt`.
- Copies replacement assets into the output folder. If a replacement asset uses a different extension than the placeholder, the script updates references in HTML/CSS/JS automatically.

## Profile JSON

Use `replacements` for text that already exists in the template:

```json
{
  "replacements": {
    "Your Name": "Alex Chen",
    "你的姓名": "陈小满",
    "内容增长候选人": "产品运营候选人"
  },
  "assets": {
    "hero-placeholder.svg": "/absolute/path/to/hero.jpg",
    "assets/contact-qr.svg": "/absolute/path/to/contact-qr.png"
  }
}
```

Keep replacements specific enough to avoid accidental changes. Prefer replacing full phrases rather than single words.

## Customization Priorities

- First viewport: candidate name, school/role, strongest proof metrics, one concise personal intro, and an optional JD matcher.
- About section: 3-4 identity cards, each with one crisp capability and evidence.
- Education/internship section: use compact cards with logos, dates, role names, and quantified bullets.
- Projects section: make the strongest project visually dominant, then add 2-3 secondary cards.
- Contact section: email, phone/WeChat, location, social link, and QR image if available.

## Privacy Check

Before delivering a reusable skill or template, scan the folder for accidental personal data:

```bash
rg -n "real-name|phone|email|school|company|social-link" .
```

Replace any real personal data with placeholders. Only generated sites for a specific user should contain that user's information.

## Responsive Requirements

Before delivery, check:

- Desktop around 1440-1920px wide.
- Narrow desktop around 900-1100px wide.
- Mobile around 390-430px wide.

Make sure navigation, visitor pill, theme toggle, music control, hero card, project cards, and contact cards do not overlap or overflow.

## Deployment

For GitHub Pages, ensure `index.html` is at the repository root or inside the configured Pages folder. For Netlify manual deploy, zip the generated output contents so `index.html` is at the zip root.
