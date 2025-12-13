/* salesinvoiceautocomplete.js
   Updated: Option 2 - Invoice number autocomplete + Global search autocomplete
   Keeps existing sales invoice calculation + material row autocomplete functionality.
*/

console.log('salesinvoiceautocomplete.js loaded (updated)');

/////////////////////////
// --- CONFIG / STATE ---
/////////////////////////

const AUTOCOMPLETE_DEBOUNCE = 300; // ms

let typingTimer = null;
let highlightedIndex = -1; // for keyboard nav
let activeSuggestionBox = null; // id of the currently visible suggestions box

/////////////////////////
// --- HELPER FUNCS ---
/////////////////////////

function safeFetch(url) {
    return fetch(url, { credentials: 'same-origin' }).then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    });
}

function buildDropdownHtmlList(items, type) {
    // items: [{value, text}] or arbitrary objects for global suggestions
    let html = '';
    items.forEach((it, idx) => {
        // keep an index data attribute for keyboard navigation
        // escape quotes in text/value
        const text = (it.text || it.value || '').toString().replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const value = (it.value || it.val || it).toString().replace(/'/g, "&#39;");
        html += `<a href="javascript:void(0)" class="dropdown-item suggestion-item" data-idx="${idx}" data-value='${value}'>${text}</a>`;
    });
    return html;
}

function showSuggestionBox(boxId, html) {
    const $box = $('#' + boxId);
    if (!$box.length) return;
    $box.html(html).show();
    activeSuggestionBox = boxId;
    highlightedIndex = -1;
}

function hideSuggestionBox(boxId) {
    const $box = $('#' + boxId);
    if ($box.length) $box.hide().empty();
    if (activeSuggestionBox === boxId) activeSuggestionBox = null;
    highlightedIndex = -1;
}

function hideAllSuggestionBoxes() {
    hideSuggestionBox('invoiceNumberSuggestions');
    hideSuggestionBox('globalSuggestions');
    // also hide any row suggestion dropdowns if present
    $('.row-suggestions-dropdown').hide().empty();
}

function setInputValueWithoutSubmitting(inputId, value) {
    const $input = $('#' + inputId);
    if ($input.length) {
        $input.val(value);
        $input.trigger('input'); // allow other listeners to run (but they won't auto-submit)
    }
}

///////////////////////////////
// --- INVOICE AUTOCOMPLETE ---
///////////////////////////////

function showInvoiceNumberSuggestions(query) {
    const boxId = 'invoiceNumberSuggestions';
    const inputId = 'invoiceNumberInput';

    if (!query || query.trim().length < 1) {
        hideSuggestionBox(boxId);
        return;
    }

    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        console.log('📡 Fetch invoice suggestions for:', query);

        // try both possible endpoints for robustness
        const endpoints = [
            `/ajserp/get-sales-invoice-suggestions/?q=${encodeURIComponent(query)}`,
            `/ajserp/api/get-sales-invoice-suggestions/?q=${encodeURIComponent(query)}`
        ];

        // race endpoints: try first, if fails try second
        safeFetch(endpoints[0]).catch(err => {
            console.warn('First invoice endpoint failed, trying alternate', err);
            return safeFetch(endpoints[1]);
        }).then(data => {
            if (!data || !data.length) {
                showSuggestionBox(boxId, `<div class="dropdown-item text-muted">No results</div>`);
                return;
            }

            // expected format: [{value, text}]
            const html = buildDropdownHtmlList(data, 'invoice');
            showSuggestionBox(boxId, html);

        }).catch(err => {
            console.error('Invoice suggestions fetch error:', err);
            hideSuggestionBox(boxId);
        });

    }, AUTOCOMPLETE_DEBOUNCE);
}

///////////////////////////////
// --- GLOBAL SEARCH AUTOCOMPLETE ---
///////////////////////////////

