document.addEventListener("DOMContentLoaded", () => {
  const sliders = [
    { el: document.getElementById("lux-slider"), out: document.getElementById("lux-slider-value") },
    { el: document.getElementById("min-lux-slider"), out: document.getElementById("min-lux-value") },
    { el: document.getElementById("max-lux-slider"), out: document.getElementById("max-lux-value") },
  ].filter(x => x.el && x.out);
  const update = (slider, outEl) => {
    const percent = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.setProperty("--fill", `${percent}%`);
    outEl.textContent = slider.value;
  };
  const enforceMinMax = () => {
    const minS = document.getElementById("min-lux-slider");
    const maxS = document.getElementById("max-lux-slider");
    if (minS && maxS && Number(minS.value) > Number(maxS.value)) {
      minS.value = maxS.value;
    }
  };

  const refreshAll = () => {
    enforceMinMax();
    sliders.forEach(s => update(s.el, s.out));
  };
  refreshAll();
  sliders.forEach(s => s.el.addEventListener("input", () => {
    refreshAll()
    message = {
      "min_lux" : parseInt(sliders[1].el.value),
      "max_lux" : parseInt(sliders[2].el.value)
    }
    publishMessage(message)
  }));
});
