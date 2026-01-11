document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("lux-slider");
  const valueEl = document.getElementById("lux-slider-value");
  if (!slider || !valueEl) return;
  const updateUI = () => {
    const percent = (slider.value - slider.min) / (slider.max - slider.min) * 100;
    slider.style.setProperty("--fill", `${percent}%`);
    valueEl.textContent = slider.value;
  };
  updateUI();
  slider.addEventListener("input", () => {
    updateUI();
    message = {
      "manual_duty" : parseInt(slider.value)
    }
    publishMessage(message)
  });
});