function showGlobalSuggestions(query) {
    const boxId = 'globalSuggestions';
    const inputId = 'globalSearchInput';

    if (!query || query.trim().length < 2) {
        hideSuggestionBox(boxId);
        return;
    }

    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        console.log('📡 Fetch global suggestions for:', query);

        // use the API path used elsewhere in your project
        const endpoint = `/ajserp/api/get-global-suggestions/?q=${encodeURIComponent(query)}`;

        safeFetch(endpoint).then(data => {
            if (!data || !data.length) {
                showSuggestionBox(boxId, `<div class="dropdown-item text-muted">No results</div>`);
                return;
            }

            // format assumed: [{value,text}] where text is human readable
            const html = buildDropdownHtmlList(data, 'global');
            showSuggestionBox(boxId, html);

        }).catch(err => {
            console.error('Global suggestions fetch error:', err);
            hideSuggestionBox(boxId);
        });

    }, AUTOCOMPLETE_DEBOUNCE);
}

///////////////////////////////////////
// --- CLICK HANDLING for suggestions -
///////////////////////////////////////

$(document).on('click', '.suggestion-item', function (e) {
    e.preventDefault();
    const $el = $(this);
    const value = $el.data('value');
    const $parent = $el.closest('.dropdown-menu');
    const parentId = $parent.attr('id');

    if (parentId === 'invoiceNumberSuggestions') {
        setInputValueWithoutSubmitting('invoiceNumberInput', value);
        hideSuggestionBox('invoiceNumberSuggestions');
        // do NOT submit
    } else if (parentId === 'globalSuggestions') {
        setInputValueWithoutSubmitting('globalSearchInput', value);
        hideSuggestionBox('globalSuggestions');
        // do NOT redirect/submit — user must click Search
    } else {
        // fallback
        hideAllSuggestionBoxes();
    }
});

///////////////////////////////////////
// --- KEYBOARD NAVIGATION (Up/Down/Enter/Esc)
///////////////////////////////////////

$(document).on('keydown', function (e) {
    // only handle when suggestion box is active
    if (!activeSuggestionBox) return;

    const $box = $('#' + activeSuggestionBox);
    const $items = $box.find('.suggestion-item');

    if (!$items.length) return;

    if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlightedIndex = Math.min(highlightedIndex + 1, $items.length - 1);
        $items.removeClass('active');
        $items.eq(highlightedIndex).addClass('active').focus();
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlightedIndex = Math.max(highlightedIndex - 1, 0);
        $items.removeClass('active');
        $items.eq(highlightedIndex).addClass('active').focus();
    } else if (e.key === 'Enter') {
        // select the highlighted item if any
        if (highlightedIndex >= 0 && highlightedIndex < $items.length) {
            e.preventDefault();
            $items.eq(highlightedIndex).trigger('click');
        } else {
            // if no highlighted suggestion, let Enter behave normally (form submit)
            // But we will prevent submitting if focus is inside invoice/global input and suggestion box is visible
            const activeInput = document.activeElement;
            if (activeInput && (activeInput.id === 'invoiceNumberInput' || activeInput.id === 'globalSearchInput')) {
                // if a suggestion box is visible, prevent accidental submit
                e.preventDefault();
            }
        }
    } else if (e.key === 'Escape') {
        hideAllSuggestionBoxes();
    }
});

///////////////////////////
// --- Outside click hide
///////////////////////////

$(document).on('click', function (e) {
    // if clicked outside any dropdown-menu and not on an input that triggers suggestions, hide
    if (!$(e.target).closest('.dropdown-menu, #invoiceNumberInput, #globalSearchInput').length) {
        hideAllSuggestionBoxes();
    }
});

//////////////////////////////////////////////////////////
// --- EXISTING: Sales Invoice calculation & material autocomplete
// (kept mostly intact; minor cleanup to avoid duplicate ready handlers)
//////////////////////////////////////////////////////////

