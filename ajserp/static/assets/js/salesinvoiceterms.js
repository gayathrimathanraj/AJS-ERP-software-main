document.addEventListener("DOMContentLoaded", function () {

  const select = document.getElementById("invoice_terms_template_select");
  const textarea = document.getElementById("invoice_terms_textarea");

  if (!select || !textarea) {
    console.log("❌ Invoice Terms elements not found");
    return;
  }

  select.addEventListener("change", function () {
    const opt = select.options[select.selectedIndex];
    if (!opt) return;

    let text = opt.getAttribute("data-body") || "";

    // ✅ CLEAN ALL ENCODED NEWLINES PROPERLY
    text = text
      .replace(/\\u000A/g, "\n")
      .replace(/\\n/g, "\n")
      .replace(/\\r/g, "")
      .replace(/\\u00A2/g, "")
      .trim();

    // ✅ AUTO-FILL INTO TEXTAREA
    textarea.value = text;
  });

});
