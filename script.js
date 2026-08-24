const navToggle = document.querySelector('.nav-toggle');
const primaryNav = document.querySelector('.primary-nav');
const year = document.querySelector('#year');
const brandMark = document.querySelector('.brand-mark');
const contactOpen = document.querySelector('a[href="mailto:neverlostsells@gmail.com"]');

const brandStylesheet = document.createElement('link');
brandStylesheet.rel = 'stylesheet';
brandStylesheet.href = 'brand-refresh.css';
document.head.appendChild(brandStylesheet);

const favicon = document.createElement('link');
favicon.rel = 'icon';
favicon.type = 'image/svg+xml';
favicon.href = 'assets/nvlt-official-logo.svg';
document.head.appendChild(favicon);

if (brandMark) {
  const logo = document.createElement('img');
  logo.className = 'brand-logo';
  logo.src = 'assets/nvlt-official-logo.svg';
  logo.alt = '';
  logo.setAttribute('aria-hidden', 'true');
  brandMark.replaceWith(logo);
}

if (year) {
  year.textContent = new Date().getFullYear();
}

if (navToggle && primaryNav) {
  navToggle.addEventListener('click', () => {
    const isOpen = primaryNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  primaryNav.addEventListener('click', (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      primaryNav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

if (contactOpen) {
  const modalStyles = document.createElement('style');
  modalStyles.textContent = `
    .contact-dialog {
      width: min(92vw, 620px);
      max-height: 90vh;
      margin: auto;
      padding: 0;
      overflow: auto;
      color: var(--text);
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 20px;
      box-shadow: 0 24px 80px rgba(15, 29, 48, .24);
    }
    .contact-dialog::backdrop {
      background: rgba(15, 29, 48, .58);
      backdrop-filter: blur(4px);
    }
    .contact-dialog-inner {
      position: relative;
      padding: clamp(1.5rem, 4vw, 2.25rem);
    }
    .contact-dialog-close {
      position: absolute;
      top: 1rem;
      right: 1rem;
      width: 40px;
      height: 40px;
      padding: 0;
      cursor: pointer;
      color: var(--text-muted);
      background: var(--surface-muted);
      border: 0;
      border-radius: 999px;
      font: inherit;
      font-size: 1.25rem;
    }
    .contact-dialog h2 {
      margin-right: 3rem;
      margin-bottom: .75rem;
      font-size: clamp(1.8rem, 5vw, 2.6rem);
    }
    .contact-dialog-intro {
      margin-bottom: 1.5rem;
      color: var(--text-muted);
    }
    .contact-form {
      display: grid;
      gap: 1rem;
    }
    .contact-form-row {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
    }
    .contact-form label {
      display: grid;
      gap: .4rem;
      font-size: .88rem;
      font-weight: 700;
    }
    .contact-form input,
    .contact-form select,
    .contact-form textarea {
      width: 100%;
      min-height: 48px;
      padding: .75rem .85rem;
      color: var(--text);
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 10px;
      font: inherit;
    }
    .contact-form textarea {
      min-height: 130px;
      resize: vertical;
    }
    .contact-form .button {
      width: max-content;
      cursor: pointer;
    }
    .contact-form-note {
      margin: 0;
      color: var(--text-muted);
      font-size: .78rem;
    }
    @media (max-width: 560px) {
      .contact-form-row {
        grid-template-columns: 1fr;
      }
    }
  `;
  document.head.appendChild(modalStyles);

  const contactDialog = document.createElement('dialog');
  contactDialog.className = 'contact-dialog';
  contactDialog.setAttribute('aria-labelledby', 'contact-dialog-title');
  contactDialog.innerHTML = `
    <div class="contact-dialog-inner">
      <button class="contact-dialog-close" type="button" aria-label="Close contact form">×</button>
      <p class="eyebrow">Contact Neverlost Systems</p>
      <h2 id="contact-dialog-title">Start a focused conversation.</h2>
      <p class="contact-dialog-intro">Tell us a little about what you’re working on and why you’re reaching out.</p>
      <form class="contact-form" action="https://formsubmit.co/neverlostsells@gmail.com" method="POST">
        <input type="hidden" name="_subject" value="New Neverlost Systems website inquiry">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" value="https://neverlostsystems.com/?sent=1#partnerships">
        <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
        <div class="contact-form-row">
          <label>Name
            <input type="text" name="name" autocomplete="name" required>
          </label>
          <label>Email
            <input type="email" name="email" autocomplete="email" required>
          </label>
        </div>
        <label>Organization <span style="font-weight:500;color:var(--text-muted);">(optional)</span>
          <input type="text" name="organization" autocomplete="organization">
        </label>
        <label>Reason for reaching out
          <select name="reason" required>
            <option value="" selected disabled>Select a topic</option>
            <option>Research collaboration</option>
            <option>Pilot partnership</option>
            <option>Technical collaboration</option>
            <option>Funding or strategic partnership</option>
            <option>Patient advocacy inquiry</option>
            <option>Other</option>
          </select>
        </label>
        <label>Message
          <textarea name="message" required></textarea>
        </label>
        <button class="button button-primary" type="submit">Send message</button>
        <p class="contact-form-note">Please do not submit sensitive medical, legal, financial, or other private records through this form.</p>
      </form>
    </div>
  `;
  document.body.appendChild(contactDialog);

  const contactClose = contactDialog.querySelector('.contact-dialog-close');

  contactOpen.addEventListener('click', (event) => {
    event.preventDefault();
    contactDialog.showModal();
  });

  contactClose.addEventListener('click', () => contactDialog.close());

  contactDialog.addEventListener('click', (event) => {
    if (event.target === contactDialog) {
      contactDialog.close();
    }
  });
}
