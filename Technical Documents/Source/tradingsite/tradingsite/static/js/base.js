const body = document.querySelector("body"),
      menuBtn = document.querySelector(".menu-button"),
      sidebar= document.querySelector(".sidebar"),
      backBtn = document.querySelector(".back"),
      darkBtn = document.querySelector(".mode-button");

      menuBtn.addEventListener("click", () =>{
          sidebar.classList.add("open");
          sidebar.classList.remove("close");
      })
      backBtn.addEventListener("click", () =>{
          sidebar.classList.remove("open");
          sidebar.classList.add("close");
      })
function toggleMode(mode) {
  const body = document.body;
  body.classList.toggle('light', mode === 'light');
  body.classList.toggle('dark', mode === 'dark');
}

// Saves the toggled mode to the local storage
function setModePreference(mode) {
  localStorage.setItem('mode', mode);
}

function getModePreference() {
  return localStorage.getItem('mode');
}

const modeSaved = getModePreference();

if (modeSaved) {
  toggleMode(modeSaved);
}

// Listen for clicks on a button that toggles between light and dark mode
document.getElementById('toggle').addEventListener('click', function() {
  const body = document.body;
  if (body.classList.contains('light')) {
      toggleMode('dark');
      setModePreference('dark');
  } else {
      toggleMode('light');
      setModePreference('light');
  }
});
document.addEventListener('click', function(event) {
  const sidebar = document.querySelector('.sidebar');
  const sidebarOpenClick = event.target.closest('.menu-button');
  const sidebarClick = event.target.closest('.sidebar');
  if (!sidebarClick && !sidebarOpenClick && !sidebar.classList.contains('close')) {
    sidebar.classList.remove("open");
    sidebar.classList.add('close');
  }
});