# Neverlost Systems Website

Public source for **[neverlostsystems.com](https://neverlostsystems.com/)**.

Neverlost Systems is developing patient-advocacy and care-navigation services supported by AI-assisted tools that help preserve important context across records, providers, benefits, and time.

## What the site presents

The current site reflects Neverlost's active company and product direction rather than an early placeholder page.

It introduces:

- the core principle **“Preserve Before You Understand”**;
- patient advocacy and care navigation as the initial market focus;
- the role of AI in increasing workflow capacity while preserving provenance, review, and human accountability;
- the Neverlost product family;
- public demonstrations and prior project work;
- current customer-discovery, pilot-design, research, and commercialization questions.

## Product family shown on the site

- **Neverlost OS** — shared foundation for case state, source context, authority, provenance, and history.
- **Neverlost Command Center** — working coordination prototype for current context, workstreams, blockers, and attention.
- **Neverlost V1.1 — Evidence Analysis** — source-linked evidence analysis, longitudinal organization, capacity themes, bottlenecks, and unresolved gaps for human review.
- **Neverlost Case Navigator** — working human-review prototype with a public synthetic demonstration.

## Implementation

The site is deliberately lightweight and dependency-free:

- semantic HTML;
- CSS with responsive layouts and the current Neverlost visual identity;
- vanilla JavaScript for site interactions;
- public-safe SVG brand assets;
- GA4 analytics;
- custom-domain configuration through `CNAME`;
- links to public Neverlost demos and related work.

There is no application build step or package dependency required to preview the site.

## Local preview

From the repository root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Opening `index.html` directly also works for most of the static site.

## Public / private boundary

This repository is intentionally public-facing. It does **not** contain private medical records, client information, credentials, or controlled internal case data.

The site describes early-stage products and prototypes. It should not be read as a claim that every product shown is a production healthcare deployment or a substitute for licensed clinical, legal, social-work, or benefits advice.

## Related public repositories

- [`neverlost-case-navigator`](https://github.com/Neverlost-AI/neverlost-case-navigator)
- [`neverlost-v1`](https://github.com/Neverlost-AI/neverlost-v1)
- [`Neverlost-full-human-pathway`](https://github.com/Neverlost-AI/Neverlost-full-human-pathway)
- [`Neverlost-capacity-aware-publishing`](https://github.com/Neverlost-AI/Neverlost-capacity-aware-publishing)
- [`reusable-codex-skills`](https://github.com/Neverlost-AI/reusable-codex-skills)

## Status

**Live public website · active company presentation · ongoing product and customer-discovery work**
