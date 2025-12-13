// suppliersearch.js - working supplier autocomplete + search + clear
(function () {

  document.addEventListener("DOMContentLoaded", function () {

    // Inputs
    const input = document.getElementById("vendorNameInput");
    const suggestionBox = document.getElementById("vendorNameSuggestions");
    const searchButton = document.getElementById("searchButton");
    const clearButton = document.getElementById("clearButton");
    const categorySelect = document.getElementById("categorySelect");
    const statusSelect = document.getElementById("statusSelect");

    console.log("suppliersearch.js loaded");

    // ✔ FIXED — CORRECT URL ALWAYS WORKS
    const SUPPLIER_SUGGEST_URL = "/ajserp/supliers/suggest-name/";

    // ESCAPE
    function escapeHtml(s) {
      return (s || "").replace(/[&<>"]/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"
      }[c]));
    }

    // SHOW SUGGESTIONS (correct function name)
    function showSuggestions(list) {
      if (!suggestionBox) return;

      suggestionBox.innerHTML = "";

      if (!list || !list.length) {
        suggestionBox.style.display = "none";
        return;
      }

      list.forEach(item => {
        const a = document.createElement("a");
        a.href = "#";
        a.className = "list-group-item list-group-item-action";
        a.style.cursor = "pointer";

        a.innerHTML = `
          <strong>${escapeHtml(item.name)}</strong>
          ${item.contact ? `<div class="small text-muted">${escapeHtml(item.contact)}</div>` : ""}
        `;

        a.addEventListener("click", function (e) {
          e.preventDefault();
          input.value = item.name;
          suggestionBox.style.display = "none";
        });

        suggestionBox.appendChild(a);
      });

      suggestionBox.style.display = "block";
    }

    // Debounce
    function debounce(fn, wait) {
      let t;
      return function () {
        clearTimeout(t);
        t = setTimeout(() => fn.apply(this, arguments), wait);
      };
    }

    // FETCH SUGGESTIONS
    async function fetchSuggestions(q) {
      if (!q) return showSuggestions([]);

      try {
        const res = await fetch(`${SUPPLIER_SUGGEST_URL}?q=${encodeURIComponent(q)}`);
        const data = await res.json();
        console.log("Fetched:", data);
        showSuggestions(data.results || []);
      } catch (err) {
        console.error("Error:", err);
        showSuggestions([]);
      }
    }

    const debouncedFetch = debounce(fetchSuggestions, 200);

    // INPUT EVENT
    if (input) {
      input.addEventListener("input", function () {
        const q = input.value.trim();
        if (!q) {
          suggestionBox.style.display = "none";
          return;
        }
        debouncedFetch(q);
      });
    }

    // OUTSIDE CLICK → HIDE
    document.addEventListener("click", function (e) {
      if (suggestionBox && e.target !== input && !suggestionBox.contains(e.target)) {
        suggestionBox.style.display = "none";
      }
    });

    // SEARCH FUNCTION
    function doSearch(nameValue) {
      const url = new URL(window.location.href);
      url.searchParams.set("name", nameValue || "");

      if (categorySelect && categorySelect.value)
        url.searchParams.set("category", categorySelect.value);
      else
        url.searchParams.delete("category");

      if (statusSelect && statusSelect.value)
        url.searchParams.set("status", statusSelect.value);
      else
        url.searchParams.delete("status");

      window.location.href = url.toString();
    }

    // SEARCH BUTTON
    if (searchButton) {
      searchButton.addEventListener("click", function () {
        doSearch(input.value.trim());
      });
    }

    // ENTER KEY SEARCH
    if (input) {
      input.addEventListener("keyup", function (e) {
        if (e.key === "Enter") {
          doSearch(input.value.trim());
        }
      });
    }

    // CLEAR BUTTON
    if (clearButton) {
      clearButton.addEventListener("click", function () {
        input.value = "";
        if (categorySelect) categorySelect.value = "";
        if (statusSelect) statusSelect.value = "";
        suggestionBox.style.display = "none";

        window.location.href = "/ajserp/supliers/";
      });
    }

    console.log("suppliersearch.js initialized successfully");

  });

})();
