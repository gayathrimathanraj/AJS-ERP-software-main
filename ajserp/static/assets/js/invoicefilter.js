 // 🛑 PAGE DETECTION - INVOICE FILTER JS
console.log('🔄 INVOICE FILTER JS LOADED - CHECKING PAGE');

const currentPath = window.location.pathname;
console.log('🔍 CURRENT URL:', currentPath);

const isRelevantPage = 
    currentPath.includes('/vendorinvoice/') || 
    currentPath.includes('/salesinvoice/') ||
    currentPath.includes('/invoice');

console.log('❓ IS RELEVANT PAGE?', isRelevantPage);

if (!isRelevantPage) {
    console.log('🛑 STOPPING INVOICE FILTER JS - NOT ON CORRECT PAGE');
    return; // Stop execution
}

console.log('✅ INVOICE FILTER JS CONTINUING - CORRECT PAGE');

 
 function toggleDropdown(e) {
        const dropdown = document.getElementById("dropdown");
        dropdown.style.display =
          dropdown.style.display === "block" ? "none" : "block";
        e.stopPropagation();
      }

      // Update tags based on *all checked options*
      function updateTags() {
        const btn = document.getElementById("dropdownBtn");
        const placeholder = document.getElementById("placeholder");
        const allCheckboxes = document.querySelectorAll(
          '#dropdown input[type="checkbox"]:not(#selectAll)'
        );
        const selectAllCheckbox = document.getElementById("selectAll");

        // Build selected array from checked options
        const selected = Array.from(allCheckboxes)
          .filter((cb) => cb.checked)
          .map((cb) => cb.value);

        // Update Select All checkbox
        selectAllCheckbox.checked = selected.length === allCheckboxes.length;

        // Remove existing tags except placeholder
        btn.querySelectorAll("span.tag").forEach((t) => t.remove());

        if (selected.length) {
          placeholder.style.display = "none";
          selected.forEach((val) => {
            const tag = document.createElement("span");
            tag.textContent = val + " ×";
            tag.className = "tag";
            tag.style.background = "#0d6efd";
            tag.style.color = "#fff";
            tag.style.padding = "5px 6px";
            tag.style.borderRadius = "12px";
            tag.style.fontSize = "12px";
            tag.style.cursor = "pointer";
            tag.style.marginRight = "3px";
            tag.onclick = (e) => {
              e.stopPropagation();
              const cb = Array.from(allCheckboxes).find((c) => c.value === val);
              if (cb) cb.checked = false;
              updateTags();
            };
            btn.insertBefore(tag, btn.children[0]);
          });
        } else {
          placeholder.style.display = "inline";
        }
      }

      // Toggle all checkboxes
      function toggleAll(selectAll) {
        const allCheckboxes = document.querySelectorAll(
          '#dropdown input[type="checkbox"]:not(#selectAll)'
        );
        allCheckboxes.forEach((cb) => (cb.checked = selectAll.checked));
        updateTags();
      }

      // Close dropdown when clicking outside
      document.addEventListener("click", function () {
        document.getElementById("dropdown").style.display = "none";
      });