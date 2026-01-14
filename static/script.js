document.addEventListener("DOMContentLoaded", () => {
  const incrementButton = document.getElementById("incrementButton");
  const resetButton = document.getElementById("resetButton");
  const counter = document.getElementById("encounterCount");
  const pokemonCard = document.getElementById("pokemon-card");

  if (!incrementButton || !resetButton || !counter || !pokemonCard) return;

  const pokemonName = pokemonCard.dataset.pokemonName;

  incrementButton.addEventListener("click", async () => {
    try {
      const response = await fetch("/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "increment",
          pokemon_name: pokemonName,
        }),
      });
      const data = await response.json();
      counter.textContent = data.encounters;
    } catch (err) {
      console.error(err);
    }
  });

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
      console.error(err);
    }
  });

  // Settings dialog
  const showButton = document.getElementById("showDialog");
  const closeButton = document.getElementById("closeDialog");
  const dialog = document.getElementById("settingsDialog");
  if (showButton && closeButton && dialog) {
    showButton.addEventListener("click", () => dialog.showModal());
    closeButton.addEventListener("click", () => dialog.close());
  }
});
