const navToggle = document.querySelector('.nav-toggle');
const primaryNav = document.querySelector('.primary-nav');
const year = document.querySelector('#year');
const brandMark = document.querySelector('.brand-mark');

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
