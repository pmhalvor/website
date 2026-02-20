(function(){
  // Parallax for background shapes. Assigns different speeds per shape.
  const config = [
    {sel: '.red-rectangle', speed: 0.18},
    {sel: '.blue-circle', speed: 0.32},
    {sel: '.yellow-square', speed: 0.5}
  ];

  const layers = config.map(c => ({el: document.querySelector(c.sel), speed: c.speed})).filter(l => l.el);
  if (!layers.length) return;

  let ticking = false;

  function update() {
    const scrollY = window.scrollY || window.pageYOffset;
    layers.forEach(l => {
      // move down proportionally to scroll, slower than page for depth
      const offset = Math.round(scrollY * l.speed);
      l.el.style.transform = `translateY(${offset}px)`;
    });
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  window.addEventListener('scroll', onScroll, {passive: true});
  // also run once to set initial positions
  update();
})();
