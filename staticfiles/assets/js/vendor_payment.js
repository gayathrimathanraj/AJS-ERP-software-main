// VENDOR PAYMENT JAVASCRIPT - COMPLETE VERSION WITH DEBUG
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Vendor Payment JavaScript loaded');
    initializeVendorPayment();
});

function initializeVendorPayment() {
    console.log('🚀 Initializing Vendor Payment...');
    
    const vendorSearchInput = document.getElementById('payment_vendor_search');
    if (vendorSearchInput) {
        vendorSearchInput.addEventListener('input', handleVendorSearch);
        console.log('✅ Vendor payment search input initialized');
    } else {
        console.log('❌ Vendor payment search input not found');
        return;
    }

    const paymentAmountInput = document.getElementById('payment_amount');
    if (paymentAmountInput) {
        paymentAmountInput.addEventListener('input', calculateBalanceFromLedger);
        console.log('✅ Payment amount input initialized');
    }

    const paymentForm = document.querySelector('form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', validatePaymentForm);
        console.log('✅ Payment form initialized');
    }

    document.addEventListener('click', closeSuggestions);
    console.log('✅ Vendor Payment initialization complete');
}

function handleVendorSearch() {
    const query = this.value.trim();
    console.log(`🔍 VENDOR PAYMENT: Searching vendors for: "${query}"`);
    
    if (query.length < 2) {
        clearVendorSuggestions();
        return;
    }
    
    fetch(`/ajserp/vendor_payment_suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log(`✅ VENDOR PAYMENT: Found ${data.length} vendor suggestions`, data);
            displayVendorSuggestions(data);
        })
        .catch(error => {
            console.error('❌ VENDOR PAYMENT: Error fetching vendor suggestions:', error);
            showError('Error loading vendor suggestions');
        });
}

function displayVendorSuggestions(vendors) {
    const suggestions = document.getElementById('payment_vendor_suggestions');
    if (!suggestions) {
        console.log('❌ VENDOR PAYMENT: Vendor suggestions container not found');
        return;
    }
    
    suggestions.innerHTML = '';
    
    if (!vendors || vendors.length === 0) {
        const noResult = document.createElement('div');
        noResult.textContent = 'No vendors found';
        suggestions.appendChild(noResult);
        suggestions.style.display = 'block';
        return;
    }
    
    vendors.forEach(vendor => {
        const div = document.createElement('div');
        const dueAmount = vendor.due_amount || 0;
        const displayText = `${vendor.vendor_code} - ${vendor.vendor_name} (Due: ₹${dueAmount.toFixed(2)})`;
        div.textContent = displayText;
        
        div.addEventListener('click', function() {
            console.log(`✅ VENDOR PAYMENT: Selected vendor:`, vendor);
            selectVendor(vendor);
        });
        
        suggestions.appendChild(div);
    });
    
    suggestions.style.display = 'block';
}

function clearVendorSuggestions() {
    const suggestions = document.getElementById('payment_vendor_suggestions');
    if (suggestions) {
        suggestions.innerHTML = '';
        suggestions.style.display = 'none';
    }
}

function selectVendor(vendor) {
    console.log(`🎯 VENDOR PAYMENT: Selecting vendor:`, vendor);
    
    document.getElementById('payment_vendor_code').value = vendor.vendor_code;
    document.getElementById('payment_vendor_name').value = vendor.vendor_name;
    
    const dueAmount = vendor.due_amount || 0;
    document.getElementById('due_amount').value = dueAmount.toFixed(2);
    console.log(`💰 VENDOR PAYMENT: Auto-filled due amount: ₹${dueAmount.toFixed(2)}`);
    
    document.getElementById('payment_amount').value = '';
    document.getElementById('balance_outstanding').value = '';
    
    clearVendorSuggestions();
    console.log('✅ VENDOR PAYMENT: Vendor selection completed');
}

function calculateBalanceFromLedger() {
    const vendorCode = document.getElementById('payment_vendor_code').value;
    const paymentAmount = parseFloat(document.getElementById('payment_amount').value) || 0;
    const dueAmount = parseFloat(document.getElementById('due_amount').value) || 0;
    
    console.log(`🧮 VENDOR PAYMENT: Calculating balance - Vendor: ${vendorCode}, Payment: ${paymentAmount}, Due: ${dueAmount}`);
    
    if (!vendorCode) {
        console.log('⚠️ VENDOR PAYMENT: No vendor selected');
        showError('Please select a vendor first');
        document.getElementById('payment_amount').value = '';
        return;
    }
    
    if (paymentAmount === 0) {
        updateBalanceDisplay(dueAmount);
        return;
    }
    
    if (paymentAmount < 0) {
        showError('Payment amount cannot be negative');
        document.getElementById('payment_amount').value = '';
        return;
    }
    
    fetch(`/ajserp/get-vendor-balance-after-payment/?vendor_code=${vendorCode}&payment_amount=${paymentAmount}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('📊 VENDOR PAYMENT: Balance calculation API response:', data);
            if (data.success) {
                updateBalanceDisplay(data.balance_after);
            } else {
                const localBalance = dueAmount - paymentAmount;
                updateBalanceDisplay(localBalance);
            }
        })
        .catch(error => {
            console.error('❌ VENDOR PAYMENT: Error calculating balance:', error);
            const localBalance = dueAmount - paymentAmount;
            updateBalanceDisplay(localBalance);
        });
}