// Calculation function (kept mostly as you had it)
function calculateSalesInvoiceWithBackend() {
    console.log('🔄 Calculating Sales Invoice with Django backend...');

    const saveBtn = $('.btn-success');
    saveBtn.prop('disabled', true).text('Calculating...');

    const lineItems = [];
    $('.line-item-row').each(function () {
        const $row = $(this);
        const materialName = $row.find('.material-name').val();

        if (materialName && materialName.trim() !== '') {
            lineItems.push({
                material_name: materialName,
                quantity: parseFloat($row.find('.quantity').val()) || 0,
                mrp: parseFloat($row.find('.mrp').val()) || 0,
                discount: parseFloat($row.find('.discount').val()) || 0,
                hsn_code: $row.find('input[name="hsn_code[]"]').val() || ''
            });
        }
    });

    if (lineItems.length === 0) {
        alert('Please add at least one material item!');
        saveBtn.prop('disabled', false).text('Save');
        return;
    }

    const roundOff = parseFloat($('#round-off').val()) || 0;

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/ajserp/create_sales_invoice/',
        method: 'POST',
        contentType: "application/json",
        headers: { "X-CSRFToken": csrftoken },
        data: JSON.stringify({ line_items: lineItems, round_off: roundOff }),
        success: function (response) {
            if (response.success) {
                response.line_items.forEach((calculatedItem, index) => {
                    const $row = $('.line-item-row').eq(index);
                    $row.find('.basic-amount').val(Number(calculatedItem.basic_amount).toFixed(2));

                    const cgstAmt = Number(calculatedItem.cgst_amount) || 0;
                    const sgstAmt = Number(calculatedItem.sgst_amount) || 0;
                    const onlyGST = cgstAmt + sgstAmt;
                    $row.find('.tax-amount').val(onlyGST.toFixed(2));

                    $row.find('.final-amount').val(Number(calculatedItem.final_amount).toFixed(2));
                    $row.find('.cgst-amount').val(Number(calculatedItem.cgst_amount).toFixed(2));
                    $row.find('.sgst-amount').val(Number(calculatedItem.sgst_amount).toFixed(2));

                    if (Number(calculatedItem.igst_amount) > 0) {
                        $row.find('.igst-amount').val(Number(calculatedItem.igst_amount).toFixed(2));
                    } else {
                        $row.find('.igst-amount').val("");
                    }

                    if (Number(calculatedItem.cess_amount) > 0) {
                        $row.find('.cess-amount').val(Number(calculatedItem.cess_amount).toFixed(2));
                    } else {
                        $row.find('.cess-amount').val("");
                    }
                });

                $('#taxable-amount-display').val(Number(response.totals.taxable_amount).toFixed(2));
                $('#cgst-value-display').val(Number(response.totals.cgst_total).toFixed(2));
                $('#sgst-value-display').val(Number(response.totals.sgst_total).toFixed(2));
                $('#igst-value-display').val(Number(response.totals.igst_total) > 0 ? Number(response.totals.igst_total).toFixed(2) : "");
                $('#cess-value-display').val(Number(response.totals.cess_total) > 0 ? Number(response.totals.cess_total).toFixed(2) : "");
                $('#grand-total-display').val(Number(response.totals.grand_total).toFixed(2));

                console.log('✅ Sales Invoice Calculations completed.');
            } else {
                alert('❌ Error: ' + response.error);
            }
        },
        error: function (xhr, status, error) {
            alert('❌ Sales Invoice Calculation failed: ' + error);
        },
        complete: function () {
            saveBtn.prop('disabled', false).text('Save');
        }
    });
}

