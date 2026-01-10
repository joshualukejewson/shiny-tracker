function toggleShiny(img) {
  const normal = img.dataset.normal;
  const shiny = img.dataset.shiny;

  img.src = img.src.includes(shiny) ? normal : shiny;
}

function setActionForm(action) {
  let form = document.getElementById("auth-form");
  if (!form) return;
  if (action === "login") {
    form.action = form.dataset.loginUrl;
  } else if (action === "register") {
    form.action = form.dataset.registerUrl;
  }
  form.method = "post";
  form.submit();
}

const showButton = document.getElementById('showDialog');
const closeButton = document.getElementById('closeDialog');
const dialog = document.getElementById('settingsDialog');

// Open the modal dialog
showButton.addEventListener('click', () => {
  dialog.showModal();
});

// Close the dialog
closeButton.addEventListener('click', () => {
  dialog.close();
});

