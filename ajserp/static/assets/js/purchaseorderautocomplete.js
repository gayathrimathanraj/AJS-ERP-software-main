console.log("purchaseorderautocomplete.js loaded");

// =====================================================================
// GLOBAL VARIABLES
// =====================================================================
let typingTimer;
const doneTypingInterval = 300;

// =====================================================================
// PAGE INITIALIZATION
// =====================================================================
$(document).ready(function () {
    console.log("📌 Initializing Purchase Order JS");

    const currentPath = window.location.pathname;
    if (!currentPath.includes("purchaseorder") && !currentPath.includes("addpurchaseorder")) {
        return;
    }

    initializeDateFields();
    initializeExistingRows();
    initializeMaterialAutocomplete();
    initializeVendorAutocomplete();
    initializeWarehouseAutocomplete();
    updateSerialNumbers();

    // Hide dropdowns when clicking outside
    $(document).click(function (e) {
        if (
            !$(e.target).closest("#vendor_search").length &&
            !$(e.target).closest("#vendor_suggestions").length &&
            !$(e.target).closest("#warehouse_search").length &&
            !$(e.target).closest("#warehouse_suggestions").length &&
            !$(e.target).closest(".row-suggestions-dropdown").length
        ) {
            $("#vendor_suggestions, #warehouse_suggestions, .row-suggestions-dropdown").hide();
        }
    });
});

// =====================================================================
// 1️⃣ ADD EMPTY ROW
// =====================================================================
function addEmptyRow() {
    console.log("➕ Adding new row");

    const tBody = $("#purchase-order-items-body");
    const lastRow = tBody.find(".line-item-row").last();

    if (lastRow.length === 0) return;

    const newRow = lastRow.clone();

    newRow.find("input[type='text'], input[type='number']").val("");
    newRow.find(".quantity").val("1");
    newRow.find(".discount").val("0");
    newRow.find(".mrp").val("0");

    newRow.find(".material-name").val("").hide();
    newRow.find(".material-search").val("").show();

    newRow.find("input[type='hidden']").val("");

    tBody.append(newRow);

    initializeMaterialAutocomplete();
    updateSerialNumbers();

    console.log("✅ New row added");
}

window.addEmptyRow = addEmptyRow;

// =====================================================================
// 2️⃣ MATERIAL AUTOCOMPLETE
// =====================================================================
function initializeMaterialAutocomplete() {
    console.log("🔄 Initializing material autocomplete");

    $(".material-search").off("input.row_autocomplete");

    $(".material-search").each(function () {
        const materialInput = $(this);
        const row = materialInput.closest("tr");
        const suggestionsDiv = materialInput.siblings(".row-suggestions-dropdown");

        materialInput.on("input.row_autocomplete", function () {
            const query = materialInput.val().trim();

            if (!query) {
                suggestionsDiv.hide().empty();
                return;
            }

            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                performMaterialAutocomplete(query, suggestionsDiv, row);
            }, doneTypingInterval);
        });
    });
}

function performMaterialAutocomplete(query, suggestionsDiv, row) {
    console.log("📡 Row Material Search:", query);

    $.ajax({
        url: "/ajserp/api/materialestimate-autocomplete/",
        data: { q: query },
        dataType: "json",
        success: function (data) {
            suggestionsDiv.empty();

            if (!data.length) {
                suggestionsDiv.html('<div class="p-2 text-muted">No results</div>').show();
                return;
            }

            data.forEach((item) => {
                const element = `
                    <div class="row-suggestion-item p-2 border-bottom"
                        data-material='${JSON.stringify(item)}'
                        style="cursor:pointer;">
                        <b>${item.material_name}</b><br>
                        <small>${item.material_code} - ₹${item.mrp}</small>
                    </div>`;

                suggestionsDiv.append(element);
            });

            suggestionsDiv.show();
        }
    });
}

// SELECT MATERIAL
$(document).on("click", ".row-suggestion-item", function () {
    const material = $(this).data("material");
    const row = $(this).closest("tr");

    row.find(".material-name").val(material.material_name).show();
    row.find(".material-search").hide();

    row.find(".mrp").val(material.mrp);
    row.find(".quantity").val(1);
    row.find(".discount").val(0);
    row.find("input[name='hsn_code[]']").val(material.hsn_code);

    getTaxRates(material.hsn_code).then((rates) => {
        row.find(".cgst-rate").val(rates.cgst);
        row.find(".sgst-rate").val(rates.sgst);
        row.find(".igst-rate").val(rates.igst);
        row.find(".cess-rate").val(rates.cess);

        calculatePurchaseOrderWithBackend();
    });

    $(this).parent().hide();
});

