const navToggle = document.querySelector('.nav-toggle');
const primaryNav = document.querySelector('.primary-nav');
const siteHeader = document.querySelector('.site-header');
const year = document.querySelector('#year');
const brandMark = document.querySelector('.brand-mark');
const runtimeScript = document.currentScript;
const siteBaseUrl = new URL('.', runtimeScript?.src || window.location.href);

if (!document.querySelector('link[href$="brand-refresh.css"]')) {
  const brandStylesheet = document.createElement('link');
  brandStylesheet.rel = 'stylesheet';
  brandStylesheet.href = new URL('brand-refresh.css', siteBaseUrl).href;
  document.head.appendChild(brandStylesheet);
}

if (!document.querySelector('link[rel~="icon"]')) {
  const favicon = document.createElement('link');
  favicon.rel = 'icon';
  favicon.type = 'image/svg+xml';
  favicon.href = new URL('assets/nvlt-official-logo.svg', siteBaseUrl).href;
  document.head.appendChild(favicon);
}

if (brandMark) {
  const logo = document.createElement('img');
  logo.className = 'brand-logo';
  logo.src = new URL('assets/nvlt-official-logo.svg', siteBaseUrl).href;
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

document.addEventListener('click', (event) => {
  const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
  if (!link || typeof window.gtag !== 'function') return;

  let destination;
  try {
    destination = new URL(link.getAttribute('href'), window.location.href);
  } catch (_) {
    return;
  }

  if (destination.origin !== window.location.origin) return;

  const current = new URL(window.location.href);
  const sameDocumentHash =
    destination.pathname === current.pathname &&
    destination.search === current.search &&
    Boolean(destination.hash);
  const pageNavigation =
    destination.pathname !== current.pathname ||
    destination.search !== current.search;

  if (!sameDocumentHash && !pageNavigation) return;

  const linkText = link.textContent.replace(/\s+/g, ' ').trim().slice(0, 100);
  const navigationArea = link.closest('.primary-nav')
    ? 'primary_nav'
    : link.closest('.hero-actions')
      ? 'hero'
      : 'content';

  window.gtag('event', 'internal_navigation', {
    link_text: linkText,
    link_url: destination.href,
    destination_path: `${destination.pathname}${destination.search}${destination.hash}`,
    destination_section: destination.hash ? destination.hash.slice(1) : 'page',
    navigation_area: navigationArea
  });
});

if (siteHeader) {
  const topThreshold = 8;
  const directionThreshold = 12;
  let lastScrollY = Math.max(window.scrollY, 0);
  let scrollTicking = false;

  const revealHeader = () => siteHeader.classList.remove('is-scroll-hidden');

  const updateHeaderVisibility = () => {
    const currentScrollY = Math.max(window.scrollY, 0);
    const scrollDelta = currentScrollY - lastScrollY;

    if (currentScrollY <= topThreshold) {
      revealHeader();
      lastScrollY = currentScrollY;
    } else if (Math.abs(scrollDelta) >= directionThreshold) {
      const menuIsOpen = primaryNav?.classList.contains('is-open');

      if (scrollDelta > 0 && !menuIsOpen) {
        siteHeader.classList.add('is-scroll-hidden');
      } else if (scrollDelta < 0) {
        revealHeader();
      }

      lastScrollY = currentScrollY;
    }

    scrollTicking = false;
  };

  window.addEventListener('scroll', () => {
    if (!scrollTicking) {
      window.requestAnimationFrame(updateHeaderVisibility);
      scrollTicking = true;
    }
  }, { passive: true });

  siteHeader.addEventListener('focusin', revealHeader);
}

const caseScreenshots = Array.from(document.querySelectorAll('.case-proof-card img'));

if (caseScreenshots.length) {
  const lightboxStyles = document.createElement('style');
  lightboxStyles.textContent = `
    .case-proof-card img {
      cursor: zoom-in;
    }
    .case-proof-card img:focus-visible {
      outline: 3px solid var(--brand);
      outline-offset: -3px;
    }
    .image-lightbox {
      width: min(96vw, 1500px);
      max-width: none;
      max-height: 96vh;
      margin: auto;
      padding: 0;
      overflow: visible;
      background: transparent;
      border: 0;
    }
    .image-lightbox::backdrop {
      background: rgba(5, 12, 24, .9);
      backdrop-filter: blur(5px);
    }
    .image-lightbox-shell {
      position: relative;
      display: flex;
      max-height: 94vh;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: .8rem;
      padding: 0 4.25rem;
    }
    .image-lightbox-image {
      display: block;
      max-width: min(86vw, 1380px);
      max-height: 82vh;
      width: auto;
      height: auto;
      object-fit: contain;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 24px 90px rgba(0, 0, 0, .45);
    }
    .image-lightbox-caption {
      max-width: min(88vw, 900px);
      margin: 0;
      color: #f5f8fc;
      font-size: .92rem;
      text-align: center;
    }
    .image-lightbox-close,
    .image-lightbox-nav {
      display: grid;
      place-items: center;
      padding: 0;
      cursor: pointer;
      color: #fff;
      background: rgba(15, 29, 48, .88);
      border: 1px solid rgba(255, 255, 255, .28);
      border-radius: 999px;
      font: inherit;
      line-height: 1;
    }
    .image-lightbox-close {
      position: fixed;
      top: max(1rem, env(safe-area-inset-top));
      right: max(1rem, env(safe-area-inset-right));
      z-index: 3;
      width: 46px;
      height: 46px;
      font-size: 1.5rem;
    }
    .image-lightbox-nav {
      position: absolute;
      top: 50%;
      z-index: 2;
      width: 52px;
      height: 52px;
      transform: translateY(-50%);
      font-size: 2rem;
    }
    .image-lightbox-prev {
      left: .35rem;
    }
    .image-lightbox-next {
      right: .35rem;
    }
    .image-lightbox-nav:hover,
    .image-lightbox-nav:focus-visible,
    .image-lightbox-close:hover,
    .image-lightbox-close:focus-visible {
      background: rgba(19, 87, 212, .96);
      outline: none;
    }
    .image-lightbox-hint {
      margin: 0;
      color: rgba(245, 248, 252, .7);
      font-size: .76rem;
      text-align: center;
    }
    @media (max-width: 640px) {
      .image-lightbox-shell {
        padding: 0 3rem;
      }
      .image-lightbox-nav {
        width: 42px;
        height: 42px;
        font-size: 1.6rem;
      }
      .image-lightbox-image {
        max-width: 88vw;
        max-height: 76vh;
      }
    }
  `;
  document.head.appendChild(lightboxStyles);

  const lightbox = document.createElement('dialog');
  lightbox.className = 'image-lightbox';
  lightbox.setAttribute('aria-label', 'Expanded Case Navigator screenshot gallery');
  lightbox.innerHTML = `
    <div class="image-lightbox-shell">
      <button class="image-lightbox-close" type="button" aria-label="Close expanded screenshot">×</button>
      <button class="image-lightbox-nav image-lightbox-prev" type="button" aria-label="Previous screenshot">‹</button>
      <img class="image-lightbox-image" alt="">
      <button class="image-lightbox-nav image-lightbox-next" type="button" aria-label="Next screenshot">›</button>
      <p class="image-lightbox-caption"></p>
      <p class="image-lightbox-hint">Use the arrow buttons or ← / → keys to browse. Press Escape or click outside to close.</p>
    </div>
  `;
  document.body.appendChild(lightbox);

  const lightboxImage = lightbox.querySelector('.image-lightbox-image');
  const lightboxCaption = lightbox.querySelector('.image-lightbox-caption');
  const lightboxClose = lightbox.querySelector('.image-lightbox-close');
  const lightboxPrev = lightbox.querySelector('.image-lightbox-prev');
  const lightboxNext = lightbox.querySelector('.image-lightbox-next');
  let lastTrigger = null;
  let currentIndex = 0;

  const showScreenshot = (index) => {
    currentIndex = (index + caseScreenshots.length) % caseScreenshots.length;
    const image = caseScreenshots[currentIndex];
    const card = image.closest('.case-proof-card');
    const caption = card ? card.querySelector('figcaption') : null;

    lightboxImage.src = image.currentSrc || image.src;
    lightboxImage.alt = image.alt;
    lightboxCaption.textContent = `${currentIndex + 1} of ${caseScreenshots.length} · ${caption ? caption.textContent.trim() : image.alt}`;
  };

  const openLightbox = (image) => {
    const index = caseScreenshots.indexOf(image);
    lastTrigger = image;
    showScreenshot(index >= 0 ? index : 0);
    lightbox.showModal();
    lightboxClose.focus();
  };

  const closeLightbox = () => {
    if (lightbox.open) {
      lightbox.close();
    }
  };

  const showPrevious = () => showScreenshot(currentIndex - 1);
  const showNext = () => showScreenshot(currentIndex + 1);

  caseScreenshots.forEach((image) => {
    image.tabIndex = 0;
    image.setAttribute('role', 'button');
    image.setAttribute('aria-label', `${image.alt}. Open full-size image.`);

    image.addEventListener('click', () => openLightbox(image));
    image.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openLightbox(image);
      }
    });
  });

  lightboxPrev.addEventListener('click', showPrevious);
  lightboxNext.addEventListener('click', showNext);
  lightboxClose.addEventListener('click', closeLightbox);

  lightbox.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      showPrevious();
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      showNext();
    }
  });

  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  lightbox.addEventListener('close', () => {
    lightboxImage.removeAttribute('src');
    if (lastTrigger) {
      lastTrigger.focus();
    }
  });
}
