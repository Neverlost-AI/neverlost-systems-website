(() => {
  const loaderScript = document.currentScript;
  const baseUrl = new URL('.', loaderScript?.src || window.location.href);

  // Shared navigation, header, and site interactions.
  const coreScript = document.createElement('script');
  coreScript.src = new URL('script-core.js', baseUrl).href;
  coreScript.async = false;
  document.head.appendChild(coreScript);

  const sectionNames = {
    top: 'Home / Hero',
    'encounter-problem': 'Two Perspectives / Encounter Problem',
    'guiding-question': 'What Work Can We Take Off the Patient',
    'initial-product': 'One Connected Healthcare Product',
    'live-demos': 'Fictional Alex Care Walkthrough',
    clinics: 'For Clinics / Discuss a Pilot',
    advocacy: 'POTS and EDS / Pilot Progression',
    about: 'Why I Built Neverlost',
    'neverlost-os': 'Neverlost OS / Shared Infrastructure',
    'early-access': 'Patient Waitlist'
  };

  const sections = Object.keys(sectionNames)
    .map((id, index) => ({
      id,
      index: index + 1,
      element: document.getElementById(id)
    }))
    .filter(({ element }) => element);

  if (!sections.length || typeof IntersectionObserver !== 'function') return;

  const viewedSections = new Set();
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;

      const sectionId = entry.target.id;
      if (!sectionId || viewedSections.has(sectionId)) continue;
      if (typeof window.gtag !== 'function') continue;

      const section = sections.find((item) => item.id === sectionId);
      viewedSections.add(sectionId);

      window.gtag('event', 'section_view', {
        section_id: sectionId,
        section_name: sectionNames[sectionId] || sectionId,
        section_index: section?.index || 0,
        section_path: `${window.location.pathname}${window.location.search}#${sectionId}`,
        page_path: `${window.location.pathname}${window.location.search}`
      });

      observer.unobserve(entry.target);
    }
  }, {
    root: null,
    rootMargin: '-20% 0px -55% 0px',
    threshold: 0
  });

  sections.forEach(({ element }) => observer.observe(element));
})();

