# Neverlost Systems website

Static source for [neverlostsystems.com](https://neverlostsystems.com/).
Neverlost Systems is the company; Neverlost Healthcare is its connected,
patient-side healthcare application in development.

## Homepage story

The homepage moves from the appointment problem to a connected product:

1. Prepare what matters for your next appointment.
2. Patient and provider perspectives on the same conversation.
3. Capture experiences, bring history together, review changes, prepare two
   audience-specific reports, and carry context into follow-up.
4. A fictional Alex walkthrough: primary care, neurology, and PCP follow-up.
5. A separate invitation for physician-led clinic evaluation, with preparation
   burden, provider review time, clarification, and follow-through as proposed measures.
6. Preparation/readiness, focused evaluation, then paid adoption and expansion
   if supported by evidence. January 2027 remains a target, not a guaranteed date.
7. The founder story, underlying OS foundation, and patient waitlist.

Earlier V2, Case Navigator, and Full Human Pathway prototypes remain linked as
secondary background. They are not presented as three current products.
No public price or funding assumptions are included. Practice-sponsored access
is described as a proposed model, with separate patient sharing permissions.

## Walkthrough scope

The homepage walkthrough is a public-facing illustration of the prototype's
connected workflow. Its patient questions and provider-context examples are
illustrative; they are not copied clinical reports or a running application.
It uses fictional Alex and clearly states that provider delivery is simulated.
No private Cloud Run URL, patient data, API credentials, or private application
access is exposed. A public URL for the connected demo video was not available
when preparing this revision; a reviewed public video can be added later.

All three stages are readable without JavaScript. When JavaScript is available,
tabs support click, Left/Right arrows, Home/End, and keyboard focus. The two
audience views stay together at each stage.

## Source and preview

The existing static stack, navy palette, Montserrat/Source Sans 3 fonts,
official logo assets, domain file, and shared core script are preserved.
`healthcare.css` adds scoped layouts; `walkthrough.js` progressively enhances
the fictional case. `script.js` names the current analytics sections.

For an ordinary local checkout:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/. No framework build or package installation is needed.
The managed review environment uses its provided preview service instead.

## Contact and privacy

The patient waitlist retains the existing POST destination:
`https://formsubmit.co/jeff@neverlostsystems.com`.
Required fields are name and email. The subject is `Neverlost Healthcare waitlist`.
The honeypot, field limits, and FormSubmit response behavior are retained.
The page explains email use, opt-out contact, participation limits, and the
instruction not to submit medical records or sensitive health details.

The clinic action opens a separate email to `jeff@neverlostsystems.com` with a
clinic-pilot subject. It does not enroll a person on the patient waitlist.
`privacy.html` explains website signup, clinic email, FormSubmit, and existing
Google Analytics use. It covers the public website, not patient-data processing.

FormSubmit recipient activation and actual inbox delivery remain unverified.
Review checks must not submit a real signup or send a clinic email without
authorization. No local success message claims delivery.

## Release boundary

This revision is for review. Do not deploy until it has been reviewed.
The existing public site and GitHub Pages branch remain the release reference.
Verify the walkthrough, form behavior, privacy copy, links, and responsive layout
before publishing. Product and pilot plans are not represented as clinical
validation, signed partnerships, or an operating patient service.

