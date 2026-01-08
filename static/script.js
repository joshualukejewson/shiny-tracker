function toggleShiny(img) {
    const normal = img.dataset.normal;
    const shiny = img.dataset.shiny;

    img.src = img.src.includes(shiny) ? normal : shiny;
}