function updateBalanceDisplay(balance) {
    const balanceField = document.getElementById('balance_outstanding');
    if (!balanceField) {
        console.log('❌ VENDOR PAYMENT: Balance field not found');
        return;
    }
    
    balanceField.value = balance.toFixed(2);
    
    if (balance < 0) {
        balanceField.style.border = '2px solid red';
        balanceField.style.color = 'red';
        balanceField.title = 'Payment exceeds due amount - This will create an advance payment';
        console.log('⚠️ VENDOR PAYMENT: Payment exceeds due amount');
    } else {
        balanceField.style.border = '';
        balanceField.style.color = '';
        balanceField.title = '';
    }
    
    console.log(`📊 VENDOR PAYMENT: Updated balance display: ₹${balance.toFixed(2)}`);
}

function validatePaymentForm(e) {
    console.log('🔍 VENDOR PAYMENT: Starting form validation...');
    
    // DEBUG: Get ALL form values
    const formData = {
        vendor_code: document.getElementById('payment_vendor_code').value,
        vendor_name: document.getElementById('payment_vendor_name').value,
        payment_amount: document.getElementById('payment_amount').value,
        due_amount: document.getElementById('due_amount').value,
        mode_of_payment: document.getElementById('mode_of_payment').value,
        payment_type: document.getElementById('payment_type').value,
        payment_date: document.getElementById('payment_date').value,
        document_number: document.getElementById('document_number').value,
        vendor_invoice: document.getElementById('vendor_invoice').value,
        payment_reference: document.getElementById('payment_reference').value,
        remarks: document.getElementById('remarks').value
    };
    
    console.log('📋 VENDOR PAYMENT: Form data:', formData);
    
    const vendorCode = formData.vendor_code;
    const paymentAmount = parseFloat(formData.payment_amount) || 0;
    const dueAmount = parseFloat(formData.due_amount) || 0;
    const modeOfPayment = formData.mode_of_payment;
    
    console.log(`📋 VENDOR PAYMENT: Key fields - Vendor: ${vendorCode}, Amount: ${paymentAmount}, Due: ${dueAmount}, Mode: ${modeOfPayment}`);
    
    let isValid = true;
    let errorMessage = '';
    
    // Basic validation
    if (!vendorCode) {
        errorMessage = 'Please select a vendor';
        isValid = false;
    } else if (paymentAmount <= 0) {
        errorMessage = 'Payment amount must be greater than 0';
        isValid = false;
    } else if (!modeOfPayment || modeOfPayment === 'Select type') {
        errorMessage = 'Please select mode of payment';
        isValid = false;
    }
    
    console.log('✅ Form validation result:', isValid, errorMessage);
    
    if (!isValid) {
        e.preventDefault();
        console.log('❌ VENDOR PAYMENT: Validation failed:', errorMessage);
        showError(errorMessage);
        return;
    }
    
    // Warn if payment exceeds due amount
    if (paymentAmount > dueAmount) {
        const confirmPayment = confirm(
            `⚠️ Payment Alert!\n\n` +
            `Payment amount: ₹${paymentAmount.toFixed(2)}\n` +
            `Due amount: ₹${dueAmount.toFixed(2)}\n\n` +
            `This payment exceeds the due amount and will create an advance payment.\n\n` +
            `Do you want to continue?`
        );
        
        if (!confirmPayment) {
            e.preventDefault();
            console.log('❌ VENDOR PAYMENT: User cancelled payment due to amount exceeding due amount');
            return;
        }
    }
    
    console.log('✅ VENDOR PAYMENT: Form validation passed - SUBMITTING FORM');
    // Form will submit normally if we reach here
}

function closeSuggestions(e) {
    const suggestions = document.getElementById('payment_vendor_suggestions');
    const searchInput = document.getElementById('payment_vendor_search');
    
    if (suggestions && !e.target.matches('#payment_vendor_search')) {
        suggestions.innerHTML = '';
        suggestions.style.display = 'none';
    }
}

function showError(message) {
    console.error('💥 VENDOR PAYMENT: Error:', message);
    alert('❌ ' + message);
}

console.log('🎯 Vendor Payment JavaScript ready');