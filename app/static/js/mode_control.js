document.addEventListener("DOMContentLoaded", () => {
  const switchEl = document.getElementById("mode-switch");
  if (!switchEl) return;
  switchEl.addEventListener("change", async (e) => {
        const input = e.target;
        if (!input.classList.contains("mode-input")) return;
        const mode = input.value; // "manual" or "auto"
        console.log("Control mode:", mode);
        // Example: disable manual tiles when auto is on
        const manualBox = document.getElementById("manual-lux-container");
        const autoBox = document.getElementById("power-selector-container");
        if (manualBox) {
            manualBox.style.opacity = (mode === "auto") ? "0.5" : "1";
            manualBox.style.pointerEvents = (mode === "auto") ? "none" : "auto";
        }
        
        if(autoBox) {
            autoBox.style.opacity = (mode === "manual") ? "0.5" : "1";
            autoBox.style.pointerEvents = (mode === "manual") ? "none" : "auto";
        }
    });
});