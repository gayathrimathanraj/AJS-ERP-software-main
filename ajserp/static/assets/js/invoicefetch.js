document.addEventListener("DOMContentLoaded", function () {

    let searchInput = document.getElementById("sales_order_search");
    let suggestionsBox = document.getElementById("sales_order_suggestions");
    let hiddenInput = document.getElementById("sales_order_id");

    // -----------------------------
    // AUTOCOMPLETE SEARCH
    // -----------------------------
    searchInput.addEventListener("keyup", function () {
        let query = this.value.trim();
        hiddenInput.value = "";  // reset

        if (query.length < 1) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            return;
        }

        fetch(`/ajserp/salesorder/autocomplete/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                let results = data.results;
                suggestionsBox.innerHTML = "";

                if (results.length === 0) {
                    suggestionsBox.style.display = "none";
                    return;
                }

                results.forEach(item => {
                    let div = document.createElement("div");
                    div.classList.add("suggestion-item");
                    div.style.padding = "6px";
                    div.style.cursor = "pointer";
                    div.style.borderBottom = "1px solid #eee";

                    div.innerHTML = `
                        <b>${item.order_number}</b>
                        <br><small>${item.customer} — ${item.date}</small>
                    `;

                    div.addEventListener("click", function () {
                        searchInput.value = item.order_number;
                        hiddenInput.value = item.id;
                        suggestionsBox.innerHTML = "";
                        suggestionsBox.style.display = "none";

                        loadSalesOrderData(item.id); // 🎯 Auto-fill form
                    });

                    suggestionsBox.appendChild(div);
                });

                suggestionsBox.style.display = "block";
            });
    });

    // Hide dropdown if clicked outside
    document.addEventListener("click", function (event) {
        if (!searchInput.contains(event.target)) {
            suggestionsBox.style.display = "none";
        }
    });



    // -------------------------------------------------------------------
    // AUTO FILL SALES ORDER INTO INVOICE (CUSTOMER, WAREHOUSE, ITEMS)
    // -------------------------------------------------------------------
    function loadSalesOrderData(orderId) {
        let url = `/ajserp/salesorder/${orderId}/json/`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("Sales order not found");
                    return;
                }

                let o = data.order;

                // ---------------- CUSTOMER ----------------
                document.getElementById("customer_search").value = o.customer.name;
                document.getElementById("customer_code").value = o.customer.id;

                document.getElementsByName("billing_address1")[0].value = o.customer.address1;
                document.getElementsByName("billing_address2")[0].value = o.customer.address2;
                document.getElementsByName("billing_city")[0].value = o.customer.city;
                document.getElementsByName("billing_state")[0].value = o.customer.state;
                document.getElementsByName("billing_postal_code")[0].value = o.customer.postal_code;

                // ---------------- WAREHOUSE ----------------
                document.getElementById("warehouse_search").value = o.warehouse.name;
                document.getElementById("warehouse_code").value = o.warehouse.code;

                // ---------------- TERMS ----------------
                document.getElementById("invoice_terms_textarea").value = o.terms_conditions;


                // ---------------- ITEMS ----------------
                let tbody = document.getElementById("sales-invoice-items-body");
                tbody.innerHTML = "";

                o.items.forEach((item, index) => {

                    let rowHTML = `
                    <tr class="line-item-row">

                        <td><span class="serial-number">${index + 1}</span></td>

                        <td>
                            <input type="hidden" name="material_id[]" value="${item.material_id}">
                            <input type="text" class="form-control material-name" name="material_name[]" value="${item.material}">
                        </td>

                        <td>
                            <input type="number" class="form-control quantity" name="quantity[]" 
                                   value="${item.quantity}" step="0.01" min="0">
                        </td>

                        <td>
                            <input type="number" class="form-control mrp" name="mrp[]" 
                                   value="${item.rate}" step="0.01" min="0" readonly>
                        </td>

                        <td>
                            <input type="number" class="form-control discount" name="discount[]" 
                                   value="${item.discount}" step="0.01" min="0">
                        </td>

                        <td><input class="form-control basic-amount" name="basic_amount[]" readonly></td>
                        <td><input class="form-control tax-amount" name="tax_amount[]" readonly></td>
                        <td>
                            <input class="form-control final-amount" name="final_amount[]" readonly>
                        </td>

                    </tr>
                    `;

                    tbody.insertAdjacentHTML("beforeend", rowHTML);
                });

                // After loading all rows → calculate totals
                calculateInvoiceTotals();
            });
    }


    // -----------------------------------------------------
    // ROW CALCULATION + FINAL INVOICE TOTALS
    // -----------------------------------------------------
    function calculateInvoiceTotals() {

        let rows = document.querySelectorAll("#sales-invoice-items-body .line-item-row");

        let taxableTotal = 0;
        let cgstTotal = 0;
        let sgstTotal = 0;
        let igstTotal = 0;
        let cessTotal = 0;
        let finalTotal = 0;

        rows.forEach(row => {
            let qty = parseFloat(row.querySelector(".quantity").value) || 0;
            let rate = parseFloat(row.querySelector(".mrp").value) || 0;
            let disc = parseFloat(row.querySelector(".discount").value) || 0;

            let basic = (qty * rate) - disc;

            let cgst = basic * 0.09;
            let sgst = basic * 0.09;
            let igst = 0;
            let cess = 0;

            let total = basic + cgst + sgst + igst + cess;

            // update UI
            row.querySelector(".basic-amount").value = basic.toFixed(2);
            row.querySelector(".tax-amount").value = (cgst + sgst).toFixed(2);
            row.querySelector(".final-amount").value = total.toFixed(2);

            // totals
            taxableTotal += basic;
            cgstTotal += cgst;
            sgstTotal += sgst;
            igstTotal += igst;
            cessTotal += cess;
            finalTotal += total;
        });

        // Panel update
        document.getElementById("taxable-amount-display").value = taxableTotal.toFixed(2);
        document.getElementById("cgst-value-display").value = cgstTotal.toFixed(2);
        document.getElementById("sgst-value-display").value = sgstTotal.toFixed(2);
        document.getElementById("igst-value-display").value = igstTotal.toFixed(2);
        document.getElementById("cess-value-display").value = cessTotal.toFixed(2);

        // Round off
        let roundOff = parseFloat(document.getElementById("round-off").value) || 0;

        document.getElementById("grand-total-display").value =
            (finalTotal + roundOff).toFixed(2);
    }


    // -----------------------------
    // RECALCULATE ON INPUT CHANGE

    document.addEventListener("input", function (event) {
        if (
            event.target.classList.contains("quantity") ||
            event.target.classList.contains("discount")
        ) {
            calculateInvoiceTotals();
        }
    });

});