// =====================================================================
// 3️⃣ TAX RATE LOOKUP
// =====================================================================
function getTaxRates(hsnCode) {
    return new Promise((resolve) => {
        $.ajax({
            url: "/ajserp/api/get-tax-rates/",
            data: { hsn_code: hsnCode },
            dataType: "json",
            success: function (data) {
                resolve(data.success ? data : { cgst: 9, sgst: 9, igst: 18, cess: 0 });
            },
            error: () => resolve({ cgst: 9, sgst: 9, igst: 18, cess: 0 })
        });
    });
}

// =====================================================================
// 4️⃣ VENDOR AUTOCOMPLETE (FINAL WORKING VERSION)
// =====================================================================
// Vendor autocomplete — DROP INTO purchaseorderautocomplete.js or a separate file
(function () {
  // Debounce helper
  function debounce(fn, delay) {
    let t;
    return function () {
      const args = arguments;
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  // Build suggestion HTML safely
  function makeSuggestionHtml(v) {
    const name = (v.vendor_name || v.text || "").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const code = (v.vendor_code || v.value || "").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const display = `${name} ${code ? `(${code})` : ""}`;
    return `<div class="vendor-item suggestion-item p-2" data-code="${code}" data-name="${name}" tabindex="0" style="cursor:pointer;">${display}</div>`;
  }

  // Main initializer
  function initializeVendorAutocomplete() {
    console.log("🔧 initializeVendorAutocomplete: starting");

    const $input = $("#vendor_search");
    const $box = $("#vendor_suggestions");

    if ($input.length === 0) {
      console.warn("⚠️ initializeVendorAutocomplete: #vendor_search not found");
      return;
    }
    if ($box.length === 0) {
      console.warn("⚠️ initializeVendorAutocomplete: #vendor_suggestions not found");
      return;
    }

    // Hide suggestions
    function hideBox() {
      $box.hide().empty();
      $input.removeAttr("aria-activedescendant");
    }

    // Show "no results"
    function showNoResults() {
      $box.html('<div class="p-2 text-muted">No vendors found</div>').show();
    }

    // Fetch suggestions
    const fetchSuggestions = debounce(function () {
      const q = $input.val().trim();
      if (!q) { hideBox(); return; }

      console.log("🔍 vendor query:", q);
      $.ajax({
        url: "/ajserp/api/vendor-search-po/",
        method: "GET",
        data: { q: q },
        dataType: "json",
        success: function (data) {
          console.log("🔍 vendor response:", data);
          if (!Array.isArray(data) || data.length === 0) {
            showNoResults();
            return;
          }
          const html = data.map(makeSuggestionHtml).join("");
          $box.html(html).show();
        },
        error: function (xhr, status, err) {
          console.error("❌ vendor autocomplete error:", status, err);
          hideBox();
        }
      });
    }, 250);

    // Input events
    $input.off(".vendorAuto").on("input.vendorAuto", function () {
      fetchSuggestions();
    });

    // Click selection (delegated)
    $(document).off("click.vendorSelect", ".vendor-item").on("click.vendorSelect", ".vendor-item", function () {
      const $el = $(this);
      const name = $el.data("name") || "";
      const code = $el.data("code") || "";

      $input.val(name);
      $("#vendor_code").val(code);
      hideBox();
      console.log("✅ vendor selected:", name, code);

      // autofill addresses (if you still want to call the details API, you can — but the new vendor_search_po view already returns addresses if you encoded them)
      $.ajax({
        url: "/ajserp/api/vendor-details-po/",
        data: { vendor_code: code },
        dataType: "json",
        success: function (res) {
          if (res && res.success) {
            $("#billing_address1").val(res.billing_address1 || "");
            $("#billing_address2").val(res.billing_address2 || "");
            $("#billing_city").val(res.billing_city || "");
            $("#billing_state").val(res.billing_state || "");
            $("#billing_postal_code").val(res.billing_postal_code || "");
          }
        },
        error: function () { /* optional fallback */ }
      });
    });

    // Keyboard navigation inside suggestions
    $input.off("keydown.vendorKeys").on("keydown.vendorKeys", function (e) {
      const visibleItems = $box.find(".vendor-item:visible");
      if (!visibleItems.length) return;

      const active = $box.find(".vendor-item.active");
      let idx = active.length ? visibleItems.index(active) : -1;

      if (e.key === "ArrowDown") {
        e.preventDefault();
        idx = Math.min(visibleItems.length - 1, idx + 1);
        visibleItems.removeClass("active").eq(idx).addClass("active").focus();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        idx = Math.max(0, idx - 1);
        visibleItems.removeClass("active").eq(idx).addClass("active").focus();
      } else if (e.key === "Enter") {
        if (idx >= 0) {
          e.preventDefault();
          visibleItems.eq(idx).trigger("click");
        }
      } else if (e.key === "Escape") {
        hideBox();
      }
    });

    // Close when clicking outside
    $(document).on("click.vendorOutside", function (e) {
      if (!$(e.target).closest("#vendor_search, #vendor_suggestions").length) hideBox();
    });

    console.log("🔧 initializeVendorAutocomplete: ready");
  }

  // Expose initializer and call on DOM ready
  $(document).ready(function () {
    initializeVendorAutocomplete();
  });

  // allow manual re-init for debugging
  window.initializeVendorAutocomplete = initializeVendorAutocomplete;
})();

// =====================================================================
// 5️⃣ WAREHOUSE AUTOCOMPLETE
// =====================================================================
function initializeWarehouseAutocomplete() {
    $("#warehouse_search").on("input", function () {
        let query = $(this).val().trim();

        if (!query) {
            $("#warehouse_suggestions").hide().empty();
            return;
        }

        $.ajax({
            url: "/ajserp/api/warehouse-autocomplete/",
            data: { q: query },
            success: function (data) {
                let list = "";

                data.forEach(w => {
                    list += `
                        <div class="suggestion-item p-2"
                             data-name="${w.warehouse_name}"
                             data-code="${w.warehouse_code}">
                             ${w.warehouse_name} (${w.warehouse_code})
                        </div>`;
                });

                $("#warehouse_suggestions").html(list).show();
            }
        });
    });

    $(document).on("click", "#warehouse_suggestions .suggestion-item", function () {
        $("#warehouse_search").val($(this).data("name"));
        $("#warehouse_code").val($(this).data("code"));
        $("#warehouse_suggestions").hide();
    });
}

// =====================================================================
// 6️⃣ BACKEND CALCULATION
// =====================================================================
function calculatePurchaseOrderWithBackend() {
    console.log("🔄 Calculating Purchase...");

    const saveBtn = $(".btn-success");
    saveBtn.prop("disabled", true).text("Calculating...");

    const lineItems = [];

    $(".line-item-row").each(function () {
        const row = $(this);
        const materialName = row.find(".material-name").val();
        if (!materialName) return;

        lineItems.push({
            material_name: materialName,
            quantity: parseFloat(row.find(".quantity").val()) || 0,
            mrp: parseFloat(row.find(".mrp").val()) || 0,
            discount: parseFloat(row.find(".discount").val()) || 0,
            hsn_code: row.find("input[name='hsn_code[]']").val()
        });
    });

    if (!lineItems.length) {
        alert("Add at least one material!");
        saveBtn.prop("disabled", false).text("Save");
        return;
    }

    $.ajax({
        url: "/ajserp/create_purchase_order/",
        method: "POST",
        contentType: "application/json",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        data: JSON.stringify({
            line_items: lineItems,
            round_off: parseFloat($("#round-off").val()) || 0
        }),
        success: function (response) {
            if (!response.success) {
                alert("Error: " + response.error);
                return;
            }

            response.line_items.forEach((item, index) => {
                const row = $(".line-item-row").eq(index);
                row.find(".basic-amount").val(item.basic_amount.toFixed(2));
                row.find(".tax-amount").val(item.tax_amount.toFixed(2));
                row.find(".final-amount").val(item.final_amount.toFixed(2));
            });

            $("#taxable-amount-display").val(response.totals.taxable_amount.toFixed(2));
            $("#cgst-value-display").val(response.totals.cgst_total.toFixed(2));
            $("#sgst-value-display").val(response.totals.sgst_total.toFixed(2));
            $("#igst-value-display").val(response.totals.igst_total.toFixed(2));
            $("#cess-value-display").val(response.totals.cess_total.toFixed(2));
            $("#grand-total-display").val(response.totals.grand_total.toFixed(2));

            console.log("✅ Calculation Completed!");
        },
        error: function () {
            alert("Calculation failed!");
        },
        complete: function () {
            saveBtn.prop("disabled", false).text("Save");
        }
    });
}

window.calculatePurchaseOrderWithBackend = calculatePurchaseOrderWithBackend;

// =====================================================================
// COOKIE GETTER
// =====================================================================
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// =====================================================================
// HELPERS
// =====================================================================
function updateSerialNumbers() {
    $(".line-item-row").each(function (i) {
        $(this).find(".serial-number").text(i + 1);
    });
}

function initializeDateFields() {
    const today = new Date().toISOString().split("T")[0];
    const validTill = new Date();
    validTill.setDate(validTill.getDate() + 30);

    $("input[name='date']").val(today);
    $("input[name='valid_till']").val(validTill.toISOString().split("T")[0]);
}

function initializeExistingRows() {
    $(".line-item-row").each(function () {
        // if already filled
    });
}
