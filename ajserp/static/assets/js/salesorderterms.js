document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("sales_terms_template_select");
  const textarea = document.getElementById("sales_terms_textarea");

  if (!select || !textarea) return;

  select.addEventListener("change", function () {
    const opt = select.options[select.selectedIndex];
    if (!opt) return;

    let text = opt.getAttribute("data-body") || "";

    text = text
      .replace(/\\u000A/g, "\n")
      .replace(/\\n/g, "\n")
      .replace(/\\r/g, "")
      .replace(/\\u00A2/g, "")
      .trim();

    textarea.value = text;

    console.log("✅ SALES ORDER TERMS SET:", text);
  });
});
