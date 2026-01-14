/**
 * Toggles the Pokémon sprite between normal and shiny versions.
 * @param {HTMLImageElement} img - The image element clicked.
 */
function toggleShiny(img) {
  const normal = img.dataset.normal;
  const shiny = img.dataset.shiny;

  img.src = img.src.includes(shiny) ? normal : shiny;
}

/**
 * Updates the action and submits the auth form for login or registration.
 * @param {string} action - Either "login" or "register".
 */
function setActionForm(action) {
  const form = document.getElementById("auth-form");
  if (!form) return;

  if (action === "login") {
    form.action = form.dataset.loginUrl;
  } else if (action === "register") {
    form.action = form.dataset.registerUrl;
  }

  form.method = "post";
  form.submit();
}

/**
 * Handles showing and closing the settings dialog modal.
 */
(function handleDialog() {
  const showButton = document.getElementById("showDialog");
  const closeButton = document.getElementById("closeDialog");
  const dialog = document.getElementById("settingsDialog");

  if (!showButton || !closeButton || !dialog) return;

  // Open the modal dialog
  showButton.addEventListener("click", () => dialog.showModal());

  // Close the modal dialog
  closeButton.addEventListener("click", () => dialog.close());
})();

/**
 * Handles incrementing and resetting Pokémon encounters via AJAX.
 */
document.addEventListener("DOMContentLoaded", () => {
  const incrementButton = document.getElementById("incrementButton");
  const resetButton = document.getElementById("resetButton");
  const counter = document.getElementById("encounterCount");
  const pokemonCard = document.getElementById("pokemon-card");

  // Exit if required elements are not present
  if (!incrementButton || !resetButton || !counter || !pokemonCard) return;

  const pokemonName = pokemonCard.dataset.pokemonName;

  /**
   * Sends an AJAX request to increment encounters.
   */
  incrementButton.addEventListener("click", async () => {
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "increment", pokemon_name: pokemonName }),
      });
      const data = await response.json();
      counter.textContent = data.encounters;
    } catch (err) {
      console.error("Failed to increment encounters:", err);
    }
  });

  /**
   * Sends an AJAX request to reset encounters.
   */
  resetButton.addEventListener("click", async () => {
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "reset", pokemon_name: pokemonName }),
      });
      const data = await response.json();
      counter.textContent = data.encounters;
    } catch (err) {
      console.error("Failed to reset encounters:", err);
    }
  });
});