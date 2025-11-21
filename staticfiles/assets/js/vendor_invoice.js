// 🛑 STRONG PAGE DETECTION - VENDOR INVOICE JS
console.log('🔄 VENDOR INVOICE JS LOADED - CHECKING PAGE');

// IMMEDIATE page check (BEFORE anything else runs)
const currentPath = window.location.pathname;
console.log('🔍 CURRENT URL:', currentPath);

// STRICT vendor invoice page detection
const isVendorInvoicePage = 
    currentPath.includes('/addvendorinvoice/') || 
    currentPath.includes('/vendorinvoice/') ||
    currentPath.endsWith('/addvendorinvoice') ||
    currentPath.endsWith('/vendorinvoice') ||
    currentPath.includes('/edit-vendor-invoice/');

console.log('❓ IS VENDOR INVOICE PAGE?', isVendorInvoicePage);

// NUCLEAR OPTION: If not on vendor invoice page, STOP COMPLETELY
if (!isVendorInvoicePage) {
    console.log('💥 VENDOR INVOICE JS: NOT ON CORRECT PAGE - STOPPING ALL EXECUTION');
    
    // Override ALL functions to do nothing
    const emptyFunction = function() { 
        console.log('🛑 VENDOR INVOICE JS BLOCKED - WRONG PAGE');
    };
    
    window.initializeVendorAutocomplete = emptyFunction;
    window.initializeTaxCalculations = emptyFunction;
    window.initializeForm = emptyFunction;
    window.calculateTotal = emptyFunction;
    window.getFieldValue = function() { return 0; };
    window.updateDisplayFieldsImmediately = emptyFunction;
    window.validateVendorInvoiceForm = function() { return true; };
    window.setDefaultDates = emptyFunction;
    window.debugElements = emptyFunction;
    window.selectVendor = emptyFunction;
    
    // STOP execution completely
    throw new Error('VENDOR INVOICE JS STOPPED - NOT ON VENDOR INVOICE PAGE');
}

console.log('✅ VENDOR INVOICE JS: ON CORRECT PAGE - CONTINUING');


// Vendor Invoice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Vendor Invoice JS loaded');
    initializeVendorAutocomplete();
    initializeTaxCalculations();
    initializeForm();
});

