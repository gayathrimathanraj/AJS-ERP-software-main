/* purchaseorderautocomplete.js
   FINAL merged + PO Number Suggestion support
*/

console.log("purchaseorderautocomplete.js loaded — FINAL");

/////////////////////// Utilities ///////////////////////

function debounce(fn, wait = 220) {
  let t;
  return function () {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, arguments), wait);
  };
}

function getCookie(name) {
  const v = `; ${document.cookie || ""}`;
  const parts = v.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

function safeText(s) {
  if (s === null || s === undefined) return "";
  return String(s).replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

/////////////////////// Page Init ///////////////////////

$(document).ready(function () {
  const path = window.location.pathname || "";
  if (!path.includes("purchaseorder") && !path.includes("addpurchaseorder")) return;

  console.log("Init purchaseorderautocomplete.js");

  initDateFields();
  initVendorAutocomplete();
  initWarehouseAutocomplete();
  initMaterialRowAutocomplete();
  initGlobalHandlers();
  bindRowChangeEvents();
  updateSerialNumbers();
});

/////////////////////// Date Fill ///////////////////////

function initDateFields() {
  const today = new Date().toISOString().split("T")[0];
  const valid = new Date();
  valid.setDate(valid.getDate() + 30);

  $("input[name='date']").val(today);
  $("#valid_till").val(valid.toISOString().split("T")[0]);
}

/////////////////////// Serial Numbers ///////////////////////

function updateSerialNumbers() {
  $("#purchase-order-items-body .line-item-row").each(function (i) {
    $(this).find(".serial-number").text(i + 1);
  });
}

/////////////////////// Global Handlers ///////////////////////

function initGlobalHandlers() {
  $(document).on("click.purchaseOrder", function (e) {
    const t = $(e.target);

    if (!t.closest("#vendor_search, #vendor_suggestions").length)
      $("#vendor_suggestions").hide();

    if (!t.closest("#warehouse_search, #warehouse_suggestions").length)
      $("#warehouse_suggestions").hide();

    if (!t.closest(".material-search, .row-suggestions-dropdown").length)
      $(".row-suggestions-dropdown").hide();
  });

  $(document).on("keydown.purchaseOrder", function (e) {
    if (e.key === "Escape") {
      $("#vendor_suggestions, #warehouse_suggestions, .row-suggestions-dropdown").hide();
    }
  });
}

///////////////////////////////////////////////////////////////
//      PURCHASE ORDER NUMBER SUGGESTION  (NEW BLOCK)        //
///////////////////////////////////////////////////////////////

function showPONumberSuggestions(q) {
  if (!q.trim()) {
    $("#poNumberSuggestions").hide();
    return;
  }

  $.ajax({
    url: "/ajserp/api/purchase-orders/suggestions/",
    method: "GET",
    data: { q },
    success: function (data) {
      let box = $("#poNumberSuggestions");
      box.empty();

      if (!data.length) {
        box.hide();
        return;
      }

      data.forEach(item => {
        box.append(`
          <div class="dropdown-item po-suggestion-item"
               data-value="${item.value}">
            ${item.text}
          </div>
        `);
      });

      box.show();
    }
  });
}

// When user selects PO Number
$(document).on("click", ".po-suggestion-item", function () {
  $("#poNumberInput").val($(this).data("value"));
  $("#poNumberSuggestions").hide();
});

/////////////////////// Vendor Autocomplete ///////////////////////

function initVendorAutocomplete() {
  const $input = $("#vendor_search");
  const $box = $("#vendor_suggestions");

  if (!$input.length || !$box.length) return;

  const fetchVendors = debounce(function () {
    const q = $input.val().trim();
    if (!q) return $box.hide().empty();

    $.ajax({
      url: "/ajserp/api/vendor-search-po/",
      method: "GET",
      data: { q },
      success: function (data) {
        $box.empty();

        if (!data.length) {
          $box.html('<div class="p-2 text-muted">No vendors found</div>').show();
          return;
        }

        data.forEach(v => {
          $box.append(`
            <div class="vendor-item p-2 border-bottom" style="cursor:pointer;"
                 data-name="${safeText(v.vendor_name)}"
                 data-code="${safeText(v.vendor_code)}"
                 data-a1="${safeText(v.billing_address1)}"
                 data-a2="${safeText(v.billing_address2)}"
                 data-city="${safeText(v.billing_city)}"
                 data-state="${safeText(v.billing_state)}"
                 data-pincode="${safeText(v.billing_postal_code)}">
              <b>${safeText(v.vendor_name)}</b> (${safeText(v.vendor_code)})
            </div>
          `);
        });

        $box.show();
      }
    });
  }, 200);

  $input.on("input", fetchVendors);

  $(document).on("click", ".vendor-item", function () {
    $("#vendor_search").val($(this).data("name"));
    $("#vendor_code").val($(this).data("code"));

    $("#billing_address1").val($(this).data("a1"));
    $("#billing_address2").val($(this).data("a2"));
    $("#billing_city").val($(this).data("city"));
    $("#billing_state").val($(this).data("state"));
    $("#billing_postal_code").val($(this).data("pincode"));

    $box.hide();
  });
}

/////////////////////// Warehouse Autocomplete ///////////////////////

function initWarehouseAutocomplete() {
  const $input = $("#warehouse_search");
  const $box = $("#warehouse_suggestions");

  const fetchWH = debounce(function () {
    const q = $input.val().trim();
    if (!q) return $box.hide().empty();

    $.ajax({
      url: "/ajserp/api/warehouse-autocomplete/",
      data: { q },
      success: function (data) {
        $box.empty();

        if (!data.length) {
          $box.html(`<div class="p-2 text-muted">No warehouses found</div>`).show();
          return;
        }

        data.forEach(w => {
          $box.append(`
            <div class="wh-item p-2 border-bottom" style="cursor:pointer;"
                 data-name="${safeText(w.warehouse_name)}"
                 data-code="${safeText(w.warehouse_code)}">
              ${safeText(w.warehouse_name)} (${safeText(w.warehouse_code)})
            </div>
          `);
        });

        $box.show();
      }
    });
  }, 180);

  $input.on("input", fetchWH);

  $(document).on("click", ".wh-item", function () {
    $("#warehouse_search").val($(this).data("name"));
    $("#warehouse_code").val($(this).data("code"));
    $box.hide();
  });
}

/////////////////////// Material Autocomplete ///////////////////////

function initMaterialRowAutocomplete() {
  $("#purchase-order-items-body .line-item-row").each(function () {
    initMaterialRowAutocompleteFor($(this));
  });
}

function initMaterialRowAutocompleteFor($row) {
  const $input = $row.find(".material-search");
  const $box = $row.find(".row-suggestions-dropdown");

  const fetchMaterial = debounce(function () {
    const q = $input.val().trim();
    if (!q) return $box.hide().empty();

    $.ajax({
      url: "/ajserp/api/materialestimate-autocomplete/",
      data: { q },
      success: function (data) {
        $box.empty();

        if (!data.length) {
          $box.html('<div class="p-2 text-muted">No results</div>').show();
          return;
        }

        data.forEach(item => {
          $box.append(`
            <div class="row-suggestion-item p-2 border-bottom"
                 style="cursor:pointer;"
                 data-item='${JSON.stringify(item).replace(/'/g, "&#39;")}'>
              <div class="fw-bold">${safeText(item.material_name)}</div>
              <small>${safeText(item.material_code)} - ₹${safeText(item.mrp)}</small>
            </div>
          `);
        });

        $box.show();
      }
    });
  }, 200);

  $input.on("input", fetchMaterial);

  $row.on("click", ".row-suggestion-item", function () {
    const item = JSON.parse($(this).attr("data-item"));

    $row.find(".material-name").val(item.material_name).show();
    $row.find(".material-search").hide();

    $row.find(".mrp").val(item.mrp);
    $row.find(".quantity").val(1);
    $row.find(".discount").val(0);

    $row.find("input[name='hsn_code[]']").val(item.hsn_code);

    getTaxRates(item.hsn_code).then(rates => {
      $row.find(".cgst-rate").val(rates.cgst);
      $row.find(".sgst-rate").val(rates.sgst);
      $row.find(".igst-rate").val(rates.igst);
      $row.find(".cess-rate").val(rates.cess);

      calculatePurchaseOrderWithBackend();
    });

    $box.hide();
  });
}

/////////////////////// Tax Fetch ///////////////////////

function getTaxRates(hsn) {
  return new Promise(resolve => {
    if (!hsn) return resolve({ cgst: 9, sgst: 9, igst: 18, cess: 0 });

    $.ajax({
      url: "/ajserp/api/get-tax-rates/",
      data: { hsn_code: hsn },
      success: function (data) {
        resolve({
          cgst: Number(data.cgst) || 0,
          sgst: Number(data.sgst) || 0,
          igst: Number(data.igst) || 0,
          cess: Number(data.cess) || 0
        });
      },
      error: () => resolve({ cgst: 9, sgst: 9, igst: 18, cess: 0 })
    });
  });
}

/////////////////////// Bind Qty/MRP/Discount ///////////////////////

function bindRowChangeEvents() {
  $("#purchase-order-items-body .line-item-row").each(function () {
    bindRowChangeEventsForRow($(this));
  });
}

function bindRowChangeEventsForRow($row) {
  const handler = debounce(() => calculatePurchaseOrderWithBackend(), 300);

  $row.on("input", "input.quantity, input.mrp, input.discount", handler);
}

/////////////////////// Calculate Purchase Order ///////////////////////

function calculatePurchaseOrderWithBackend() {
  console.log("Calculating purchase order…");

  const line_items = [];

  $("#purchase-order-items-body .line-item-row").each(function () {
    const r = $(this);
    const name = r.find(".material-name").val();

    if (!name) return;

    line_items.push({
      material_name: name,
      quantity: Number(r.find(".quantity").val()) || 0,
      mrp: Number(r.find(".mrp").val()) || 0,
      discount: Number(r.find(".discount").val()) || 0,
      hsn_code: r.find("input[name='hsn_code[]']").val()
    });
  });

  if (!line_items.length) return;

  $.ajax({
    url: "/ajserp/create_purchase_order/",
    method: "POST",
    contentType: "application/json",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    data: JSON.stringify({
      line_items,
      round_off: Number($("#round-off").val()) || 0
    }),
    success: function (res) {
      if (!res.success) return;

      res.line_items.forEach((item, idx) => {
        const row = $("#purchase-order-items-body .line-item-row").eq(idx);

        row.find(".basic-amount").val(item.basic_amount.toFixed(2));
        row.find(".tax-amount").val(item.tax_amount.toFixed(2));
        row.find(".final-amount").val(item.final_amount.toFixed(2));

        row.find(".cgst-amount").val(item.cgst_amount.toFixed(2));
        row.find(".sgst-amount").val(item.sgst_amount.toFixed(2));
        row.find(".igst-amount").val(item.igst_amount ? item.igst_amount.toFixed(2) : "");
        row.find(".cess-amount").val(item.cess_amount ? item.cess_amount.toFixed(2) : "");
      });

      $("#taxable-amount-display").val(res.totals.taxable_amount.toFixed(2));
      $("#cgst-value-display").val(res.totals.cgst_total.toFixed(2));
      $("#sgst-value-display").val(res.totals.sgst_total.toFixed(2));
      $("#igst-value-display").val(res.totals.igst_total ? res.totals.igst_total.toFixed(2) : "");
      $("#cess-value-display").val(res.totals.cess_total ? res.totals.cess_total.toFixed(2) : "");
      $("#grand-total-display").val(res.totals.grand_total.toFixed(2));
    }
  });
}

/////////////////////// END ///////////////////////
