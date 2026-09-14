(() => {
  const loaderScript = document.currentScript;
  const baseUrl = new URL('.', loaderScript?.src || window.location.href);

  // Preserve the existing site behavior in a separate immutable core file.
  const coreScript = document.createElement('script');
  coreScript.src = new URL('script-core.js', baseUrl).href;
  coreScript.async = false;
  document.head.appendChild(coreScript);

  const sectionNames = {
    top: 'Home / Hero',
    why: 'Why Neverlost',
    focus: 'Initial Market',
    'why-ai': 'Why AI',
    products: 'Product Family',
    approach: 'How We Build',
    advocacy: 'Patient Advocacy and Care Navigation',
    work: 'Public Work',
    stage: 'Current Stage',
    validation: 'Customer Discovery',
    about: 'About',
    partnerships: 'Partnerships'
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