// Vendor Autocomplete Functionality
function initializeVendorAutocomplete() {
    const vendorSearch = document.getElementById('vendor_search');
    const vendorSuggestions = document.getElementById('vendor_suggestions');
    const vendorCodeField = document.getElementById('vendor_code');
    const vendorNameDisplay = document.getElementById('vendor_name_display');
    const address1Field = document.getElementById('id_address1');
    const address2Field = document.getElementById('id_address2');

    if (!vendorSearch) {
        console.log('❌ Vendor search element not found');
        return;
    }

    vendorSearch.addEventListener('input', function() {
        const query = this.value.trim();
        console.log('🔍 Vendor search query:', query);
        
        if (query.length < 2) {
            vendorSuggestions.style.display = 'none';
            return;
        }

        // FIXED: Use correct URL pattern
        fetch(`/ajserp/vendor-search/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(vendors => {
                console.log('✅ Vendors found:', vendors);
                vendorSuggestions.innerHTML = '';
                if (vendors.length > 0) {
                    vendors.forEach(vendor => {
                        const div = document.createElement('div');
                        div.className = 'autocomplete-suggestion';
                        div.textContent = `${vendor.vendor_code} - ${vendor.vendor_name}`;
                        div.dataset.vendorCode = vendor.vendor_code;
                        div.dataset.vendorName = vendor.vendor_name;
                        div.dataset.address1 = vendor.billing_address1 || '';
                        div.dataset.address2 = vendor.billing_address2 || '';
                        div.addEventListener('click', function() {
                            selectVendor(vendor);
                        });
                        vendorSuggestions.appendChild(div);
                    });
                    vendorSuggestions.style.display = 'block';
                } else {
                    vendorSuggestions.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('❌ Error fetching vendors:', error);
                vendorSuggestions.style.display = 'none';
            });
    });

    function selectVendor(vendor) {
        console.log('✅ Vendor selected:', vendor);
        vendorSearch.value = `${vendor.vendor_code} - ${vendor.vendor_name}`;
        if (vendorCodeField) vendorCodeField.value = vendor.vendor_code;
        if (vendorNameDisplay) vendorNameDisplay.value = vendor.vendor_name;
        if (address1Field) address1Field.value = vendor.billing_address1 || '';
        if (address2Field) address2Field.value = vendor.billing_address2 || '';
        vendorSuggestions.style.display = 'none';
        
        calculateTotal();
    }

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!vendorSearch.contains(e.target) && !vendorSuggestions.contains(e.target)) {
            vendorSuggestions.style.display = 'none';
        }
    });
}

// Tax Calculation Functionality
function initializeTaxCalculations() {
    console.log('🔧 Initializing tax calculations');
    
    // Add auto-calculation
    initializeAutoCalculation();
    
    const calculationFields = [
        'id_basic_amount', 'basic_amount', 
        'id_cgst_rate', 'cgst_rate',
        'id_sgst_rate', 'sgst_rate', 
        'id_igst_rate', 'igst_rate',
        'id_cess_rate', 'cess_rate', 
        'id_discount_amount', 'discount_amount',
        'id_tds_rate', 'tds_rate', 
        'id_tax_type', 'tax_type'
    ];

    calculationFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('change', calculateTotal);
            field.addEventListener('input', calculateTotal);
        }
    });

    // Add event listener for cess checkbox
    const cessCheckbox = document.getElementById('id_cess_applicable') || document.getElementById('cess_applicable');
    if (cessCheckbox) {
        cessCheckbox.addEventListener('change', calculateTotal);
    }
}

// Auto-calculation when basic amount or tax rates change
function initializeAutoCalculation() {
    console.log('🔧 Initializing auto-calculation');
    
    const calculationFields = [
        'id_basic_amount', 'basic_amount',
        'id_cgst_rate', 'cgst_rate',
        'id_sgst_rate', 'sgst_rate',
        'id_igst_rate', 'igst_rate',
        'id_cess_rate', 'cess_rate',
        'id_discount_amount', 'discount_amount',
        'id_tds_rate', 'tds_rate',
        'id_tax_type', 'tax_type'
    ];

    calculationFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateTotal);
            field.addEventListener('change', calculateTotal);
        }
    });

    // Initial calculation
    setTimeout(calculateTotal, 100);
}

// Calculate total automatically (frontend calculation)
function calculateTotal() {
    console.log('🧮 Calculating totals...');
    
    // Try multiple possible field IDs
    const basicAmount = getFieldValue('id_basic_amount', 'basic_amount') || 0;
    const cgstRate = getFieldValue('id_cgst_rate', 'cgst_rate') || 0;
    const sgstRate = getFieldValue('id_sgst_rate', 'sgst_rate') || 0;
    const igstRate = getFieldValue('id_igst_rate', 'igst_rate') || 0;
    const cessRate = getFieldValue('id_cess_rate', 'cess_rate') || 0;
    const discountAmount = getFieldValue('id_discount_amount', 'discount_amount') || 0;
    const tdsRate = getFieldValue('id_tds_rate', 'tds_rate') || 0;
    const taxType = getFieldValue('id_tax_type', 'tax_type') || 'CGST';
    const cessApplicable = document.getElementById('id_cess_applicable') ? 
                          document.getElementById('id_cess_applicable').checked : false;

    console.log('📊 Calculation inputs:', {
        basicAmount, cgstRate, sgstRate, igstRate, cessRate, 
        discountAmount, tdsRate, taxType, cessApplicable
    });

    // Calculate tax amounts
    let cgstAmount = 0, sgstAmount = 0, igstAmount = 0, cessAmount = 0;

    if (taxType === 'CGST' || taxType === 'cgst') {
        cgstAmount = (basicAmount * cgstRate) / 100;
        sgstAmount = (basicAmount * sgstRate) / 100;
    } else if (taxType === 'IGST' || taxType === 'igst') {
        igstAmount = (basicAmount * igstRate) / 100;
    }

    if (cessApplicable) {
        cessAmount = (basicAmount * cessRate) / 100;
    }

    const tdsAmount = (basicAmount * tdsRate) / 100;

    // Calculate total
    const taxTotal = cgstAmount + sgstAmount + igstAmount + cessAmount;
    const totalAmount = basicAmount + taxTotal - discountAmount - tdsAmount;

    console.log('✅ Calculated totals:', {
        basicAmount, cgstAmount, sgstAmount, igstAmount, 
        cessAmount, discountAmount, tdsAmount, totalAmount
    });

    // Update display fields immediately
    updateDisplayFieldsImmediately({
        basic_amount: basicAmount,
        cgst_amount: cgstAmount,
        sgst_amount: sgstAmount,
        igst_amount: igstAmount,
        cess_amount: cessAmount,
        discount_amount: discountAmount,
        tds_amount: tdsAmount,
        total_amount: totalAmount
    });
}

// Helper function to get field value with multiple possible IDs
function getFieldValue(...possibleIds) {
    for (const id of possibleIds) {
        const field = document.getElementById(id);
        if (field && field.value !== '') {
            return parseFloat(field.value) || 0;
        }
    }
    return 0;
}

// Update display fields immediately (without waiting for backend)
function updateDisplayFieldsImmediately(totals) {
    console.log('📝 Updating display fields:', totals);
    
    const fields = {
        'basic_amount_display': totals.basic_amount,
        'cgst_amount_display': totals.cgst_amount,
        'sgst_amount_display': totals.sgst_amount,
        'igst_amount_display': totals.igst_amount,
        'cess_amount_display': totals.cess_amount,
        'discount_amount_display': totals.discount_amount,
        'tds_amount_display': totals.tds_amount,
        'total_amount_display': totals.total_amount
    };

    for (const [fieldId, value] of Object.entries(fields)) {
        const field = document.getElementById(fieldId);
        if (field) {
            if (fieldId === 'total_amount_display') {
                field.value = '₹' + value.toFixed(2);
            } else {
                field.value = '₹' + value.toFixed(2);
            }
        } else {
            console.log(`❌ Field not found: ${fieldId}`);
        }
    }
}

// Get CSRF token for AJAX requests
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

// Form validation
function validateVendorInvoiceForm() {
    console.log('🔍 Validating form...');
    
    const requiredFields = [
        'id_transaction_type', 'transaction_type',
        'id_document_date', 'document_date',
        'vendor_code',
        'id_payment_terms', 'payment_terms',
        'id_invoice_number', 'invoice_number',
        'id_invoice_date', 'invoice_date',
        'id_hsn_code', 'hsn_code',
        'id_material_service_details', 'material_service_details',
        'id_uom', 'uom',
        'id_quantity', 'quantity',
        'id_address1', 'address1',
        'id_tax_type', 'tax_type',
        'id_basic_amount', 'basic_amount'
    ];

    for (const fieldId of requiredFields) {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            alert(`Please fill in ${field.placeholder || field.name}`);
            field.focus();
            return false;
        }
    }

    const quantity = getFieldValue('id_quantity', 'quantity');
    const basicAmount = getFieldValue('id_basic_amount', 'basic_amount');
    
    if (quantity <= 0) {
        alert('Quantity must be greater than 0');
        return false;
    }
    
    if (basicAmount <= 0) {
        alert('Basic amount must be greater than 0');
        return false;
    }

    console.log('✅ Form validation passed');
    return true;
}

// Auto-set today's date for date fields
function setDefaultDates() {
    const today = new Date().toISOString().split('T')[0];
    
    const dateFields = [
        'id_document_date', 'document_date',
        'id_invoice_date', 'invoice_date'
    ];
    
    dateFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value) {
            field.value = today;
        }
    });
}

// Initialize form when page loads
function initializeForm() {
    console.log('🔧 Initializing form...');
    
    setDefaultDates();
    
    const form = document.getElementById('vendorInvoiceForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('📤 Form submitted, validating...');
            if (!validateVendorInvoiceForm()) {
                e.preventDefault();
                console.log('❌ Form validation failed');
            } else {
                console.log('✅ Form validation passed, submitting...');
            }
        });
    } else {
        console.log('❌ Form element not found');
    }
}

// Debug: Check if elements exist
function debugElements() {
    console.log('🔍 Debugging elements:');
    const importantElements = [
        'vendor_search', 'vendor_code', 'vendor_name_display',
        'id_basic_amount', 'basic_amount', 'total_amount_display',
        'vendorInvoiceForm'
    ];
    
    importantElements.forEach(id => {
        const element = document.getElementById(id);
        console.log(`${id}:`, element ? 'FOUND' : 'NOT FOUND');
    });
}

// Run debug on load
setTimeout(debugElements, 500);