// READY: initialize page-level behavior (only on invoice pages)
$(function () {
    const pathname = window.location.pathname;
    if (!(pathname.includes('salesinvoice') || pathname.includes('addsalesinvoice'))) {
        console.log('Not a sales invoice page — autocompletes inactive.');
        return;
    }

    // Hook invoice & global inputs
    $('#invoiceNumberInput').on('input', function () {
        showInvoiceNumberSuggestions(this.value);
    });

    $('#globalSearchInput').on('input', function () {
        showGlobalSuggestions(this.value);
    });

    // If user presses Enter in inputs and there's a highlighted suggestion, handled by keydown above.
    // Otherwise let normal form submit occur when pressing Search button.

    // Prevent Enter key from submitting the form when suggestion box visible for these inputs
    $('#invoiceNumberInput, #globalSearchInput').on('keydown', function (e) {
        if (e.key === 'Enter' && activeSuggestionBox) {
            e.preventDefault();
            // if an item is highlighted, select it
            const $box = $('#' + activeSuggestionBox);
            const $highlight = $box.find('.suggestion-item.active');
            if ($highlight.length) {
                $highlight.trigger('click');
            }
        }
    });

    // Ensure clicking a suggestion hides boxes (handled globally) and does not auto-submit.

    // MATERIAL ROW AUTOCOMPLETE: re-use your existing row-autocomplete code pattern
    // (simplified re-initialization to avoid duplicate handlers)

    let doneTypingInterval = 300;
    function initializeMaterialAutocomplete() {
        console.log('Initializing material row autocomplete');
        $('.material-search').off('input.row_autocomplete');
        $('.material-search').each(function () {
            const materialSearch = $(this);
            const row = materialSearch.closest('tr');
            const suggestionsDiv = materialSearch.siblings('.row-suggestions-dropdown');

            materialSearch.on('input.row_autocomplete', function () {
                clearTimeout(typingTimer);
                const query = $(this).val().trim();
                if (query.length < 1) {
                    suggestionsDiv.hide().empty();
                    return;
                }

                typingTimer = setTimeout(function () {
                    $.ajax({
                        url: "/ajserp/api/materialestimate-autocomplete/",
                        data: { q: query },
                        dataType: "json",
                        success: function (data) {
                            if (!data || !data.length) {
                                suggestionsDiv.html('<div class="p-2 text-muted">No results</div>').show();
                                return;
                            }
                            let items = '';
                            data.forEach(function (item) {
                                const displayText = `<div class="fw-bold">${item.material_name}</div><small class="text-muted">${item.material_code} - ₹${item.mrp}</small>`;
                                const itemData = {
                                    material_name: item.material_name,
                                    material_code: item.material_code,
                                    mrp: item.mrp,
                                    hsn_code: item.hsn_code || ''
                                };
                                items += `<div class="row-suggestion-item p-2 border-bottom" data-material='${JSON.stringify(itemData).replace(/'/g, "&#39;")}' style="cursor:pointer;">${displayText}</div>`;
                            });
                            suggestionsDiv.html(items).show();
                        },
                        error: function (xhr, status, error) {
                            suggestionsDiv.hide().html('<div class="p-2 text-danger">Error loading data</div>');
                        }
                    });
                }, doneTypingInterval);
            });
        });
    }

    // Handle selecting a row suggestion
    $(document).on('click', '.row-suggestion-item', function () {
        const material = $(this).data('material');
        const suggestionsDiv = $(this).closest('.row-suggestions-dropdown');
        const materialInput = suggestionsDiv.siblings('.material-search');
        const row = materialInput.closest('tr');

        // populate basic fields — keep your original populate logic if complex
        row.find('.material-name').val(material.material_name).show();
        row.find('.material-search').val('').hide();
        row.find('.quantity').val(1);
        row.find('.mrp').val(material.mrp);
        row.find('input[name="hsn_code[]"]').val(material.hsn_code || '');

        suggestionsDiv.hide().empty();
        calculateSalesInvoiceWithBackend();
    });

    // Call initializer on ready
    initializeMaterialAutocomplete();

    // Expose calculate function globally (used elsewhere)
    window.calculateSalesInvoiceWithBackend = calculateSalesInvoiceWithBackend;
    window.initializeMaterialAutocomplete = initializeMaterialAutocomplete;

    console.log('salesinvoiceautocomplete.js initialized on invoice page.');
});
