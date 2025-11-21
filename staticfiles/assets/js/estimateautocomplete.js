console.log('estimateautocomplete.js loaded');

// Move this function OUTSIDE document ready
function calculateWithBackend() {
    console.log('🔄 Calculating with Django backend...');
    
    // Show loading
    const saveBtn = $('.btn-success');
    saveBtn.prop('disabled', true).text('Calculating...');
    
    // Collect all line items
    const lineItems = [];
    
    $('.line-item-row').each(function() {
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
    
    // ✅ GET CSRF TOKEN
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
    
    // Send to Django for calculation
    $.ajax({
        url: '/ajserp/create_estimate/',  // FIXED URL - use correct endpoint
        method: 'POST',
        contentType: "application/json",
        headers: {
            "X-CSRFToken": csrftoken
        },
        data: JSON.stringify({
            line_items: lineItems,
            round_off: roundOff
        }),
        success: function(response) {
            if (response.success) {
                // Update table with calculated amounts
                response.line_items.forEach((calculatedItem, index) => {
                    const $row = $('.line-item-row').eq(index);
                    
                    $row.find('.basic-amount').val(calculatedItem.basic_amount.toFixed(2));
                    $row.find('.tax-amount').val(calculatedItem.tax_amount.toFixed(2));
                    $row.find('.final-amount').val(calculatedItem.final_amount.toFixed(2));
                    
                    // Update hidden fields
                    $row.find('.cgst-amount').val(calculatedItem.cgst_amount.toFixed(2));
                    $row.find('.sgst-amount').val(calculatedItem.sgst_amount.toFixed(2));
                    $row.find('.igst-amount').val(calculatedItem.igst_amount.toFixed(2));
                    $row.find('.cess-amount').val(calculatedItem.cess_amount.toFixed(2));
                });
                
                // Update totals panel
                $('#taxable-amount-display').val(response.totals.taxable_amount.toFixed(2));
                $('#cgst-value-display').val(response.totals.cgst_total.toFixed(2));
                $('#sgst-value-display').val(response.totals.sgst_total.toFixed(2));
                $('#igst-value-display').val(response.totals.igst_total.toFixed(2));
                $('#cess-value-display').val(response.totals.cess_total.toFixed(2));
                $('#grand-total-display').val(response.totals.grand_total.toFixed(2));

                
                
                alert('✅ Calculations completed successfully!');
            } else {
                alert('❌ Error: ' + response.error);
            }
        },
        error: function(xhr, status, error) {
            alert('❌ Calculation failed: ' + error);
        },
        complete: function() {
            saveBtn.prop('disabled', false).text('Save');
        }
    });
}

$(document).ready(function(){
    // Page detection - only run on estimate pages
    const currentPath = window.location.pathname;
    if (!currentPath.includes('estimate') && !currentPath.includes('addestimate')) {
        return;
    }
    
    let typingTimer;
    const doneTypingInterval = 300;
    let itemCounter = 0;

    // Initialize date fields
    initializeDateFields();

    // Initialize material autocomplete for all existing rows
    initializeMaterialAutocomplete();

    // Customer Search Autocomplete
    $("#customer_search").on("input", function(){
        handleCustomerSearch(this);
    });

    // Handle customer selection
    $(document).on("click", "#customer_suggestions div", function(){
        const customer = $(this).data('customer');
        if (customer) {
            selectCustomer(customer);
        }
    });

    // Warehouse Search Autocomplete
    $("#warehouse_search").on("input", function(){
        handleWarehouseSearch(this);
    });

    // Handle warehouse selection
    $(document).on("click", "#warehouse_suggestions div", function(){
        const warehouse = $(this).data('warehouse');
        if (warehouse) {
            $("#warehouse_search").val(warehouse.warehouse_name);
            $("#warehouse_code").val(warehouse.warehouse_code);
            $("#warehouse_suggestions").hide();
        }
    });

    // Close suggestions when clicking outside
    $(document).click(function(e){
        if (!$(e.target).closest('#customer_search').length && 
            !$(e.target).closest('#customer_suggestions').length &&
            !$(e.target).closest('#warehouse_search').length && 
            !$(e.target).closest('#warehouse_suggestions').length &&
            !$(e.target).closest('.autocomplete-container').length && 
            !$(e.target).closest('#material_suggestions').length &&
            !$(e.target).closest('.row-autocomplete-container').length && 
            !$(e.target).closest('.row-suggestions-dropdown').length) {
            $("#customer_suggestions, #warehouse_suggestions, #material_suggestions, .row-suggestions-dropdown").hide();
        }
    });

    // Material Search Autocomplete (Main search box at top)
    $("#material_search").on("input", function(){
        handleMaterialSearch(this);
    });

    // Handle material selection from main search
    $(document).on("click", "#material_suggestions .suggestion-item", function(){
        const material = $(this).data('material');
        selectMaterial(material);
        $("#material_suggestions").hide().empty();
    });

    // Handle material selection from ROW autocomplete
    $(document).on("click", ".row-suggestion-item", function() {
        const material = $(this).data('material');
        const suggestionsDiv = $(this).closest('.row-suggestions-dropdown');
        const materialInput = suggestionsDiv.siblings('.material-search');
        const row = materialInput.closest('tr');
        
        populateMaterialRow(row, material);
        suggestionsDiv.hide().empty();
        materialInput.val(''); // Clear the row search input only
    });

    // Event handlers for line items
    $(document).on("click", ".delete-row", function() {
        const row = $(this).closest('tr');
        const rows = $('.line-item-row').length;
        
        if (rows > 1) {
            const confirmed = confirm("Are you sure you want to delete this row?");
            if (confirmed) {
                row.remove();
                updateSerialNumbers();
            }
        } else {
            alert("At least one row must remain.");
        }
    });

    // Form validation on submit
    $('#estimateForm').on('submit', function(e) {
        if (!validateEstimateForm()) {
            e.preventDefault();
            return false;
        }
        return true;
    });

    // Initialize existing rows on page load
    initializeExistingRows();
    updateSerialNumbers();

    // Initialize material autocomplete for all rows
    function initializeMaterialAutocomplete() {
        console.log('🔄 Initializing material autocomplete for all rows');
        
        // Remove existing autocomplete handlers to prevent duplicates
        $('.material-search').off('input.row_autocomplete');
        
        // Add autocomplete to all material search fields in rows
        $('.material-search').each(function() {
            const materialSearch = $(this);
            const row = materialSearch.closest('tr');
            const suggestionsDiv = materialSearch.siblings('.row-suggestions-dropdown');
            
            materialSearch.on('input.row_autocomplete', function() {
                const inputElement = this;
                console.log('🔍 Row autocomplete triggered for row:', row.index());
                handleRowAutocomplete(inputElement, suggestionsDiv);
            });
        });
    }

    // Handle autocomplete for row material fields
    function handleRowAutocomplete(inputElement, suggestionsDiv) {
        clearTimeout(typingTimer);
        let query = $(inputElement).val().trim();

        console.log('🔍 Row autocomplete query:', query);

        if (query.length < 1) {
            suggestionsDiv.hide().empty();
            return;
        }

        typingTimer = setTimeout(function(){
            console.log('📡 Making row autocomplete API request for:', query);
            
            $.ajax({
                url: "/ajserp/api/materialestimate-autocomplete/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    console.log('✅ Row autocomplete API response:', data);
                    let items = "";
                    
                    if (data && data.length > 0) {
                        data.forEach(function(item){
                            let displayText = `
                                <div class="fw-bold">${item.material_name}</div>
                                <small class="text-muted">${item.material_code} - ₹${item.mrp}</small>
                            `;
                            
                            let itemData = {
                                material_name: item.material_name,
                                material_code: item.material_code,
                                mrp: item.mrp,
                                hsn_code: item.hsn_code || '',
                                category: item.category || 'General'
                            };
                            
                            items += `
                                <div class="row-suggestion-item p-2 border-bottom" 
                                     data-material='${JSON.stringify(itemData).replace(/'/g, "&#39;")}'
                                     style="cursor: pointer;">
                                    ${displayText}
                                </div>`;
                        });
                        suggestionsDiv.html(items).show();
                        console.log('🎯 Row suggestions displayed');
                    } else {
                        suggestionsDiv.html('<div class="p-2 text-muted">No results found</div>').show();
                    }
                },
                error: function(xhr, status, error) {
                    console.error('❌ Row autocomplete API error:', error);
                    suggestionsDiv.hide().html('<div class="p-2 text-danger">Error loading data</div>');
                }
            });
        }, doneTypingInterval);
    }

    // Customer Search Functions
    function handleCustomerSearch(inputElement) {
        clearTimeout(typingTimer);
        const query = $(inputElement).val().trim();

        if (query.length < 2) {
            $("#customer_suggestions").hide().empty();
            return;
        }

        typingTimer = setTimeout(function(){
            $.ajax({
                url: "/ajserp/api/customer-autocomplete/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    let items = "";
                    if (data && data.length > 0) {
                        data.forEach(function(customer){
                            items += `<div data-customer='${JSON.stringify(customer).replace(/'/g, "&#39;")}'>${customer.customer_name} (${customer.customer_code})</div>`;
                        });
                        $("#customer_suggestions").html(items).show();
                    } else {
                        $("#customer_suggestions").html('<div>No customers found</div>').show();
                    }
                },
                error: function() {
                    $("#customer_suggestions").hide().html('<div>Error loading customers</div>');
                }
            });
        }, doneTypingInterval);
    }

    function selectCustomer(customer) {
        $("#customer_search").val(customer.customer_name);
        $("#customer_code").val(customer.customer_code);
        $("#customer_suggestions").hide();
        
        // Auto-fill billing address
        if (customer.billing_address1) {
            $('input[name="billing_address1"]').val(customer.billing_address1);
        }
        if (customer.billing_address2) {
            $('input[name="billing_address2"]').val(customer.billing_address2);
        }
        if (customer.billing_city) {
            $('input[name="billing_city"]').val(customer.billing_city);
        }
        if (customer.billing_state) {
            $('input[name="billing_state"]').val(customer.billing_state);
        }
        if (customer.billing_postal_code) {
            $('input[name="billing_postal_code"]').val(customer.billing_postal_code);
        }
    }

    // Warehouse Search Functions
    function handleWarehouseSearch(inputElement) {
        clearTimeout(typingTimer);
        const query = $(inputElement).val().trim();

        if (query.length < 2) {
            $("#warehouse_suggestions").hide().empty();
            return;
        }

        typingTimer = setTimeout(function(){
            $.ajax({
                url: "/ajserp/api/warehouse-autocomplete/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    let items = "";
                    if (data && data.length > 0) {
                        data.forEach(function(warehouse){
                            items += `<div data-warehouse='${JSON.stringify(warehouse).replace(/'/g, "&#39;")}'>${warehouse.warehouse_name} (${warehouse.warehouse_code})</div>`;
                        });
                        $("#warehouse_suggestions").html(items).show();
                    } else {
                        $("#warehouse_suggestions").html('<div>No warehouses found</div>').show();
                    }
                },
                error: function() {
                    $("#warehouse_suggestions").hide().html('<div>Error loading warehouses</div>');
                }
            });
        }, doneTypingInterval);
    }

    // Material Search Functions
    function handleMaterialSearch(inputElement) {
        clearTimeout(typingTimer);
        let query = $(inputElement).val().trim();

        console.log('🔍 Material search query:', query);

        if (query.length < 1) {
            $("#material_suggestions").hide().empty();
            return;
        }

        typingTimer = setTimeout(function(){
            console.log('📡 Making material autocomplete API request for:', query);
            
            $.ajax({
                url: "/ajserp/api/materialestimate-autocomplete/",
                data: {q: query},
                dataType: "json",
                success: function(data){
                    console.log('✅ Material autocomplete API response:', data);
                    let items = "";
                    
                    if (data && data.length > 0) {
                        data.forEach(function(item){
                            let displayText = `
                                <div class="fw-bold">${item.material_name}</div>
                                <small class="text-muted">${item.material_code} - ₹${item.mrp}</small>
                            `;
                            
                            let itemData = {
                                material_name: item.material_name,
                                material_code: item.material_code,
                                mrp: item.mrp,
                                hsn_code: item.hsn_code || '',
                                category: item.category || 'General'
                            };
                            
                            items += `
                                <div class="suggestion-item p-2 border-bottom" 
                                     data-material='${JSON.stringify(itemData).replace(/'/g, "&#39;")}'
                                     style="cursor: pointer;">
                                    ${displayText}
                                </div>`;
                        });
                        $("#material_suggestions").html(items).show();
                        console.log('🎯 Material suggestions displayed');
                    } else {
                        $("#material_suggestions").html('<div class="p-2 text-muted">No results found</div>').show();
                    }
                },
                error: function(xhr, status, error) {
                    console.error('❌ Material autocomplete API error:', error);
                    $("#material_suggestions").hide().html('<div class="p-2 text-danger">Error loading data</div>');
                }
            });
        }, doneTypingInterval);
    }

    // Handle material selection from main search
    function selectMaterial(material) {
        // Check if material already exists
        const materialName = material.material_name;
        const existingMaterial = $(`.material-name[value="${materialName}"]`);
        if (existingMaterial.length > 0) {
            alert('This material is already added to the estimate');
            return;
        }
        
        // Find the first empty row or add a new one
        let targetRow = $('.line-item-row').first();
        
        // If the first row already has data, add a new row
        if (targetRow.find('.material-name').val()) {
            addEmptyRow();
            targetRow = $('.line-item-row').last();
        }
        
        populateMaterialRow(targetRow, material);
        
        $("#material_suggestions").hide().empty();
    }

    function initializeDateFields() {
        // Set today's date as default
        const today = new Date().toISOString().split('T')[0];
        const validTill = new Date();
        validTill.setDate(validTill.getDate() + 30);
        const validTillFormatted = validTill.toISOString().split('T')[0];
        
        $('input[name="date"]').val(today);
        $('input[name="valid_till"]').val(validTillFormatted);
    }

    function updateSerialNumbers() {
        $('.line-item-row').each(function(index) {
            $(this).find('.serial-number').text(index + 1);
        });
    }

    function initializeExistingRows() {
        // Initialize any existing rows on page load
        $('.line-item-row').each(function(index) {
            const row = $(this);
            if (!row.attr('id') && row.find('.material-name').val()) {
                itemCounter++;
                const rowId = `item-${itemCounter}`;
                row.attr('id', rowId);
            }
        });
    }

    function populateMaterialRow(row, material) {
        itemCounter++;
        const rowId = `item-${itemCounter}`;
        row.attr('id', rowId);
        
        console.log('🎯 Starting to populate row with material:', material.material_name);
        
        // Get tax rates for this material
        getTaxRates(material.hsn_code).then(taxRates => {
            // Populate row fields
            row.find('.serial-number').text($('.line-item-row').index(row) + 1);
            row.find('.material-name').val(material.material_name).show();
            row.find('.material-search').val('').hide(); // Hide search field, show material name
            row.find('.quantity').val(1);
            row.find('.mrp').val(material.mrp);
            row.find('.discount').val(0);
            
            // Update hidden fields with tax rates (for server-side calculation)
            row.find('input[name="hsn_code[]"]').val(material.hsn_code || '');
            row.find('.cgst-rate').val(taxRates.cgst || 9);
            row.find('.sgst-rate').val(taxRates.sgst || 9);
            row.find('.igst-rate').val(taxRates.igst || 18);
            row.find('.cess-rate').val(taxRates.cess || 0);
            
            console.log('✅ Row populated successfully');

            // Auto-calculate only if material was successfully populated
        calculateWithBackend();

        }).catch(error => {
            console.error("❌ Error in populateMaterialRow:", error);
            // Use default tax rates as fallback
            row.find('.serial-number').text($('.line-item-row').index(row) + 1);
            row.find('.material-name').val(material.material_name).show();
            row.find('.material-search').val('').hide();
            row.find('.quantity').val(1);
            row.find('.mrp').val(material.mrp);
            row.find('.discount').val(0);
            row.find('input[name="hsn_code[]"]').val(material.hsn_code || '');
        });
    }

    function getTaxRates(hsnCode) {
        return new Promise((resolve, reject) => {
            if (!hsnCode) {
                console.log('📊 No HSN code provided, using default tax rates');
                resolve({cgst: 9, sgst: 9, igst: 18, cess: 0});
                return;
            }
            
            console.log('📊 Fetching tax rates for HSN:', hsnCode);
            
            $.ajax({
                url: "/ajserp/api/get-tax-rates/",
                data: {hsn_code: hsnCode},
                dataType: "json",
                success: function(data) {
                    console.log('📊 Tax rates API response:', data);
                    
                    if (data.success) {
                        resolve({
                            cgst: data.cgst,
                            sgst: data.sgst, 
                            igst: data.igst,
                            cess: data.cess
                        });
                    } else {
                        console.log('📊 Using default tax rates for HSN:', hsnCode);
                        resolve({cgst: 9, sgst: 9, igst: 18, cess: 0});
                    }
                },
                error: function(xhr, status, error) {
                    console.error("❌ Tax rate API error:", error);
                    resolve({cgst: 9, sgst: 9, igst: 18, cess: 0});
                }
            });
        });
    }

    // Form validation
    function validateEstimateForm() {
        const items = $('.line-item-row').length;
        if (items === 0) {
            alert('Please add at least one material item');
            return false;
        }
        
        const customer = $('#customer_code').val();
        if (!customer) {
            alert('Please select a customer');
            return false;
        }
        
        const warehouse = $('#warehouse_code').val();
        if (!warehouse) {
            alert('Please select a warehouse');
            return false;
        }
        
        // Validate individual line items
        let hasErrors = false;
        $('.line-item-row').each(function() {
            const quantity = parseFloat($(this).find('.quantity').val()) || 0;
            const mrp = parseFloat($(this).find('.mrp').val()) || 0;
            const materialName = $(this).find('.material-name').val();
            
            if (!materialName) {
                alert('Please select material for all items');
                hasErrors = true;
                return false;
            }
            
            if (quantity <= 0) {
                alert('Please enter valid quantity for all items');
                hasErrors = true;
                return false;
            }
            
            if (mrp < 0) {
                alert('Please enter valid MRP for all items');
                hasErrors = true;
                return false;
            }
        });
        
        if (hasErrors) {
            return false;
        }
        
        return true;
    }

    // Add Empty Row function
    function addEmptyRow() {
        const tBody = $("#estimate-items-body");
        const lastRow = tBody.find('.line-item-row').last();
        
        if (lastRow.length === 0) return;

        const newRow = lastRow.clone();
        
        // Clear all input values
        newRow.find('input[type="text"]').val('');
        newRow.find('input[type="number"]').val(function() {
            const input = $(this);
            if (input.hasClass('quantity')) return '1';
            if (input.hasClass('mrp') || input.hasClass('discount')) return '0';
            return '';
        });
        
        // Clear hidden fields
        newRow.find('input[type="hidden"]').val('');
        
        // Remove any existing ID
        newRow.removeAttr('id');
        
        // Show search field, hide material name field for new empty row
        newRow.find('.material-name').hide().val('');
        newRow.find('.material-search').show().val('');
        
        // Add to table
        tBody.append(newRow);
        
        // RE-INITIALIZE AUTCOMPLETE FOR ALL ROWS (including the new one)
        initializeMaterialAutocomplete();
        
        // Update serial numbers
        updateSerialNumbers();
        
        console.log('✅ New row added and autocomplete initialized');
    }

    // Make addEmptyRow available globally
    window.addEmptyRow = addEmptyRow;
 // ============ ADD CALCULATION FUNCTION HERE ============
    
}); 
