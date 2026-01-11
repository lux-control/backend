document.addEventListener("DOMContentLoaded", () => {
  const presetRadios = document.querySelectorAll(
    'input[type="radio"][name="lux_preset"]'
  );

  presetRadios.forEach((radio) => {
    radio.addEventListener("change", () => {
      if (!radio.checked) return;

      message = {
        "target_lux": parseFloat(target_lux[radio.value]) 
      }
      console.log(message)
      publishMessage(message)
    });
  });
});