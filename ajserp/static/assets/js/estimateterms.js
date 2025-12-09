document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("terms_template_select");
  const textarea = document.getElementById("terms_textarea");
  const hidden = document.getElementById("terms_hidden");

  if (!select || !textarea || !hidden) return;

  select.addEventListener("change", function () {
    const opt = select.options[select.selectedIndex];
    if (!opt) return;

    let text = opt.getAttribute("data-body") || "";

    // ✅ Clean encoded junk
    text = text
      .replace(/\\u000A/g, "\n")
      .replace(/\\n/g, "\n")
      .replace(/\\r/g, "")
      .replace(/\\u00A2/g, "")
      .trim();

    // ✅ Show in textarea
    textarea.value = text;

    // ✅ SEND TO BACKEND
    hidden.value = text;

    console.log("✅ TERMS SET:", text);
  });
});
