# Neverlost Systems Website

Source for [neverlostsystems.com](https://neverlostsystems.com/).

Patient-side infrastructure for complex healthcare. The website introduces the
patient-side coordination gap, the shared Neverlost OS infrastructure in
development, and a planned virtual pilot for POTS / EDS patients and families.

## Homepage

- Dark navy hero and pale blue panel system aligned with the current Neverlost investor-deck visual language.
- POTS / EDS positioned as the initial patient community, emphasizing its highly engaged peer networks and complex multi-provider care.
- Customer-facing pilot roadmap: late-2026 preparation, January 2027 virtual pilot, then product improvement and broader access.
- The first Join Early Access action appears with the POTS / EDS pilot roadmap and explicitly references January 2027.
- The patient-side coordination gap remains the core problem statement.
- Neverlost OS is presented as the shared infrastructure layer in development.
- Full Human Pathway, Neverlost V2, and Case Navigator now sit directly beneath Neverlost OS in one horizontal desktop row.
- The founder story remains, while team titles and the long-term organizational scale model have been removed from the customer-facing homepage.
- An early-access form; general inquiries use jeff@neverlostsystems.com in the footer.

## Selected working prototypes

- [Full Human Pathway](https://neverlost-full-human-pathway.vercel.app/): coordinate the person’s broader situation and prepare the next handoff.
- [Neverlost V2](https://neverlost-v1-portfolio.vercel.app/v2): organize and examine source-linked evidence in context.
- [Case Navigator](https://neverlost-case-navigator.vercel.app/): review AI-generated findings before accepting them into a case.

Public demonstrations use fictional / synthetic cases.

## Implementation and local preview

The existing static stack remains: semantic HTML, responsive CSS, vanilla
JavaScript, and GA4 section/navigation events. No package manager, application
build, TypeScript, linter, or automated test suite is configured in this repository.

The original `assets/nvlt-official-logo.svg`, `styles.css`, `brand-refresh.css`,
domain file, and core palette are retained. `positioning.css` now carries the
homepage-specific deck-inspired visual system, including condensed headings,
navy anchor sections, pale blue panels, responsive roadmap cards, and the
horizontal Neverlost OS application row.

From the repository root:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/.

## Early-access delivery

The inline form retains the site's existing FormSubmit service, with:

- POST destination: `https://formsubmit.co/jeff@neverlostsystems.com`
- Required name and email; optional role and interest.
- Subject: `Neverlost Systems early access`.
- A honeypot and the provider's default spam protection.
- A visible instruction not to submit sensitive medical information.

FormSubmit may require the recipient to activate the form via an email link.
The new recipient's activation and actual inbox delivery must be confirmed
before release. Local review checks the destination, field serialization,
required fields, and responsive layout without sending an external submission.
No local success message claims delivery; the form service handles the response.

## Release boundary

This revision is for review. Do not deploy until it has been reviewed.
The pilot remains planned, Neverlost OS remains in development, and customer
demand and healthcare partnerships are not represented as validated or signed.
The website and prototype demonstrations do not replace professional care.
