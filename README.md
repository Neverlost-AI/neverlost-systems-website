# Neverlost Systems Website

Public source for **[neverlostsystems.com](https://neverlostsystems.com/)**.

Neverlost Systems is building patient advocacy and software around a simple problem: patients should not have to start their story over at every appointment, and providers should not have to reconstruct it from scratch each time.

The public site centers the company around carrying complex health context forward, preparing what matters for the encounter in front of the patient and provider, and keeping that information connected to the original evidence.

## What the site presents

The homepage now focuses on:

- the patient/provider reconstruction problem inside limited clinical time;
- carrying longitudinal context forward instead of repeatedly rebuilding it;
- patient advocacy and appointment preparation as the initial commercial focus;
- clear boundaries between software, advocates, patients, and clinical decision-making;
- two live public applications: Neverlost V2 and Case Navigator;
- customer discovery and the questions Neverlost is still validating;
- the founder story behind the problem and product direction.

The homepage intentionally does **not** present the older product-family architecture, Command Center, V1.1, the eight-step development loop, or a standalone “Why AI” section as the primary company story. Those remain part of the broader technical history and product direction where relevant.

## Live software

- **Neverlost V2 — Live Evidence Analysis** — source-linked evidence analysis, prioritization, review, and synthesis while keeping outputs connected to the underlying evidence.
  - https://neverlost-v1-portfolio.vercel.app/v2
- **Neverlost Case Navigator** — human-reviewed AI workflow where proposed findings can be accepted, edited, rejected, or held before reviewed information becomes part of the case.
  - https://neverlost-case-navigator.vercel.app/

These are early-stage applications and technical demonstrations, not production clinical systems or substitutes for professional care.

## Implementation

The site is deliberately lightweight and dependency-free:

- semantic HTML;
- CSS with responsive layouts and the current Neverlost visual identity;
- vanilla JavaScript for site interactions;
- GA4 analytics, including section-view events for the current homepage structure;
- custom-domain configuration through `CNAME`;
- direct links to the live Neverlost applications.

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

The site describes early-stage products, patient-advocacy work, customer discovery, and prototypes. It should not be read as a claim of proven clinical outcomes or as medical, legal, social-work, or benefits advice.

## Related public repositories

- [`neverlost-case-navigator`](https://github.com/Neverlost-AI/neverlost-case-navigator)
- [`neverlost-v1`](https://github.com/Neverlost-AI/neverlost-v1)
- [`Neverlost-full-human-pathway`](https://github.com/Neverlost-AI/Neverlost-full-human-pathway)
- [`Neverlost-capacity-aware-publishing`](https://github.com/Neverlost-AI/Neverlost-capacity-aware-publishing)
- [`reusable-codex-skills`](https://github.com/Neverlost-AI/reusable-codex-skills)

## Status

**Live public website · patient-advocacy focus · working software · active customer discovery**
