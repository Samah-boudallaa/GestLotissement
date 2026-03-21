document.addEventListener("DOMContentLoaded", function () {
  // == Dark mode toggle (localStorage) ==
  const darkToggle = document.getElementById("dark-toggle");
  const body = document.body;
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") body.classList.add("dark-mode");

  darkToggle?.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
  });

  // == Active nav link ==
  const links = document.querySelectorAll(".main-nav a.nav-link");
  const path = window.location.pathname;
  links.forEach(a => {
    if (a.getAttribute("href") === path || (path === "/" && a.getAttribute("href").endsWith("index"))) {
      a.classList.add("active");
    }
  });

  // == Drag & drop ==
  const dropArea = document.getElementById("drop-area");
  const fileInput = document.getElementById("file-input");
  if (dropArea) {
    ["dragenter","dragover"].forEach(ev => {
      dropArea.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); dropArea.classList.add("dragover"); });
    });
    ["dragleave","drop"].forEach(ev => {
      dropArea.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); dropArea.classList.remove("dragover"); });
    });
    dropArea.addEventListener("drop", e => {
      const dt = e.dataTransfer;
      if (dt.files && dt.files.length) {
        fileInput.files = dt.files;
        showToast("Fichier prêt à être téléchargé.", "info");
      }
    });
  }

  // == Simple toast auto-hide ==
  setTimeout(()=> {
    const toasts = document.querySelectorAll(".toast");
    toasts.forEach(t => {
      t.classList.add("show");
      setTimeout(()=> t.remove(), 5000);
    });
  }, 200);

  // == Search filter for table ==
  const search = document.getElementById("search");
  if (search) {
    search.addEventListener("input", () => {
      const q = search.value.toLowerCase();
      const rows = document.querySelectorAll("#lots-table tbody tr");
      rows.forEach(r => {
        const rowText = r.textContent.toLowerCase();
        r.style.display = rowText.includes(q) ? "" : "none";
      });
    });
  }
});

function showToast(message, type="info") {
  const container = document.getElementById("flashes") || (() => {
    const div = document.createElement("div"); div.id = "flashes"; document.body.appendChild(div); return div;
  })();
  const t = document.createElement("div");
  t.className = `toast ${type}`;
  t.textContent = message;
  container.appendChild(t);
  setTimeout(()=> t.remove(), 5000);
}
