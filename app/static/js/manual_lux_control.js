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
    message_payload["manual_lux"] = parseInt(slider.value)
    publishMessage(message_payload)
    console.log(message_payload["manual_lux"])
  });
});
